"""
Tests for source map generation
"""

import json
import pytest
from compiler.sourcemap import SourceMapGenerator, SourceMapping
from compiler.parser.ast import SourceLocation


class TestSourceMapGenerator:
    """Tests for source map generation"""

    @pytest.fixture
    def generator(self):
        """Create source map generator"""
        return SourceMapGenerator(
            generated_file="output.js",
            source_file="input.as4"
        )

    def test_basic_source_map_structure(self, generator):
        """Test basic source map structure"""
        sourcemap = generator.generate()

        assert sourcemap["version"] == 3
        assert sourcemap["file"] == "output.js"
        assert sourcemap["sources"] == ["input.as4"]
        assert "mappings" in sourcemap
        assert "names" in sourcemap

    def test_add_simple_mapping(self, generator):
        """Test adding a simple mapping"""
        generator.add_mapping(
            generated_line=1,
            generated_column=0,
            source_line=1,
            source_column=0
        )

        assert len(generator.mappings) == 1
        mapping = generator.mappings[0]

        assert mapping.generated_line == 1
        assert mapping.generated_column == 0
        assert mapping.source_line == 1
        assert mapping.source_column == 0

    def test_add_mapping_with_name(self, generator):
        """Test adding mapping with identifier name"""
        generator.add_mapping(
            generated_line=1,
            generated_column=4,
            source_line=1,
            source_column=4,
            name="count"
        )

        assert len(generator.names) == 1
        assert "count" in generator.names

        mapping = generator.mappings[0]
        assert mapping.name == "count"

    def test_add_mapping_from_location(self, generator):
        """Test adding mapping from AST location"""
        location = SourceLocation(
            file="input.as4",
            line=5,
            column=10,
            end_line=5,
            end_column=15
        )

        generator.add_mapping_from_location(
            generated_line=3,
            generated_column=8,
            location=location,
            name="myVar"
        )

        mapping = generator.mappings[0]
        assert mapping.generated_line == 3
        assert mapping.generated_column == 8
        assert mapping.source_line == 5
        assert mapping.source_column == 9  # Column is 1-based in AST, 0-based in source map

    def test_vlq_encoding_positive(self, generator):
        """Test VLQ encoding of positive numbers"""
        assert generator.encode_vlq(0) == "A"
        assert generator.encode_vlq(1) == "C"
        assert generator.encode_vlq(15) == "e"

    def test_vlq_encoding_negative(self, generator):
        """Test VLQ encoding of negative numbers"""
        assert generator.encode_vlq(-1) == "D"
        assert generator.encode_vlq(-15) == "f"

    def test_mappings_string_single_line(self, generator):
        """Test mappings string with single line"""
        generator.add_mapping(1, 0, 1, 0)
        generator.add_mapping(1, 10, 1, 5)

        mappings = generator.generate_mappings_string()

        # Should contain two segments separated by comma
        assert ',' in mappings
        assert ';' not in mappings  # No line changes

    def test_mappings_string_multiple_lines(self, generator):
        """Test mappings string with multiple lines"""
        generator.add_mapping(1, 0, 1, 0)
        generator.add_mapping(2, 0, 2, 0)
        generator.add_mapping(3, 0, 3, 0)

        mappings = generator.generate_mappings_string()

        # Should contain semicolons for line changes
        assert mappings.count(';') >= 2

    def test_json_output(self, generator):
        """Test JSON output format"""
        generator.add_mapping(1, 0, 1, 0, name="test")

        json_str = generator.to_json()
        data = json.loads(json_str)

        assert data["version"] == 3
        assert data["file"] == "output.js"
        assert data["sources"] == ["input.as4"]
        assert "test" in data["names"]

    def test_base64_output(self, generator):
        """Test base64 data URL output"""
        generator.add_mapping(1, 0, 1, 0)

        base64_url = generator.to_base64()

        assert base64_url.startswith("data:application/json;charset=utf-8;base64,")

    def test_inline_comment(self, generator):
        """Test inline source map comment"""
        generator.add_mapping(1, 0, 1, 0)

        comment = generator.get_inline_comment()

        assert comment.startswith("//# sourceMappingURL=data:application/json")

    def test_multiple_names(self, generator):
        """Test handling multiple identifier names"""
        generator.add_mapping(1, 0, 1, 0, name="count")
        generator.add_mapping(1, 10, 1, 5, name="total")
        generator.add_mapping(2, 0, 2, 0, name="count")  # Reuse name

        assert len(generator.names) == 2
        assert "count" in generator.names
        assert "total" in generator.names

    def test_mappings_sorted_by_generated_position(self, generator):
        """Test mappings are sorted by generated position"""
        # Add mappings out of order
        generator.add_mapping(3, 0, 3, 0)
        generator.add_mapping(1, 0, 1, 0)
        generator.add_mapping(2, 5, 2, 2)
        generator.add_mapping(2, 0, 2, 0)

        mappings_str = generator.generate_mappings_string()

        # Should generate valid mappings string
        assert mappings_str

    def test_empty_mappings(self, generator):
        """Test generating source map with no mappings"""
        mappings_str = generator.generate_mappings_string()

        assert mappings_str == ""

    def test_save_to_file(self, generator, tmp_path):
        """Test saving source map to file"""
        generator.add_mapping(1, 0, 1, 0, name="test")

        output_file = tmp_path / "output.js.map"
        generator.save(str(output_file))

        assert output_file.exists()

        # Verify contents
        with open(output_file, 'r') as f:
            data = json.load(f)

        assert data["version"] == 3
        assert data["file"] == "output.js"
