// OpenFlex Reactivity Runtime
// Simple implementation of Signals and Effects

class Signal {
    constructor(initialValue) {
        this._value = initialValue;
        this._subscribers = [];
    }

    get value() {
        // Track dependency if we're in an effect
        if (currentEffect) {
            this._subscribers.push(currentEffect);
        }
        return this._value;
    }

    set value(newValue) {
        if (this._value !== newValue) {
            this._value = newValue;
            // Notify all subscribers
            this._subscribers.forEach(effect => effect());
        }
    }
}

class Computed {
    constructor(fn) {
        this._fn = fn;
        this._value = undefined;
        this._dirty = true;
        this._subscribers = [];
    }

    get value() {
        if (this._dirty) {
            this._value = this._fn();
            this._dirty = false;
        }
        if (currentEffect) {
            this._subscribers.push(currentEffect);
        }
        return this._value;
    }
}

let currentEffect = null;

function createEffect(fn) {
    currentEffect = fn;
    fn();
    currentEffect = null;
}

module.exports = {
    Signal,
    Computed,
    createEffect
};
