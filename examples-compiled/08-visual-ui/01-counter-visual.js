// Counter Visual - Interface com Botões Reais
// Exemplo de UI visual reativa sem MXML (JavaScript puro)

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
        if (this._value !== newValue) {
            this._value = newValue;
            this._subscribers.forEach(effect => effect());
        }
    }
}

let currentEffect = null;

function createEffect(fn) {
    currentEffect = fn;
    fn();
    currentEffect = null;
}

// App State
const count = new Signal(0);
const history = new Signal([]);

// Actions
function increment() {
    count.value = count.value + 1;
    addToHistory('Incrementado');
}

function decrement() {
    count.value = count.value - 1;
    addToHistory('Decrementado');
}

function reset() {
    count.value = 0;
    history.value = [];
    addToHistory('Reset');
}

function addToHistory(action) {
    const timestamp = new Date().toLocaleTimeString();
    history.value = [...history.value, { action, count: count.value, time: timestamp }];
}

// Render UI
function createApp() {
    const app = document.getElementById('app');

    // Container principal
    app.innerHTML = `
        <div style="max-width: 600px; margin: 50px auto; padding: 30px; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="text-align: center; color: #2c3e50; margin-bottom: 30px;">
                🔢 Contador Reativo
            </h1>

            <div style="text-align: center; margin-bottom: 30px;">
                <div id="count-display" style="font-size: 72px; font-weight: bold; color: #3498db; margin-bottom: 20px;">
                    0
                </div>

                <div style="display: flex; gap: 10px; justify-content: center; margin-bottom: 20px;">
                    <button id="btn-decrement" style="background: #e74c3c; color: white; border: none; padding: 15px 30px; font-size: 18px; border-radius: 8px; cursor: pointer; font-weight: bold;">
                        ➖ Decrementar
                    </button>
                    <button id="btn-increment" style="background: #27ae60; color: white; border: none; padding: 15px 30px; font-size: 18px; border-radius: 8px; cursor: pointer; font-weight: bold;">
                        ➕ Incrementar
                    </button>
                </div>

                <button id="btn-reset" style="background: #95a5a6; color: white; border: none; padding: 10px 20px; font-size: 14px; border-radius: 8px; cursor: pointer;">
                    🔄 Reset
                </button>
            </div>

            <div style="border-top: 2px solid #ecf0f1; padding-top: 20px;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">📜 Histórico</h3>
                <div id="history-list" style="max-height: 200px; overflow-y: auto; background: #f8f9fa; padding: 15px; border-radius: 8px;">
                    <p style="color: #95a5a6; text-align: center;">Nenhuma ação ainda...</p>
                </div>
            </div>
        </div>
    `;

    // Event Listeners
    document.getElementById('btn-increment').addEventListener('click', increment);
    document.getElementById('btn-decrement').addEventListener('click', decrement);
    document.getElementById('btn-reset').addEventListener('click', reset);

    // Reactive Updates
    createEffect(() => {
        const display = document.getElementById('count-display');
        if (display) {
            display.textContent = count.value;
            // Animação de mudança
            display.style.transform = 'scale(1.2)';
            setTimeout(() => {
                display.style.transform = 'scale(1)';
            }, 150);
        }
    });

    createEffect(() => {
        const historyList = document.getElementById('history-list');
        if (historyList && history.value.length > 0) {
            historyList.innerHTML = history.value
                .slice()
                .reverse()
                .map(item => `
                    <div style="padding: 8px; margin-bottom: 8px; background: white; border-radius: 4px; border-left: 3px solid #3498db;">
                        <strong>${item.action}</strong> → Contador: ${item.count}
                        <span style="color: #95a5a6; font-size: 12px;">(${item.time})</span>
                    </div>
                `)
                .join('');
        }
    });

    trace('✅ App renderizada! Interface visual ativa.');
}

// Initialize when DOM is ready
if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createApp);
    } else {
        createApp();
    }
}
