# 🚀 Exemplos Básicos - OpenFlex

Esta pasta contém exemplos básicos para você começar a usar o OpenFlex ActionScript 4.0.

## 📂 Exemplos Disponíveis

### 01 - Hello World (`01-hello-world.as4`)
O exemplo mais simples possível. Demonstra:
- Declaração de função básica
- Uso da função `trace()` para saída no console
- Retorno de valores de funções

**Para executar:**
```bash
./openflex build 01-hello-world.as4 -o 01-hello-world.js
node 01-hello-world.js
```

### 02 - Variáveis (`02-variables.as4`)
Demonstra o uso de variáveis e tipos de dados. Inclui:
- Tipos básicos (String, Number, Boolean)
- Arrays com tipagem genérica
- Objetos literais
- Constantes (const)

**Para executar:**
```bash
./openflex build 02-variables.as4 -o 02-variables.js
node 02-variables.js
```

### 06 - Exemplo Completo (`06-complete-basics.as4`)
Um exemplo mais completo que mostra:
- Múltiplas funções trabalhando juntas
- Controle de fluxo (if/else)
- Loops (for, while)
- Arrays tipados
- Operações matemáticas
- Manipulação de strings

**Para executar:**
```bash
./openflex build 06-complete-basics.as4 -o 06-complete-basics.js
node 06-complete-basics.js
```

## 🌐 Executar no Navegador

Abra o arquivo `run-example.html` no seu navegador para executar os exemplos interativamente!

```bash
# Se você tiver um servidor web local
python3 -m http.server 8000

# Então abra: http://localhost:8000/run-example.html
```

## 📚 Conceitos Aprendidos

- ✅ Funções e tipagem
- ✅ Variáveis (const, var)
- ✅ Tipos básicos (String, Number, Boolean)
- ✅ Arrays tipados com genéricos (`Array<T>`)
- ✅ Objetos literais
- ✅ Controle de fluxo (if/else)
- ✅ Loops (for, while)
- ✅ Operações matemáticas

## 🔗 Próximos Passos

Depois de dominar os exemplos básicos, avance para:
- `../02-modern-js/` - Recursos modernos do JavaScript
- `../03-reactive/` - Programação reativa
- `../04-components/` - Componentes MXML

## 💡 Dicas

1. **Tipagem é opcional mas recomendada**: Você pode omitir os tipos, mas é melhor usá-los para ter melhor documentação e detecção de erros.

2. **Use genéricos em arrays**: Sempre prefira `Array<String>` ao invés de apenas `Array`.

3. **trace() vs console.log()**: Use `trace()` no AS4, ele será convertido para `console.log()` no JavaScript.
