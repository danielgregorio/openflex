# 🎨 Interfaces Visuais Reativas

**Finalmente interfaces visuais REAIS!** Estes exemplos criam UIs interativas no navegador com botões, inputs, animações e reatividade.

## 🆚 Diferença dos Outros Exemplos

| Outros Exemplos | Estes Exemplos |
|----------------|----------------|
| `trace()` / console.log | **UI visual no DOM** |
| Apenas texto | **Botões, inputs, listas** |
| Sem interação | **Totalmente interativo** |
| Output estático | **Reativo e dinâmico** |

## 📂 Exemplos Disponíveis

### 🔢 01 - Contador Reativo

**Arquivo:** `01-counter-visual.html`

Interface de contador com:
- ✅ **Botões visuais** (incrementar/decrementar/reset)
- ✅ **Display numérico grande** com animações
- ✅ **Histórico de ações** com timestamp
- ✅ **Estado reativo** usando Signals
- ✅ **Updates automáticos** da UI

### ✅ 02 - Lista de Tarefas

**Arquivo:** `02-todo-list-visual.html`

Todo List completa com:
- ✅ **Input** para adicionar tarefas
- ✅ **Checkboxes** para marcar como completo
- ✅ **Botões** para remover tarefas
- ✅ **Filtros** (Todas/Ativas/Completas)
- ✅ **Estatísticas** em tempo real
- ✅ **Limpar completadas**

## 🚀 Como Usar

```bash
# Servir a pasta
cd examples-compiled
python -m http.server 8000

# Abrir: http://localhost:8000/08-visual-ui/index.html
```

## 🔧 Como Funciona a Reatividade

### Signals (Estado Reativo)
```javascript
const count = new Signal(0);
count.value = 5;  // Notifica subscribers
```

### Effects (Atualizações Automáticas)
```javascript
createEffect(() => {
    element.textContent = count.value;  // Atualiza automaticamente
});
```

## 💡 Conceitos Demonstrados

- ✅ Reatividade Fine-Grained (Signals + Effects)
- ✅ DOM Manipulation
- ✅ Event Handling
- ✅ Array Methods (map, filter)
- ✅ Inline CSS Styling

## 🎨 Expandindo os Exemplos

**Ideias para Praticar:**
- Adicionar localStorage
- Conectar com APIs
- Adicionar animações
- Criar novos componentes
- Implementar validações

---

<div align="center">

**🎨 Interfaces visuais reativas com OpenFlex! 🎨**

[Ver Galeria](./index.html) | [Voltar ao Menu](../index.html)

</div>
