#!/usr/bin/env python3
"""
Adiciona @import do Flex Classic Theme aos arquivos MXML
"""

import os
import re
from pathlib import Path

def add_theme_import_to_mxml(mxml_path):
    """Adiciona @import do tema dentro de <fx:Style>"""
    with open(mxml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar se já tem o import
    if 'neo-flex-classic-theme.css' in content:
        print(f"  ⏭️  Já tem import: {mxml_path}")
        return False

    # Calcular caminho relativo para runtime
    depth = len(Path(mxml_path).relative_to('examples-compiled').parts) - 1
    runtime_path = '../' * depth + 'runtime'

    # Procurar por <fx:Style> e adicionar @import logo após
    import_line = f"@import url('{runtime_path}/neo-flex-classic-theme.css');\n\n        "

    # Regex para encontrar <fx:Style> seguido de conteúdo
    pattern = r'(<fx:Style>\s*)'

    if re.search(pattern, content):
        new_content = re.sub(pattern, r'\1' + import_line, content, count=1)

        with open(mxml_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✅ Import adicionado: {mxml_path}")
        return True
    else:
        print(f"  ⚠️  Sem <fx:Style>: {mxml_path}")
        return False


def main():
    print("🎨 Adicionando @import do tema aos arquivos MXML\n")

    # Encontrar todos os MXMLs em 08-visual-ui
    mxml_files = []
    for file in Path('examples-compiled/08-visual-ui').glob('*.mxml'):
        mxml_files.append(str(file))

    print(f"📁 Encontrados {len(mxml_files)} arquivos MXML\n")

    added = 0
    skipped = 0

    for mxml_file in sorted(mxml_files):
        if add_theme_import_to_mxml(mxml_file):
            added += 1
        else:
            skipped += 1

    print(f"\n✅ Concluído!")
    print(f"   Adicionados: {added}")
    print(f"   Já existiam: {skipped}")
    print(f"   Total: {len(mxml_files)}")


if __name__ == '__main__':
    main()
