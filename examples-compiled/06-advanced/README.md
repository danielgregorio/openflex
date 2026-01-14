# 🎯 Exemplos Avançados - OpenFlex

Esta pasta contém exemplos avançados demonstrando recursos e padrões sofisticados do OpenFlex.

## 📂 Exemplos Disponíveis

### Advanced Demo (`advanced-demo.as4`)
Demonstração completa de recursos avançados:
- **Generics Complexos**: Tipos genéricos aninhados e restrições
- **Higher-Order Functions**: Funções que retornam funções
- **Closures**: Encapsulamento de estado
- **Type Guards**: Verificação de tipos em runtime
- **Advanced Patterns**: Builder, Factory, Observer

**Para executar:**
```bash
./openflex build advanced-demo.as4 -o advanced-demo.js
node advanced-demo.js
```

### Pattern Matching Full (`pattern-matching-full.as4`)
Demonstração completa do sistema de pattern matching:
- **Nested Patterns**: Padrões aninhados complexos
- **Guards with Multiple Conditions**: Guardas complexas
- **Destructuring in Patterns**: Extração de valores em patterns
- **Exhaustive Matching**: Garantir que todos os casos estão cobertos
- **Type-based Matching**: Match baseado em tipos

**Para executar:**
```bash
./openflex build pattern-matching-full.as4 -o pattern-matching-full.js --force
node pattern-matching-full.js
```

## 📚 Conceitos Avançados

### 1. Generics Avançados

#### Generic Constraints
```actionscript
function processItems<T extends Comparable>(items: Array<T>): Array<T> {
    return items.sort((a, b) => a.compareTo(b));
}
```

#### Multiple Type Parameters
```actionscript
function zip<A, B>(arr1: Array<A>, arr2: Array<B>): Array<[A, B]> {
    return arr1.map((item, i) => [item, arr2[i]]);
}
```

#### Generic Classes
```actionscript
class Container<T> {
    private value: T;

    constructor(val: T) {
        this.value = val;
    }

    get(): T {
        return this.value;
    }

    set(val: T): void {
        this.value = val;
    }
}
```

### 2. Higher-Order Functions

#### Function Composition
```actionscript
function compose<A, B, C>(
    f: (b: B) => C,
    g: (a: A) => B
): (a: A) => C {
    return (a: A): C => f(g(a));
}

const addOne = (x: Number): Number => x + 1;
const double = (x: Number): Number => x * 2;

const addOneThenDouble = compose(double, addOne);
trace(addOneThenDouble(5)); // 12
```

#### Currying
```actionscript
function curry<A, B, C>(
    fn: (a: A, b: B) => C
): (a: A) => (b: B) => C {
    return (a: A) => (b: B) => fn(a, b);
}

const add = (a: Number, b: Number): Number => a + b;
const curriedAdd = curry(add);
const add5 = curriedAdd(5);
trace(add5(10)); // 15
```

### 3. Pattern Matching Avançado

#### Nested Destructuring
```actionscript
match (value) {
    case { user: { name: String n, age: Number a } }:
        trace(`User ${n} is ${a} years old`);

    case { items: [first, ...rest] }:
        trace(`First item: ${first}, Rest: ${rest}`);

    case [x, y, z]:
        trace(`Three elements: ${x}, ${y}, ${z}`);
}
```

#### Guards com Múltiplas Condições
```actionscript
match (person) {
    case { age: Number a, country: String c }
        if a >= 18 && c === "US":
        return "Can vote in US";

    case { age: Number a, country: String c }
        if a >= 16 && c === "Brazil":
        return "Can vote in Brazil";

    default:
        return "Cannot vote";
}
```

### 4. Type Guards

```actionscript
function isString(value: any): Boolean {
    return typeof value === "string";
}

function isNumber(value: any): Boolean {
    return typeof value === "number";
}

function processValue(value: any): void {
    if (isString(value)) {
        trace("String length:", value.length);
    } else if (isNumber(value)) {
        trace("Number doubled:", value * 2);
    }
}
```

### 5. Design Patterns

#### Builder Pattern
```actionscript
class QueryBuilder {
    private query: String = "";

    select(fields: Array<String>): QueryBuilder {
        this.query += "SELECT " + fields.join(", ");
        return this;
    }

    from(table: String): QueryBuilder {
        this.query += " FROM " + table;
        return this;
    }

    where(condition: String): QueryBuilder {
        this.query += " WHERE " + condition;
        return this;
    }

    build(): String {
        return this.query;
    }
}

const query = new QueryBuilder()
    .select(["id", "name"])
    .from("users")
    .where("age > 18")
    .build();
```

#### Factory Pattern
```actionscript
interface Shape {
    function draw(): void;
}

class Circle implements Shape {
    function draw(): void {
        trace("Drawing circle");
    }
}

class Square implements Shape {
    function draw(): void {
        trace("Drawing square");
    }
}

class ShapeFactory {
    static function create(type: String): Shape {
        match (type) {
            case "circle":
                return new Circle();
            case "square":
                return new Square();
            default:
                throw new Error("Unknown shape type");
        }
    }
}
```

#### Observer Pattern
```actionscript
class Observable {
    private observers: Array<Function> = [];

    subscribe(fn: Function): Function {
        this.observers.push(fn);
        return () => {
            const index = this.observers.indexOf(fn);
            this.observers.splice(index, 1);
        };
    }

    notify(data: any): void {
        this.observers.forEach(fn => fn(data));
    }
}

const observable = new Observable();
const unsubscribe = observable.subscribe((data) => {
    trace("Received:", data);
});

observable.notify("Hello!"); // Received: Hello!
unsubscribe();
observable.notify("Goodbye!"); // (não imprime nada)
```

### 6. Memoization

```actionscript
function memoize<A, B>(fn: (a: A) => B): (a: A) => B {
    const cache: Object = {};

    return (arg: A): B => {
        const key: String = String(arg);
        if (cache[key] !== undefined) {
            trace("Cache hit for:", key);
            return cache[key];
        }

        trace("Computing for:", key);
        const result: B = fn(arg);
        cache[key] = result;
        return result;
    };
}

// Exemplo de uso
function fibonacci(n: Number): Number {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

const memoizedFib = memoize(fibonacci);
trace(memoizedFib(10)); // Computing...
trace(memoizedFib(10)); // Cache hit!
```

### 7. Async Patterns

#### Promise Composition
```actionscript
async function fetchUserData(userId: Number): Promise<Object> {
    const user = await fetchUser(userId);
    const posts = await fetchPosts(user.id);
    const comments = await fetchComments(posts.map(p => p.id));

    return {
        user,
        posts,
        comments
    };
}
```

#### Promise.all for Parallel Execution
```actionscript
async function fetchAllData(): Promise<Object> {
    const [users, products, orders] = await Promise.all([
        fetchUsers(),
        fetchProducts(),
        fetchOrders()
    ]);

    return { users, products, orders };
}
```

#### Retry Pattern
```actionscript
async function retryAsync<T>(
    fn: () => Promise<T>,
    maxRetries: Number = 3
): Promise<T> {
    let lastError: Error;

    for (let i = 0; i < maxRetries; i++) {
        try {
            return await fn();
        } catch (error) {
            lastError = error;
            trace(`Retry ${i + 1} of ${maxRetries}`);
            await sleep(1000 * Math.pow(2, i)); // Exponential backoff
        }
    }

    throw lastError;
}
```

## 🎯 Exercícios Práticos

1. **Implemente uma estrutura de dados persistente** (List, Map, Set) que nunca muta.

2. **Crie um sistema de middleware** similar ao Express.js para processamento de requests.

3. **Implemente um parser de expressões** usando pattern matching.

4. **Crie um sistema de validação type-safe** usando generics.

5. **Implemente um state machine** usando pattern matching e tipos.

## 🔗 Próximos Passos

- Contribua com seus próprios exemplos avançados
- Explore a documentação completa da linguagem
- Participe da comunidade OpenFlex

## 💡 Dicas

1. **Use Type Safety**: Aproveite ao máximo o sistema de tipos para evitar bugs.

2. **Prefira Imutabilidade**: Código imutável é mais fácil de raciocinar e testar.

3. **Componha Funções**: Pequenas funções compostas são mais reutilizáveis.

4. **Pattern Matching > If/Else**: Use pattern matching para código mais expressivo.

5. **Generics para Reutilização**: Tipos genéricos permitem código altamente reutilizável.

## ⚠️ Performance Considerations

- **Memoization** tem overhead de memória
- **Closures** podem causar memory leaks se não limpar referências
- **Recursão profunda** pode estourar a stack - use loops ou trampolining
- **Pattern matching** pode ter custo em patterns muito complexos

## 🎓 Recursos Adicionais

- Functional Programming in JavaScript
- Design Patterns (Gang of Four)
- TypeScript Advanced Types
- Reactive Programming Patterns
