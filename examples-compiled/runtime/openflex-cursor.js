/**
 * OpenFlex CursorManager Runtime
 * Provides Flex-style cursor management
 * API: CursorManager.setBusyCursor(), removeBusyCursor(), setCursor(), removeCursor()
 */
(function() {
    'use strict';

    // Cursor priority stack
    let cursorStack = [];
    let busyCursorCount = 0;
    let cursorOverlay = null;

    // Built-in cursor types (Flex-style)
    const CURSOR_TYPES = {
        // Standard cursors
        AUTO: 'auto',
        DEFAULT: 'default',
        POINTER: 'pointer',
        CROSSHAIR: 'crosshair',
        TEXT: 'text',
        MOVE: 'move',
        HELP: 'help',
        NOT_ALLOWED: 'not-allowed',

        // Resize cursors
        N_RESIZE: 'n-resize',
        S_RESIZE: 's-resize',
        E_RESIZE: 'e-resize',
        W_RESIZE: 'w-resize',
        NE_RESIZE: 'ne-resize',
        NW_RESIZE: 'nw-resize',
        SE_RESIZE: 'se-resize',
        SW_RESIZE: 'sw-resize',
        EW_RESIZE: 'ew-resize',
        NS_RESIZE: 'ns-resize',

        // Special cursors
        WAIT: 'wait',
        PROGRESS: 'progress',
        GRAB: 'grab',
        GRABBING: 'grabbing',
        ZOOM_IN: 'zoom-in',
        ZOOM_OUT: 'zoom-out',

        // Flex-specific (mapped to CSS equivalents)
        BUSY: 'wait',
        HAND: 'pointer',
        IBEAM: 'text',
        SIZE_ALL: 'move',
        SIZE_NESW: 'nesw-resize',
        SIZE_NS: 'ns-resize',
        SIZE_NWSE: 'nwse-resize',
        SIZE_WE: 'ew-resize'
    };

    // Custom cursor definitions (CSS url() based)
    const customCursors = {};

    /**
     * Create the cursor overlay element (for custom animated cursors)
     */
    function ensureOverlay() {
        if (!cursorOverlay && typeof document !== 'undefined') {
            cursorOverlay = document.createElement('div');
            cursorOverlay.id = 'openflex-cursor-overlay';
            cursorOverlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 999999;
                pointer-events: none;
                display: none;
            `;
            document.body.appendChild(cursorOverlay);
        }
        return cursorOverlay;
    }

    /**
     * Apply the current cursor from the stack
     */
    function applyCursor() {
        if (typeof document === 'undefined') return;

        const overlay = ensureOverlay();

        if (cursorStack.length === 0) {
            // No cursor override
            document.body.style.cursor = '';
            overlay.style.display = 'none';
            return;
        }

        const currentCursor = cursorStack[cursorStack.length - 1];

        if (currentCursor.type === 'custom' && currentCursor.element) {
            // Custom cursor element (animated spinner, etc.)
            overlay.innerHTML = '';
            overlay.appendChild(currentCursor.element);
            overlay.style.display = 'block';
            document.body.style.cursor = 'none';

            // Track mouse position
            if (!overlay._tracking) {
                overlay._tracking = true;
                document.addEventListener('mousemove', (e) => {
                    if (overlay.firstChild) {
                        overlay.firstChild.style.left = e.clientX + 'px';
                        overlay.firstChild.style.top = e.clientY + 'px';
                    }
                });
            }
        } else {
            // Standard CSS cursor
            overlay.style.display = 'none';
            document.body.style.cursor = currentCursor.cursor || 'auto';

            // Also set on all elements for stronger override
            document.documentElement.style.cursor = currentCursor.cursor || '';
        }
    }

    /**
     * CursorManager - Flex-style API
     */
    const CursorManager = {
        // Expose cursor type constants
        ...CURSOR_TYPES,

        /**
         * Set the busy cursor (stacking - call removeBusyCursor for each setBusyCursor)
         */
        setBusyCursor() {
            busyCursorCount++;
            if (busyCursorCount === 1) {
                this.setCursor('busy', CURSOR_TYPES.BUSY, 1000);
            }
        },

        /**
         * Remove the busy cursor
         */
        removeBusyCursor() {
            if (busyCursorCount > 0) {
                busyCursorCount--;
                if (busyCursorCount === 0) {
                    this.removeCursor('busy');
                }
            }
        },

        /**
         * Set a cursor by ID
         * @param {string} id - Unique identifier for this cursor
         * @param {string} cursor - CSS cursor value or CURSOR_TYPES constant
         * @param {number} priority - Higher priority cursors take precedence (default: 0)
         */
        setCursor(id, cursor, priority = 0) {
            // Remove existing cursor with same ID
            this.removeCursor(id);

            // Resolve cursor type
            const resolvedCursor = CURSOR_TYPES[cursor.toUpperCase()] || cursor;

            // Add to stack
            cursorStack.push({
                id,
                cursor: resolvedCursor,
                priority,
                type: 'css'
            });

            // Sort by priority (higher priority = later in array = takes effect)
            cursorStack.sort((a, b) => a.priority - b.priority);

            applyCursor();
        },

        /**
         * Set a custom cursor with an element (for animated cursors)
         * @param {string} id - Unique identifier
         * @param {HTMLElement} element - The cursor element
         * @param {number} priority - Priority level
         */
        setCustomCursor(id, element, priority = 0) {
            this.removeCursor(id);

            // Style the element for cursor use
            element.style.position = 'fixed';
            element.style.pointerEvents = 'none';
            element.style.transform = 'translate(-50%, -50%)';

            cursorStack.push({
                id,
                element,
                priority,
                type: 'custom'
            });

            cursorStack.sort((a, b) => a.priority - b.priority);
            applyCursor();
        },

        /**
         * Remove a cursor by ID
         * @param {string} id - The cursor ID to remove
         */
        removeCursor(id) {
            const index = cursorStack.findIndex(c => c.id === id);
            if (index !== -1) {
                cursorStack.splice(index, 1);
                applyCursor();
            }
        },

        /**
         * Remove all cursors
         */
        removeAllCursors() {
            cursorStack = [];
            busyCursorCount = 0;
            applyCursor();
        },

        /**
         * Get the current cursor stack (for debugging)
         */
        getCursorStack() {
            return [...cursorStack];
        },

        /**
         * Register a custom cursor type
         * @param {string} name - Cursor name
         * @param {string} url - URL to cursor image
         * @param {number} hotspotX - Hotspot X coordinate
         * @param {number} hotspotY - Hotspot Y coordinate
         */
        registerCursor(name, url, hotspotX = 0, hotspotY = 0) {
            customCursors[name] = `url('${url}') ${hotspotX} ${hotspotY}, auto`;
        },

        /**
         * Create a spinning busy cursor element
         * @returns {HTMLElement}
         */
        createSpinnerCursor() {
            const spinner = document.createElement('div');
            spinner.className = 'neo-cursor-spinner';
            spinner.innerHTML = `
                <svg width="24" height="24" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" stroke="#666" stroke-width="2" fill="none" opacity="0.3"/>
                    <path d="M12 2 A10 10 0 0 1 22 12" stroke="#333" stroke-width="2" fill="none" stroke-linecap="round">
                        <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="1s" repeatCount="indefinite"/>
                    </path>
                </svg>
            `;
            return spinner;
        },

        /**
         * Create a thinking cursor (dots animation)
         * @returns {HTMLElement}
         */
        createThinkingCursor() {
            const thinking = document.createElement('div');
            thinking.className = 'neo-cursor-thinking';
            thinking.innerHTML = `
                <div style="display: flex; gap: 3px; background: rgba(0,0,0,0.7); padding: 6px 10px; border-radius: 12px;">
                    <div class="neo-thinking-dot" style="width: 6px; height: 6px; background: white; border-radius: 50%; animation: neo-thinking 1.4s ease-in-out infinite;"></div>
                    <div class="neo-thinking-dot" style="width: 6px; height: 6px; background: white; border-radius: 50%; animation: neo-thinking 1.4s ease-in-out 0.2s infinite;"></div>
                    <div class="neo-thinking-dot" style="width: 6px; height: 6px; background: white; border-radius: 50%; animation: neo-thinking 1.4s ease-in-out 0.4s infinite;"></div>
                </div>
            `;

            // Add animation styles if not present
            if (!document.getElementById('neo-cursor-styles')) {
                const style = document.createElement('style');
                style.id = 'neo-cursor-styles';
                style.textContent = `
                    @keyframes neo-thinking {
                        0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
                        40% { transform: scale(1); opacity: 1; }
                    }
                    @keyframes neo-spin {
                        from { transform: translate(-50%, -50%) rotate(0deg); }
                        to { transform: translate(-50%, -50%) rotate(360deg); }
                    }
                `;
                document.head.appendChild(style);
            }

            return thinking;
        },

        /**
         * Set thinking cursor (animated dots)
         */
        setThinkingCursor() {
            this.setCustomCursor('thinking', this.createThinkingCursor(), 900);
        },

        /**
         * Remove thinking cursor
         */
        removeThinkingCursor() {
            this.removeCursor('thinking');
        },

        /**
         * Set spinner cursor (animated spinning circle)
         */
        setSpinnerCursor() {
            this.setCustomCursor('spinner', this.createSpinnerCursor(), 950);
        },

        /**
         * Remove spinner cursor
         */
        removeSpinnerCursor() {
            this.removeCursor('spinner');
        },

        /**
         * Execute a function with busy cursor
         * @param {Function} fn - Async function to execute
         * @returns {Promise} Result of the function
         */
        async withBusyCursor(fn) {
            this.setBusyCursor();
            try {
                return await fn();
            } finally {
                this.removeBusyCursor();
            }
        },

        /**
         * Execute a function with thinking cursor
         * @param {Function} fn - Async function to execute
         * @returns {Promise} Result of the function
         */
        async withThinkingCursor(fn) {
            this.setThinkingCursor();
            try {
                return await fn();
            } finally {
                this.removeThinkingCursor();
            }
        }
    };

    // Export for browser
    if (typeof window !== 'undefined') {
        window.CursorManager = CursorManager;

        // Also expose cursor types directly
        window.CursorType = CURSOR_TYPES;
    }

    // Export for Node.js/CommonJS
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { CursorManager, CursorType: CURSOR_TYPES };
    }
})();
