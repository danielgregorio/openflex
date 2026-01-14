# ✨ JavaScript Moderno - OpenFlex

Esta pasta contém exemplos de recursos modernos do JavaScript implementados no ActionScript 4.0.

## 📂 Exemplos Disponíveis

### Pattern Matching (`pattern-matching.as4`)
Demonstra o pattern matching, um recurso poderoso para trabalhar com diferentes casos:
- Match expressions para diferentes tipos de dados
- Patterns com guardas (condições)
- Destructuring em patterns
- Default cases

**Para executar:**
```bash
./openflex build pattern-matching.as4 -o pattern-matching.js
node pattern-matching.js
```

**Exemplo de código:**
```actionscript
match (value) {
    case Number n if n > 0:
        return "Número positivo";
    case String s:
        return "String: " + s;
    default:
        return "Outro tipo";
}
```

### Destructuring (`destructuring-demo.as4`)
Mostra como extrair valores de arrays e objetos de forma elegante:
- Array destructuring
- Object destructuring
- Nested destructuring
- Rest/spread operators

**Para executar:**
```bash
./openflex build destructuring-demo.as4 -o destructuring-demo.js --force
node destructuring-demo.js
```

### Optional Chaining (`optional-chaining-demo.as4`)
Demonstra o operador de optional chaining (?.) para acessar propriedades de forma segura:
- Acesso seguro a propriedades aninhadas
- Evita erros de "null/undefined"
- Simplifica verificações de existência

**Para executar:**
```bash
./openflex build optional-chaining-demo.as4 -o optional-chaining-demo.js --force
node optional-chaining-demo.js
```

**Exemplo de código:**
```actionscript
const value = obj?.property?.nestedProperty;
// Se obj ou property forem null/undefined, retorna undefined
```

### Async/Await (`async-await-demo.as4`)
Exemplos de programação assíncrona moderna:
- Funções async
- Await para esperar promises
- Tratamento de erros com try/catch
- Promises em paralelo

**Para executar:**
```bash
./openflex build async-await-demo.as4 -o async-await-demo.js --force
node async-await-demo.js
```

## 🌐 Executar no Navegador

Abra o arquivo `run-example.html` no seu navegador para executar os exemplos interativamente!

```bash
python3 -m http.server 8000
# Abra: http://localhost:8000/run-example.html
```

## 📚 Conceitos Aprendidos

- ✅ **Pattern Matching**: Correspondência de padrões com guardas
- ✅ **Destructuring**: Extração de valores de estruturas complexas
- ✅ **Optional Chaining**: Acesso seguro a propriedades (?.operator)
- ✅ **Nullish Coalescing**: Operador ?? para valores padrão
- ✅ **Async/Await**: Programação assíncrona moderna
- ✅ **Spread Operator**: Expansão de arrays e objetos (...)

## 🔗 Próximos Passos

Depois de dominar os recursos modernos:
- `../03-reactive/` - Programação reativa com observables
- `../04-components/` - Componentes reutilizáveis em MXML
- `../05-full-apps/` - Aplicações completas

## 💡 Dicas

1. **Pattern Matching é poderoso**: Use-o para substituir longas cadeias de if/else.

2. **Optional Chaining evita bugs**: Sempre use `?.` ao acessar propriedades que podem não existir.

3. **Async/Await simplifica promises**: É mais legível que `.then()` e `.catch()`.

4. **Destructuring torna o código mais limpo**: Extraia apenas os valores que você precisa.

## ⚠️ Nota sobre --force

Alguns exemplos podem precisar da flag `--force` durante a compilação pois usam recursos experimentais ou em desenvolvimento. O código JavaScript gerado funcionará corretamente.
