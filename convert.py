from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
import sys
import os
import base64
import re
import time

# ------------------ Args ------------------
if len(sys.argv) < 3:
    print("Uso: python convert.py <arquivo_ou_pasta_html> <pasta_saida_md>")
    sys.exit(1)

input_path = sys.argv[1]
output_dir = sys.argv[2]
assets_dir = os.path.join(output_dir, "assets")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(assets_dir, exist_ok=True)

# ------------------ Markdown Converter ------------------
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

# ------------------ Base64 Image Handler ------------------
def save_base64_image(data_uri, index, run_ts):
    match = re.match(
        r'data:image/([^;]+);base64,(.+)',
        data_uri,
        re.DOTALL
    )
    if not match:
        return None

    ext, data = match.groups()
    filename = f"img-{run_ts}-{index}.{ext}"
    filepath = os.path.join(assets_dir, filename)

    with open(filepath, "wb") as f:
        f.write(base64.b64decode(data))

    return filename  # só o nome (Obsidian)

# ------------------ HTML → MD ------------------
def convert_html_file(html_file):
    base_name = os.path.splitext(os.path.basename(html_file))[0]
    md_file = os.path.join(output_dir, base_name + ".md")

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["style", "script"]):
        tag.decompose()

    img_index = 1
    run_ts = int(time.time() * 1000)  # timestamp por arquivo

    for img in soup.find_all("img"):
        src = img.get("src", "")

        if src.startswith("data:image"):
            new_src = save_base64_image(src, img_index, run_ts)
            if new_src:
                img["src"] = new_src
                img_index += 1
            else:
                img.decompose()
        else:
            img.decompose()

    markdown = md_custom(str(soup))

    markdown = re.sub(
        r'!\[\]\(([^)]+)\)',
        r'![[\1]]',
        markdown
    )

    with open(md_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✔ Convertido: {html_file}")
    print(f"  → {md_file}")

# ------------------ Runner ------------------
if os.path.isfile(input_path):
    convert_html_file(input_path)

elif os.path.isdir(input_path):
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith(".html"):
                convert_html_file(os.path.join(root, file))
else:
    print("❌ Caminho inválido")
