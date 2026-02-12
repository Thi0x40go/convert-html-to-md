from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
import sys
import os

# ---------- Validação ----------
if len(sys.argv) < 3:
    print("Uso: python convert.py <arquivo_ou_pasta_html> <pasta_saida_md>")
    sys.exit(1)

input_path = sys.argv[1]
output_dir = sys.argv[2]

os.makedirs(output_dir, exist_ok=True)

# ---------- Markdown Converter ----------
class NoTableConverter(MarkdownConverter):
    def convert_table(self, el, text, parent_tags=None):
        return str(el)

    def convert_tr(self, el, text, parent_tags=None):
        return str(el)

    def convert_td(self, el, text, parent_tags=None):
        return str(el)

    def convert_th(self, el, text, parent_tags=None):
        return str(el)

def md_custom(html):
    return NoTableConverter().convert(html)

# ---------- Função de conversão ----------
def convert_html_file(html_file):
    base_name = os.path.splitext(os.path.basename(html_file))[0]
    md_file = os.path.join(output_dir, base_name + ".md")

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # remover tags indesejadas
    for tag in soup(["style", "script", "img"]):
        tag.decompose()

    markdown = md_custom(str(soup))

    with open(md_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✔ Convertido: {html_file} → {md_file}")

# ---------- Processamento ----------
if os.path.isfile(input_path):
    convert_html_file(input_path)

elif os.path.isdir(input_path):
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith(".html"):
                convert_html_file(os.path.join(root, file))

else:
    print("❌ Caminho inválido")
    sys.exit(1)
