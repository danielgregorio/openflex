"""
Tests for Selection functionality in NeoMXMLCompiler
"""

import pytest
from compiler.neo_mxml_compiler import NeoMXMLCompiler


class TestSelectionCompiler:
    """Tests for selection attribute recognition and code generation"""

    @pytest.fixture
    def compiler(self):
        """Create NeoMXMLCompiler instance"""
        return NeoMXMLCompiler()

    def test_list_selected_index_generates_tracking(self, compiler):
        """selectedIndex on List generates selection tracking code"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}, {label: "Banana"}];
        @reactive var selected: Number = -1;
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          selectedIndex="{selected}" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "currentSelectedIndex" in js
        assert "selected.value" in js

    def test_list_selected_index_adds_selected_class(self, compiler):
        """selectedIndex on List generates code to add 'selected' class"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
        @reactive var selected: Number = 0;
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          selectedIndex="{selected}" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "'neo-list-item selected'" in js or "selected" in js

    def test_list_change_event_generates_handler(self, compiler):
        """change event on List generates event handler call"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
        @reactive var selected: Number = -1;
        function onSelectionChange(event): void {
            trace("changed");
        }
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          selectedIndex="{selected}" change="onSelectionChange" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "onSelectionChange" in js
        assert "oldIndex !== index" in js

    def test_list_item_click_generates_handler(self, compiler):
        """itemClick event on List generates click handler"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
        function onItemClick(event): void {
            trace("clicked");
        }
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          itemClick="onItemClick" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "onItemClick" in js
        assert "addEventListener('click'" in js

    def test_list_item_double_click_generates_handler(self, compiler):
        """itemDoubleClick event on List generates dblclick handler"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
        function onItemDblClick(event): void {
            trace("double clicked");
        }
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          itemDoubleClick="onItemDblClick" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "onItemDblClick" in js
        assert "addEventListener('dblclick'" in js

    def test_datagrid_selected_index_generates_tracking(self, compiler):
        """selectedIndex on DataGrid generates selection tracking code"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var data: Array = [{name: "Alice", age: 30}];
        @reactive var selected: Number = -1;
    </fx:Script>
    <DataGrid dataProvider="{data}" selectedIndex="{selected}">
        <DataGridColumn headerText="Name" dataField="name" />
        <DataGridColumn headerText="Age" dataField="age" />
    </DataGrid>
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "currentSelectedIndex" in js
        assert "selected.value" in js

    def test_datagrid_change_event_generates_handler(self, compiler):
        """change event on DataGrid generates event handler call"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var data: Array = [{name: "Alice", age: 30}];
        @reactive var selected: Number = -1;
        function onRowChange(event): void {
            trace("changed");
        }
    </fx:Script>
    <DataGrid dataProvider="{data}" selectedIndex="{selected}" change="onRowChange">
        <DataGridColumn headerText="Name" dataField="name" />
    </DataGrid>
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "onRowChange" in js
        assert "oldIndex !== index" in js

    def test_selection_attrs_not_in_html_output(self, compiler):
        """Selection attributes should NOT appear as HTML attributes"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
        @reactive var selected: Number = 0;
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label"
          selectedIndex="{selected}" change="handler" itemClick="handler2" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        # The innerHTML template section should not contain these attributes
        if "innerHTML" in js:
            html_part = js.split("innerHTML")[1].split("`;")[0]
            assert "selectedIndex=" not in html_part
            assert "change=" not in html_part
            assert "itemClick=" not in html_part

    def test_no_selection_attrs_no_click_handler(self, compiler):
        """Without selection attributes, no click handler should be generated for items"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        # Should not have selection click handler
        assert "Selection click handler" not in js

    def test_event_object_contains_item_and_index(self, compiler):
        """Event handlers receive object with item and index"""
        mxml = """<?xml version="1.0" encoding="utf-8"?>
<Application xmlns:fx="http://openflex.dev/core">
    <fx:Script>
        @reactive var fruits: Array = [{label: "Apple"}];
        function onClick(event): void { }
    </fx:Script>
    <List dataProvider="{fruits}" labelField="label" itemClick="onClick" />
</Application>"""
        js = compiler.compile(mxml, "test.mxml")
        assert "{ item: item, index: index" in js
