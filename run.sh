#!/bin/bash

# Define directories
DOWNLOADS_DIR="/home/thiago/Downloads"
WORKSPACE_LIVRO_DIR="/home/thiago/Dev/convert-html-to-md/livro"
OBSIDIAN_LIVRO_DIR="/home/thiago/Obsidian/Livros"
SCRIPT_DIR="/home/thiago/Dev/convert-html-to-md"

echo "=========================================="
echo "Iniciando processo de conversão de livros"
echo "=========================================="

# 1. Move HTML files from Downloads to the workspace libro folder
echo "1. Movendo arquivos HTML de $DOWNLOADS_DIR para a pasta temporária..."
python3 -c "
import os, shutil
downloads = '$DOWNLOADS_DIR'
livro = '$WORKSPACE_LIVRO_DIR'
os.makedirs(livro, exist_ok=True)
count = 0
for f in os.listdir(downloads):
    if f.lower().endswith('.html') and ('|' in f or '｜' in f):
        shutil.move(os.path.join(downloads, f), os.path.join(livro, f))
        print(f'  -> Movido: {f}')
        count += 1
print(f'Concluído: {count} arquivos movidos.')
"

# 2. Run the conversion script (input is workspace libro dir, output is Obsidian Livros dir)
echo "2. Executando script de conversão..."
cd "$SCRIPT_DIR"
poetry run python convert.py "$WORKSPACE_LIVRO_DIR" "$OBSIDIAN_LIVRO_DIR"

echo "=========================================="
echo "Processo concluído com sucesso!"
echo "=========================================="
