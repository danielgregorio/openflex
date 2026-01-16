#!/usr/bin/env python3
"""
Adiciona o Flex Classic Theme CSS a todos os exemplos HTML
"""

import os
import re
from pathlib import Path

def add_flex_theme_to_html(html_path):
    """Adiciona link para o tema Flex Classic CSS"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar se já tem o tema
    if 'neo-flex-classic-theme.css' in content:
        print(f"  ⏭️  Já tem tema: {html_path}")
        return False

    # Calcular caminho relativo para runtime
    depth = len(Path(html_path).relative_to('examples-compiled').parts) - 1
    runtime_path = '../' * depth + 'runtime'

    # Procurar pelo </head> e adicionar link para CSS antes dele
    theme_link = f'    <link rel="stylesheet" href="{runtime_path}/neo-flex-classic-theme.css">\n</head>'

    if '</head>' in content:
        new_content = content.replace('</head>', theme_link)

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✅ Tema adicionado: {html_path}")
        return True
    else:
        print(f"  ⚠️  Sem tag </head>: {html_path}")
        return False


def main():
    print("🎨 Adicionando Flex Classic Theme a todos os exemplos\n")

    # Encontrar todos os HTMLs em 08-visual-ui
    html_files = []
    for file in Path('examples-compiled/08-visual-ui').glob('*.html'):
        if file.name not in ['index.html', 'test-viewer.html']:
            html_files.append(str(file))

    # Adicionar também 09-data-components
    for file in Path('examples-compiled/09-data-components').glob('*.html'):
        if file.name != 'index.html':
            html_files.append(str(file))

    print(f"📁 Encontrados {len(html_files)} arquivos HTML\n")

    added = 0
    skipped = 0

    for html_file in sorted(html_files):
        if add_flex_theme_to_html(html_file):
            added += 1
        else:
            skipped += 1

    print(f"\n✅ Concluído!")
    print(f"   Adicionados: {added}")
    print(f"   Já existiam: {skipped}")
    print(f"   Total: {len(html_files)}")


if __name__ == '__main__':
    main()
