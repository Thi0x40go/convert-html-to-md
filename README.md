# HTML to Markdown Book Converter

Esta é uma ferramenta automatizada para converter capítulos de livros salvos em formato HTML para Markdown (.md) estruturado e otimizado para visualização no Obsidian.

## Características

- **Filtro de Ruído (Sidebar & TOC)**: Identifica e remove menus laterais, botões de navegação e tabelas de conteúdo repetidas para manter apenas o texto real do livro.
- **Assets Organizados localmente**: Salva imagens base64 de cada capítulo em uma pasta local `assets/` dentro do próprio diretório do livro correspondente.
- **Imagens Descritivas**: Renomeia as imagens usando o título do capítulo (ex: `1. Introdução-1.png`) em vez de timestamps indecifráveis.
- **Wikilinks Obsidian**: Converte links de imagens para a sintaxe do Obsidian `![[assets/imagem.png|Alt Text]]`.
- **Automação de Entrada e Saída**: O script move automaticamente os arquivos baixados da pasta `Downloads` para o processamento e envia o resultado diretamente para o seu Vault do Obsidian.

## Estrutura do Projeto

- `convert.py`: Script principal em Python que realiza a conversão de um arquivo HTML ou de uma pasta inteira.
- `run.sh`: Script em Bash de automação total que move os HTMLs da pasta `Downloads` e inicia a conversão.
- `livro/`: Diretório temporário utilizado como área de trabalho (stage) para o processamento dos HTMLs.

## Pré-requisitos

Esta ferramenta utiliza o Python 3.x e o gerenciador de dependências **Poetry**.

Instale as dependências executando:
```bash
poetry install
```

## Como Usar

### Execução Automatizada (Recomendado)

Sempre que você baixar capítulos/livros na sua pasta de Downloads com o formato de nome padrão contendo pipe (`|` ou `｜`), basta executar o script de automação na raiz do repositório:

```bash
./run.sh
```

Este script irá:
1. Buscar arquivos `*.html` contendo `|` ou `｜` em `~/Downloads`.
2. Mover esses arquivos para a pasta temporária `livro/`.
3. Executar o `convert.py` enviando os arquivos `.md` e `assets/` diretamente para o seu Vault em `~/Obsidian/Livros/`.
4. Deletar os HTMLs temporários após a conversão bem-sucedida.

### Execução Manual do Python

Caso queira fazer uma conversão manual personalizada, você pode rodar o `convert.py` diretamente:

```bash
poetry run python convert.py <caminho_entrada_html_ou_pasta> <caminho_saida_md>
```