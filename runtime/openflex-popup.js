/**
 * OpenFlex PopUp Runtime
 * Provides Alert, TitleWindow, and PopUp components
 * Flex-style API for modal dialogs
 */
(function() {
    'use strict';

    // Alert button flags (matching Flex API)
    const Alert = {
        OK: 0x0001,
        CANCEL: 0x0002,
        YES: 0x0004,
        NO: 0x0008,

        /**
         * Show an alert dialog
         * @param {string} message - The message to display
         * @param {string} title - The title of the alert
         * @param {number} flags - Button flags (Alert.OK | Alert.CANCEL, etc.)
         * @param {Function} callback - Callback function (receives button name)
         * @param {HTMLElement} parent - Parent element (optional, defaults to document.body)
         * @returns {HTMLElement} The alert element
         */
        show(message, title = 'Alert', flags = Alert.OK, callback = null, parent = null) {
            const container = parent || document.body;

            // Determine which buttons to show
            const buttons = [];
            if (flags & Alert.OK) buttons.push({ name: 'OK', label: 'OK' });
            if (flags & Alert.YES) buttons.push({ name: 'YES', label: 'Yes' });
            if (flags & Alert.NO) buttons.push({ name: 'NO', label: 'No' });
            if (flags & Alert.CANCEL) buttons.push({ name: 'CANCEL', label: 'Cancel' });

            // Create overlay
            const overlay = document.createElement('div');
            overlay.className = 'neo-modal-overlay neo-modal';
            overlay.style.display = 'flex';

            // Create alert window
            const alertEl = document.createElement('div');
            alertEl.className = 'neo-titlewindow neo-alert';

            // Header
            const header = document.createElement('div');
            header.className = 'neo-titlewindow-header';
            header.innerHTML = `<span class="neo-titlewindow-title">${title}</span>`;
            alertEl.appendChild(header);

            // Content
            const content = document.createElement('div');
            content.className = 'neo-alert-content';
            content.innerHTML = `<span class="neo-alert-message">${message}</span>`;
            alertEl.appendChild(content);

            // Buttons
            const buttonsContainer = document.createElement('div');
            buttonsContainer.className = 'neo-alert-buttons';

            buttons.forEach(btn => {
                const button = document.createElement('button');
                button.className = 'neo-button';
                button.textContent = btn.label;
                button.addEventListener('click', () => {
                    overlay.remove();
                    if (callback) callback(btn.name);
                });
                buttonsContainer.appendChild(button);
            });

            alertEl.appendChild(buttonsContainer);
            overlay.appendChild(alertEl);
            container.appendChild(overlay);

            return alertEl;
        }
    };

    const OpenFlexPopUp = {
        /**
         * Create a TitleWindow programmatically
         * @param {Object} options - TitleWindow options
         * @returns {HTMLElement} The TitleWindow element
         */
        createTitleWindow(options = {}) {
            const {
                title = 'Window',
                content = '',
                width = 400,
                height = 'auto',
                modal = true,
                showCloseButton = true,
                onClose = null,
                parent = null
            } = options;

            const container = parent || document.body;

            // Create overlay
            const overlay = document.createElement('div');
            overlay.className = 'neo-modal-overlay' + (modal ? ' neo-modal' : '');
            overlay.style.display = 'flex';

            // Create window
            const windowEl = document.createElement('div');
            windowEl.className = 'neo-titlewindow';
            windowEl.style.width = typeof width === 'number' ? `${width}px` : width;
            if (height !== 'auto') {
                windowEl.style.height = typeof height === 'number' ? `${height}px` : height;
            }

            // Header
            const header = document.createElement('div');
            header.className = 'neo-titlewindow-header';

            const titleSpan = document.createElement('span');
            titleSpan.className = 'neo-titlewindow-title';
            titleSpan.textContent = title;
            header.appendChild(titleSpan);

            if (showCloseButton) {
                const closeBtn = document.createElement('button');
                closeBtn.className = 'neo-titlewindow-close';
                closeBtn.innerHTML = '&times;';
                closeBtn.addEventListener('click', () => {
                    this.close(overlay);
                    if (onClose) onClose();
                });
                header.appendChild(closeBtn);
            }

            windowEl.appendChild(header);

            // Body
            const body = document.createElement('div');
            body.className = 'neo-titlewindow-body';
            if (typeof content === 'string') {
                body.innerHTML = content;
            } else if (content instanceof HTMLElement) {
                body.appendChild(content);
            }
            windowEl.appendChild(body);

            overlay.appendChild(windowEl);

            // Store references
            overlay._window = windowEl;
            windowEl._overlay = overlay;

            return overlay;
        },

        /**
         * Show a popup element
         * @param {HTMLElement} popup - The popup overlay element
         * @param {HTMLElement} parent - Parent element (optional)
         */
        show(popup, parent = null) {
            const container = parent || document.body;
            if (!popup.parentElement) {
                container.appendChild(popup);
            }
            popup.style.display = 'flex';
        },

        /**
         * Close a popup element
         * @param {HTMLElement} popup - The popup overlay element
         * @param {boolean} remove - Whether to remove from DOM (default: true)
         */
        close(popup, remove = true) {
            popup.style.display = 'none';
            if (remove && popup.parentElement) {
                popup.remove();
            }
        },

        /**
         * Center a popup in the viewport
         * @param {HTMLElement} popup - The popup window element
         */
        center(popup) {
            const window = popup._window || popup;
            window.style.position = 'relative';
            window.style.margin = 'auto';
        }
    };

    // Export for browser
    if (typeof window !== 'undefined') {
        window.Alert = Alert;
        window.OpenFlexPopUp = OpenFlexPopUp;
    }

    // Export for Node.js/CommonJS
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = { Alert, OpenFlexPopUp };
    }
})();
