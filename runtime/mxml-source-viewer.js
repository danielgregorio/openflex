/**
 * MXML Source Viewer
 * Adiciona funcionalidade "View Source" com syntax highlighting para exemplos OpenFlex
 */

class MXMLSourceViewer {
    constructor() {
        this.isVisible = false;
        this.sourceCode = '';
    }

    /**
     * Inicializa o viewer com o caminho do arquivo MXML
     */
    async init(mxmlPath) {
        try {
            const response = await fetch(mxmlPath);
            this.sourceCode = await response.text();
            this.createUI();
        } catch (error) {
            console.error('Erro ao carregar MXML source:', error);
        }
    }

    /**
     * Aplica syntax highlighting básico ao código MXML
     */
    highlightMXML(code) {
        // Escape HTML
        code = code
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        // XML tags
        code = code.replace(/(&lt;\/?)([\w:]+)/g, '$1<span class="xml-tag">$2</span>');

        // Attributes
        code = code.replace(/([\w:]+)(=)/g, '<span class="xml-attr">$1</span>$2');

        // Strings
        code = code.replace(/("([^"]*)")/g, '<span class="xml-string">$1</span>');
        code = code.replace(/('([^']*)')/g, '<span class="xml-string">$1</span>');

        // Comments
        code = code.replace(/(&lt;!--.*?--&gt;)/g, '<span class="xml-comment">$1</span>');

        // CDATA
        code = code.replace(/(&lt;!\[CDATA\[[\s\S]*?\]\]&gt;)/g, '<span class="xml-cdata">$1</span>');

        // Keywords dentro de CDATA (AS4)
        code = code.replace(/\b(var|function|return|if|else|const|let|class|extends|implements|interface|public|private|protected|static|import|from|export|default|async|await|void|Number|String|Boolean|Array|Object)\b/g, '<span class="js-keyword">$1</span>');

        // Decorators AS4
        code = code.replace(/@(reactive|computed|bindable|inject)/g, '<span class="as4-decorator">@$1</span>');

        // Binding expressions
        code = code.replace(/(\{[^}]+\})/g, '<span class="mxml-binding">$1</span>');

        return code;
    }

    /**
     * Cria a UI do viewer
     */
    createUI() {
        // Criar botão flutuante
        const button = document.createElement('button');
        button.id = 'mxml-view-source-btn';
        button.innerHTML = '📄 View Source MXML';
        button.className = 'mxml-source-btn';
        button.onclick = () => this.toggle();
        document.body.appendChild(button);

        // Criar modal overlay
        const overlay = document.createElement('div');
        overlay.id = 'mxml-source-overlay';
        overlay.className = 'mxml-source-overlay';
        overlay.onclick = (e) => {
            if (e.target === overlay) this.hide();
        };

        // Criar modal content
        const modal = document.createElement('div');
        modal.className = 'mxml-source-modal';

        const header = document.createElement('div');
        header.className = 'mxml-source-header';
        header.innerHTML = `
            <h3>📄 MXML Source Code</h3>
            <button class="mxml-close-btn" onclick="window.mxmlSourceViewer.hide()">✖</button>
        `;

        const codeContainer = document.createElement('div');
        codeContainer.className = 'mxml-source-code-container';
        codeContainer.innerHTML = `<pre><code>${this.highlightMXML(this.sourceCode)}</code></pre>`;

        const footer = document.createElement('div');
        footer.className = 'mxml-source-footer';
        footer.innerHTML = `
            <span>OpenFlex Neo - Syntax: MXML + ActionScript 4</span>
            <button onclick="navigator.clipboard.writeText(window.mxmlSourceViewer.sourceCode); this.textContent='✅ Copiado!';">📋 Copiar Código</button>
        `;

        modal.appendChild(header);
        modal.appendChild(codeContainer);
        modal.appendChild(footer);
        overlay.appendChild(modal);
        document.body.appendChild(overlay);

        // Adicionar estilos
        this.injectStyles();
    }

    /**
     * Injeta estilos CSS
     */
    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .mxml-source-btn {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                background: linear-gradient(to bottom, #4a90e2 0%, #357abd 100%);
                color: white;
                border: 1px solid #2d5f8d;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                cursor: pointer;
                box-shadow: 0 3px 8px rgba(0, 0, 0, 0.3);
                transition: all 0.2s;
            }

            .mxml-source-btn:hover {
                background: linear-gradient(to bottom, #5a9ff2 0%, #4585cd 100%);
                transform: translateY(-2px);
                box-shadow: 0 5px 12px rgba(0, 0, 0, 0.4);
            }

            .mxml-source-overlay {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.7);
                z-index: 10000;
                backdrop-filter: blur(4px);
            }

            .mxml-source-overlay.visible {
                display: flex;
                align-items: center;
                justify-content: center;
                animation: fadeIn 0.2s;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .mxml-source-modal {
                background: white;
                border-radius: 8px;
                max-width: 90%;
                max-height: 90%;
                width: 1200px;
                display: flex;
                flex-direction: column;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
                animation: slideIn 0.3s;
            }

            @keyframes slideIn {
                from { transform: translateY(-50px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }

            .mxml-source-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 16px 20px;
                border-bottom: 2px solid #e0e0e0;
                background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
                border-radius: 8px 8px 0 0;
            }

            .mxml-source-header h3 {
                margin: 0;
                color: #2c3e50;
                font-size: 18px;
            }

            .mxml-close-btn {
                background: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.2s;
            }

            .mxml-close-btn:hover {
                background: #c82333;
            }

            .mxml-source-code-container {
                flex: 1;
                overflow: auto;
                background: #1e1e1e;
                padding: 0;
            }

            .mxml-source-code-container pre {
                margin: 0;
                padding: 20px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 13px;
                line-height: 1.6;
                color: #d4d4d4;
            }

            .mxml-source-code-container code {
                display: block;
            }

            .mxml-source-footer {
                padding: 12px 20px;
                border-top: 2px solid #e0e0e0;
                background: #f8f9fa;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 12px;
                color: #6c757d;
                border-radius: 0 0 8px 8px;
            }

            .mxml-source-footer button {
                background: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 14px;
                cursor: pointer;
                font-size: 12px;
                transition: background 0.2s;
            }

            .mxml-source-footer button:hover {
                background: #218838;
            }

            /* Syntax Highlighting */
            .xml-tag { color: #569cd6; font-weight: bold; }
            .xml-attr { color: #9cdcfe; }
            .xml-string { color: #ce9178; }
            .xml-comment { color: #6a9955; font-style: italic; }
            .xml-cdata { color: #d4d4d4; background: #2d2d30; }
            .js-keyword { color: #c586c0; font-weight: bold; }
            .as4-decorator { color: #dcdcaa; font-weight: bold; }
            .mxml-binding { color: #4ec9b0; font-weight: bold; }
        `;
        document.head.appendChild(style);
    }

    /**
     * Mostra o viewer
     */
    show() {
        this.isVisible = true;
        document.getElementById('mxml-source-overlay').classList.add('visible');
        document.getElementById('mxml-view-source-btn').textContent = '✖ Fechar Source';
    }

    /**
     * Esconde o viewer
     */
    hide() {
        this.isVisible = false;
        document.getElementById('mxml-source-overlay').classList.remove('visible');
        document.getElementById('mxml-view-source-btn').textContent = '📄 View Source MXML';
    }

    /**
     * Toggle visibility
     */
    toggle() {
        if (this.isVisible) {
            this.hide();
        } else {
            this.show();
        }
    }
}

// Instância global será criada pelos scripts HTML individuais
// window.mxmlSourceViewer = new MXMLSourceViewer();
