/**
 * OpenFlex Charts Runtime - ECharts Wrapper
 * Provides Flex-style chart API using Apache ECharts
 *
 * Supports: ColumnChart, BarChart, LineChart, AreaChart, PieChart, DoughnutChart
 */
(function() {
    'use strict';

    const OpenFlexCharts = {
        /**
         * Create a new chart instance
         * @param {HTMLElement} container - The container element
         * @param {Object} config - Chart configuration from MXML
         * @returns {Object|null} ECharts instance or null if ECharts not loaded
         */
        createChart(container, config) {
            if (typeof echarts === 'undefined') {
                console.error('ECharts not loaded. Include echarts.min.js before this script.');
                container.innerHTML = '<div class="neo-chart-loading">ECharts not loaded</div>';
                return null;
            }

            const chart = echarts.init(container);
            const option = this.buildOption(config, []);
            chart.setOption(option);

            // Handle resize with ResizeObserver
            const resizeObserver = new ResizeObserver(() => {
                chart.resize();
            });
            resizeObserver.observe(container);
            container._chartResizeObserver = resizeObserver;
            container._chartInstance = chart;

            return chart;
        },

        /**
         * Build ECharts option from MXML config
         * @param {Object} config - Chart configuration
         * @param {Array} data - Data array
         * @returns {Object} ECharts option object
         */
        buildOption(config, data) {
            const chartType = config.chartType;
            const series = config.series || [];

            // Flex Classic color palette
            const colorPalette = [
                '#4F81BD', // Blue
                '#C0504D', // Red
                '#9BBB59', // Green
                '#8064A2', // Purple
                '#4BACC6', // Teal
                '#F79646', // Orange
                '#2C4D75', // Dark Blue
                '#772C2A', // Dark Red
                '#5E7530', // Dark Green
                '#4D3B62'  // Dark Purple
            ];

            // Base option with Flex Classic styling
            const option = {
                color: colorPalette,
                tooltip: {
                    trigger: chartType === 'pie' || chartType === 'doughnut' ? 'item' : 'axis',
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    borderColor: '#999',
                    borderWidth: 1,
                    textStyle: {
                        color: '#333',
                        fontSize: 11
                    },
                    axisPointer: {
                        type: chartType === 'line' || chartType === 'area' ? 'cross' : 'shadow'
                    }
                },
                legend: {
                    data: series.map(s => s.displayName).filter(Boolean),
                    top: 'top',
                    textStyle: {
                        fontSize: 11,
                        color: '#333'
                    }
                }
            };

            // Handle different chart types
            if (chartType === 'pie' || chartType === 'doughnut') {
                option.series = series.map(s => ({
                    type: 'pie',
                    radius: chartType === 'doughnut' ? ['40%', '70%'] : '70%',
                    center: ['50%', '55%'],
                    data: data.map(d => ({
                        value: d[s.field] || d[s.yField] || 0,
                        name: d[s.nameField] || d[config.horizontalAxis?.categoryField] || ''
                    })),
                    name: s.displayName,
                    label: {
                        fontSize: 11
                    },
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }));
            } else {
                // Bar, Column, Line, Area charts
                const categoryField = config.horizontalAxis?.categoryField || 'name';
                const categories = data.map(d => d[categoryField]);

                // Grid for proper spacing
                option.grid = {
                    left: '3%',
                    right: '4%',
                    bottom: '10%',
                    top: series.length > 1 ? '15%' : '10%',
                    containLabel: true
                };

                option.xAxis = {
                    type: 'category',
                    data: categories,
                    name: config.horizontalAxis?.title || '',
                    nameLocation: 'center',
                    nameGap: 30,
                    axisLine: {
                        lineStyle: {
                            color: '#999'
                        }
                    },
                    axisLabel: {
                        fontSize: 11,
                        color: '#333'
                    },
                    axisTick: {
                        alignWithLabel: true
                    }
                };

                option.yAxis = {
                    type: 'value',
                    name: config.verticalAxis?.title || '',
                    nameLocation: 'center',
                    nameGap: 50,
                    min: config.verticalAxis?.minimum !== undefined ? parseFloat(config.verticalAxis.minimum) : undefined,
                    max: config.verticalAxis?.maximum !== undefined ? parseFloat(config.verticalAxis.maximum) : undefined,
                    axisLine: {
                        lineStyle: {
                            color: '#999'
                        }
                    },
                    axisLabel: {
                        fontSize: 11,
                        color: '#333'
                    },
                    splitLine: {
                        lineStyle: {
                            color: '#E0E0E0'
                        }
                    }
                };

                // Swap axes for horizontal bar chart
                if (chartType === 'bar') {
                    const temp = option.xAxis;
                    option.xAxis = option.yAxis;
                    option.yAxis = temp;
                    option.yAxis.type = 'category';
                    option.xAxis.type = 'value';
                }

                option.series = series.map((s, idx) => {
                    const seriesType = this._getSeriesType(chartType, s.type);
                    const seriesOption = {
                        type: seriesType,
                        data: data.map(d => d[s.yField] || 0),
                        name: s.displayName || `Series ${idx + 1}`,
                        smooth: chartType === 'line' || chartType === 'area' || s.type === 'line',
                        emphasis: {
                            focus: 'series'
                        }
                    };

                    // Add area style for area charts
                    if (chartType === 'area' || s.isArea) {
                        seriesOption.areaStyle = {
                            opacity: 0.3
                        };
                    }

                    // Bar specific options
                    if (seriesType === 'bar') {
                        seriesOption.barMaxWidth = 50;
                        seriesOption.itemStyle = {
                            borderRadius: [2, 2, 0, 0]
                        };
                    }

                    // Line specific options
                    if (seriesType === 'line') {
                        seriesOption.symbol = 'circle';
                        seriesOption.symbolSize = 6;
                    }

                    return seriesOption;
                });
            }

            return option;
        },

        /**
         * Get ECharts series type from chart type and series type
         * @private
         */
        _getSeriesType(chartType, seriesType) {
            if (chartType === 'column' || chartType === 'bar') {
                return 'bar';
            }
            if (chartType === 'line' || chartType === 'area') {
                return 'line';
            }
            if (seriesType === 'bar') {
                return 'bar';
            }
            if (seriesType === 'line') {
                return 'line';
            }
            return 'bar';
        },

        /**
         * Update chart with new data (reactive)
         * @param {Object} chart - ECharts instance
         * @param {Array} data - New data array
         * @param {Object} config - Chart configuration
         */
        updateChartData(chart, data, config) {
            if (!chart) return;

            const option = this.buildOption(config, data);
            chart.setOption(option, { notMerge: false });
        },

        /**
         * Destroy chart and cleanup
         * @param {Object} chart - ECharts instance
         * @param {HTMLElement} container - Container element
         */
        destroyChart(chart, container) {
            if (container && container._chartResizeObserver) {
                container._chartResizeObserver.disconnect();
                delete container._chartResizeObserver;
            }
            if (chart) {
                chart.dispose();
            }
            if (container) {
                delete container._chartInstance;
            }
        },

        /**
         * Resize chart to fit container
         * @param {Object} chart - ECharts instance
         */
        resizeChart(chart) {
            if (chart) {
                chart.resize();
            }
        }
    };

    // Export for browser
    if (typeof window !== 'undefined') {
        window.OpenFlexCharts = OpenFlexCharts;
    }

    // Export for Node.js/CommonJS
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = OpenFlexCharts;
    }
})();
