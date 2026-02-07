/**
 * OpenFlex Example Gallery - Main Application
 */

class ExampleGallery {
    constructor() {
        this.currentExample = null;
        this.openCategories = new Set(['ui', 'data', 'charts', 'controls']); // Default open categories
        this.sourceCache = {};
        this.sourceViewerOpen = false;

        this.init();
    }

    init() {
        this.renderTree();
        this.setupEventListeners();

        // Check URL hash for deep linking
        const hashExample = this.getExampleFromHash();
        if (hashExample && ExamplesData.examples[hashExample]) {
            this.selectExample(hashExample);
        } else {
            this.showWelcome();
        }
    }

    // ==================== URL Hash / Deep Linking ====================

    getExampleFromHash() {
        const hash = window.location.hash;
        if (hash && hash.startsWith('#app=')) {
            return hash.substring(5); // Remove '#app='
        }
        return null;
    }

    updateUrlHash(exampleId) {
        const newUrl = `${window.location.pathname}#app=${exampleId}`;
        window.history.pushState({ example: exampleId }, '', newUrl);
    }

    // ==================== Tree Navigation ====================

    renderTree() {
        const container = document.getElementById('sidebar-tree');
        container.innerHTML = '';

        ExamplesData.tree.forEach(category => {
            const categoryNode = this.createCategoryNode(category);
            container.appendChild(categoryNode);
        });
    }

    createCategoryNode(category) {
        const node = document.createElement('div');
        node.className = 'tree-node';
        node.dataset.id = category.id;

        const isOpen = this.openCategories.has(category.id);

        // Category item
        const item = document.createElement('div');
        item.className = 'tree-item category';
        item.innerHTML = `
            <span class="tree-disclosure ${isOpen ? 'open' : ''}">▶</span>
            <span class="tree-icon">${category.icon}</span>
            <span class="tree-label">${category.name}</span>
        `;

        item.addEventListener('click', (e) => {
            this.toggleCategory(category.id, node);
        });

        node.appendChild(item);

        // Children container
        const children = document.createElement('div');
        children.className = `tree-children ${isOpen ? 'open' : ''}`;

        category.children.forEach(example => {
            const exampleItem = this.createExampleItem(example);
            children.appendChild(exampleItem);
        });

        node.appendChild(children);
        return node;
    }

    createExampleItem(example) {
        const item = document.createElement('div');
        item.className = 'tree-item';
        item.dataset.id = example.id;
        item.innerHTML = `
            <span class="tree-disclosure empty">▶</span>
            <span class="tree-icon">${example.icon}</span>
            <span class="tree-label">${example.name}</span>
        `;

        item.addEventListener('click', (e) => {
            e.stopPropagation();
            this.selectExample(example.id);
        });

        return item;
    }

    toggleCategory(categoryId, node) {
        const children = node.querySelector('.tree-children');
        const disclosure = node.querySelector('.tree-disclosure');

        if (this.openCategories.has(categoryId)) {
            this.openCategories.delete(categoryId);
            children.classList.remove('open');
            disclosure.classList.remove('open');
        } else {
            this.openCategories.add(categoryId);
            children.classList.add('open');
            disclosure.classList.add('open');
        }
    }

    selectExample(exampleId, skipHashUpdate = false) {
        // Update selection in tree
        document.querySelectorAll('.tree-item.selected').forEach(el => {
            el.classList.remove('selected');
        });

        const item = document.querySelector(`.tree-item[data-id="${exampleId}"]`);
        if (item) {
            item.classList.add('selected');

            // Ensure parent category is expanded
            const categoryNode = item.closest('.tree-node');
            if (categoryNode) {
                const categoryId = categoryNode.dataset.id;
                if (!this.openCategories.has(categoryId)) {
                    this.openCategories.add(categoryId);
                    categoryNode.querySelector('.tree-children').classList.add('open');
                    categoryNode.querySelector('.tree-disclosure').classList.add('open');
                }
            }
        }

        // Update URL hash for deep linking
        if (!skipHashUpdate) {
            this.updateUrlHash(exampleId);
        }

        // Load example
        this.loadExample(exampleId);
    }

    // ==================== Example Loading ====================

    showWelcome() {
        const previewArea = document.getElementById('preview-area');
        previewArea.innerHTML = `
            <div class="welcome-screen">
                <div class="logo">🚀</div>
                <h2>OpenFlex Neo Examples</h2>
                <p>Select an example from the tree on the left to see it in action.
                   Each example demonstrates different features of the OpenFlex Neo framework.</p>
            </div>
        `;
        this.updateHeader(null);
    }

    showLoading() {
        const previewArea = document.getElementById('preview-area');
        previewArea.innerHTML = `
            <div class="loading-screen">
                <div class="loading-spinner"></div>
                <div>Loading example...</div>
            </div>
        `;
    }

    async loadExample(exampleId) {
        const example = ExamplesData.examples[exampleId];
        if (!example) {
            console.error('Example not found:', exampleId);
            return;
        }

        this.currentExample = { id: exampleId, ...example };
        this.showLoading();
        this.updateHeader(example);

        try {
            // Cache buster to force reload during development
            const cacheBuster = `?v=${Date.now()}`;

            // Fetch the component JS
            const componentResponse = await fetch(example.component + cacheBuster);
            if (!componentResponse.ok) {
                throw new Error(`Failed to load component: ${example.component} (${componentResponse.status})`);
            }
            let componentCode = await componentResponse.text();

            // Fetch the runtime (browser version without CommonJS exports)
            const runtimeResponse = await fetch('../runtime/openflex-runtime-browser.js' + cacheBuster);
            if (!runtimeResponse.ok) {
                throw new Error(`Failed to load runtime (${runtimeResponse.status})`);
            }
            const runtimeCode = await runtimeResponse.text();

            // Fetch the DnD runtime if needed
            let dndCode = '';
            if (componentCode.includes('OpenFlexDnD')) {
                const dndResponse = await fetch('../runtime/openflex-dnd.js' + cacheBuster);
                if (dndResponse.ok) {
                    dndCode = await dndResponse.text();
                }
            }

            // Fetch the Charts runtime if needed
            let chartsCode = '';
            if (componentCode.includes('OpenFlexCharts')) {
                const chartsResponse = await fetch('../runtime/openflex-charts.js' + cacheBuster);
                if (chartsResponse.ok) {
                    chartsCode = await chartsResponse.text();
                }
            }

            // Fetch the Calendar runtime if needed
            let calendarCode = '';
            if (componentCode.includes('OpenFlexCalendar')) {
                const calendarResponse = await fetch('../runtime/openflex-calendar.js' + cacheBuster);
                if (calendarResponse.ok) {
                    calendarCode = await calendarResponse.text();
                }
            }

            // Fetch the PopUp runtime if needed
            let popupCode = '';
            if (componentCode.includes('OpenFlexPopUp') || componentCode.includes('Alert.show')) {
                const popupResponse = await fetch('../runtime/openflex-popup.js' + cacheBuster);
                if (popupResponse.ok) {
                    popupCode = await popupResponse.text();
                }
            }

            // Fetch the Validators runtime if needed
            let validatorsCode = '';
            if (componentCode.includes('OpenFlexValidators')) {
                const validatorsResponse = await fetch('../runtime/openflex-validators.js' + cacheBuster);
                if (validatorsResponse.ok) {
                    validatorsCode = await validatorsResponse.text();
                }
            }

            // Fetch the ColorPicker runtime if needed
            let colorpickerCode = '';
            if (componentCode.includes('OpenFlexColorPicker')) {
                const colorpickerResponse = await fetch('../runtime/openflex-colorpicker.js' + cacheBuster);
                if (colorpickerResponse.ok) {
                    colorpickerCode = await colorpickerResponse.text();
                }
            }

            // Fetch the States runtime if needed
            let statesCode = '';
            if (componentCode.includes('OpenFlexStates')) {
                const statesResponse = await fetch('../runtime/openflex-states.js' + cacheBuster);
                if (statesResponse.ok) {
                    statesCode = await statesResponse.text();
                }
            }

            // Fetch the Cursor runtime if needed
            let cursorCode = '';
            if (componentCode.includes('CursorManager')) {
                const cursorResponse = await fetch('../runtime/openflex-cursor.js' + cacheBuster);
                if (cursorResponse.ok) {
                    cursorCode = await cursorResponse.text();
                }
            }

            // Fetch CSS theme
            const cssResponse = await fetch('../runtime/neo-flex-classic-theme.css' + cacheBuster);
            if (!cssResponse.ok) {
                throw new Error(`Failed to load CSS theme (${cssResponse.status})`);
            }
            const cssCode = await cssResponse.text();

            // Handle @import statements in the component's styles
            // Extract @import urls and fetch them, then inline the CSS
            const componentDir = example.component.substring(0, example.component.lastIndexOf('/') + 1);
            const importRegex = /@import\s+url\(['"]?([^'")]+)['"]?\);?/g;
            let match;
            const importPromises = [];
            const importUrls = [];

            while ((match = importRegex.exec(componentCode)) !== null) {
                const importUrl = match[1];
                importUrls.push({ original: match[0], url: importUrl });

                // Resolve relative URL based on component location
                let resolvedUrl = importUrl;
                if (!importUrl.startsWith('http') && !importUrl.startsWith('/')) {
                    // Handle ../runtime/ paths - they're relative to the component
                    if (importUrl.startsWith('../runtime/')) {
                        resolvedUrl = importUrl; // Already correct relative to gallery
                    } else {
                        resolvedUrl = componentDir + importUrl;
                    }
                }
                importPromises.push(
                    fetch(resolvedUrl)
                        .then(r => r.ok ? r.text() : '')
                        .catch(() => '')
                );
            }

            // Wait for all imports to be fetched
            const importedCss = await Promise.all(importPromises);

            // Replace @import statements with inlined CSS
            for (let i = 0; i < importUrls.length; i++) {
                componentCode = componentCode.replace(
                    importUrls[i].original,
                    `/* Inlined from ${importUrls[i].url} */\n${importedCss[i]}\n`
                );
            }

            // Handle fetch() calls for external JSON data files
            // Match patterns like: fetch('./tree-demo-data.json')
            const fetchRegex = /fetch\(['"]\.\/([^'"]+\.json)['"]\)/g;
            const dataFiles = {};
            let fetchMatch;

            while ((fetchMatch = fetchRegex.exec(componentCode)) !== null) {
                const jsonFile = fetchMatch[1];
                if (!dataFiles[jsonFile]) {
                    const resolvedUrl = componentDir + jsonFile;
                    try {
                        const dataResponse = await fetch(resolvedUrl + cacheBuster);
                        if (dataResponse.ok) {
                            const jsonData = await dataResponse.text();
                            dataFiles[jsonFile] = jsonData;
                        }
                    } catch (e) {
                        console.warn('Could not pre-fetch data file:', resolvedUrl);
                    }
                }
            }

            // Inject pre-fetched data as window.__PRELOADED_DATA__
            let preloadedDataCode = '';
            if (Object.keys(dataFiles).length > 0) {
                preloadedDataCode = `window.__PRELOADED_DATA__ = ${JSON.stringify(dataFiles)};`;

                // Replace fetch calls with preloaded data access
                for (const [filename, data] of Object.entries(dataFiles)) {
                    const originalFetch = `fetch('./${filename}')`;
                    const replacement = `Promise.resolve({ ok: true, json: () => Promise.resolve(JSON.parse(window.__PRELOADED_DATA__['${filename}'])) })`;
                    componentCode = componentCode.split(originalFetch).join(replacement);
                }
            }

            // Handle <link rel='stylesheet' href='./xxx.css'> in shadow DOM
            // Match patterns like: href='./tree-demo.css'
            const cssLinkRegex = /href=['"]\.\/([^'"]+\.css)['"]/g;
            let cssMatch;
            const processedCssFiles = new Set();

            while ((cssMatch = cssLinkRegex.exec(componentCode)) !== null) {
                const cssFile = cssMatch[1];
                if (processedCssFiles.has(cssFile)) continue;
                processedCssFiles.add(cssFile);

                const resolvedUrl = componentDir + cssFile;
                try {
                    const cssResponse = await fetch(resolvedUrl + cacheBuster);
                    if (cssResponse.ok) {
                        const cssContent = await cssResponse.text();
                        // Replace the link with inline style (handle both quote styles)
                        const linkPatternSingle = `<link rel='stylesheet' href='./${cssFile}'>`;
                        const linkPatternDouble = `<link rel="stylesheet" href="./${cssFile}">`;
                        const styleReplacement = `<style>/* Inlined from ${cssFile} */\n${cssContent}</style>`;
                        componentCode = componentCode.split(linkPatternSingle).join(styleReplacement);
                        componentCode = componentCode.split(linkPatternDouble).join(styleReplacement);
                    }
                } catch (e) {
                    console.warn('Could not pre-fetch CSS file:', resolvedUrl);
                }
            }

            // Create the preview
            this.renderPreview(componentCode, runtimeCode, dndCode, chartsCode, calendarCode, popupCode, validatorsCode, colorpickerCode, statesCode, cursorCode, cssCode, preloadedDataCode);

        } catch (error) {
            console.error('Error loading example:', error);
            this.showError(error.message);
        }
    }

    renderPreview(componentCode, runtimeCode, dndCode, chartsCode, calendarCode, popupCode, validatorsCode, colorpickerCode, statesCode, cursorCode, cssCode, preloadedDataCode = '') {
        const previewArea = document.getElementById('preview-area');

        // Check if ECharts is needed
        const needsECharts = chartsCode && chartsCode.length > 0;
        const echartsScript = needsECharts
            ? '<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"><\/script>'
            : '';

        // Build the HTML for the iframe
        const html = `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    ${echartsScript}
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 15px;
            background: #E8E8E8;
        }
        .error-display {
            color: #c00;
            background: #fee;
            border: 1px solid #c00;
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 12px;
            white-space: pre-wrap;
        }
        ${cssCode}
    </style>
</head>
<body>
    <script>
        // Global error handler
        window.onerror = function(msg, url, line, col, error) {
            document.body.innerHTML = '<div class="error-display">Error: ' + msg + '\\nLine: ' + line + '</div>';
            return true;
        };
    <\/script>
    <script>
        // Preloaded data for external JSON files
        ${preloadedDataCode}
    <\/script>
    <script>
        // Runtime
        ${runtimeCode}
    <\/script>
    <script>
        // Verify runtime loaded
        if (!window.OpenFlexRuntime) {
            console.error('OpenFlexRuntime not loaded!');
            document.body.innerHTML = '<div class="error-display">Error: OpenFlexRuntime not loaded</div>';
        }
    <\/script>
    ${dndCode ? `<script>${dndCode}<\/script>` : ''}
    ${chartsCode ? `<script>${chartsCode}<\/script>` : ''}
    ${calendarCode ? `<script>${calendarCode}<\/script>` : ''}
    ${popupCode ? `<script>${popupCode}<\/script>` : ''}
    ${validatorsCode ? `<script>${validatorsCode}<\/script>` : ''}
    ${colorpickerCode ? `<script>${colorpickerCode}<\/script>` : ''}
    ${statesCode ? `<script>${statesCode}<\/script>` : ''}
    ${cursorCode ? `<script>${cursorCode}<\/script>` : ''}
    <script>
        // Component
        ${componentCode}
    <\/script>
    <app-root></app-root>
</body>
</html>`;

        // Create iframe with srcdoc via JavaScript property (more reliable than attribute)
        previewArea.innerHTML = '';
        const iframe = document.createElement('iframe');
        iframe.className = 'preview-frame';
        // allow-scripts: Run JavaScript
        // allow-same-origin: Required for external CDN scripts like ECharts
        iframe.sandbox = 'allow-scripts allow-same-origin';
        iframe.srcdoc = html;
        previewArea.appendChild(iframe);
    }

    showError(message) {
        const previewArea = document.getElementById('preview-area');
        previewArea.innerHTML = `
            <div class="welcome-screen">
                <div class="logo">⚠️</div>
                <h2>Error Loading Example</h2>
                <p>${message}</p>
            </div>
        `;
    }

    updateHeader(example) {
        const header = document.getElementById('preview-header');

        if (!example) {
            header.innerHTML = `
                <span class="preview-title">Welcome</span>
                <span class="preview-spacer"></span>
            `;
            return;
        }

        const tagsHtml = example.tags.map(tag =>
            `<span class="preview-tag">${tag}</span>`
        ).join('');

        header.innerHTML = `
            <span class="preview-title">${example.name}</span>
            <span class="preview-category">${example.category}</span>
            <div class="preview-tags">${tagsHtml}</div>
            <span class="preview-spacer"></span>
            <div class="preview-actions">
                <button class="preview-btn" onclick="gallery.toggleSource()">
                    📄 View Source
                </button>
                <button class="preview-btn" onclick="gallery.openInNewTab()">
                    🔗 Open in Tab
                </button>
            </div>
        `;
    }

    // ==================== Source Viewer ====================

    async toggleSource() {
        const viewer = document.getElementById('source-viewer');

        if (this.sourceViewerOpen) {
            viewer.classList.remove('open');
            this.sourceViewerOpen = false;
            return;
        }

        if (!this.currentExample) return;

        this.sourceViewerOpen = true;
        viewer.classList.add('open');

        // Load source files
        await this.loadSourceFiles();
    }

    async loadSourceFiles() {
        if (!this.currentExample) return;

        const tabs = document.getElementById('source-tabs');
        const content = document.getElementById('source-content');

        tabs.innerHTML = '';
        content.innerHTML = '<div class="loading-screen"><div class="loading-spinner"></div></div>';

        const files = this.currentExample.files;
        const sources = {};

        // Load all files
        for (const file of files) {
            try {
                const cacheKey = file.path;
                if (!this.sourceCache[cacheKey]) {
                    const response = await fetch(file.path);
                    this.sourceCache[cacheKey] = await response.text();
                }
                sources[file.name] = {
                    content: this.sourceCache[cacheKey],
                    type: file.type
                };
            } catch (error) {
                sources[file.name] = {
                    content: `// Error loading file: ${error.message}`,
                    type: file.type
                };
            }
        }

        // Also load compiled JS
        const jsFile = this.currentExample.component;
        const jsName = jsFile.split('/').pop();
        try {
            if (!this.sourceCache[jsFile]) {
                const response = await fetch(jsFile);
                this.sourceCache[jsFile] = await response.text();
            }
            sources[jsName] = {
                content: this.sourceCache[jsFile],
                type: 'js'
            };
        } catch (error) {
            // Ignore JS loading errors
        }

        // Render tabs
        let first = true;
        for (const [name, data] of Object.entries(sources)) {
            const tab = document.createElement('button');
            tab.className = `source-tab ${first ? 'active' : ''}`;
            tab.textContent = name;
            tab.onclick = () => this.showSourceTab(name, sources);
            tabs.appendChild(tab);

            if (first) {
                this.showSourceContent(data.content, data.type);
                first = false;
            }
        }
    }

    showSourceTab(name, sources) {
        // Update active tab
        document.querySelectorAll('.source-tab').forEach(tab => {
            tab.classList.toggle('active', tab.textContent === name);
        });

        const data = sources[name];
        this.showSourceContent(data.content, data.type);
    }

    showSourceContent(content, type) {
        const container = document.getElementById('source-content');
        const highlighted = this.highlightSyntax(content, type);
        container.innerHTML = `<pre class="source-code">${highlighted}</pre>`;
    }

    highlightSyntax(code, type) {
        // Tokenization approach to avoid regex conflicts
        let html = this.escapeHtmlLight(code);
        const tokens = [];

        const placeholder = (cls, content) => {
            const id = tokens.length;
            tokens.push({ cls, content });
            return `\uE000${id}\uE001`; // Private Use Area characters as placeholders
        };

        if (type === 'mxml' || type === 'xml') {
            // 1. Comments first (highest priority)
            html = html.replace(/(&lt;!--[\s\S]*?--&gt;)/g, m => placeholder('comment', m));

            // 2. CDATA sections - capture separately
            html = html.replace(/(&lt;!\[CDATA\[)([\s\S]*?)(\]\]&gt;)/g, (m, open, content, close) => {
                return placeholder('comment', open) + placeholder('cdata', content) + placeholder('comment', close);
            });

            // 3. String values in attributes
            html = html.replace(/(&quot;[^&]*&quot;)/g, m => placeholder('value', m));
            html = html.replace(/(&#39;[^&]*&#39;)/g, m => placeholder('value', m));

            // 4. Binding expressions {expr}
            html = html.replace(/\{([^}]+)\}/g, (m, expr) => placeholder('binding', '{' + expr + '}'));

            // 5. Tag brackets and names
            html = html.replace(/(&lt;\/?)([\w:]+)/g, (m, bracket, tag) => {
                return placeholder('bracket', bracket) + placeholder('tag', tag);
            });

            // 6. Closing brackets
            html = html.replace(/\/&gt;/g, m => placeholder('bracket', '/&gt;'));
            html = html.replace(/&gt;/g, m => placeholder('bracket', '&gt;'));

            // 7. Attribute names
            html = html.replace(/([\w:.-]+)=/g, (m, attr) => placeholder('attr', attr) + '=');

            // 8. AS4 decorators in CDATA
            html = html.replace(/@(reactive|computed|bindable)\b/g, m => placeholder('decorator', m));

            // 9. Keywords
            html = html.replace(/\b(var|function|return|if|else|const|let|new|this|true|false|null)\b/g,
                m => placeholder('keyword', m));

        } else if (type === 'js') {
            // Comments
            html = html.replace(/(\/\/.*$)/gm, m => placeholder('comment', m));
            html = html.replace(/(\/\*[\s\S]*?\*\/)/g, m => placeholder('comment', m));
            // Strings
            html = html.replace(/(&quot;[^&]*&quot;)/g, m => placeholder('string', m));
            html = html.replace(/(&#39;[^&]*&#39;)/g, m => placeholder('string', m));
            html = html.replace(/(`[^`]*`)/g, m => placeholder('string', m));
            // Keywords
            html = html.replace(/\b(const|let|var|function|class|extends|return|if|else|for|while|new|this|typeof|instanceof)\b/g,
                m => placeholder('keyword', m));

        } else if (type === 'json') {
            // JSON keys
            html = html.replace(/(&quot;[\w]+&quot;)(\s*:)/g, (m, key, colon) => placeholder('attr', key) + colon);
            // JSON string values
            html = html.replace(/:(\s*)(&quot;[^&]*&quot;)/g, (m, space, val) => ':' + space + placeholder('string', val));
            // JSON numbers
            html = html.replace(/:\s*(-?\d+\.?\d*)/g, (m, num) => ': ' + placeholder('number', num));
            // JSON booleans/null
            html = html.replace(/\b(true|false|null)\b/g, m => placeholder('keyword', m));

        } else if (type === 'css') {
            // CSS comments
            html = html.replace(/(\/\*[\s\S]*?\*\/)/g, m => placeholder('comment', m));
            // CSS selectors
            html = html.replace(/^([.#]?[\w-]+)/gm, m => placeholder('tag', m));
            // CSS properties
            html = html.replace(/([\w-]+)(\s*:)/g, (m, prop, colon) => placeholder('attr', prop) + colon);
            // CSS values
            html = html.replace(/:([^;{]+)/g, (m, val) => ':' + placeholder('value', val));
        }

        // Replace all placeholders with actual spans
        for (let i = 0; i < tokens.length; i++) {
            const { cls, content } = tokens[i];
            html = html.split(`\uE000${i}\uE001`).join(`<span class="hl-${cls}">${content}</span>`);
        }

        return html;
    }

    escapeHtmlLight(text) {
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    closeSource() {
        const viewer = document.getElementById('source-viewer');
        viewer.classList.remove('open');
        this.sourceViewerOpen = false;
    }

    // ==================== Actions ====================

    openInNewTab() {
        if (!this.currentExample) return;

        // Map example IDs to their HTML file paths
        const htmlPaths = {
            // UI Components
            counter: '../08-visual-ui/counter-test.html',
            todo: '../08-visual-ui/todolist-test.html',
            calculator: '../08-visual-ui/calculatorapp-test.html',
            timer: '../08-visual-ui/timerapp-test.html',
            temperature: '../08-visual-ui/temperatureapp-test.html',
            quiz: '../08-visual-ui/quizapp-test.html',
            dashboard: '../08-visual-ui/dashboardapp-test.html',
            colorpicker: '../08-visual-ui/colorpickerapp-test.html',
            form: '../08-visual-ui/formapp-test.html',
            flexclassic: '../08-visual-ui/flex-classic-demo.html',
            // Data Components
            datacomponents: '../09-data-components/data-components-demo.html',
            dragdrop: '../10-drag-drop/drag-drop-demo.html',
            selection: '../11-selection/selection-demo.html',
            itemrenderers: '../12-item-renderers/item-renderers-demo.html',
            tree: '../13-tree/tree-demo.html',
            // Charts
            chartdemo: '../14-charts/chart-demo.html',
            columnchart: '../14-charts/column-chart-demo.html',
            barchart: '../14-charts/bar-chart-demo.html',
            linechart: '../14-charts/line-chart-demo.html',
            areachart: '../14-charts/area-chart-demo.html',
            piechart: '../14-charts/pie-chart-demo.html',
            doughnutchart: '../14-charts/doughnut-chart-demo.html',
            // Controls & Navigation
            sliders: '../15-sliders/sliderdemo-test.html',
            states: '../16-states/statesdemo-test.html',
            calendar: '../17-calendar/calendardemo-test.html',
            tabs: '../18-tabs/tabnavigatordemo-test.html',
            popups: '../19-popups/popupdemo-test.html',
            validators: '../20-validators/validatorsdemo-test.html',
            colorpickerdemo: '../21-colorpicker/colorpickerdemo-test.html',
            cursors: '../22-cursors/cursor-demo.html',
            // Full Apps (may need mock server)
            ecommerce: '../05-full-apps/ecommerce/store-app.html',
            cms: '../05-full-apps/cms/cms-app.html',
            // Basic
            simple: '../04-components/simple.html',
            counterbasic: '../04-components/counter/index.html'
        };

        const htmlPath = htmlPaths[this.currentExample.id];
        if (htmlPath) {
            window.open(htmlPath, '_blank');
        } else {
            alert(`HTML file not found for: ${this.currentExample.name}`);
        }
    }

    // ==================== Search ====================

    setupEventListeners() {
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filterTree(e.target.value);
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.sourceViewerOpen) {
                this.closeSource();
            }
        });

        // Browser back/forward navigation
        window.addEventListener('popstate', (e) => {
            const hashExample = this.getExampleFromHash();
            if (hashExample && ExamplesData.examples[hashExample]) {
                this.selectExample(hashExample, true); // skipHashUpdate = true
            } else {
                this.showWelcome();
            }
        });
    }

    filterTree(query) {
        const normalizedQuery = query.toLowerCase().trim();

        if (!normalizedQuery) {
            // Show all
            document.querySelectorAll('.tree-node').forEach(node => {
                node.style.display = '';
            });
            document.querySelectorAll('.tree-item').forEach(item => {
                item.style.display = '';
            });
            return;
        }

        // Filter examples
        document.querySelectorAll('.tree-node').forEach(categoryNode => {
            const categoryId = categoryNode.dataset.id;
            let hasVisibleChildren = false;

            categoryNode.querySelectorAll('.tree-item:not(.category)').forEach(item => {
                const exampleId = item.dataset.id;
                const example = ExamplesData.examples[exampleId];

                if (!example) {
                    item.style.display = 'none';
                    return;
                }

                const matches =
                    example.name.toLowerCase().includes(normalizedQuery) ||
                    example.description.toLowerCase().includes(normalizedQuery) ||
                    example.tags.some(tag => tag.toLowerCase().includes(normalizedQuery));

                item.style.display = matches ? '' : 'none';
                if (matches) hasVisibleChildren = true;
            });

            // Show/hide category based on whether it has visible children
            categoryNode.style.display = hasVisibleChildren ? '' : 'none';

            // Auto-expand categories with matches
            if (hasVisibleChildren && normalizedQuery) {
                this.openCategories.add(categoryId);
                categoryNode.querySelector('.tree-children').classList.add('open');
                categoryNode.querySelector('.tree-disclosure').classList.add('open');
            }
        });
    }
}

// Initialize gallery
let gallery;
document.addEventListener('DOMContentLoaded', () => {
    gallery = new ExampleGallery();
});
