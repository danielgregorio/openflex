#!/bin/bash

# Criar HTMLs de teste para cada exemplo

create_test_html() {
    local APP_NAME=$1
    local TITLE=$2
    local ICON=$3
    
    cat > "${APP_NAME,,}-test.html" <<EOF
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>$TITLE - OpenFlex Neo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            overflow-x: hidden;
        }
    </style>
</head>
<body>
    <app-root></app-root>
    
    <script src="../runtime/openflex-runtime-browser.js"></script>
    <script src="${APP_NAME}-component.js"></script>
    <script>console.log('✅ $TITLE loaded!');</script>
</body>
</html>
EOF
    echo "Created ${APP_NAME,,}-test.html"
}

cd /home/user/openflex/examples-compiled/08-visual-ui

create_test_html "CalculatorApp" "Calculadora" "🧮"
create_test_html "TimerApp" "Cronômetro" "⏱️"
create_test_html "TemperatureApp" "Conversor de Temperatura" "🌡️"
create_test_html "QuizApp" "Quiz Interativo" "🎯"
create_test_html "DashboardApp" "Dashboard" "📊"
create_test_html "ColorPickerApp" "Color Picker" "🎨"
create_test_html "FormApp" "Formulário" "📝"

echo "All test HTMLs created!"
