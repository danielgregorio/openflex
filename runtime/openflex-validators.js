/**
 * OpenFlex Validators Runtime
 * Provides form validation components
 * Flex-style API for data validation
 */
(function() {
    'use strict';

    /**
     * Base Validator class
     */
    class Validator {
        constructor(options = {}) {
            this.source = options.source || null;
            this.property = options.property || 'value';
            this.trigger = options.trigger || null;
            this.triggerEvent = options.triggerEvent || 'change';
            this.requiredFieldError = options.requiredFieldError || 'This field is required.';
            this.enabled = true;
            this._boundValidate = this.validate.bind(this);
        }

        /**
         * Attach validator to source element
         */
        attach() {
            const el = this._getSourceElement();
            if (!el) return;

            el.addEventListener(this.triggerEvent, this._boundValidate);
            el.addEventListener('blur', this._boundValidate);
        }

        /**
         * Detach validator from source element
         */
        detach() {
            const el = this._getSourceElement();
            if (!el) return;

            el.removeEventListener(this.triggerEvent, this._boundValidate);
            el.removeEventListener('blur', this._boundValidate);
        }

        /**
         * Get the source element
         */
        _getSourceElement() {
            if (typeof this.source === 'string') {
                return document.getElementById(this.source);
            }
            return this.source;
        }

        /**
         * Get the value to validate
         */
        _getValue() {
            const el = this._getSourceElement();
            if (!el) return null;
            return el[this.property] || el.value || '';
        }

        /**
         * Validate the value
         * @returns {Object} Validation result { valid: boolean, errorMessage: string }
         */
        validate() {
            if (!this.enabled) {
                return { valid: true, errorMessage: '' };
            }

            const value = this._getValue();
            const result = this.doValidation(value);

            this._applyVisualFeedback(result);

            return result;
        }

        /**
         * Perform the actual validation (override in subclasses)
         * @param {*} value - The value to validate
         * @returns {Object} Validation result
         */
        doValidation(value) {
            return { valid: true, errorMessage: '' };
        }

        /**
         * Apply visual feedback to the source element
         * @param {Object} result - Validation result
         */
        _applyVisualFeedback(result) {
            const el = this._getSourceElement();
            if (!el) return;

            el.classList.remove('neo-valid', 'neo-invalid');
            el.classList.add(result.valid ? 'neo-valid' : 'neo-invalid');

            // Find or create error message element
            let errorEl = el.parentElement.querySelector('.neo-validation-error');
            if (result.valid) {
                if (errorEl) errorEl.textContent = '';
            } else {
                if (!errorEl) {
                    errorEl = document.createElement('span');
                    errorEl.className = 'neo-validation-error';
                    el.parentElement.appendChild(errorEl);
                }
                errorEl.textContent = result.errorMessage;
            }
        }
    }

    /**
     * String Validator - validates string length
     */
    class StringValidator extends Validator {
        constructor(options = {}) {
            super(options);
            this.minLength = options.minLength !== undefined ? parseInt(options.minLength) : null;
            this.maxLength = options.maxLength !== undefined ? parseInt(options.maxLength) : null;
            this.tooShortError = options.tooShortError || `Must be at least ${this.minLength} characters.`;
            this.tooLongError = options.tooLongError || `Must be no more than ${this.maxLength} characters.`;
        }

        doValidation(value) {
            const str = String(value || '');

            if (this.minLength !== null && str.length < this.minLength) {
                return { valid: false, errorMessage: this.tooShortError };
            }

            if (this.maxLength !== null && str.length > this.maxLength) {
                return { valid: false, errorMessage: this.tooLongError };
            }

            return { valid: true, errorMessage: '' };
        }
    }

    /**
     * Number Validator - validates numeric values
     */
    class NumberValidator extends Validator {
        constructor(options = {}) {
            super(options);
            this.minValue = options.minValue !== undefined ? parseFloat(options.minValue) : null;
            this.maxValue = options.maxValue !== undefined ? parseFloat(options.maxValue) : null;
            this.notANumberError = options.notANumberError || 'Please enter a valid number.';
            this.lowerThanMinError = options.lowerThanMinError || `Value must be at least ${this.minValue}.`;
            this.greaterThanMaxError = options.greaterThanMaxError || `Value must be no more than ${this.maxValue}.`;
        }

        doValidation(value) {
            const num = parseFloat(value);

            if (isNaN(num)) {
                return { valid: false, errorMessage: this.notANumberError };
            }

            if (this.minValue !== null && num < this.minValue) {
                return { valid: false, errorMessage: this.lowerThanMinError };
            }

            if (this.maxValue !== null && num > this.maxValue) {
                return { valid: false, errorMessage: this.greaterThanMaxError };
            }

            return { valid: true, errorMessage: '' };
        }
    }

    /**
     * RegExp Validator - validates against a regular expression
     */
    class RegExpValidator extends Validator {
        constructor(options = {}) {
            super(options);
            this.pattern = options.pattern || '';
            this.flags = options.flags || '';
            this.noMatchError = options.noMatchError || 'Invalid format.';
        }

        doValidation(value) {
            if (!this.pattern) {
                return { valid: true, errorMessage: '' };
            }

            const regex = new RegExp(this.pattern, this.flags);
            const isValid = regex.test(String(value || ''));

            return {
                valid: isValid,
                errorMessage: isValid ? '' : this.noMatchError
            };
        }
    }

    /**
     * Email Validator - validates email addresses
     */
    class EmailValidator extends RegExpValidator {
        constructor(options = {}) {
            super({
                ...options,
                pattern: options.pattern || '^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$'
            });
            this.noMatchError = options.invalidEmailError || 'Please enter a valid email address.';
        }
    }

    /**
     * Phone Validator - validates phone numbers
     */
    class PhoneValidator extends RegExpValidator {
        constructor(options = {}) {
            super({
                ...options,
                pattern: options.pattern || '^\\d{10,}$'
            });
            this.noMatchError = options.invalidPhoneError || 'Please enter a valid phone number.';
        }
    }

    /**
     * Date Validator - validates date values
     */
    class DateValidator extends Validator {
        constructor(options = {}) {
            super(options);
            this.minDate = options.minDate ? new Date(options.minDate) : null;
            this.maxDate = options.maxDate ? new Date(options.maxDate) : null;
            this.invalidDateError = options.invalidDateError || 'Please enter a valid date.';
            this.dateOutOfRangeError = options.dateOutOfRangeError || 'Date is out of allowed range.';
        }

        doValidation(value) {
            const date = new Date(value);

            if (isNaN(date.getTime())) {
                return { valid: false, errorMessage: this.invalidDateError };
            }

            if (this.minDate && date < this.minDate) {
                return { valid: false, errorMessage: this.dateOutOfRangeError };
            }

            if (this.maxDate && date > this.maxDate) {
                return { valid: false, errorMessage: this.dateOutOfRangeError };
            }

            return { valid: true, errorMessage: '' };
        }
    }

    /**
     * Validation utility functions
     */
    const OpenFlexValidators = {
        /**
         * Create a validator instance by type
         * @param {string} type - Validator type (string, number, email, regexp, phone, date)
         * @param {Object} options - Validator options
         * @returns {Validator} Validator instance
         */
        createValidator(type, options = {}) {
            switch (type.toLowerCase()) {
                case 'string':
                    return new StringValidator(options);
                case 'number':
                    return new NumberValidator(options);
                case 'email':
                    return new EmailValidator(options);
                case 'regexp':
                case 'regex':
                    return new RegExpValidator(options);
                case 'phone':
                    return new PhoneValidator(options);
                case 'date':
                    return new DateValidator(options);
                default:
                    return new Validator(options);
            }
        },

        /**
         * Setup validation on an element with multiple validators
         * @param {HTMLElement} element - The element to validate
         * @param {Array} validators - Array of validator instances
         * @param {Function} callback - Callback function (receives { valid, errors })
         */
        setupValidation(element, validators, callback = null) {
            validators.forEach(validator => {
                validator.source = element;
                validator.attach();
            });

            const validateAll = () => {
                const results = validators.map(v => v.validate());
                const allValid = results.every(r => r.valid);
                const errors = results.filter(r => !r.valid).map(r => r.errorMessage);

                if (callback) {
                    callback({ valid: allValid, errors });
                }

                return { valid: allValid, errors };
            };

            element.addEventListener('blur', validateAll);

            return validateAll;
        },

        /**
         * Validate a form (all inputs with validators)
         * @param {HTMLElement} form - The form element
         * @returns {Object} Validation result { valid, errors }
         */
        validateForm(form) {
            const inputs = form.querySelectorAll('[data-validate]');
            let allValid = true;
            const errors = [];

            inputs.forEach(input => {
                if (input._validators) {
                    input._validators.forEach(validator => {
                        const result = validator.validate();
                        if (!result.valid) {
                            allValid = false;
                            errors.push(result.errorMessage);
                        }
                    });
                }
            });

            return { valid: allValid, errors };
        },

        // Export validator classes
        Validator,
        StringValidator,
        NumberValidator,
        RegExpValidator,
        EmailValidator,
        PhoneValidator,
        DateValidator
    };

    // Export for browser
    if (typeof window !== 'undefined') {
        window.OpenFlexValidators = OpenFlexValidators;
        // Also export individual classes for convenience
        window.StringValidator = StringValidator;
        window.NumberValidator = NumberValidator;
        window.EmailValidator = EmailValidator;
        window.RegExpValidator = RegExpValidator;
        window.PhoneValidator = PhoneValidator;
        window.DateValidator = DateValidator;
    }

    // Export for Node.js/CommonJS
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = OpenFlexValidators;
    }
})();
