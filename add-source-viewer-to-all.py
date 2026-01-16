#!/usr/bin/env python3
"""
Adiciona MXML Source Viewer a todos os exemplos HTML
"""

import os
import re
from pathlib import Path

def add_source_viewer_to_html(html_path):
    """Adiciona o script do source viewer a um arquivo HTML"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar se já tem o source viewer
    if 'mxml-source-viewer.js' in content:
        print(f"  ⏭️  Já tem source viewer: {html_path}")
        return False

    # Encontrar o nome do arquivo MXML correspondente
    html_name = Path(html_path).stem

    # Tentar diferentes padrões de nome MXML
    mxml_patterns = [
        html_name.replace('-test', '') + '.mxml',
        html_name.replace('-', '') + '.mxml',
        ''.join(word.capitalize() for word in html_name.split('-')) + '.mxml',
        html_name.title().replace('-', '') + 'App.mxml',
    ]

    # Detectar qual arquivo MXML existe no mesmo diretório
    html_dir = Path(html_path).parent
    mxml_file = None
    for pattern in mxml_patterns:
        potential_mxml = html_dir / pattern
        if potential_mxml.exists():
            mxml_file = pattern
            break

    # Se não encontrou MXML, usar nome baseado em heurística
    if not mxml_file:
        # Extrair nome do componente JS se existir
        js_match = re.search(r'<script src="([^"]+component\.js)"', content)
        if js_match:
            js_file = js_match.group(1)
            mxml_file = js_file.replace('-component.js', '.mxml')
        else:
            # Fallback: usar nome do HTML
            mxml_file = html_name.replace('-test', '').replace('-', '') + '.mxml'

    # Calcular caminho relativo para runtime
    depth = len(Path(html_path).relative_to('examples-compiled').parts) - 1
    runtime_path = '../' * depth + 'runtime'

    # Adicionar script antes do </body>
    viewer_script = f'''
    <script src="{runtime_path}/mxml-source-viewer.js"></script>

    <script>
        // Inicializar viewer de source code MXML
        document.addEventListener('DOMContentLoaded', () => {{
            if (typeof MXMLSourceViewer !== 'undefined') {{
                window.mxmlSourceViewer = new MXMLSourceViewer();
                window.mxmlSourceViewer.init('{mxml_file}');
            }}
        }});
    </script>
</body>'''

    # Substituir </body> pelo novo conteúdo
    if '</body>' in content:
        new_content = content.replace('</body>', viewer_script)

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✅ Adicionado source viewer: {html_path} -> {mxml_file}")
        return True
    else:
        print(f"  ⚠️  Sem tag </body>: {html_path}")
        return False


def main():
    print("🚀 Adicionando MXML Source Viewer a todos os exemplos\n")

    # Encontrar todos os HTMLs em examples-compiled
    html_files = []
    for root, dirs, files in os.walk('examples-compiled'):
        for file in files:
            if file.endswith('.html') and file != 'index.html':
                html_files.append(os.path.join(root, file))

    print(f"📁 Encontrados {len(html_files)} arquivos HTML\n")

    added = 0
    skipped = 0

    for html_file in sorted(html_files):
        if add_source_viewer_to_html(html_file):
            added += 1
        else:
            skipped += 1

    print(f"\n✅ Concluído!")
    print(f"   Adicionados: {added}")
    print(f"   Já existiam: {skipped}")
    print(f"   Total: {len(html_files)}")


if __name__ == '__main__':
    main()
