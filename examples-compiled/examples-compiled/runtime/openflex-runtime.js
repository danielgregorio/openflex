/**
 * OpenFlex Neo Runtime
 * Reactivity System - Solid.js inspired signals
 */

// Track the currently running effect
let currentEffect = null;

/**
 * Signal - Reactive primitive
 * @template T
 */
class Signal {
  constructor(value) {
    this._value = value;
    this._subscribers = new Set();
  }

  get value() {
    // Track dependency if we're inside an effect or computed
    if (currentEffect) {
      this._subscribers.add(currentEffect);
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

  // Alias for getting the value
  get() {
    return this.value;
  }

  // Alias for setting the value
  set(newValue) {
    this.value = newValue;
  }
}

/**
 * Computed - Derived reactive value
 * @template T
 */
class Computed {
  constructor(computation) {
    this._computation = computation;
    this._value = undefined;
    this._stale = true;
    this._subscribers = new Set();

    // Create an effect that re-runs when dependencies change
    this._effect = () => {
      this._stale = true;
      // Notify subscribers that this computed is stale
      this._subscribers.forEach(effect => effect());
    };
  }

  get value() {
    if (this._stale) {
      // Re-compute
      const prevEffect = currentEffect;
      currentEffect = this._effect;
      this._value = this._computation();
      currentEffect = prevEffect;
      this._stale = false;
    }

    // Track dependency
    if (currentEffect) {
      this._subscribers.add(currentEffect);
    }

    return this._value;
  }

  get() {
    return this.value;
  }
}

/**
 * Effect - Side effect that runs when dependencies change
 */
function createEffect(fn) {
  const effect = () => {
    const prevEffect = currentEffect;
    currentEffect = effect;
    fn();
    currentEffect = prevEffect;
  };

  // Run immediately
  effect();

  return effect;
}

/**
 * Batch - Run multiple updates without triggering effects until done
 */
function batch(fn) {
  const prevEffect = currentEffect;
  currentEffect = null;
  fn();
  currentEffect = prevEffect;
}

/**
 * Untrack - Read signals without creating dependencies
 */
function untrack(fn) {
  const prevEffect = currentEffect;
  currentEffect = null;
  const result = fn();
  currentEffect = prevEffect;
  return result;
}

// Export for use in compiled code
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    Signal,
    Computed,
    createEffect,
    batch,
    untrack
  };
}

// Global exports for browser
if (typeof window !== 'undefined') {
  window.OpenFlex = {
    Signal,
    Computed,
    createEffect,
    batch,
    untrack
  };
}
