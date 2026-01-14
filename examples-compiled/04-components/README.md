# 🎨 Componentes MXML - OpenFlex

Esta pasta contém exemplos de componentes reutilizáveis usando MXML (Markup Language XML).

## 📂 Exemplos Disponíveis

### Simple Component (`simple.mxml`)
Um componente MXML simples demonstrando:
- Sintaxe básica do MXML
- Binding de dados
- Event handlers
- Props e estado

**Para compilar:**
```bash
./compile-mxml.py simple.mxml
```

### Counter Component (`counter/App.mxml`)
Um contador interativo mostrando:
- Estado reativo do componente
- Event handling (clicks)
- Atualização automática da UI
- Composição de componentes

**Para usar:**
```bash
cd counter
# Compile e execute conforme instruções no README da pasta
```

## 🏗️ Estrutura MXML

### Anatomia de um Componente MXML

```xml
<Application>
    <Script>
        // Lógica do componente em ActionScript 4
        const [count, setCount] = signal(0);

        function increment(): void {
            setCount(count() + 1);
        }
    </Script>

    <Container>
        <Text>Count: {count()}</Text>
        <Button onClick={increment}>
            Incrementar
        </Button>
    </Container>
</Application>
```

## 📚 Conceitos de Componentes

### 1. Declaração
Componentes MXML começam com uma tag raiz:
- `<Application>` - Componente principal
- `<Component>` - Componente reutilizável
- `<View>` - View simples

### 2. Script Section
Use `<Script>` para adicionar lógica:
```xml
<Script>
    function handleClick(): void {
        trace("Clicked!");
    }
</Script>
```

### 3. Data Binding
Vincule dados com `{}`:
```xml
<Text>{message}</Text>
<Input value={name} />
```

### 4. Event Handlers
Conecte eventos a funções:
```xml
<Button onClick={handleClick}>Click Me</Button>
<Input onChange={handleChange} />
```

### 5. Props
Passe dados para componentes filhos:
```xml
<MyComponent
    title="Hello"
    count={10}
    onUpdate={handleUpdate}
/>
```

## 🎯 Componentes Disponíveis

### Componentes Built-in

- **Container**: Layout container
- **Text**: Renderização de texto
- **Button**: Botão interativo
- **Input**: Campo de entrada
- **List**: Lista de itens
- **Grid**: Layout em grade

### Componentes Customizados

Você pode criar seus próprios componentes:

```xml
<!-- UserCard.mxml -->
<Component name="UserCard">
    <Props>
        name: String
        email: String
    </Props>

    <Container>
        <Text>{name}</Text>
        <Text>{email}</Text>
    </Container>
</Component>
```

## 🔄 Reatividade em Componentes

MXML integra perfeitamente com o sistema de reatividade:

```xml
<Application>
    <Script>
        const [items, setItems] = signal([]);
        const total = computed(() => items().length);

        function addItem(item: Object): void {
            setItems([...items(), item]);
        }
    </Script>

    <Container>
        <Text>Total: {total()}</Text>
        <List items={items()} />
    </Container>
</Application>
```

## 🌐 Executar no Navegador

Os componentes MXML compilam para JavaScript e podem rodar no navegador:

```bash
# Compile o componente
./compile-mxml.py simple.mxml

# Inicie um servidor
python3 -m http.server 8000

# Abra no navegador
# http://localhost:8000/simple.html
```

## 🔗 Próximos Passos

Depois de dominar componentes básicos:
- `../05-full-apps/` - Veja aplicações completas usando múltiplos componentes
- `../06-advanced/` - Padrões avançados de composição

## 💡 Dicas

1. **Mantenha Componentes Pequenos**: Um componente deve ter uma responsabilidade única.

2. **Use Props para Configuração**: Passe configuração via props, não hardcode.

3. **Eventos para Comunicação**: Use eventos para comunicar mudanças para cima na árvore.

4. **Composição sobre Herança**: Combine componentes pequenos para criar UIs complexas.

5. **Separe Lógica de Apresentação**: Use `<Script>` para lógica, MXML para UI.

## 🎓 Recursos Adicionais

- Inspirado em: React JSX, Vue SFC, Svelte Components
- Sintaxe XML familiar para desenvolvedores Flash/Flex
- Type-safe props e events
- Hot reload durante desenvolvimento (em breve)
