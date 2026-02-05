"""
Tests for Drag-and-Drop compilation in NeoMXMLCompiler
"""

import pytest
from compiler.neo_mxml_compiler import NeoMXMLCompiler


class TestDnDCompiler:
    """Tests for DnD attribute recognition and code generation"""

    @pytest.fixture
    def compiler(self):
        """Create NeoMXMLCompiler instance"""
        return NeoMXMLCompiler()

    def test_list_drag_enabled_generates_setup_drag_source(self, compiler):
        """dragEnabled='true' on List generates setupDragSource in JS"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}, {label: "Banana"}];
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          dragEnabled="true" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "setupDragSource" in js

    def test_list_drop_enabled_generates_setup_drop_target(self, compiler):
        """dropEnabled='true' on List generates setupDropTarget in JS"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}, {label: "Banana"}];
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          dropEnabled="true" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "setupDropTarget" in js

    def test_no_dnd_attrs_no_import(self, compiler):
        """Without DnD attributes, no OpenFlexDnD import should be present"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "OpenFlexDnD" not in js
        assert "openflex-dnd" not in js

    def test_dnd_attrs_trigger_conditional_import(self, compiler):
        """With DnD attributes, conditional import of OpenFlexDnD is present"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          dragEnabled="true" dropEnabled="true" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "OpenFlexDnD" in js
        assert "openflex-dnd.js" in js

    def test_dnd_event_handlers_in_generated_js(self, compiler):
        """DnD event handlers (dragDrop='{handler}') appear in generated JS"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
        function handleDrop(event): void {
            trace("dropped");
        }
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          dropEnabled="true" dragDrop="handleDrop" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "onDragDrop" in js
        assert "handleDrop" in js

    def test_drag_move_enabled_generates_move_action(self, compiler):
        """dragMoveEnabled='true' generates action: 'move' in JS"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          dragEnabled="true" dragMoveEnabled="true" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "action: 'move'" in js

    def test_datagrid_drag_enabled_generates_setup_drag_source(self, compiler):
        """DataGrid with dragEnabled generates setupDragSource(row, ...)"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var data: Array = [{name: "Alice", age: 30}];
    </fx:Script>
    <DataGrid dataProvider="{data}" dragEnabled="true">
        <DataGridColumn headerText="Name" dataField="name" />
        <DataGridColumn headerText="Age" dataField="age" />
    </DataGrid>
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "setupDragSource(row" in js

    def test_dnd_attrs_not_in_html_output(self, compiler):
        """DnD attributes should NOT appear as HTML attributes in innerHTML"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          dragEnabled="true" dropEnabled="true" dragMoveEnabled="true" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        # The innerHTML template section should not contain these attributes
        # Find the innerHTML template
        assert "dragEnabled=" not in js.split("innerHTML")[1] if "innerHTML" in js else True
        assert "dropEnabled=" not in js.split("innerHTML")[1] if "innerHTML" in js else True
        assert "dragMoveEnabled=" not in js.split("innerHTML")[1] if "innerHTML" in js else True
