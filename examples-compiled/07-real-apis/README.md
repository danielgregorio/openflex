# 🌐 Aplicações Consumindo APIs Reais

Esta pasta contém aplicações práticas que consomem **APIs públicas reais** da internet!

## 📂 Aplicações Disponíveis

### 📝 01 - Blog com JSONPlaceholder

**API:** https://jsonplaceholder.typicode.com

Aplicação de blog completa que consome:
- **Posts** - Artigos do blog
- **Users** - Informações dos autores
- **Comments** - Comentários nos posts

**Features:**
- Lista posts com título e conteúdo
- Mostra informações do autor (nome, email, website)
- Exibe comentários de cada post
- Formatação bonita no console

**Para executar:**
```bash
node 01-blog-jsonplaceholder.js
```

---

### 🎮 02 - Pokédex com PokeAPI

**API:** https://pokeapi.co

Pokédex interativa com dados reais de Pokémon!

**Features:**
- Informações completas de Pokémon
- Stats (HP, Attack, Defense, etc.) com barras visuais
- Tipos, habilidades e movimentos
- Altura, peso e outras características
- Pokémon inclusos: Pikachu, Bulbasaur, Charmander, Squirtle, Mewtwo

**Para executar:**
```bash
node 02-pokedex-pokeapi.js
```

**Exemplo de saída:**
```
═══════════════════════════════════════════════════════════
🎮 #25 - PIKACHU
═══════════════════════════════════════════════════════════

📊 Stats:
  hp                   ███████████░░░░ 35
  attack               ███████████████ 55
  defense              ████████░░░░░░░ 40
  ...
```

---

### 🌍 03 - Explorer de Países

**API:** https://restcountries.com

Explore informações detalhadas sobre todos os países do mundo!

**Features:**
- Informações completas de países
- População, área, capital
- Idiomas e moedas
- Fronteiras e fusos horários
- Estatísticas por região
- Top 5 países mais populosos
- Top 5 maiores países por área

**Para executar:**
```bash
node 03-countries-restcountries.js
```

**Foca em:** América do Sul (Brasil, Argentina, Chile, Peru, Colômbia)

---

## 🌐 Executar no Navegador

Abra o HTML runner para uma experiência interativa:

```bash
# Na pasta examples-compiled
python -m http.server 8000

# Acesse: http://localhost:8000/07-real-apis/run-example.html
```

### No HTML Runner você pode:
- ✅ Escolher qual aplicação executar
- ✅ Ver a saída em tempo real
- ✅ Testar diferentes APIs com um clique
- ✅ Scroll automático conforme os dados chegam

---

## 🔧 Como Funcionam

### Fetch API
Todas as aplicações usam a **Fetch API** moderna:

```javascript
const response = await fetch('https://api.example.com/data');
const data = await response.json();
```

### Async/Await
Operações assíncronas com sintaxe limpa:

```javascript
async function getData() {
    const posts = await getPosts();
    const user = await getUser(posts[0].userId);
    trace(user.name);
}
```

### Error Handling
Todas as apps têm tratamento de erros:

```javascript
try {
    const data = await fetchData();
} catch (error) {
    trace('Erro:', error.message);
}
```

---

## 📊 APIs Utilizadas

| API | URL | Descrição |
|-----|-----|-----------|
| **JSONPlaceholder** | jsonplaceholder.typicode.com | API fake para testes com posts, users, comments |
| **PokeAPI** | pokeapi.co | Dados completos de todos os Pokémon |
| **REST Countries** | restcountries.com | Informações de todos os países do mundo |

**Todas são:**
- ✅ Gratuitas
- ✅ Sem autenticação necessária
- ✅ CORS habilitado
- ✅ Bem documentadas

---

## 💡 Dicas de Uso

### 1. **Modificar os exemplos**
Experimente buscar outros dados:

```javascript
// Ao invés de posts 1-10, buscar posts específicos
const post = await fetch(`${API_URL}/posts/42`);

// Buscar outros Pokémon
const pokemon = await getPokemon('mewtwo');

// Buscar países por região
const countries = await getCountriesByRegion('europe');
```

### 2. **Adicionar Mais Features**
Ideias para expandir:
- Adicionar busca por nome
- Filtros personalizados
- Cache de resultados
- Interface visual (DOM)

### 3. **Combinar APIs**
Crie apps que usam múltiplas APIs:
```javascript
// Buscar dados de várias fontes
const [posts, pokemon, countries] = await Promise.all([
    fetch(API_POSTS),
    fetch(API_POKEMON),
    fetch(API_COUNTRIES)
]);
```

---

## 🔗 Documentação das APIs

- **JSONPlaceholder**: https://jsonplaceholder.typicode.com/guide
- **PokeAPI**: https://pokeapi.co/docs/v2
- **REST Countries**: https://restcountries.com

---

## 🎯 Próximos Passos

Depois de explorar essas aplicações:
1. Modifique-as para buscar outros dados
2. Crie suas próprias apps com outras APIs públicas
3. Adicione interface visual (DOM manipulation)
4. Implemente cache e otimizações

### Outras APIs Públicas Interessantes:
- **GitHub API** - Repos, usuários, issues
- **Chuck Norris API** - Piadas do Chuck Norris
- **Dog CEO** - Fotos aleatórias de cachorros
- **NASA API** - Dados espaciais e astronomy picture of the day
- **OpenWeatherMap** - Dados meteorológicos

---

## ✅ Testado e Funcional

Todas as aplicações foram testadas e funcionam tanto no:
- ✅ **Node.js** (terminal)
- ✅ **Navegador** (HTML runner)

---

<div align="center">

**🌐 Explore o mundo através de APIs públicas com OpenFlex! 🌐**

[Voltar ao Menu Principal](../index.html) | [Ver Outras Categorias](../README.md)

</div>
