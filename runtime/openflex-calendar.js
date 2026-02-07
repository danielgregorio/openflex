/**
 * OpenFlex Calendar Runtime
 * Provides Calendar, DateField, and DatePicker components
 * Flex-style API for date selection
 */
(function() {
    'use strict';

    const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'];
    const DAYS = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];

    const OpenFlexCalendar = {
        /**
         * Render a calendar in the given container
         * @param {HTMLElement} container - The container element
         * @param {Object} options - Calendar options
         */
        renderCalendar(container, options = {}) {
            const {
                selectedDate = null,
                minDate = null,
                maxDate = null,
                showWeekNumbers = false,
                showToday = true,
                onSelect = null,
                changeHandler = null
            } = options;

            // Parse dates
            const selected = selectedDate ? this._parseDate(selectedDate) : null;
            const min = minDate ? this._parseDate(minDate) : null;
            const max = maxDate ? this._parseDate(maxDate) : null;

            // Current view state (stored on container)
            if (!container._calendarState) {
                container._calendarState = {
                    viewYear: selected ? selected.getFullYear() : new Date().getFullYear(),
                    viewMonth: selected ? selected.getMonth() : new Date().getMonth()
                };
            }
            const state = container._calendarState;

            // Build calendar HTML
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            const firstDay = new Date(state.viewYear, state.viewMonth, 1);
            const lastDay = new Date(state.viewYear, state.viewMonth + 1, 0);
            const startDay = firstDay.getDay();
            const daysInMonth = lastDay.getDate();

            let html = '<div class="neo-calendar-header">';
            html += '<div class="neo-calendar-nav">';
            html += '<button class="neo-calendar-nav-btn" data-action="prev-year">&laquo;</button>';
            html += '<button class="neo-calendar-nav-btn" data-action="prev-month">&lsaquo;</button>';
            html += '</div>';
            html += `<span class="neo-calendar-title">${MONTHS[state.viewMonth]} ${state.viewYear}</span>`;
            html += '<div class="neo-calendar-nav">';
            html += '<button class="neo-calendar-nav-btn" data-action="next-month">&rsaquo;</button>';
            html += '<button class="neo-calendar-nav-btn" data-action="next-year">&raquo;</button>';
            html += '</div>';
            html += '</div>';

            // Weekday headers
            html += '<div class="neo-calendar-weekdays">';
            if (showWeekNumbers) {
                html += '<div class="neo-calendar-weekday">#</div>';
            }
            for (const day of DAYS) {
                html += `<div class="neo-calendar-weekday">${day}</div>`;
            }
            html += '</div>';

            // Calendar grid
            html += '<div class="neo-calendar-grid">';

            // Previous month days
            const prevMonthLastDay = new Date(state.viewYear, state.viewMonth, 0).getDate();
            for (let i = startDay - 1; i >= 0; i--) {
                const day = prevMonthLastDay - i;
                const date = new Date(state.viewYear, state.viewMonth - 1, day);
                const disabled = this._isDisabled(date, min, max);
                html += `<div class="neo-calendar-day other-month${disabled ? ' disabled' : ''}" data-date="${this._formatISO(date)}">${day}</div>`;
            }

            // Current month days
            for (let day = 1; day <= daysInMonth; day++) {
                const date = new Date(state.viewYear, state.viewMonth, day);
                const isToday = date.getTime() === today.getTime();
                const isSelected = selected && date.getTime() === selected.getTime();
                const disabled = this._isDisabled(date, min, max);

                let classes = 'neo-calendar-day';
                if (isToday && showToday) classes += ' today';
                if (isSelected) classes += ' selected';
                if (disabled) classes += ' disabled';

                html += `<div class="${classes}" data-date="${this._formatISO(date)}">${day}</div>`;
            }

            // Next month days
            const totalCells = startDay + daysInMonth;
            const remainingCells = (7 - (totalCells % 7)) % 7;
            for (let day = 1; day <= remainingCells; day++) {
                const date = new Date(state.viewYear, state.viewMonth + 1, day);
                const disabled = this._isDisabled(date, min, max);
                html += `<div class="neo-calendar-day other-month${disabled ? ' disabled' : ''}" data-date="${this._formatISO(date)}">${day}</div>`;
            }

            html += '</div>';

            container.innerHTML = html;

            // Event handlers
            container.querySelectorAll('.neo-calendar-nav-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const action = btn.dataset.action;
                    if (action === 'prev-year') {
                        state.viewYear--;
                    } else if (action === 'prev-month') {
                        state.viewMonth--;
                        if (state.viewMonth < 0) {
                            state.viewMonth = 11;
                            state.viewYear--;
                        }
                    } else if (action === 'next-month') {
                        state.viewMonth++;
                        if (state.viewMonth > 11) {
                            state.viewMonth = 0;
                            state.viewYear++;
                        }
                    } else if (action === 'next-year') {
                        state.viewYear++;
                    }
                    this.renderCalendar(container, options);
                });
            });

            container.querySelectorAll('.neo-calendar-day:not(.disabled)').forEach(dayEl => {
                dayEl.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const dateStr = dayEl.dataset.date;
                    const date = this._parseDate(dateStr);

                    if (onSelect) {
                        onSelect(date);
                    }
                    if (changeHandler && typeof window[changeHandler] === 'function') {
                        window[changeHandler]({ selectedDate: date });
                    }
                });
            });
        },

        /**
         * Format a date according to a format string
         * @param {Date} date - The date to format
         * @param {string} format - Format string (yyyy-MM-dd, etc.)
         * @returns {string} Formatted date string
         */
        formatDate(date, format = 'yyyy-MM-dd') {
            if (!date) return '';
            if (!(date instanceof Date)) {
                date = this._parseDate(date);
            }

            const year = date.getFullYear();
            const month = date.getMonth() + 1;
            const day = date.getDate();

            return format
                .replace('yyyy', year)
                .replace('MM', month.toString().padStart(2, '0'))
                .replace('dd', day.toString().padStart(2, '0'))
                .replace('M', month)
                .replace('d', day);
        },

        /**
         * Parse a date string or Date object
         * @param {string|Date} value - The value to parse
         * @returns {Date} Parsed date
         */
        _parseDate(value) {
            if (value instanceof Date) return new Date(value.getTime());
            if (typeof value === 'string') {
                const date = new Date(value);
                date.setHours(0, 0, 0, 0);
                return date;
            }
            return null;
        },

        /**
         * Format date as ISO string (yyyy-MM-dd)
         * @param {Date} date - The date to format
         * @returns {string} ISO date string
         */
        _formatISO(date) {
            return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
        },

        /**
         * Check if a date is disabled
         * @param {Date} date - The date to check
         * @param {Date|null} min - Minimum date
         * @param {Date|null} max - Maximum date
         * @returns {boolean} True if disabled
         */
        _isDisabled(date, min, max) {
            if (min && date < min) return true;
            if (max && date > max) return true;
            return false;
        }
    };

    // Export for browser
    if (typeof window !== 'undefined') {
        window.OpenFlexCalendar = OpenFlexCalendar;
    }

    // Export for Node.js/CommonJS
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = OpenFlexCalendar;
    }
})();
