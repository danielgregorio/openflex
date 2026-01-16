#!/bin/bash
# Recompila todos os exemplos MXML

cd "$(dirname "$0")"

echo "🔨 Recompilando todos os exemplos MXML..."
echo

# 08-visual-ui
echo "📁 08-visual-ui/"
python compile-mxml.py examples-compiled/08-visual-ui/CalculatorApp.mxml examples-compiled/08-visual-ui/CalculatorApp-component.js
python compile-mxml.py examples-compiled/08-visual-ui/ColorPickerApp.mxml examples-compiled/08-visual-ui/ColorPickerApp-component.js
python compile-mxml.py examples-compiled/08-visual-ui/CounterApp.mxml examples-compiled/08-visual-ui/CounterApp-component.js
python compile-mxml.py examples-compiled/08-visual-ui/DashboardApp.mxml examples-compiled/08-visual-ui/DashboardApp-component.js
python compile-mxml.py examples-compiled/08-visual-ui/FlexClassicDemo.mxml examples-compiled/08-visual-ui/FlexClassicDemo-component.js
python compile-mxml.py examples-compiled/08-visual-ui/FormApp.mxml examples-compiled/08-visual-ui/FormApp-component.js
python compile-mxml.py examples-compiled/08-visual-ui/QuizApp.mxml examples-compiled/08-visual-ui/QuizApp-component.js
python compile-mxml.py examples-compiled/08-visual-ui/TemperatureApp.mxml examples-compiled/08-visual-ui/TemperatureApp-component.js
python compile-mxml.py examples-compiled/08-visual-ui/TimerApp.mxml examples-compiled/08-visual-ui/TimerApp-component.js
python compile-mxml.py examples-compiled/08-visual-ui/TodoListApp.mxml examples-compiled/08-visual-ui/TodoListApp-component.js

echo
echo "✅ Recompilação concluída!"
