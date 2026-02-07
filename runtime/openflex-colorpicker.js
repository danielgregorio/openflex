/**
 * OpenFlex ColorPicker Runtime
 * Provides ColorPicker component with HSV picker
 * Flex-style API for color selection
 */
(function() {
    'use strict';

    // Preset color swatches (Web-safe colors)
    const PRESET_COLORS = [
        '#FF0000', '#FF6600', '#FFCC00', '#FFFF00', '#CCFF00',
        '#66FF00', '#00FF00', '#00FF66', '#00FFCC', '#00FFFF',
        '#00CCFF', '#0066FF', '#0000FF', '#6600FF', '#CC00FF',
        '#FF00FF', '#FF00CC', '#FF0066', '#FFFFFF', '#CCCCCC',
        '#999999', '#666666', '#333333', '#000000', '#990000',
        '#996600', '#999900', '#669900', '#009900', '#009966'
    ];

    const OpenFlexColorPicker = {
        /**
         * Initialize a color picker in the given container
         * @param {HTMLElement} container - The popup container element
         * @param {Object} options - ColorPicker options
         */
        init(container, options = {}) {
            const {
                color = '#FF0000',
                showTextField = true,
                onChange = null
            } = options;

            // Parse initial color
            let hsv = this.hexToHsv(color);
            container._colorState = { hsv, color };

            // Get elements
            const satvalEl = container.querySelector('.neo-colorpicker-satval');
            const satvalPtr = container.querySelector('.neo-colorpicker-satval-pointer');
            const hueEl = container.querySelector('.neo-colorpicker-hue');
            const huePtr = container.querySelector('.neo-colorpicker-hue-pointer');
            const inputEl = container.querySelector('.neo-colorpicker-input');
            const swatchesEl = container.querySelector('.neo-colorpicker-swatches');

            // Update satval background based on hue
            const updateSatvalBackground = () => {
                const hueColor = this.hsvToHex(hsv.h, 100, 100);
                satvalEl.style.background = `linear-gradient(to right, white, ${hueColor})`;
            };

            // Update pointer positions
            const updatePointers = () => {
                if (satvalPtr) {
                    satvalPtr.style.left = `${hsv.s}%`;
                    satvalPtr.style.top = `${100 - hsv.v}%`;
                }
                if (huePtr) {
                    huePtr.style.left = `${(hsv.h / 360) * 100}%`;
                }
            };

            // Update color from HSV
            const updateColor = () => {
                const newColor = this.hsvToHex(hsv.h, hsv.s, hsv.v);
                container._colorState.color = newColor;
                container._colorState.hsv = { ...hsv };

                if (inputEl) inputEl.value = newColor;
                if (satvalPtr) satvalPtr.style.backgroundColor = newColor;

                updateSatvalBackground();

                if (onChange) {
                    onChange(newColor);
                }
            };

            // Saturation/Value picker
            if (satvalEl) {
                const handleSatval = (e) => {
                    const rect = satvalEl.getBoundingClientRect();
                    let x = (e.clientX - rect.left) / rect.width;
                    let y = (e.clientY - rect.top) / rect.height;
                    x = Math.max(0, Math.min(1, x));
                    y = Math.max(0, Math.min(1, y));

                    hsv.s = x * 100;
                    hsv.v = (1 - y) * 100;

                    updatePointers();
                    updateColor();
                };

                satvalEl.addEventListener('mousedown', (e) => {
                    e.preventDefault();
                    handleSatval(e);

                    const onMove = (e) => handleSatval(e);
                    const onUp = () => {
                        document.removeEventListener('mousemove', onMove);
                        document.removeEventListener('mouseup', onUp);
                    };

                    document.addEventListener('mousemove', onMove);
                    document.addEventListener('mouseup', onUp);
                });
            }

            // Hue picker
            if (hueEl) {
                const handleHue = (e) => {
                    const rect = hueEl.getBoundingClientRect();
                    let x = (e.clientX - rect.left) / rect.width;
                    x = Math.max(0, Math.min(1, x));

                    hsv.h = x * 360;

                    updatePointers();
                    updateColor();
                };

                hueEl.addEventListener('mousedown', (e) => {
                    e.preventDefault();
                    handleHue(e);

                    const onMove = (e) => handleHue(e);
                    const onUp = () => {
                        document.removeEventListener('mousemove', onMove);
                        document.removeEventListener('mouseup', onUp);
                    };

                    document.addEventListener('mousemove', onMove);
                    document.addEventListener('mouseup', onUp);
                });
            }

            // Text input
            if (inputEl) {
                inputEl.addEventListener('change', (e) => {
                    const newColor = e.target.value;
                    if (/^#[0-9A-Fa-f]{6}$/.test(newColor)) {
                        hsv = this.hexToHsv(newColor);
                        updatePointers();
                        updateColor();
                    }
                });
            }

            // Color swatches
            if (swatchesEl) {
                swatchesEl.innerHTML = '';
                PRESET_COLORS.forEach(swatchColor => {
                    const swatch = document.createElement('div');
                    swatch.className = 'neo-colorpicker-swatch';
                    swatch.style.backgroundColor = swatchColor;
                    swatch.addEventListener('click', () => {
                        hsv = this.hexToHsv(swatchColor);
                        updatePointers();
                        updateColor();
                    });
                    swatchesEl.appendChild(swatch);
                });
            }

            // Initial update
            updateSatvalBackground();
            updatePointers();
            if (inputEl) inputEl.value = color;
            if (satvalPtr) satvalPtr.style.backgroundColor = color;
        },

        /**
         * Convert hex color to RGB
         * @param {string} hex - Hex color string
         * @returns {Object} RGB object { r, g, b }
         */
        hexToRgb(hex) {
            const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            return result ? {
                r: parseInt(result[1], 16),
                g: parseInt(result[2], 16),
                b: parseInt(result[3], 16)
            } : { r: 0, g: 0, b: 0 };
        },

        /**
         * Convert RGB to hex color
         * @param {number} r - Red (0-255)
         * @param {number} g - Green (0-255)
         * @param {number} b - Blue (0-255)
         * @returns {string} Hex color string
         */
        rgbToHex(r, g, b) {
            return '#' + [r, g, b].map(x => {
                const hex = Math.round(x).toString(16);
                return hex.length === 1 ? '0' + hex : hex;
            }).join('').toUpperCase();
        },

        /**
         * Convert RGB to HSV
         * @param {number} r - Red (0-255)
         * @param {number} g - Green (0-255)
         * @param {number} b - Blue (0-255)
         * @returns {Object} HSV object { h, s, v }
         */
        rgbToHsv(r, g, b) {
            r /= 255; g /= 255; b /= 255;
            const max = Math.max(r, g, b);
            const min = Math.min(r, g, b);
            const d = max - min;

            let h = 0;
            const s = max === 0 ? 0 : (d / max) * 100;
            const v = max * 100;

            if (d !== 0) {
                switch (max) {
                    case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
                    case g: h = ((b - r) / d + 2) / 6; break;
                    case b: h = ((r - g) / d + 4) / 6; break;
                }
                h *= 360;
            }

            return { h, s, v };
        },

        /**
         * Convert HSV to RGB
         * @param {number} h - Hue (0-360)
         * @param {number} s - Saturation (0-100)
         * @param {number} v - Value (0-100)
         * @returns {Object} RGB object { r, g, b }
         */
        hsvToRgb(h, s, v) {
            h /= 360; s /= 100; v /= 100;

            let r, g, b;
            const i = Math.floor(h * 6);
            const f = h * 6 - i;
            const p = v * (1 - s);
            const q = v * (1 - f * s);
            const t = v * (1 - (1 - f) * s);

            switch (i % 6) {
                case 0: r = v; g = t; b = p; break;
                case 1: r = q; g = v; b = p; break;
                case 2: r = p; g = v; b = t; break;
                case 3: r = p; g = q; b = v; break;
                case 4: r = t; g = p; b = v; break;
                case 5: r = v; g = p; b = q; break;
            }

            return {
                r: Math.round(r * 255),
                g: Math.round(g * 255),
                b: Math.round(b * 255)
            };
        },

        /**
         * Convert hex to HSV
         * @param {string} hex - Hex color string
         * @returns {Object} HSV object { h, s, v }
         */
        hexToHsv(hex) {
            const rgb = this.hexToRgb(hex);
            return this.rgbToHsv(rgb.r, rgb.g, rgb.b);
        },

        /**
         * Convert HSV to hex
         * @param {number} h - Hue (0-360)
         * @param {number} s - Saturation (0-100)
         * @param {number} v - Value (0-100)
         * @returns {string} Hex color string
         */
        hsvToHex(h, s, v) {
            const rgb = this.hsvToRgb(h, s, v);
            return this.rgbToHex(rgb.r, rgb.g, rgb.b);
        }
    };

    // Export for browser
    if (typeof window !== 'undefined') {
        window.OpenFlexColorPicker = OpenFlexColorPicker;
    }

    // Export for Node.js/CommonJS
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = OpenFlexColorPicker;
    }
})();
