#!/usr/bin/env python3
"""
🚀 OpenFlex Examples - Quick Start Server
Levanta servidor HTTP automaticamente e abre o navegador
"""
import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

PORT = 8000
DIRECTORY = Path(__file__).parent

def main():
    print("=" * 60)
    print("🚀 OpenFlex Examples Server")
    print("=" * 60)
    print(f"📁 Diretório: {DIRECTORY}")
    print(f"🌐 Porta: {PORT}")
    print()
    
    # Mudar para o diretório dos exemplos
    os.chdir(DIRECTORY)
    
    # Configurar servidor HTTP
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}/index.html"
            
            print(f"✅ Servidor rodando em: {url}")
            print()
            print("📚 Categorias disponíveis:")
            print("   • 01-basics         - Conceitos fundamentais")
            print("   • 02-modern-js      - JavaScript moderno")
            print("   • 03-reactive       - Programação reativa")
            print("   • 06-advanced       - Recursos avançados")
            print("   • 07-real-apis      - Consumo de APIs públicas")
            print("   • 08-visual-ui      - Interfaces visuais")
            print()
            print("🌐 Abrindo navegador...")
            
            # Abrir navegador automaticamente
            try:
                webbrowser.open(url)
                print("✅ Navegador aberto!")
            except:
                print("⚠️  Não foi possível abrir o navegador automaticamente.")
                print(f"   Por favor, abra manualmente: {url}")
            
            print()
            print("=" * 60)
            print("Servidor rodando... Pressione Ctrl+C para parar")
            print("=" * 60)
            print()
            
            # Servir requisições
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print()
        print("=" * 60)
        print("👋 Servidor finalizado. Até logo!")
        print("=" * 60)
        sys.exit(0)
    except OSError as e:
        if e.errno == 98 or e.errno == 48:  # Address already in use
            print(f"❌ Erro: Porta {PORT} já está em uso!")
            print(f"   Tente fechar outros servidores ou use outra porta.")
        else:
            print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
