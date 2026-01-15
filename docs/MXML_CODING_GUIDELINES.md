# OpenFlex Neo MXML - Guia de Codificação

## ⚠️ REGRAS CRÍTICAS PARA SCRIPTS MXML

### ✅ USE: `var` e `const` (Sintaxe AS4)

O compilador MXML usa uma grammar **ActionScript 4 (AS4)**, que NÃO reconhece `let` do JavaScript moderno.

**Correto:**
```xml
<fx:Script><![CDATA[
    var result: Number = 0;
    const MAX_VALUE: Number = 100;
]]></fx:Script>
```

**ERRADO (causará bugs):**
```xml
<fx:Script><![CDATA[
    let result = 0;  // ❌ Compilará como " = 0;" sem o nome da variável!
]]></fx:Script>
```

### 🔄 Conversão Automática

O compilador **converte automaticamente**:
- AS4 `var` → JavaScript `let`
- AS4 `const` → JavaScript `const`

Você escreve AS4, o output é JavaScript moderno!

---

## 📚 Sintaxe AS4 vs JavaScript

| Feature | AS4 (MXML) | JavaScript Output |
|---------|------------|-------------------|
| Variável mutável | `var x: Number = 0` | `let x = 0` |
| Constante | `const X: Number = 10` | `const X = 10` |
| Reatividade | `@reactive var count: Number` | `const count = new Signal(0)` |
| Computed | `@computed var doubled: Number { ... }` | `const doubled = new Computed(() => ...)` |

---

## 🐛 Bug Histórico (Resolvido)

### O Problema

Antes da correção, código MXML como:
```as4
let result = 0;
```

Era parseado pela grammar tree-sitter como:
```
ERROR: 'let'
expression_statement: 'result = 0;'
```

Gerando JavaScript quebrado:
```javascript
let = 0;  // ❌ Sem nome de variável!
```

### A Solução

Usar apenas keywords AS4 válidas:
```as4
var result: Number = 0;  // ✅
```

---

## 📖 Tipos AS4

### Tipos Primitivos
- `Number` - números (int e float)
- `String` - strings
- `Boolean` - true/false
- `Array` - arrays
- `Object` - objetos
- `void` - funções sem retorno

### Tipos Nullable
```as4
var name: String? = null;  // Pode ser null
```

### Tipos Genéricos
```as4
var items: Array<String> = [];
var map: Map<String, Number> = {};
```

---

## 🎯 Decoradores

### @reactive
Cria um Signal reativo:
```as4
@reactive var count: Number = 0;
// Compila para: const count = new Signal(0);
```

### @computed
Cria um Computed reativo:
```as4
@computed var doubled: Number {
    return count * 2;
}
// Compila para: const doubled = new Computed(() => count.value * 2);
```

---

## 📝 Exemplos Completos

### Contador Reativo
```xml
<Application xmlns:fx="http://openflex.dev/core" xmlns="http://openflex.dev/neo">
    <fx:Script><![CDATA[
        @reactive var count: Number = 0;

        @computed var doubled: Number {
            return count * 2;
        }

        function increment(): void {
            count = count + 1;
        }
    ]]></fx:Script>

    <VBox>
        <Label text="{count}" />
        <Label text="{'Doubled: ' + doubled}" />
        <Button label="+" click="{increment}" />
    </VBox>
</Application>
```

### Lista de Tarefas
```xml
<Application xmlns:fx="http://openflex.dev/core" xmlns="http://openflex.dev/neo">
    <fx:Script><![CDATA[
        @reactive var todos: Array = [];
        @reactive var newText: String = "";

        var nextId: Number = 1;  // ✅ var, não let!

        function addTodo(): void {
            if (newText.trim() === "") return;

            todos = [...todos, {
                id: nextId++,
                text: newText,
                completed: false
            }];

            newText = "";
        }
    ]]></fx:Script>

    <VBox>
        <TextInput text="{newText}" />
        <Button label="Add" click="{addTodo}" />

        <Repeater dataProvider="{todos}">
            <Label text="{item.text}" />
        </Repeater>
    </VBox>
</Application>
```

---

## 🚨 Erros Comuns e Soluções

### 1. Usar `let` em vez de `var`
```as4
let x = 0;  // ❌ ERRADO
var x: Number = 0;  // ✅ CORRETO
```

### 2. Esquecer CDATA em scripts com operadores
```xml
<!-- ❌ ERRADO - < e > quebram XML -->
<fx:Script>
    if (x < 10) { }
</fx:Script>

<!-- ✅ CORRETO - CDATA protege operadores -->
<fx:Script><![CDATA[
    if (x < 10) { }
]]></fx:Script>
```

### 3. Acessar variáveis reativas diretamente
```as4
@reactive var count: Number = 0;

function double(): Number {
    return count * 2;  // ✅ Compilador adiciona .value automaticamente
}
```

O compilador converte `count` para `count.value` automaticamente quando detecta que é uma variável reativa!

---

## 📚 Referências

- **Documentação completa:** `/docs/README.md`
- **Exemplos:** `/examples-compiled/08-visual-ui/`
- **Grammar AS4:** `/compiler/parser/tree-sitter-as4/`
- **Compilador:** `/compiler/neo_mxml_compiler.py`

---

**Última atualização:** 2026-01-15
**Versão:** 1.0
