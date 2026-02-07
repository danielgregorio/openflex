/**
 * OpenFlex States Runtime
 * Provides States & Transitions support
 * Flex-style API for view states
 */
(function() {
    'use strict';

    const OpenFlexStates = {
        /**
         * Apply a state to a shadow root
         * @param {ShadowRoot} shadowRoot - The shadow root containing elements
         * @param {string} stateName - The name of the state to apply
         * @param {Object} config - States configuration
         */
        applyState(shadowRoot, stateName, config = {}) {
            const { states = {}, defaultState = 'default' } = config;

            // Get base state if this state is based on another
            const stateConfig = states[stateName] || {};
            const basedOn = stateConfig.basedOn;

            // Process includeIn/excludeFrom elements
            const elements = shadowRoot.querySelectorAll('[data-include-in], [data-exclude-from]');

            elements.forEach(el => {
                const includeIn = el.dataset.includeIn ? el.dataset.includeIn.split(',').map(s => s.trim()) : null;
                const excludeFrom = el.dataset.excludeFrom ? el.dataset.excludeFrom.split(',').map(s => s.trim()) : null;

                let visible = true;

                if (includeIn) {
                    // Element is only visible in specific states
                    visible = includeIn.includes(stateName) ||
                              (basedOn && includeIn.includes(basedOn));
                }

                if (excludeFrom) {
                    // Element is hidden in specific states
                    if (excludeFrom.includes(stateName) ||
                        (basedOn && excludeFrom.includes(basedOn))) {
                        visible = false;
                    }
                }

                el.style.display = visible ? '' : 'none';
            });

            // Process state-specific attribute overrides
            const elementsWithStateAttrs = shadowRoot.querySelectorAll('[data-state-attrs]');

            elementsWithStateAttrs.forEach(el => {
                try {
                    const stateAttrs = JSON.parse(el.dataset.stateAttrs || '{}');

                    // Get attributes for current state
                    const currentStateAttrs = stateAttrs[stateName] || {};
                    const baseStateAttrs = basedOn ? (stateAttrs[basedOn] || {}) : {};
                    const defaultStateAttrs = stateAttrs[defaultState] || stateAttrs['default'] || {};

                    // Merge: default -> basedOn -> current
                    const mergedAttrs = { ...defaultStateAttrs, ...baseStateAttrs, ...currentStateAttrs };

                    // Apply attributes
                    Object.entries(mergedAttrs).forEach(([attr, value]) => {
                        if (attr === 'visible') {
                            el.style.display = value === 'true' || value === true ? '' : 'none';
                        } else if (attr === 'enabled') {
                            el.disabled = !(value === 'true' || value === true);
                        } else if (attr.startsWith('style.')) {
                            const styleProp = attr.substring(6);
                            el.style[styleProp] = value;
                        } else if (attr === 'text' || attr === 'label') {
                            el.textContent = value;
                        } else {
                            el.setAttribute(attr, value);
                        }
                    });
                } catch (e) {
                    console.error('Error parsing state attrs:', e);
                }
            });
        },

        /**
         * Create a state manager for a component
         * @param {ShadowRoot} shadowRoot - The shadow root
         * @param {Object} statesConfig - States configuration from MXML
         * @param {Function} onStateChange - Callback when state changes
         * @returns {Object} State manager
         */
        createStateManager(shadowRoot, statesConfig, onStateChange = null) {
            let currentState = statesConfig.initialState || 'default';

            const manager = {
                get currentState() {
                    return currentState;
                },

                set currentState(newState) {
                    if (newState !== currentState && statesConfig.states[newState]) {
                        const oldState = currentState;
                        currentState = newState;

                        OpenFlexStates.applyState(shadowRoot, newState, statesConfig);

                        if (onStateChange) {
                            onStateChange({ oldState, newState });
                        }
                    }
                },

                /**
                 * Go to a specific state
                 * @param {string} stateName - The state name
                 */
                goToState(stateName) {
                    this.currentState = stateName;
                },

                /**
                 * Check if a state exists
                 * @param {string} stateName - The state name
                 * @returns {boolean} True if state exists
                 */
                hasState(stateName) {
                    return !!statesConfig.states[stateName];
                },

                /**
                 * Get all state names
                 * @returns {string[]} Array of state names
                 */
                getStates() {
                    return Object.keys(statesConfig.states);
                }
            };

            // Apply initial state
            OpenFlexStates.applyState(shadowRoot, currentState, statesConfig);

            return manager;
        },

        /**
         * Parse state attributes from an element (attr.stateName="value" syntax)
         * @param {Object} attributes - Element attributes object
         * @returns {Object} Parsed state attributes
         */
        parseStateAttributes(attributes) {
            const stateAttrs = {};

            Object.entries(attributes).forEach(([attr, value]) => {
                const dotIndex = attr.indexOf('.');
                if (dotIndex > 0) {
                    const baseAttr = attr.substring(0, dotIndex);
                    const stateName = attr.substring(dotIndex + 1);

                    if (!stateAttrs[stateName]) {
                        stateAttrs[stateName] = {};
                    }
                    stateAttrs[stateName][baseAttr] = value;
                }
            });

            return stateAttrs;
        },

        /**
         * Add transition effects between states
         * @param {HTMLElement} element - The element to transition
         * @param {Object} options - Transition options
         */
        addTransition(element, options = {}) {
            const {
                property = 'all',
                duration = 300,
                easing = 'ease',
                delay = 0
            } = options;

            element.style.transition = `${property} ${duration}ms ${easing} ${delay}ms`;
        }
    };

    // Export for browser
    if (typeof window !== 'undefined') {
        window.OpenFlexStates = OpenFlexStates;
    }

    // Export for Node.js/CommonJS
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = OpenFlexStates;
    }
})();
