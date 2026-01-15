// Todo List Visual - Lista de Tarefas Interativa
// UI visual com adicionar, remover e marcar como completo

const trace = typeof console !== 'undefined' ? console.log : () => {};

// Reactivity Runtime
class Signal {
    constructor(initialValue) {
        this._value = initialValue;
        this._subscribers = [];
    }

    get value() {
        if (typeof currentEffect !== 'undefined' && currentEffect) {
            this._subscribers.push(currentEffect);
        }
        return this._value;
    }

    set value(newValue) {
        this._value = newValue;
        this._subscribers.forEach(effect => effect());
    }
}

let currentEffect = null;

function createEffect(fn) {
    currentEffect = fn;
    fn();
    currentEffect = null;
}

// App State
const todos = new Signal([]);
const filter = new Signal('all'); // all, active, completed
let nextId = 1;

// Actions
function addTodo(text) {
    if (!text.trim()) return;

    todos.value = [...todos.value, {
        id: nextId++,
        text: text.trim(),
        completed: false,
        createdAt: new Date().toLocaleString()
    }];

    trace(`✅ Tarefa adicionada: "${text}"`);
}

function toggleTodo(id) {
    todos.value = todos.value.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
    );
}

function deleteTodo(id) {
    const todo = todos.value.find(t => t.id === id);
    todos.value = todos.value.filter(t => t.id !== id);
    trace(`🗑️ Tarefa removida: "${todo.text}"`);
}

function clearCompleted() {
    const count = todos.value.filter(t => t.completed).length;
    todos.value = todos.value.filter(t => !t.completed);
    trace(`🗑️ ${count} tarefas completadas removidas`);
}

// Render UI
function createApp() {
    const app = document.getElementById('app');

    app.innerHTML = `
        <div style="max-width: 700px; margin: 50px auto; padding: 30px; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="text-align: center; color: #2c3e50; margin-bottom: 30px;">
                ✅ Lista de Tarefas
            </h1>

            <!-- Input -->
            <div style="margin-bottom: 30px; display: flex; gap: 10px;">
                <input
                    id="todo-input"
                    type="text"
                    placeholder="Adicionar nova tarefa..."
                    style="flex: 1; padding: 15px; font-size: 16px; border: 2px solid #e0e0e0; border-radius: 8px; outline: none;"
                />
                <button
                    id="btn-add"
                    style="background: #3498db; color: white; border: none; padding: 15px 30px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold;"
                >
                    ➕ Adicionar
                </button>
            </div>

            <!-- Filters -->
            <div style="display: flex; gap: 10px; margin-bottom: 20px; justify-content: center;">
                <button class="filter-btn" data-filter="all" style="padding: 8px 16px; border: 2px solid #3498db; background: #3498db; color: white; border-radius: 6px; cursor: pointer; font-weight: bold;">
                    Todas
                </button>
                <button class="filter-btn" data-filter="active" style="padding: 8px 16px; border: 2px solid #3498db; background: white; color: #3498db; border-radius: 6px; cursor: pointer;">
                    Ativas
                </button>
                <button class="filter-btn" data-filter="completed" style="padding: 8px 16px; border: 2px solid #3498db; background: white; color: #3498db; border-radius: 6px; cursor: pointer;">
                    Completas
                </button>
            </div>

            <!-- Stats -->
            <div id="stats" style="text-align: center; margin-bottom: 20px; color: #7f8c8d; font-size: 14px;">
                0 tarefas
            </div>

            <!-- Todo List -->
            <div id="todo-list" style="margin-bottom: 20px;">
                <p style="text-align: center; color: #95a5a6; padding: 40px;">
                    Nenhuma tarefa ainda. Adicione uma acima!
                </p>
            </div>

            <!-- Clear Completed -->
            <div style="text-align: center;">
                <button
                    id="btn-clear"
                    style="background: #e74c3c; color: white; border: none; padding: 10px 20px; font-size: 14px; border-radius: 6px; cursor: pointer;"
                >
                    🗑️ Limpar Completadas
                </button>
            </div>
        </div>
    `;

    // Event Listeners
    const input = document.getElementById('todo-input');
    const btnAdd = document.getElementById('btn-add');

    btnAdd.addEventListener('click', () => {
        addTodo(input.value);
        input.value = '';
    });

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTodo(input.value);
            input.value = '';
        }
    });

    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            filter.value = btn.dataset.filter;

            // Update active button
            document.querySelectorAll('.filter-btn').forEach(b => {
                if (b === btn) {
                    b.style.background = '#3498db';
                    b.style.color = 'white';
                } else {
                    b.style.background = 'white';
                    b.style.color = '#3498db';
                }
            });
        });
    });

    document.getElementById('btn-clear').addEventListener('click', clearCompleted);

    // Reactive Updates
    createEffect(() => {
        const todoList = document.getElementById('todo-list');
        const currentFilter = filter.value;

        let filteredTodos = todos.value;
        if (currentFilter === 'active') {
            filteredTodos = todos.value.filter(t => !t.completed);
        } else if (currentFilter === 'completed') {
            filteredTodos = todos.value.filter(t => t.completed);
        }

        if (filteredTodos.length === 0) {
            todoList.innerHTML = '<p style="text-align: center; color: #95a5a6; padding: 40px;">Nenhuma tarefa aqui!</p>';
            return;
        }

        todoList.innerHTML = filteredTodos.map(todo => `
            <div style="display: flex; align-items: center; padding: 15px; margin-bottom: 10px; background: ${todo.completed ? '#f8f9fa' : 'white'}; border: 2px solid ${todo.completed ? '#27ae60' : '#e0e0e0'}; border-radius: 8px;">
                <input
                    type="checkbox"
                    ${todo.completed ? 'checked' : ''}
                    onchange="window.toggleTodo(${todo.id})"
                    style="width: 20px; height: 20px; cursor: pointer; margin-right: 15px;"
                />
                <div style="flex: 1;">
                    <div style="font-size: 16px; color: #2c3e50; ${todo.completed ? 'text-decoration: line-through; color: #95a5a6;' : ''}">
                        ${todo.text}
                    </div>
                    <div style="font-size: 12px; color: #95a5a6; margin-top: 4px;">
                        ${todo.createdAt}
                    </div>
                </div>
                <button
                    onclick="window.deleteTodo(${todo.id})"
                    style="background: #e74c3c; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;"
                >
                    🗑️ Remover
                </button>
            </div>
        `).join('');
    });

    createEffect(() => {
        const stats = document.getElementById('stats');
        const total = todos.value.length;
        const active = todos.value.filter(t => !t.completed).length;
        const completed = todos.value.filter(t => t.completed).length;

        stats.textContent = `${total} total • ${active} ativas • ${completed} completas`;
    });

    // Make functions globally accessible for inline handlers
    window.toggleTodo = toggleTodo;
    window.deleteTodo = deleteTodo;

    trace('✅ Todo List renderizada!');
}

// Initialize
if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createApp);
    } else {
        createApp();
    }
}
