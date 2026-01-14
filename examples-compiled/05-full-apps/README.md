# 🚀 Aplicações Completas - OpenFlex

Esta pasta contém exemplos de aplicações completas e funcionais construídas com OpenFlex.

## 📂 Aplicações Disponíveis

### 🛒 E-Commerce Store
**Pasta:** `ecommerce/`

Uma loja de e-commerce completa com:
- **Catálogo de Produtos**: Listagem com filtros e busca
- **Carrinho de Compras**: Adicionar/remover itens, calcular total
- **Checkout**: Processo de finalização de compra
- **Gerenciamento de Estado**: Estado global reativo
- **API Integration**: Chamadas assíncronas para backend

**Arquivos:**
- `StoreApp.mxml` - Componente principal da loja
- `ShoppingCart.mxml` - Componente do carrinho
- `store.as4` - Lógica de negócio e estado
- `mock-api-server.js` - API mock para testes

**Para executar:**
```bash
cd ecommerce
# 1. Inicie o servidor de API mock
node mock-api-server.js

# 2. Em outro terminal, compile a aplicação
./compile-mxml.py StoreApp.mxml

# 3. Inicie um servidor web
python3 -m http.server 8000

# 4. Abra: http://localhost:8000/StoreApp.html
```

**Recursos Demonstrados:**
- ✅ Componentes reutilizáveis
- ✅ Estado global com signals
- ✅ Async/await para API calls
- ✅ Computed values para cálculos
- ✅ Event handling
- ✅ Formulários e validação
- ✅ Roteamento básico

---

### 📝 CMS (Content Management System)
**Pasta:** `cms/`

Um sistema de gerenciamento de conteúdo com:
- **Editor de Conteúdo**: Rich text editor
- **Lista de Posts**: CRUD completo (Create, Read, Update, Delete)
- **Categorias e Tags**: Organização de conteúdo
- **Preview em Tempo Real**: Visualização ao editar
- **Autenticação**: Login e permissões de usuário

**Arquivos:**
- `CMSApp.mxml` - Aplicação principal do CMS
- `ContentEditor.mxml` - Editor de conteúdo
- `cms.as4` - Lógica e estado do CMS
- `mock-api-server.js` - Backend simulado

**Para executar:**
```bash
cd cms
# 1. Inicie o servidor de API
node mock-api-server.js

# 2. Compile a aplicação
./compile-mxml.py CMSApp.mxml

# 3. Inicie servidor web
python3 -m http.server 8000

# 4. Abra: http://localhost:8000/CMSApp.html
```

**Recursos Demonstrados:**
- ✅ Formulários complexos
- ✅ Validação de dados
- ✅ Autenticação e autorização
- ✅ CRUD operations
- ✅ Estado persistente
- ✅ Rich text editing
- ✅ File uploads (simulado)

## 🏗️ Arquitetura das Aplicações

### Estrutura de Pastas Típica

```
app-name/
├── components/          # Componentes reutilizáveis
│   ├── Button.mxml
│   ├── Input.mxml
│   └── Card.mxml
├── views/              # Views/páginas principais
│   ├── Home.mxml
│   ├── Products.mxml
│   └── Cart.mxml
├── services/           # Lógica de negócio
│   ├── api.as4
│   └── store.as4
├── App.mxml            # Componente raiz
└── README.md           # Documentação específica
```

### Padrões de Arquitetura Usados

#### 1. Component-Based Architecture
Aplicação dividida em componentes pequenos e reutilizáveis.

#### 2. Reactive State Management
Estado global usando signals e computed values:

```actionscript
// store.as4
const [products, setProducts] = signal([]);
const [cart, setCart] = signal([]);

const cartTotal = computed(() =>
    cart().reduce((sum, item) => sum + item.price * item.quantity, 0)
);
```

#### 3. Service Layer
Lógica de negócio e API calls separados dos componentes:

```actionscript
// api.as4
async function fetchProducts(): Promise<Array<Product>> {
    const response = await fetch("/api/products");
    return response.json();
}
```

#### 4. Event-Driven Communication
Componentes se comunicam via eventos customizados.

## 📚 Conceitos Avançados

### 1. Global State Management

```actionscript
// Criar um store global
class AppStore {
    const [user, setUser] = signal(null);
    const [cart, setCart] = signal([]);

    const isAuthenticated = computed(() => user() !== null);

    function login(credentials: Object): Promise<void> {
        // Lógica de login
    }

    function addToCart(product: Product): void {
        setCart([...cart(), product]);
    }
}

const store = new AppStore();
```

### 2. Async Data Fetching

```actionscript
async function loadData(): Promise<void> {
    try {
        const data = await api.fetchProducts();
        setProducts(data);
    } catch (error) {
        setError(error.message);
    } finally {
        setLoading(false);
    }
}
```

### 3. Form Validation

```actionscript
const [formData, setFormData] = signal({
    email: "",
    password: ""
});

const isValid = computed(() => {
    const data = formData();
    return data.email.includes("@") && data.password.length >= 8;
});
```

### 4. Routing (Básico)

```actionscript
const [currentRoute, setCurrentRoute] = signal("home");

function navigate(route: String): void {
    setCurrentRoute(route);
    window.history.pushState({}, "", `/${route}`);
}
```

## 🧪 Testando as Aplicações

### Iniciar Servidor de Desenvolvimento

```bash
# Terminal 1: API Mock
node mock-api-server.js

# Terminal 2: Web Server
python3 -m http.server 8000
```

### Testar Funcionalidades

1. **E-Commerce:**
   - Adicionar produtos ao carrinho
   - Atualizar quantidades
   - Fazer checkout
   - Buscar produtos

2. **CMS:**
   - Criar novo post
   - Editar post existente
   - Deletar post
   - Filtrar por categoria

## 🔧 Customização

### Modificar API Endpoint

Edite os arquivos `.as4` para apontar para sua API real:

```actionscript
// Trocar de:
const API_URL = "http://localhost:3000/api";

// Para:
const API_URL = "https://sua-api.com/api";
```

### Adicionar Novas Features

1. Crie novos componentes em `components/`
2. Adicione lógica em `services/`
3. Integre no componente principal
4. Teste e itere

## 🔗 Próximos Passos

- `../06-advanced/` - Padrões avançados de arquitetura
- Veja a documentação principal para deployment
- Contribua com suas próprias aplicações de exemplo!

## 💡 Dicas

1. **Start Small**: Comece com features básicas e expanda gradualmente.

2. **Separe Concerns**: Mantenha UI, lógica e dados separados.

3. **Use TypeScript**: Aproveite a tipagem para evitar bugs.

4. **Mock APIs First**: Desenvolva com dados mockados antes de integrar APIs reais.

5. **Test Early**: Teste cada feature conforme implementa.

## 🎓 Recursos Adicionais

- Cada aplicação tem seu próprio README com detalhes específicos
- Veja os comentários no código para explicações detalhadas
- Experimente modificar e aprender fazendo!
