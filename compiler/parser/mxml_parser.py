"""
MXML Neo Parser

Parses MXML files with Neo namespace and extracts:
- AS4 Script blocks
- CSS Style blocks
- Component tree
- Data bindings
"""

import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    raise ImportError("lxml is required. Install with: pip install lxml")

from .as4_parser import AS4Parser
from .ast import Program, Statement


# ============================================================================
# MXML AST Nodes
# ============================================================================

@dataclass
class MXMLComponent:
    """MXML component node"""
    tag: str  # Component name (Button, VBox, etc.)
    properties: Dict[str, Any] = field(default_factory=dict)
    children: List['MXMLComponent'] = field(default_factory=list)
    text_content: Optional[str] = None
    is_root: bool = False


@dataclass
class MXMLApplication:
    """Complete MXML application"""
    root_component: MXMLComponent
    script_ast: Optional[Program] = None  # Parsed AS4 from <fx:Script>
    styles: str = ""  # CSS from <fx:Style>
    metadata: Dict[str, str] = field(default_factory=dict)


# ============================================================================
# MXML Parser
# ============================================================================

class MXMLParser:
    """Parser for MXML Neo files"""

    # Neo namespace URIs
    NS_FX = "http://openflex.dev/core"
    NS_NEO = "http://openflex.dev/neo"

    # Legacy Flex namespaces (for compatibility)
    NS_FLEX_FX = "http://ns.adobe.com/mxml/2009"
    NS_SPARK = "library://ns.adobe.com/flex/spark"
    NS_MX = "library://ns.adobe.com/flex/mx"

    def __init__(self):
        """Initialize MXML parser"""
        self.as4_parser = AS4Parser()

    def parse(self, source: str, filename: str = "<input>") -> MXMLApplication:
        """
        Parse MXML source code

        Args:
            source: MXML source code
            filename: Source file name

        Returns:
            MXMLApplication with parsed content
        """
        # Preprocess MXML to normalize binding syntax before XML parsing
        source = self._preprocess_mxml(source)

        # Parse XML
        try:
            root = etree.fromstring(source.encode('utf-8'))
        except etree.XMLSyntaxError as e:
            raise SyntaxError(f"Invalid MXML: {e}")

        # Extract namespaces
        nsmap = root.nsmap if hasattr(root, 'nsmap') else {}

        # Detect namespace (Neo or legacy Flex)
        default_ns = nsmap.get(None, self.NS_NEO)
        fx_ns = nsmap.get('fx', self.NS_FX)

        # Extract script blocks
        script_code = self._extract_scripts(root, fx_ns, filename)

        # Extract style blocks
        styles = self._extract_styles(root, fx_ns)

        # Extract metadata (title, etc.)
        metadata = self._extract_metadata(root)

        # Parse root component
        root_component = self._parse_component(root, default_ns, fx_ns)
        root_component.is_root = True

        # Parse AS4 script
        script_ast = None
        if script_code:
            script_ast = self.as4_parser.parse(script_code, f"{filename}:<fx:Script>")

        return MXMLApplication(
            root_component=root_component,
            script_ast=script_ast,
            styles=styles,
            metadata=metadata
        )

    def parse_file(self, filepath: str) -> MXMLApplication:
        """Parse MXML file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        return self.parse(source, filepath)

    def _preprocess_mxml(self, source: str) -> str:
        """Preprocess MXML to normalize binding syntax before XML parsing."""
        return preprocess_mxml_bindings(source)

    def _extract_scripts(self, root: etree.Element, fx_ns: str, filename: str) -> str:
        """Extract all <fx:Script> blocks"""
        scripts = []

        # Find all Script elements
        for script_elem in root.findall(f".//{{{fx_ns}}}Script"):
            script_text = script_elem.text
            if script_text:
                scripts.append(script_text.strip())

            # Remove script element so it doesn't appear in component tree
            parent = script_elem.getparent()
            if parent is not None:
                parent.remove(script_elem)

        return "\n\n".join(scripts)

    def _extract_styles(self, root: etree.Element, fx_ns: str) -> str:
        """Extract all <fx:Style> blocks"""
        styles = []

        # Find all Style elements
        for style_elem in root.findall(f".//{{{fx_ns}}}Style"):
            # Check for external source
            source_attr = style_elem.get('source')
            if source_attr:
                # TODO: Load external CSS file
                styles.append(f"/* External: {source_attr} */")
            else:
                style_text = style_elem.text
                if style_text:
                    styles.append(style_text.strip())

            # Remove style element
            parent = style_elem.getparent()
            if parent is not None:
                parent.remove(style_elem)

        return "\n\n".join(styles)

    def _extract_metadata(self, root: etree.Element) -> Dict[str, str]:
        """Extract metadata from root element"""
        metadata = {}

        # Extract common attributes
        for attr in ('title', 'width', 'height'):
            value = root.get(attr)
            if value:
                metadata[attr] = value

        return metadata

    def _parse_component(
        self,
        elem: etree.Element,
        default_ns: str,
        fx_ns: str
    ) -> MXMLComponent:
        """Parse a component element recursively"""

        # Get tag name (without namespace)
        tag = self._get_tag_name(elem)

        # Skip fx: elements (Script, Style, Metadata)
        if elem.tag.startswith(f"{{{fx_ns}}}"):
            return None

        # Extract properties from attributes
        properties = {}
        for attr_name, attr_value in elem.attrib.items():
            # Skip namespace declarations
            if attr_name.startswith('{http://www.w3.org/2000/xmlns/}'):
                continue
            if attr_name in ('xmlns', 'xmlns:fx', 'xmlns:s', 'xmlns:mx'):
                continue

            # Parse attribute value (handle data binding)
            parsed_value = self._parse_attribute_value(attr_value)
            properties[attr_name] = parsed_value

        # Extract text content
        text_content = None
        if elem.text and elem.text.strip():
            text_content = elem.text.strip()

        # Parse children recursively
        children = []
        for child_elem in elem:
            # Skip comments
            if isinstance(child_elem, etree._Comment):
                continue

            child_component = self._parse_component(child_elem, default_ns, fx_ns)
            if child_component:
                children.append(child_component)

        return MXMLComponent(
            tag=tag,
            properties=properties,
            children=children,
            text_content=text_content
        )

    def _get_tag_name(self, elem: etree.Element) -> str:
        """Extract tag name without namespace"""
        tag = elem.tag
        if '}' in tag:
            # Remove namespace: {http://...}TagName -> TagName
            tag = tag.split('}')[1]
        return tag

    def _parse_attribute_value(self, value: str) -> Any:
        """
        Parse attribute value, handling:
        - Data binding: {variable}
        - Numbers: 42, 3.14
        - Booleans: true, false
        - Strings: everything else
        """
        # Data binding: {expression}
        if value.startswith('{') and value.endswith('}'):
            expression = value[1:-1]
            return {'binding': expression}

        # Boolean
        if value.lower() == 'true':
            return True
        if value.lower() == 'false':
            return False

        # Number
        try:
            # Try int first
            if '.' not in value:
                return int(value)
            else:
                return float(value)
        except ValueError:
            pass

        # String (default)
        return value

    def print_tree(self, app: MXMLApplication, indent: int = 0):
        """Debug: Print component tree"""
        def print_component(comp: MXMLComponent, level: int):
            prefix = "  " * level
            props_str = ", ".join(f"{k}={v}" for k, v in list(comp.properties.items())[:3])
            if len(comp.properties) > 3:
                props_str += ", ..."
            print(f"{prefix}<{comp.tag} {props_str}>")
            for child in comp.children:
                print_component(child, level + 1)

        print("\n=== MXML Component Tree ===")
        print_component(app.root_component, 0)

        if app.script_ast:
            print("\n=== AS4 Script ===")
            print(f"Imports: {len(app.script_ast.imports)}")
            print(f"Declarations: {len(app.script_ast.declarations)}")

        if app.styles:
            print("\n=== Styles ===")
            print(f"{len(app.styles)} characters of CSS")


# ============================================================================
# Helper Functions
# ============================================================================

def preprocess_mxml_bindings(source: str) -> str:
    """
    Preprocess MXML to normalize binding syntax before XML parsing.

    Converts JSX-like unquoted bindings:
        attr={expr}  →  attr="{expr}"

    Handles nested braces (e.g. arrow functions: onClick={() => { ... }}).
    Skips content inside <fx:Script> and <fx:Style> blocks.

    This is a standalone function that can be used by any MXML compiler.
    """
    # Protect fx:Script and fx:Style blocks from modification
    protected = {}
    counter = [0]

    def protect_block(match):
        key = f'\x00PROT_{counter[0]}\x00'
        counter[0] += 1
        protected[key] = match.group(0)
        return key

    source = re.sub(
        r'(<fx:Script\b[\s\S]*?</fx:Script>|<fx:Style\b[\s\S]*?</fx:Style>)',
        protect_block, source
    )

    # Find all unquoted bindings: attr={...} with nested brace support
    attr_pattern = re.compile(r'(\s)([\w:.-]+)=\{')
    replacements = []
    matched_ranges = []

    for match in attr_pattern.finditer(source):
        # Skip if inside a previously matched range
        if any(s <= match.start() < e for s, e in matched_ranges):
            continue

        brace_start = match.end()  # position after ={

        # Find matching } with depth tracking, respecting string literals
        depth = 1
        k = brace_start
        in_string = None
        while k < len(source) and depth > 0:
            ch = source[k]
            if in_string:
                if ch == in_string and (k == 0 or source[k - 1] != '\\'):
                    in_string = None
            else:
                if ch == '"' or ch == "'":
                    in_string = ch
                elif ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
            k += 1

        if depth == 0:
            expr = source[brace_start:k - 1]
            # Escape XML-special characters inside the expression
            expr = expr.replace('&', '&amp;')
            expr = expr.replace('"', '&quot;')
            expr = expr.replace('<', '&lt;')
            replacement = f'{match.group(1)}{match.group(2)}="{{{expr}}}"'
            replacements.append((match.start(), k, replacement))
            matched_ranges.append((match.start(), k))

    # Apply replacements in reverse order to preserve positions
    for start, end, replacement in reversed(replacements):
        source = source[:start] + replacement + source[end:]

    # Restore protected blocks
    for key, value in protected.items():
        source = source.replace(key, value)

    return source


def parse_mxml_file(filepath: str) -> MXMLApplication:
    """Convenience function to parse MXML file"""
    parser = MXMLParser()
    return parser.parse_file(filepath)


def parse_mxml(source: str, filename: str = "<input>") -> MXMLApplication:
    """Convenience function to parse MXML source"""
    parser = MXMLParser()
    return parser.parse(source, filename)
