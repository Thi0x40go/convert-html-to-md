from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
import sys
import os

if len(sys.argv) < 2:
    print("Uso: python convert.py <arquivo_html_entrada>")
    sys.exit(1)

html_file = sys.argv[1]
md_file = os.path.splitext(os.path.basename(html_file))[0] + ".md"

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

with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# remover tags indesejadas
for tag in soup(["style", "script", "img"]):
    tag.decompose()

markdown = md_custom(str(soup))

with open(md_file, "w", encoding="utf-8") as f:
    f.write(markdown)

print(f"Markdown gerado em: {md_file}")
