# ⚡ Programação Reativa - OpenFlex

Esta pasta contém exemplos de programação reativa usando o sistema de reatividade do OpenFlex.

## 📂 Exemplos Disponíveis

### Reatividade Básica (`reactivity-demo.as4`)
Introdução aos conceitos básicos de reatividade:
- Signals (valores reativos)
- Computed (valores derivados)
- Effects (efeitos colaterais automáticos)
- Watchers (observadores de mudanças)

**Para executar:**
```bash
./openflex build reactivity-demo.as4 -o reactivity-demo.js
node reactivity-demo.js
```

**Exemplo de código:**
```actionscript
// Criar um signal
const [count, setCount] = signal(0);

// Criar um computed
const doubled = computed(() => count() * 2);

// Criar um effect
effect(() => {
    trace("Count mudou:", count());
});

// Atualizar o valor (triggera o effect automaticamente)
setCount(5);
```

### Reatividade Completa (`complete-reactivity.as4`)
Exemplo mais avançado mostrando:
- Múltiplos signals interconectados
- Computed values complexos
- Effects com dependências múltiplas
- Casos de uso práticos (carrinho de compras, formulários)

**Para executar:**
```bash
./openflex build complete-reactivity.as4 -o complete-reactivity.js
node complete-reactivity.js
```

## 🌐 Executar no Navegador

Abra o arquivo `run-example.html` no seu navegador para executar os exemplos interativamente!

```bash
python3 -m http.server 8000
# Abra: http://localhost:8000/run-example.html
```

## 📚 Conceitos Aprendidos

### Signals
Signals são valores reativos que podem ser observados:
```actionscript
const [value, setValue] = signal(initialValue);
const current = value();  // Ler o valor
setValue(newValue);        // Atualizar o valor
```

### Computed Values
Valores derivados que se atualizam automaticamente:
```actionscript
const doubled = computed(() => value() * 2);
// doubled será recalculado sempre que value mudar
```

### Effects
Efeitos colaterais que executam automaticamente quando dependências mudam:
```actionscript
effect(() => {
    console.log("Value:", value());
    // Executa toda vez que value() mudar
});
```

### Watchers
Observadores que reagem a mudanças específicas:
```actionscript
watch(value, (newVal, oldVal) => {
    console.log(`Changed from ${oldVal} to ${newVal}`);
});
```

## 🎯 Casos de Uso

### 1. Contador Reativo
```actionscript
const [count, setCount] = signal(0);
const isEven = computed(() => count() % 2 === 0);

effect(() => {
    trace(count(), "is", isEven() ? "even" : "odd");
});
```

### 2. Carrinho de Compras
```actionscript
const [items, setItems] = signal([]);
const total = computed(() =>
    items().reduce((sum, item) => sum + item.price, 0)
);

effect(() => {
    trace("Total:", total());
});
```

### 3. Formulário Reativo
```actionscript
const [name, setName] = signal("");
const [email, setEmail] = signal("");
const isValid = computed(() =>
    name().length > 0 && email().includes("@")
);
```

## 🔗 Próximos Passos

Depois de dominar a programação reativa:
- `../04-components/` - Use reatividade em componentes MXML
- `../05-full-apps/` - Veja aplicações completas usando reatividade
- `../06-advanced/` - Padrões avançados de reatividade

## 💡 Dicas

1. **Minimize Effects**: Effects têm custo de performance. Use computed quando possível.

2. **Evite Loops Infinitos**: Não atualize um signal dentro de um effect que o observa.

3. **Signals são Granular**: Crie signals pequenos e específicos ao invés de um grande objeto reativo.

4. **Computed é Memoizado**: Valores computed são cacheados e só recalculam quando necessário.

5. **Use Batch para Múltiplas Atualizações**: Se você precisa atualizar vários signals, use batch para otimizar.

## 🎓 Recursos Adicionais

- Inspirado em: Solid.js, Vue 3 Reactivity, Svelte Stores
- Sistema de reatividade fine-grained (granular)
- Sem Virtual DOM - atualizações diretas e eficientes
