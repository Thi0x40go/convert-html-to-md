# Índice do Conversor HTML → Markdown

Este arquivo serve como um índice rápido de arquivos e instruções de uso do conversor.

## 📁 Estrutura de Arquivos Principais

- [README.md](file:///home/thiago/Dev/convert-html-to-md/README.md): Documentação completa de uso do projeto e pré-requisitos.
- [convert.py](file:///home/thiago/Dev/convert-html-to-md/convert.py): Script de conversão principal com a lógica do BeautifulSoup, filtros de sidebar e wikilinks.
- [run.sh](file:///home/thiago/Dev/convert-html-to-md/run.sh): Shell script executável para automatizar o fluxo Downloads → Conversão → Obsidian.
- [.agents/AGENTS.md](file:///home/thiago/Dev/convert-html-to-md/.agents/AGENTS.md): Regras de comportamento e especificações técnicas para futuros Agentes de IA que trabalharem neste projeto.

## 🚀 Como Rodar o Fluxo Completo

Para converter automaticamente todos os livros novos em sua pasta de downloads e movê-los diretamente para o Obsidian, abra seu terminal neste diretório e execute:

```bash
./run.sh
```

## 🛠️ Configurações Importantes

Caso você mude o caminho das pastas no futuro, edite as seguintes variáveis no início do [run.sh](file:///home/thiago/Dev/convert-html-to-md/run.sh):

- `DOWNLOADS_DIR`: Pasta onde você baixa os arquivos HTML brutos.
- `WORKSPACE_LIVRO_DIR`: Pasta temporária onde o script processa os arquivos.
- `OBSIDIAN_LIVRO_DIR`: Pasta destino no seu vault do Obsidian (atualmente setado para `~/Obsidian/Livros`).
