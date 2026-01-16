# 📄 MXML Source Viewer

Visualizador interativo de código-fonte MXML com syntax highlighting para todos os exemplos OpenFlex Neo.

## ✨ Features

### 🎨 Syntax Highlighting Completo
- **XML Tags** (azul): `<Application>`, `<VBox>`, `<DataGrid>`
- **Atributos** (ciano): `dataProvider`, `labelField`, `width`
- **Strings** (laranja): valores entre aspas
- **Comentários** (verde): `<!-- comentários XML -->`
- **Keywords AS4** (roxo): `var`, `function`, `return`, `if`, `else`
- **Decorators** (amarelo): `@reactive`, `@computed`, `@bindable`
- **Binding Expressions** (teal): `{variavel}`, `{computed.value}`
- **CDATA** (cinza escuro): código ActionScript 4

### 🎯 Interface Moderna
- Botão flutuante no canto superior direito
- Modal overlay elegante com backdrop blur
- Animações suaves (fadeIn/slideIn)
- Scroll vertical/horizontal automático
- Tema dark (#1e1e1e) estilo VS Code
- Responsivo e acessível

### 🔧 Funcionalidades
- **Copiar código** para clipboard com um clique
- **Feedback visual** quando código é copiado (✅ Copiado!)
- **Auto-detecção** do arquivo MXML correspondente
- **Fechar com ESC** ou clicando fora do modal
- **Botão dinâmico**: "View Source" ↔ "Fechar Source"

## 📦 Instalação

### Opção 1: Automática (Script Python)

```bash
python add-source-viewer-to-all.py
```

Este script:
- Encontra todos os HTMLs em `examples-compiled/`
- Adiciona o script do viewer automaticamente
- Calcula caminhos relativos corretos
- Detecta nomes de arquivos MXML por heurísticas

### Opção 2: Manual

Adicione ao final do `<body>` do seu HTML:

```html
<script src="../../runtime/mxml-source-viewer.js"></script>

<script>
    // Inicializar viewer de source code MXML
    document.addEventListener('DOMContentLoaded', () => {
        if (typeof MXMLSourceViewer !== 'undefined') {
            window.mxmlSourceViewer = new MXMLSourceViewer();
            window.mxmlSourceViewer.init('SeuArquivo.mxml');
        }
    });
</script>
```

**Ajuste o caminho relativo** de acordo com a profundidade do seu HTML:

| HTML Location | Script Path |
|---------------|-------------|
| `examples-compiled/*.html` | `runtime/mxml-source-viewer.js` |
| `examples-compiled/08-visual-ui/*.html` | `../runtime/mxml-source-viewer.js` |
| `examples-compiled/09-data-components/*.html` | `../../runtime/mxml-source-viewer.js` |

## 🎨 Customização

### Modificar Estilos

O viewer injeta estilos dinamicamente. Para customizar, edite `runtime/mxml-source-viewer.js`:

```javascript
// Botão flutuante (linha ~111)
.mxml-source-btn {
    background: linear-gradient(to bottom, #4a90e2 0%, #357abd 100%);
    // ... seus estilos
}

// Modal (linha ~145)
.mxml-source-modal {
    max-width: 90%;
    width: 1200px;
    // ... seus estilos
}

// Código (linha ~177)
.mxml-source-code-container pre {
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 13px;
    // ... seus estilos
}
```

### Modificar Cores de Syntax

```javascript
// Syntax Highlighting (linha ~256)
.xml-tag { color: #569cd6; font-weight: bold; }
.xml-attr { color: #9cdcfe; }
.xml-string { color: #ce9178; }
.js-keyword { color: #c586c0; font-weight: bold; }
.as4-decorator { color: #dcdcaa; font-weight: bold; }
.mxml-binding { color: #4ec9b0; font-weight: bold; }
```

## 🔍 Como Funciona

1. **Carrega MXML via fetch**: `await fetch(mxmlPath)`
2. **Aplica highlighting**: regex para detectar tags, atributos, strings, etc
3. **Cria UI dinamicamente**: botão + modal overlay
4. **Injeta estilos**: CSS inline no `<head>`
5. **Gerencia estado**: show/hide via classes CSS

## 📚 API

### Classe `MXMLSourceViewer`

```javascript
class MXMLSourceViewer {
    async init(mxmlPath)     // Carrega e inicializa o viewer
    show()                    // Mostra o modal
    hide()                    // Esconde o modal
    toggle()                  // Alterna visibilidade
    highlightMXML(code)       // Aplica syntax highlighting
    createUI()                // Cria elementos DOM
    injectStyles()            // Injeta CSS
}
```

### Uso Programático

```javascript
// Criar instância
const viewer = new MXMLSourceViewer();

// Inicializar com arquivo MXML
await viewer.init('MeuApp.mxml');

// Controlar visibilidade
viewer.show();
viewer.hide();
viewer.toggle();

// Acessar código fonte
console.log(viewer.sourceCode);
```

## 🎯 Exemplos

### Todos os 20 exemplos já incluem o viewer:

#### Básicos
- ✅ `01-basics/run-example.html`
- ✅ `02-modern-js/run-example.html`
- ✅ `03-reactive/run-example.html`
- ✅ `06-advanced/run-example.html`
- ✅ `07-real-apis/run-example.html`

#### Visual UI (10 exemplos)
- ✅ `08-visual-ui/counter-test.html`
- ✅ `08-visual-ui/todolist-test.html`
- ✅ `08-visual-ui/calculatorapp-test.html`
- ✅ `08-visual-ui/formapp-test.html`
- ✅ `08-visual-ui/quizapp-test.html`
- ✅ `08-visual-ui/timerapp-test.html`
- ✅ `08-visual-ui/temperatureapp-test.html`
- ✅ `08-visual-ui/dashboardapp-test.html`
- ✅ `08-visual-ui/colorpickerapp-test.html`
- ✅ `08-visual-ui/flex-classic-demo.html`

#### Data Components
- ✅ `09-data-components/data-components-demo.html`

## 🐛 Troubleshooting

### Botão não aparece
- Verifique se o script está carregando: `console.log(typeof MXMLSourceViewer)`
- Confirme que `DOMContentLoaded` foi disparado
- Verifique erros no console (F12)

### Arquivo MXML não carrega
- Confirme que o arquivo existe no mesmo diretório do HTML
- Verifique o nome passado para `init()` (case-sensitive)
- Veja erros de CORS no console (use um servidor HTTP, não `file://`)

### Syntax highlighting quebrado
- Código MXML deve ser válido XML
- Verifique se `<` e `>` estão escapados corretamente
- Confira regex em `highlightMXML()` (linha ~28)

### Botão "Copiar" não funciona
- Navegador precisa suportar `navigator.clipboard`
- Página deve estar em HTTPS ou localhost
- Verifique se `window.mxmlSourceViewer.sourceCode` está definido

## 🚀 Performance

- **Lazy loading**: UI só é criada após `init()`
- **Cache**: Código MXML carregado uma vez
- **CSS injected**: Apenas 1 `<style>` tag
- **Minimalista**: 307 linhas, ~13KB não-minificado

## 🎓 Inspiração

Baseado no "View Source" do Adobe Flex SDK Tour de Force, com design modernizado para 2024/2025.

## 📝 License

MIT - Mesma licença do OpenFlex Neo

---

**Criado por**: Claude (Anthropic)
**Data**: Janeiro 2025
**Versão**: 1.0.0
