"""
OpenFlex Neo - Error Handling
Beautiful, helpful error messages with code snippets
"""

from typing import Optional, List
from compiler.parser.ast import SourceLocation


class CompilerError(Exception):
    """Base class for all compiler errors"""

    def __init__(
        self,
        message: str,
        location: Optional[SourceLocation] = None,
        suggestion: Optional[str] = None,
        source_code: Optional[str] = None
    ):
        self.message = message
        self.location = location
        self.suggestion = suggestion
        self.source_code = source_code
        super().__init__(message)

    def format_error(self, use_color: bool = True) -> str:
        """Format error with code snippet and helpful information"""
        lines = []

        # Color codes
        RED = '\033[91m' if use_color else ''
        YELLOW = '\033[93m' if use_color else ''
        BLUE = '\033[94m' if use_color else ''
        BOLD = '\033[1m' if use_color else ''
        RESET = '\033[0m' if use_color else ''
        DIM = '\033[2m' if use_color else ''

        # Error header
        lines.append(f"{RED}{BOLD}✗ Error:{RESET} {self.message}")

        # Location info
        if self.location:
            lines.append(f"{BLUE}  ╭─ {self.location.file}:{self.location.line}:{self.location.column}{RESET}")

            # Code snippet with line numbers
            if self.source_code:
                source_lines = self.source_code.split('\n')
                error_line_idx = self.location.line - 1

                # Show context: 2 lines before, error line, 2 lines after
                start_line = max(0, error_line_idx - 2)
                end_line = min(len(source_lines), error_line_idx + 3)

                for i in range(start_line, end_line):
                    line_num = i + 1
                    line_content = source_lines[i]

                    if i == error_line_idx:
                        # Error line - highlight
                        lines.append(f"{BLUE}  │{RESET}")
                        lines.append(f"{BLUE}  │ {DIM}{line_num:4}{RESET} │ {line_content}")

                        # Add caret pointer
                        col = self.location.column - 1
                        end_col = self.location.end_column - 1 if self.location.end_column else col + 1
                        pointer_length = max(1, end_col - col)
                        pointer = ' ' * col + RED + '^' * pointer_length + RESET
                        lines.append(f"{BLUE}  │{RESET}       │ {pointer}")
                    else:
                        # Context lines - dimmed
                        lines.append(f"{BLUE}  │ {DIM}{line_num:4} │ {line_content}{RESET}")

            lines.append(f"{BLUE}  ╰─{RESET}")

        # Suggestion
        if self.suggestion:
            lines.append(f"{YELLOW}{BOLD}  💡 Suggestion:{RESET} {self.suggestion}")

        return '\n'.join(lines)


class ParseError(CompilerError):
    """Error during parsing"""
    pass


class TypeError(CompilerError):
    """Error during type checking"""
    pass


class CodegenError(CompilerError):
    """Error during code generation"""
    pass


class ErrorFormatter:
    """Formats errors with helpful context"""

    @staticmethod
    def get_source_excerpt(source: str, line: int, column: int, context: int = 2) -> str:
        """Get excerpt of source code around error location"""
        lines = source.split('\n')
        start = max(0, line - context - 1)
        end = min(len(lines), line + context)
        return '\n'.join(lines[start:end])

    @staticmethod
    def suggest_fix(error_type: str, message: str) -> Optional[str]:
        """Suggest fixes for common errors"""
        suggestions = {
            'unexpected_token': "Check for missing semicolons, brackets, or parentheses",
            'undefined_variable': "Make sure the variable is declared before use",
            'type_mismatch': "Check that the types are compatible or add a type cast",
            'null_reference': "Use optional chaining (?.) or check for null first",
            'missing_return': "Add a return statement or change return type to void",
            'invalid_decorator': "Check decorator name and placement (decorators go before declarations)",
            'import_not_found': "Verify the import path and that the file exists",
            'unexpected_eof': "Check for unclosed brackets, braces, or quotes",
        }

        # Check error_type first
        if error_type and error_type in suggestions:
            return suggestions[error_type]

        # Fallback: check message content
        for key, suggestion in suggestions.items():
            if key in message.lower().replace(' ', '_'):
                return suggestion

        return None


def create_parse_error(
    message: str,
    source: str,
    location: Optional[SourceLocation] = None,
    error_type: Optional[str] = None
) -> ParseError:
    """Create a parse error with helpful context"""
    suggestion = ErrorFormatter.suggest_fix(error_type or '', message) if error_type else None

    return ParseError(
        message=message,
        location=location,
        suggestion=suggestion,
        source_code=source if location else None
    )


def create_type_error(
    message: str,
    source: str,
    location: Optional[SourceLocation] = None,
    expected_type: Optional[str] = None,
    actual_type: Optional[str] = None
) -> TypeError:
    """Create a type error with helpful context"""

    suggestion = None
    if expected_type and actual_type:
        suggestion = f"Expected type '{expected_type}' but got '{actual_type}'"
    else:
        suggestion = ErrorFormatter.suggest_fix('type_mismatch', message)

    return TypeError(
        message=message,
        location=location,
        suggestion=suggestion,
        source_code=source if location else None
    )


def create_codegen_error(
    message: str,
    source: str,
    location: Optional[SourceLocation] = None
) -> CodegenError:
    """Create a code generation error"""
    return CodegenError(
        message=message,
        location=location,
        source_code=source if location else None
    )


# Example error messages for common issues
COMMON_ERRORS = {
    'missing_semicolon': "Missing semicolon at end of statement",
    'unexpected_eof': "Unexpected end of file - check for unclosed brackets or quotes",
    'invalid_syntax': "Invalid syntax",
    'undefined_variable': "Variable '{name}' is not defined",
    'type_mismatch': "Type mismatch: cannot assign {actual} to {expected}",
    'null_safety': "Possible null reference - use optional chaining or null check",
    'missing_decorator': "Reactive variables require @reactive decorator",
    'duplicate_declaration': "Variable '{name}' is already declared",
}
