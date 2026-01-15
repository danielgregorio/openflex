# 📚 Exemplos Compilados - OpenFlex

Bem-vindo à coleção completa de exemplos do OpenFlex ActionScript 4.0! Esta pasta contém exemplos organizados e **prontos para executar**, com código-fonte (.as4/.mxml) e versões compiladas (.js).

## 🎯 O que você encontrará aqui

Diferente da pasta `/examples` que contém principalmente arquivos de origem não compilados, esta pasta (`/examples-compiled`) foi criada para fornecer:

✅ **Exemplos organizados por categoria**
✅ **Arquivos .as4/.mxml + .js compilados**
✅ **HTML runners para testar no navegador**
✅ **READMEs completos com explicações**
✅ **Exemplos progressivos do básico ao avançado**

## 📂 Estrutura das Pastas

### 🚀 [01-basics/](./01-basics/)
**Nível: Iniciante**

Exemplos fundamentais para começar:
- Hello World
- Variáveis e tipos
- Funções
- Loops
- Condicionais

👉 **Comece aqui se você é novo no OpenFlex!**

---

### ✨ [02-modern-js/](./02-modern-js/)
**Nível: Intermediário**

Recursos modernos do JavaScript:
- Pattern Matching
- Destructuring
- Optional Chaining (?.)
- Nullish Coalescing (??)
- Async/Await
- Spread Operators

---

### ⚡ [03-reactive/](./03-reactive/)
**Nível: Intermediário**

Programação reativa:
- Signals (valores reativos)
- Computed values (derivados)
- Effects (efeitos colaterais)
- Watchers (observadores)

---

### 🎨 [04-components/](./04-components/)
**Nível: Intermediário**

Componentes MXML:
- Componentes reutilizáveis
- Data binding
- Event handling
- Props e estado
- Composição de componentes

---

### 🚀 [05-full-apps/](./05-full-apps/)
**Nível: Avançado**

Aplicações completas:
- **E-Commerce**: Loja online com carrinho
- **CMS**: Sistema de gerenciamento de conteúdo
- Integração com APIs
- Estado global
- Roteamento

---

### 🎯 [06-advanced/](./06-advanced/)
**Nível: Avançado**

Padrões avançados:
- Generics complexos
- Higher-order functions
- Design patterns (Builder, Factory, Observer)
- Type guards
- Memoization

---

### 🌐 [07-real-apis/](./07-real-apis/)
**Nível: Intermediário/Avançado**

Aplicações que consomem APIs públicas reais:
- **Blog**: JSONPlaceholder API (posts, usuários, comentários)
- **Pokédex**: PokeAPI (dados de Pokémon completos)
- **Países**: REST Countries API (informações geográficas)

✨ Todos os exemplos fazem requisições HTTP reais e processam dados JSON!

---

### 🎨 [08-visual-ui/](./08-visual-ui/)
**Nível: Intermediário**

Interfaces visuais reativas com DOM manipulation:
- **Contador Visual**: Botões, displays, animações
- **Todo List**: Inputs, checkboxes, filtros
- Estado reativo com Signals
- Event handlers
- Updates automáticos da UI

✨ Exemplos com UIs reais, não apenas console.log!

---

## 🚦 Guia de Aprendizado

### Para Iniciantes

```
1. 01-basics/        → Fundamentos (1-2 horas)
2. 02-modern-js/     → Recursos modernos (2-3 horas)
3. 03-reactive/      → Programação reativa (2-3 horas)
4. 04-components/    → Componentes MXML (3-4 horas)
```

### Para Desenvolvedores Experientes

```
1. 02-modern-js/     → Recursos únicos do AS4 (1 hora)
2. 03-reactive/      → Sistema de reatividade (1 hora)
3. 05-full-apps/     → Aplicações completas (2-3 horas)
4. 06-advanced/      → Padrões avançados (2-3 horas)
```

## 🏃 Como Executar os Exemplos

### 🚀 Quick Start (Mais Rápido!)

Agora você pode iniciar o servidor com um único comando!

**Windows:**
```bash
cd examples-compiled/
start.bat
```

**Linux/Mac:**
```bash
cd examples-compiled/
./start.sh
# ou
python3 start.py
```

O script vai:
- ✅ Levantar servidor HTTP automaticamente
- ✅ Abrir o navegador com a página principal
- ✅ Mostrar todas as categorias disponíveis

### Opção 1: Node.js (Recomendado para aprender)

```bash
# Navegar para qualquer pasta
cd 01-basics/

# Executar um exemplo JavaScript compilado
node 01-hello-world.js

# Ou compilar e executar um arquivo AS4
../../openflex build 01-hello-world.as4 -o output.js
node output.js
```

### Opção 2: Navegador (Recomendado para exemplos visuais)

```bash
# Iniciar servidor HTTP em qualquer pasta
cd 01-basics/
python3 -m http.server 8000

# Abrir no navegador
# http://localhost:8000/run-example.html
```

### Opção 3: Compilar seus próprios exemplos

```bash
# AS4 para JavaScript
./openflex build seu-arquivo.as4 -o saida.js

# MXML para JavaScript
./compile-mxml.py seu-componente.mxml
```

## 📖 Convenções Usadas

### Nomenclatura de Arquivos

- **Arquivos numerados**: Ordem de aprendizado recomendada
  - `01-hello-world.as4` → Primeiro exemplo
  - `02-variables.as4` → Segundo exemplo

- **Arquivos descritivos**: Exemplos temáticos
  - `pattern-matching.as4` → Exemplo de pattern matching
  - `reactivity-demo.as4` → Demo de reatividade

### Estrutura de Código

Todos os exemplos seguem o mesmo padrão:

```actionscript
// Comentário descritivo do que o exemplo demonstra

// Importações (se necessário)
import { signal, computed } from "openflex/reactive";

// Funções auxiliares
function helper(): void {
    // ...
}

// Função principal
function main(): void {
    // Código do exemplo aqui
    trace("Hello, OpenFlex!");
}

// Executar
main();
```

## 🎨 Recursos Visuais

### HTML Runners

Cada pasta com exemplos JavaScript tem um arquivo `run-example.html` que permite:

- ✅ Selecionar exemplos de um dropdown
- ✅ Executar no navegador
- ✅ Ver saída do console em tempo real
- ✅ Interface amigável e colorida
- ✅ **NOVO:** Botão "📄 Ver Código Fonte (.as4)" para ver o código OpenFlex original!

### Botões "View Source"

**Todos os exemplos agora incluem acesso direto ao código fonte!**

Quando você executa um exemplo no navegador, você verá um botão verde **"📄 Ver Código Fonte (.as4)"** que:

- Abre o arquivo ActionScript 4 original em uma nova aba
- Permite comparar o código fonte com o JavaScript compilado
- Facilita o aprendizado mostrando como OpenFlex funciona

**Como usar:**
1. Execute qualquer exemplo no navegador
2. Clique no botão verde "📄 Ver Código Fonte (.as4)"
3. Compare o código .as4 original com o resultado no navegador
4. Aprenda como OpenFlex compila para JavaScript moderno!

### Screenshots e GIFs

Exemplos visuais incluem screenshots em seus READMEs (quando aplicável).

## 🔧 Troubleshooting

### Erro de compilação

```bash
# Tente com --force para exemplos experimentais
./openflex build arquivo.as4 -o saida.js --force
```

### Erro ao executar no Node.js

```bash
# Verifique se você tem Node.js instalado
node --version

# Deve ser v14 ou superior
```

### Exemplos não carregam no navegador

```bash
# Certifique-se de estar usando um servidor HTTP
# NÃO abra o arquivo diretamente (file://)

# Use um desses:
python3 -m http.server 8000
# ou
npx serve
# ou
php -S localhost:8000
```

## 💡 Dicas Gerais

### 1. Leia os READMEs

Cada pasta tem um README detalhado com:
- Descrição dos exemplos
- Conceitos explicados
- Como executar
- Dicas específicas

### 2. Experimente Modificar

A melhor forma de aprender é modificando os exemplos:
- Mude valores
- Adicione funcionalidades
- Quebre o código (e conserte)

### 3. Use o Type System

OpenFlex tem tipagem forte - use-a!

```actionscript
// Bom ✅
function add(a: Number, b: Number): Number {
    return a + b;
}

// Funciona mas não recomendado ❌
function add(a, b) {
    return a + b;
}
```

### 4. Trace é seu amigo

Use `trace()` para debug:

```actionscript
trace("Valor:", minhaVariavel);
trace("Tipo:", typeof minhaVariavel);
```

### 5. Leia o código compilado

Veja o JavaScript gerado para entender como OpenFlex funciona:

```bash
# Compile e compare
cat exemplo.as4
cat exemplo.js
```

## 🌟 Próximos Passos

Depois de explorar os exemplos:

1. **Leia a documentação completa**: `/docs/`
2. **Veja o guia de demos**: `DEMO_GUIDE.md`
3. **Explore aplicações reais**: `/examples/ecommerce/`, `/examples/cms/`
4. **Contribua**: Crie seus próprios exemplos!

## 🤝 Contribuindo

Gostaria de adicionar um exemplo? Ótimo!

1. Crie o arquivo `.as4` ou `.mxml`
2. Compile para `.js`
3. Adicione ao README da pasta
4. Teste para garantir que funciona
5. Faça um pull request!

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/yourusername/openflex/issues)
- **Discussões**: [GitHub Discussions](https://github.com/yourusername/openflex/discussions)
- **Documentação**: `/docs/` no repositório

## 📝 Licença

Todos os exemplos estão sob a mesma licença do OpenFlex (ver LICENSE na raiz do projeto).

---

<div align="center">

**🎉 Divirta-se aprendendo OpenFlex! 🎉**

[Voltar ao início](#-exemplos-compilados---openflex) | [Documentação Principal](../README.md)

</div>
