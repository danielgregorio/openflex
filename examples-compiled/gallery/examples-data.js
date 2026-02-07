/**
 * OpenFlex Example Gallery - Examples Catalog
 * Defines all available examples with metadata and file paths
 */

const ExamplesData = {
    // Tree structure for navigation
    tree: [
        {
            id: 'ui',
            name: 'UI Components',
            icon: '📱',
            children: [
                { id: 'counter', name: 'Counter', icon: '🔢' },
                { id: 'todo', name: 'Todo List', icon: '✅' },
                { id: 'calculator', name: 'Calculator', icon: '🧮' },
                { id: 'timer', name: 'Timer', icon: '⏱️' },
                { id: 'temperature', name: 'Temperature', icon: '🌡️' },
                { id: 'quiz', name: 'Quiz', icon: '🎯' },
                { id: 'dashboard', name: 'Dashboard', icon: '📊' },
                { id: 'colorpicker', name: 'Color Picker', icon: '🎨' },
                { id: 'form', name: 'Form Validation', icon: '📝' },
                { id: 'flexclassic', name: 'Design System', icon: '🎨' }
            ]
        },
        {
            id: 'data',
            name: 'Data Components',
            icon: '📊',
            children: [
                { id: 'datacomponents', name: 'List & DataGrid', icon: '📋' },
                { id: 'dragdrop', name: 'Drag & Drop', icon: '🎯' },
                { id: 'selection', name: 'Selection', icon: '☑️' },
                { id: 'itemrenderers', name: 'Item Renderers', icon: '🏷️' },
                { id: 'tree', name: 'Tree', icon: '🌳' }
            ]
        },
        {
            id: 'controls',
            name: 'Controls & Navigation',
            icon: '🎛️',
            children: [
                { id: 'sliders', name: 'Sliders & Steppers', icon: '🎚️' },
                { id: 'tabs', name: 'TabNavigator', icon: '📑' },
                { id: 'states', name: 'States & Transitions', icon: '🔄' },
                { id: 'calendar', name: 'Calendar & DatePicker', icon: '📅' },
                { id: 'popups', name: 'Popups & Alerts', icon: '💬' },
                { id: 'validators', name: 'Validators', icon: '✅' },
                { id: 'colorpickerdemo', name: 'ColorPicker (HSV)', icon: '🎨' },
                { id: 'cursors', name: 'CursorManager', icon: '🖱️' }
            ]
        },
        {
            id: 'charts',
            name: 'Charts',
            icon: '📈',
            children: [
                { id: 'chartdemo', name: 'Chart Demo (All)', icon: '📊' },
                { id: 'columnchart', name: 'Column Chart', icon: '📊' },
                { id: 'barchart', name: 'Bar Chart', icon: '📊' },
                { id: 'linechart', name: 'Line Chart', icon: '📈' },
                { id: 'areachart', name: 'Area Chart', icon: '📉' },
                { id: 'piechart', name: 'Pie Chart', icon: '🥧' },
                { id: 'doughnutchart', name: 'Doughnut Chart', icon: '🍩' }
            ]
        },
        {
            id: 'apps',
            name: 'Full Applications',
            icon: '🏢',
            children: [
                { id: 'ecommerce', name: 'E-Commerce Store', icon: '🛒' },
                { id: 'cms', name: 'CMS Editor', icon: '📰' }
            ]
        },
        {
            id: 'basic',
            name: 'Basic Examples',
            icon: '📦',
            children: [
                { id: 'simple', name: 'Simple Component', icon: '📄' },
                { id: 'counterbasic', name: 'Counter (Basic)', icon: '🔄' }
            ]
        }
    ],

    // Detailed example definitions
    examples: {
        // UI Components
        counter: {
            name: 'Counter',
            description: 'Simple reactive counter demonstrating @reactive signals and @computed properties',
            category: 'UI Components',
            tags: ['reactive', 'computed', 'beginner'],
            component: '../08-visual-ui/CounterApp-component.js',
            files: [
                { name: 'CounterApp.mxml', path: '../08-visual-ui/CounterApp.mxml', type: 'mxml' }
            ]
        },
        todo: {
            name: 'Todo List',
            description: 'Complete todo app with filters, array manipulation and two-way binding',
            category: 'UI Components',
            tags: ['reactive', 'repeater', 'filters'],
            component: '../08-visual-ui/TodoListApp-component.js',
            files: [
                { name: 'TodoListApp.mxml', path: '../08-visual-ui/TodoListApp.mxml', type: 'mxml' },
                { name: 'todo-list-app-data.json', path: '../08-visual-ui/todo-list-app-data.json', type: 'json' },
                { name: 'todo-list-app.css', path: '../08-visual-ui/todo-list-app.css', type: 'css' }
            ]
        },
        calculator: {
            name: 'Calculator',
            description: 'Functional calculator with grid layout and basic operations',
            category: 'UI Components',
            tags: ['grid', 'events', 'state'],
            component: '../08-visual-ui/CalculatorApp-component.js',
            files: [
                { name: 'CalculatorApp.mxml', path: '../08-visual-ui/CalculatorApp.mxml', type: 'mxml' },
                { name: 'calculator-app.css', path: '../08-visual-ui/calculator-app.css', type: 'css' }
            ]
        },
        timer: {
            name: 'Timer',
            description: 'Stopwatch with play/pause controls and time formatting',
            category: 'UI Components',
            tags: ['setInterval', 'formatting', 'controls'],
            component: '../08-visual-ui/TimerApp-component.js',
            files: [
                { name: 'TimerApp.mxml', path: '../08-visual-ui/TimerApp.mxml', type: 'mxml' },
                { name: 'timer-app.css', path: '../08-visual-ui/timer-app.css', type: 'css' }
            ]
        },
        temperature: {
            name: 'Temperature Converter',
            description: 'Multi-unit conversion with slider, dynamic colors and emojis',
            category: 'UI Components',
            tags: ['computed', 'binding', 'slider'],
            component: '../08-visual-ui/TemperatureApp-component.js',
            files: [
                { name: 'TemperatureApp.mxml', path: '../08-visual-ui/TemperatureApp.mxml', type: 'mxml' }
            ]
        },
        quiz: {
            name: 'Quiz',
            description: 'Multiple choice quiz with progress bar and scoring',
            category: 'UI Components',
            tags: ['state-machine', 'progress', 'scoring'],
            component: '../08-visual-ui/QuizApp-component.js',
            files: [
                { name: 'QuizApp.mxml', path: '../08-visual-ui/QuizApp.mxml', type: 'mxml' },
                { name: 'quiz-app-data.json', path: '../08-visual-ui/quiz-app-data.json', type: 'json' },
                { name: 'quiz-app.css', path: '../08-visual-ui/quiz-app.css', type: 'css' }
            ]
        },
        dashboard: {
            name: 'Dashboard',
            description: 'Executive dashboard with metric cards and number formatting',
            category: 'UI Components',
            tags: ['cards', 'formatting', 'layout'],
            component: '../08-visual-ui/DashboardApp-component.js',
            files: [
                { name: 'DashboardApp.mxml', path: '../08-visual-ui/DashboardApp.mxml', type: 'mxml' },
                { name: 'dashboard-app.css', path: '../08-visual-ui/dashboard-app.css', type: 'css' }
            ]
        },
        colorpicker: {
            name: 'Color Picker',
            description: 'RGB color picker with sliders and HEX/RGB conversion',
            category: 'UI Components',
            tags: ['computed', 'sliders', 'conversion'],
            component: '../08-visual-ui/ColorPickerApp-component.js',
            files: [
                { name: 'ColorPickerApp.mxml', path: '../08-visual-ui/ColorPickerApp.mxml', type: 'mxml' },
                { name: 'color-picker-app.css', path: '../08-visual-ui/color-picker-app.css', type: 'css' }
            ]
        },
        form: {
            name: 'Form Validation',
            description: 'Contact form with real-time validation and error messages',
            category: 'UI Components',
            tags: ['validation', 'regex', 'errors'],
            component: '../08-visual-ui/FormApp-component.js',
            files: [
                { name: 'FormApp.mxml', path: '../08-visual-ui/FormApp.mxml', type: 'mxml' },
                { name: 'form-app.css', path: '../08-visual-ui/form-app.css', type: 'css' }
            ]
        },
        flexclassic: {
            name: 'Design System',
            description: 'Complete iOS-style design system showcase with forms, toggles, lists, tabs and cards',
            category: 'UI Components',
            tags: ['design-system', 'ios', 'components', 'showcase'],
            component: '../08-visual-ui/FlexClassicDemo-component.js',
            files: [
                { name: 'FlexClassicDemo.mxml', path: '../08-visual-ui/FlexClassicDemo.mxml', type: 'mxml' }
            ]
        },

        // Data Components
        datacomponents: {
            name: 'List & DataGrid',
            description: 'Data-bound List, DataGrid, ComboBox and Repeater components',
            category: 'Data Components',
            tags: ['list', 'datagrid', 'combobox', 'repeater'],
            component: '../09-data-components/DataComponentsDemo-component.js',
            files: [
                { name: 'DataComponentsDemo.mxml', path: '../09-data-components/DataComponentsDemo.mxml', type: 'mxml' },
                { name: 'data-components-demo-data.json', path: '../09-data-components/data-components-demo-data.json', type: 'json' },
                { name: 'data-components-demo.css', path: '../09-data-components/data-components-demo.css', type: 'css' }
            ]
        },
        dragdrop: {
            name: 'Drag & Drop',
            description: 'Drag items between lists with visual feedback and drop indicators',
            category: 'Data Components',
            tags: ['dnd', 'dragEnabled', 'dropEnabled'],
            component: '../10-drag-drop/DragDropDemo-component.js',
            files: [
                { name: 'DragDropDemo.mxml', path: '../10-drag-drop/DragDropDemo.mxml', type: 'mxml' },
                { name: 'drag-drop-demo-data.json', path: '../10-drag-drop/drag-drop-demo-data.json', type: 'json' },
                { name: 'drag-drop-demo.css', path: '../10-drag-drop/drag-drop-demo.css', type: 'css' }
            ]
        },
        selection: {
            name: 'Selection',
            description: 'Selection tracking with selectedIndex, change and itemClick events',
            category: 'Data Components',
            tags: ['selection', 'selectedIndex', 'events'],
            component: '../11-selection/SelectionDemo-component.js',
            files: [
                { name: 'SelectionDemo.mxml', path: '../11-selection/SelectionDemo.mxml', type: 'mxml' },
                { name: 'selection-demo-data.json', path: '../11-selection/selection-demo-data.json', type: 'json' },
                { name: 'selection-demo.css', path: '../11-selection/selection-demo.css', type: 'css' }
            ]
        },
        itemrenderers: {
            name: 'Item Renderers',
            description: 'Custom formatting with labelFunction for List and DataGrid',
            category: 'Data Components',
            tags: ['labelFunction', 'formatting', 'renderers'],
            component: '../12-item-renderers/ItemRenderersDemo-component.js',
            files: [
                { name: 'ItemRenderersDemo.mxml', path: '../12-item-renderers/ItemRenderersDemo.mxml', type: 'mxml' },
                { name: 'item-renderers-demo-data.json', path: '../12-item-renderers/item-renderers-demo-data.json', type: 'json' },
                { name: 'item-renderers-demo.css', path: '../12-item-renderers/item-renderers-demo.css', type: 'css' }
            ]
        },
        tree: {
            name: 'Tree',
            description: 'Hierarchical tree with expand/collapse, icons and selection',
            category: 'Data Components',
            tags: ['tree', 'hierarchical', 'expand'],
            component: '../13-tree/TreeDemo-component.js',
            files: [
                { name: 'TreeDemo.mxml', path: '../13-tree/TreeDemo.mxml', type: 'mxml' },
                { name: 'tree-demo-data.json', path: '../13-tree/tree-demo-data.json', type: 'json' },
                { name: 'tree-demo.css', path: '../13-tree/tree-demo.css', type: 'css' }
            ]
        },

        // Controls & Navigation
        sliders: {
            name: 'Sliders & Steppers',
            description: 'HSlider, VSlider e NumericStepper com two-way binding e live dragging',
            category: 'Controls & Navigation',
            tags: ['slider', 'stepper', 'range', 'input'],
            component: '../15-sliders/SliderDemo-component.js',
            files: [
                { name: 'SliderDemo.mxml', path: '../15-sliders/SliderDemo.mxml', type: 'mxml' },
                { name: 'slider-demo.css', path: '../15-sliders/slider-demo.css', type: 'css' }
            ]
        },
        tabs: {
            name: 'TabNavigator',
            description: 'TabNavigator e ViewStack para navegacao entre views com tabs clicaveis',
            category: 'Controls & Navigation',
            tags: ['tabs', 'navigation', 'viewstack', 'panels'],
            component: '../18-tabs/TabNavigatorDemo-component.js',
            files: [
                { name: 'TabNavigatorDemo.mxml', path: '../18-tabs/TabNavigatorDemo.mxml', type: 'mxml' },
                { name: 'tabnavigator-demo.css', path: '../18-tabs/tabnavigator-demo.css', type: 'css' }
            ]
        },
        states: {
            name: 'States & Transitions',
            description: 'Estados de view dinamicos com transicoes suaves entre modos',
            category: 'Controls & Navigation',
            tags: ['states', 'transitions', 'view', 'dynamic'],
            component: '../16-states/StatesDemo-component.js',
            files: [
                { name: 'StatesDemo.mxml', path: '../16-states/StatesDemo.mxml', type: 'mxml' },
                { name: 'states-demo.css', path: '../16-states/states-demo.css', type: 'css' }
            ]
        },
        calendar: {
            name: 'Calendar & DatePicker',
            description: 'Calendar, DateField e DatePicker para selecao de datas',
            category: 'Controls & Navigation',
            tags: ['calendar', 'date', 'datepicker', 'datefield'],
            component: '../17-calendar/CalendarDemo-component.js',
            files: [
                { name: 'CalendarDemo.mxml', path: '../17-calendar/CalendarDemo.mxml', type: 'mxml' },
                { name: 'calendar-demo.css', path: '../17-calendar/calendar-demo.css', type: 'css' }
            ]
        },
        popups: {
            name: 'Popups & Alerts',
            description: 'Alert.show(), TitleWindow e PopUp para dialogos modais',
            category: 'Controls & Navigation',
            tags: ['alert', 'popup', 'modal', 'dialog', 'titlewindow'],
            component: '../19-popups/PopUpDemo-component.js',
            files: [
                { name: 'PopUpDemo.mxml', path: '../19-popups/PopUpDemo.mxml', type: 'mxml' },
                { name: 'popup-demo.css', path: '../19-popups/popup-demo.css', type: 'css' }
            ]
        },
        validators: {
            name: 'Validators',
            description: 'Validacao de formularios com Email, String, Number e RegExp validators',
            category: 'Controls & Navigation',
            tags: ['validation', 'form', 'email', 'regex', 'validators'],
            component: '../20-validators/ValidatorsDemo-component.js',
            files: [
                { name: 'ValidatorsDemo.mxml', path: '../20-validators/ValidatorsDemo.mxml', type: 'mxml' },
                { name: 'validators-demo.css', path: '../20-validators/validators-demo.css', type: 'css' }
            ]
        },
        colorpickerdemo: {
            name: 'ColorPicker (HSV)',
            description: 'Seletor de cores com picker HSV, input hex e swatches predefinidas',
            category: 'Controls & Navigation',
            tags: ['colorpicker', 'hsv', 'hex', 'color', 'picker'],
            component: '../21-colorpicker/ColorPickerDemo-component.js',
            files: [
                { name: 'ColorPickerDemo.mxml', path: '../21-colorpicker/ColorPickerDemo.mxml', type: 'mxml' },
                { name: 'colorpicker-demo.css', path: '../21-colorpicker/colorpicker-demo.css', type: 'css' }
            ]
        },
        cursors: {
            name: 'CursorManager',
            description: 'Sistema de gerenciamento de cursores Flex-style com busy, thinking, spinner e cursores customizados',
            category: 'Controls & Navigation',
            tags: ['cursor', 'cursormanager', 'busy', 'spinner', 'ui'],
            component: '../22-cursors/CursorDemo-component.js',
            files: [
                { name: 'CursorDemo.mxml', path: '../22-cursors/CursorDemo.mxml', type: 'mxml' },
                { name: 'cursor-demo.css', path: '../22-cursors/cursor-demo.css', type: 'css' }
            ]
        },

        // Charts
        chartdemo: {
            name: 'Chart Demo (All)',
            description: 'Demonstracao completa de todos os tipos de graficos: Column, Line, Area, Pie, Bar, Doughnut',
            category: 'Charts',
            tags: ['charts', 'echarts', 'visualization', 'reactive', 'all'],
            component: '../14-charts/ChartDemo-component.js',
            files: [
                { name: 'ChartDemo.mxml', path: '../14-charts/ChartDemo.mxml', type: 'mxml' },
                { name: 'chart-demo-data.json', path: '../14-charts/chart-demo-data.json', type: 'json' },
                { name: 'chart-demo.css', path: '../14-charts/chart-demo.css', type: 'css' }
            ]
        },
        columnchart: {
            name: 'Column Chart',
            description: 'Grafico de colunas verticais para comparar valores entre categorias',
            category: 'Charts',
            tags: ['charts', 'column', 'bar', 'comparison'],
            component: '../14-charts/ColumnChartDemo-component.js',
            files: [
                { name: 'ColumnChartDemo.mxml', path: '../14-charts/ColumnChartDemo.mxml', type: 'mxml' },
                { name: 'column-chart-demo-data.json', path: '../14-charts/column-chart-demo-data.json', type: 'json' }
            ]
        },
        barchart: {
            name: 'Bar Chart',
            description: 'Grafico de barras horizontais para rankings e comparacoes',
            category: 'Charts',
            tags: ['charts', 'bar', 'horizontal', 'ranking'],
            component: '../14-charts/BarChartDemo-component.js',
            files: [
                { name: 'BarChartDemo.mxml', path: '../14-charts/BarChartDemo.mxml', type: 'mxml' },
                { name: 'bar-chart-demo-data.json', path: '../14-charts/bar-chart-demo-data.json', type: 'json' }
            ]
        },
        linechart: {
            name: 'Line Chart',
            description: 'Grafico de linhas para tendencias e series temporais',
            category: 'Charts',
            tags: ['charts', 'line', 'trend', 'time-series'],
            component: '../14-charts/LineChartDemo-component.js',
            files: [
                { name: 'LineChartDemo.mxml', path: '../14-charts/LineChartDemo.mxml', type: 'mxml' },
                { name: 'line-chart-demo-data.json', path: '../14-charts/line-chart-demo-data.json', type: 'json' }
            ]
        },
        areachart: {
            name: 'Area Chart',
            description: 'Grafico de area para volumes acumulados e tendencias preenchidas',
            category: 'Charts',
            tags: ['charts', 'area', 'volume', 'cumulative'],
            component: '../14-charts/AreaChartDemo-component.js',
            files: [
                { name: 'AreaChartDemo.mxml', path: '../14-charts/AreaChartDemo.mxml', type: 'mxml' },
                { name: 'area-chart-demo-data.json', path: '../14-charts/area-chart-demo-data.json', type: 'json' }
            ]
        },
        piechart: {
            name: 'Pie Chart',
            description: 'Grafico de pizza para proporcoes e partes de um todo',
            category: 'Charts',
            tags: ['charts', 'pie', 'proportion', 'percentage'],
            component: '../14-charts/PieChartDemo-component.js',
            files: [
                { name: 'PieChartDemo.mxml', path: '../14-charts/PieChartDemo.mxml', type: 'mxml' },
                { name: 'pie-chart-demo-data.json', path: '../14-charts/pie-chart-demo-data.json', type: 'json' }
            ]
        },
        doughnutchart: {
            name: 'Doughnut Chart',
            description: 'Grafico de rosca com furo central para destacar totais',
            category: 'Charts',
            tags: ['charts', 'doughnut', 'donut', 'ring'],
            component: '../14-charts/DoughnutChartDemo-component.js',
            files: [
                { name: 'DoughnutChartDemo.mxml', path: '../14-charts/DoughnutChartDemo.mxml', type: 'mxml' },
                { name: 'doughnut-chart-demo-data.json', path: '../14-charts/doughnut-chart-demo-data.json', type: 'json' },
                { name: 'doughnut-chart-demo.css', path: '../14-charts/doughnut-chart-demo.css', type: 'css' }
            ]
        },

        // Full Applications
        ecommerce: {
            name: 'E-Commerce Store',
            description: 'Complete store with product listing and shopping cart',
            category: 'Full Applications',
            tags: ['app', 'cart', 'products'],
            component: '../05-full-apps/ecommerce/StoreApp-component.js',
            files: [
                { name: 'StoreApp.mxml', path: '../05-full-apps/ecommerce/StoreApp.mxml', type: 'mxml' },
                { name: 'ShoppingCart.mxml', path: '../05-full-apps/ecommerce/ShoppingCart.mxml', type: 'mxml' }
            ]
        },
        cms: {
            name: 'CMS Editor',
            description: 'Content management system with editor and preview',
            category: 'Full Applications',
            tags: ['app', 'cms', 'editor'],
            component: '../05-full-apps/cms/CMSApp-component.js',
            files: [
                { name: 'CMSApp.mxml', path: '../05-full-apps/cms/CMSApp.mxml', type: 'mxml' },
                { name: 'ContentEditor.mxml', path: '../05-full-apps/cms/ContentEditor.mxml', type: 'mxml' }
            ]
        },

        // Basic Examples
        simple: {
            name: 'Simple Component',
            description: 'Minimal MXML component example',
            category: 'Basic Examples',
            tags: ['basic', 'minimal', 'beginner'],
            component: '../04-components/simple-component.js',
            files: [
                { name: 'simple.mxml', path: '../04-components/simple.mxml', type: 'mxml' }
            ]
        },
        counterbasic: {
            name: 'Counter (Basic)',
            description: 'Basic counter example with simple structure',
            category: 'Basic Examples',
            tags: ['basic', 'counter', 'beginner'],
            component: '../04-components/counter/App-component.js',
            files: [
                { name: 'App.mxml', path: '../04-components/counter/App.mxml', type: 'mxml' }
            ]
        }
    }
};

// Export for use
if (typeof window !== 'undefined') {
    window.ExamplesData = ExamplesData;
}
