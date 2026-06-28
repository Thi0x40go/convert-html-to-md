# Regras de Conversão de Livros (HTML → Markdown)

Este repositório contém uma ferramenta automatizada para converter livros e artigos em HTML (raspados da O'Reilly e fontes similares) para Markdown otimizado para o Obsidian.

## Diretrizes para Agentes de IA

Sempre que trabalhar neste repositório, siga as regras abaixo:

### 1. Fluxo de Execução e Automação
- O processo é automatizado pelo script `run.sh`.
- **Origem (Input)**: Os arquivos HTML brutos são baixados em `/home/thiago/Downloads/` com o padrão de nome `Capítulo ｜ Livro (Timestamp).html`.
- **Pasta Temporária**: Os arquivos HTML correspondentes ao padrão são movidos para `livro/` no workspace para processamento temporário.
- **Destino (Output)**: O output final do Markdown (`.md`) e das pastas locais de `assets` deve ir diretamente para o vault do Obsidian em `/home/thiago/Obsidian/Livros/<Nome do Livro>/`.
- **Autoclean**: Arquivos HTML de origem devem ser removidos (`os.remove`) do diretório temporário após uma conversão bem-sucedida.

### 2. Lógica de Conversão (`convert.py`)
- **Filtro de Barra Lateral (Sidebar/Menu/TOC)**:
  - Ignorar tags `<article>` que tenham ancestrais do tipo `aside` ou `nav`.
  - Ignorar tags `<article>` sob elementos que contenham `sidebar`, `menu`, `toc` ou `tableofcontents` na classe ou ID (exceto se a classe/ID indicar estados como `open`, `toggle`, `show` ou `hide`).
  - **Decomposição pós-seleção**: Antes de converter o conteúdo do `<article>` principal, deve-se buscar e decompor (`tag.decompose()`) de forma recursiva qualquer subelemento que corresponda aos critérios de sidebar acima para evitar que menus e Tabelas de Conteúdo aninhados poluam o markdown final.
- **Assets e Imagens**:
  - Salvar as imagens codificadas em base64 localmente dentro da pasta `assets/` do respectivo livro (ex: `Obsidian/Livros/<Nome do Livro>/assets/`).
  - **Nomenclatura Descritiva**: Remover todos os timestamps e nomear as imagens baseando-se no título limpo do capítulo seguindo o formato `{titulo-capitulo}-{index}.{extensao}`.
  - **Wikilinks**: Substituir referências de imagem no Markdown final para o formato wikilink do Obsidian: `![[assets/nome-imagem.png|Alt Text]]`.
