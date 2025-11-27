"""
OpenFlex Neo - Source Map Generator
Generate source maps for debugging compiled code
"""

import json
import base64
from typing import List, Optional, Tuple
from dataclasses import dataclass
from compiler.parser.ast import SourceLocation


@dataclass
class SourceMapping:
    """Single source mapping entry"""
    generated_line: int
    generated_column: int
    source_file: str
    source_line: int
    source_column: int
    name: Optional[str] = None


class SourceMapGenerator:
    """
    Generate source maps compatible with Source Map v3 specification
    https://sourcemaps.info/spec.html
    """

    def __init__(self, generated_file: str, source_file: str):
        """
        Initialize source map generator

        Args:
            generated_file: Path to generated JavaScript file
            source_file: Path to original source file
        """
        self.generated_file = generated_file
        self.source_file = source_file
        self.mappings: List[SourceMapping] = []
        self.names: List[str] = []

    def add_mapping(
        self,
        generated_line: int,
        generated_column: int,
        source_line: int,
        source_column: int,
        name: Optional[str] = None
    ) -> None:
        """
        Add a mapping between generated and source code

        Args:
            generated_line: Line number in generated file (1-based)
            generated_column: Column number in generated file (0-based)
            source_line: Line number in source file (1-based)
            source_column: Column number in source file (0-based)
            name: Optional identifier name
        """
        mapping = SourceMapping(
            generated_line=generated_line,
            generated_column=generated_column,
            source_file=self.source_file,
            source_line=source_line,
            source_column=source_column,
            name=name
        )

        self.mappings.append(mapping)

        if name and name not in self.names:
            self.names.append(name)

    def add_mapping_from_location(
        self,
        generated_line: int,
        generated_column: int,
        location: SourceLocation,
        name: Optional[str] = None
    ) -> None:
        """
        Add mapping from AST source location

        Args:
            generated_line: Line in generated code
            generated_column: Column in generated code
            location: Source location from AST
            name: Optional identifier name
        """
        self.add_mapping(
            generated_line=generated_line,
            generated_column=generated_column,
            source_line=location.line,
            source_column=location.column - 1,  # Convert to 0-based
            name=name
        )

    def encode_vlq(self, value: int) -> str:
        """
        Encode integer as Variable Length Quantity (VLQ)

        Args:
            value: Integer to encode

        Returns:
            Base64 VLQ encoded string
        """
        VLQ_BASE_SHIFT = 5
        VLQ_BASE = 1 << VLQ_BASE_SHIFT
        VLQ_BASE_MASK = VLQ_BASE - 1
        VLQ_CONTINUATION_BIT = VLQ_BASE

        # Convert to VLQ signed representation
        if value < 0:
            vlq = ((-value) << 1) | 1
        else:
            vlq = value << 1

        result = []

        # Handle zero specially
        if vlq == 0:
            return self._base64_encode(0)

        while vlq > 0:
            digit = vlq & VLQ_BASE_MASK
            vlq >>= VLQ_BASE_SHIFT

            if vlq > 0:
                digit |= VLQ_CONTINUATION_BIT

            result.append(self._base64_encode(digit))

        return ''.join(result)

    def _base64_encode(self, value: int) -> str:
        """Encode single digit to base64"""
        BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        return BASE64_CHARS[value]

    def generate_mappings_string(self) -> str:
        """
        Generate the mappings string for source map

        Returns:
            Encoded mappings string
        """
        if not self.mappings:
            return ""

        # Sort by generated position
        sorted_mappings = sorted(
            self.mappings,
            key=lambda m: (m.generated_line, m.generated_column)
        )

        result = []
        prev_generated_line = 1
        prev_generated_column = 0
        prev_source_line = 0
        prev_source_column = 0
        prev_name_index = 0

        for mapping in sorted_mappings:
            # Handle line changes
            while prev_generated_line < mapping.generated_line:
                result.append(';')
                prev_generated_line += 1
                prev_generated_column = 0

            if result and result[-1] != ';':
                result.append(',')

            # Generated column (relative to previous)
            result.append(self.encode_vlq(mapping.generated_column - prev_generated_column))
            prev_generated_column = mapping.generated_column

            # Source file index (always 0 for single file)
            result.append(self.encode_vlq(0))

            # Source line (relative to previous)
            result.append(self.encode_vlq(mapping.source_line - 1 - prev_source_line))
            prev_source_line = mapping.source_line - 1

            # Source column (relative to previous)
            result.append(self.encode_vlq(mapping.source_column - prev_source_column))
            prev_source_column = mapping.source_column

            # Name index (if present)
            if mapping.name:
                name_index = self.names.index(mapping.name)
                result.append(self.encode_vlq(name_index - prev_name_index))
                prev_name_index = name_index

        return ''.join(result)

    def generate(self) -> dict:
        """
        Generate complete source map

        Returns:
            Source map as dictionary
        """
        return {
            "version": 3,
            "file": self.generated_file,
            "sources": [self.source_file],
            "names": self.names,
            "mappings": self.generate_mappings_string()
        }

    def to_json(self, indent: Optional[int] = None) -> str:
        """
        Generate source map as JSON string

        Args:
            indent: JSON indentation (None for compact)

        Returns:
            JSON source map
        """
        return json.dumps(self.generate(), indent=indent)

    def to_base64(self) -> str:
        """
        Generate source map as base64 data URL

        Returns:
            Base64 encoded source map data URL
        """
        json_str = self.to_json()
        encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        return f"data:application/json;charset=utf-8;base64,{encoded}"

    def get_inline_comment(self) -> str:
        """
        Get source map as inline comment for JavaScript

        Returns:
            JavaScript comment with embedded source map
        """
        return f"//# sourceMappingURL={self.to_base64()}"

    def save(self, output_file: str) -> None:
        """
        Save source map to file

        Args:
            output_file: Path to output .map file
        """
        with open(output_file, 'w') as f:
            f.write(self.to_json(indent=2))
