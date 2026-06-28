from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
import sys
import os
import base64
import re

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
    return NoTableConverter(heading_style='atx', bullets='-').convert(html)

# ------------------ Helper Functions ------------------
def sanitize_filename(name):
    # Remove standard invalid characters for filesystems: \ / : * ? " < > |
    sanitized = re.sub(r'[\\/:*?"<>|]', '', name)
    sanitized = re.sub(r'\s+', ' ', sanitized)
    return sanitized.strip()

def is_inside_sidebar(tag):
    for parent in tag.parents:
        if parent.name in ['aside', 'nav']:
            return True
        parent_id = parent.get('id', '')
        if not isinstance(parent_id, str):
            parent_id = ''
            
        pid_lower = parent_id.lower()
        if any(w in pid_lower for w in ['sidebar', 'menu', 'toc', 'tableofcontents']):
            if not any(x in pid_lower for x in ['open', 'toggle', 'show', 'hide']):
                return True
                
        parent_classes = parent.get('class', [])
        if isinstance(parent_classes, list):
            for cls in parent_classes:
                cls_lower = str(cls).lower()
                if any(w in cls_lower for w in ['sidebar', 'menu', 'toc', 'tableofcontents']):
                    if not any(x in cls_lower for x in ['open', 'toggle', 'show', 'hide']):
                        return True
        elif isinstance(parent_classes, str):
            cls_lower = parent_classes.lower()
            if any(w in cls_lower for w in ['sidebar', 'menu', 'toc', 'tableofcontents']):
                if not any(x in cls_lower for x in ['open', 'toggle', 'show', 'hide']):
                    return True
    return False

def remove_sidebars(soup):
    # Find all aside, nav tags
    for tag in soup.find_all(['aside', 'nav']):
        tag.decompose()
        
    # Find all divs, sections, etc. that are sidebars
    for tag in soup.find_all(True):
        if not tag.name:
            continue
        try:
            # Check if tag is already decomposed
            if tag.parent is None and tag.name != '[document]':
                continue
        except:
            continue
            
        tag_id = tag.get('id', '')
        if isinstance(tag_id, list):
            tag_id = ' '.join(tag_id)
        elif not tag_id:
            tag_id = ''
            
        pid_lower = tag_id.lower()
        if any(w in pid_lower for w in ['sidebar', 'menu', 'toc', 'tableofcontents']):
            if not any(x in pid_lower for x in ['open', 'toggle', 'show', 'hide']):
                tag.decompose()
                continue
                
        tag_classes = tag.get('class', [])
        if isinstance(tag_classes, list):
            is_sidebar = False
            for cls in tag_classes:
                cls_lower = str(cls).lower()
                if any(w in cls_lower for w in ['sidebar', 'menu', 'toc', 'tableofcontents']):
                    if not any(x in cls_lower for x in ['open', 'toggle', 'show', 'hide']):
                        is_sidebar = True
                        break
            if is_sidebar:
                tag.decompose()
        elif isinstance(tag_classes, str):
            cls_lower = tag_classes.lower()
            if any(w in cls_lower for w in ['sidebar', 'menu', 'toc', 'tableofcontents']):
                if not any(x in cls_lower for x in ['open', 'toggle', 'show', 'hide']):
                    tag.decompose()

# ------------------ Base64 Image Handler ------------------
def save_base64_image(data_uri, index, chapter_name, local_assets_dir):
    match = re.match(
        r'data:image/([^;]+);base64,(.+)',
        data_uri,
        re.DOTALL
    )
    if not match:
        return None

    mime_subtype, data = match.groups()
    ext_map = {
        'jpeg': 'jpg',
        'png': 'png',
        'gif': 'gif',
        'svg+xml': 'svg',
        'webp': 'webp',
        'bmp': 'bmp',
        'x-icon': 'ico'
    }
    ext = ext_map.get(mime_subtype.lower(), mime_subtype.lower())
    ext = re.sub(r'[^a-zA-Z0-9]', '', ext)
    if not ext:
        ext = 'png'
        
    clean_chapter = sanitize_filename(chapter_name)
    filename = f"{clean_chapter}-{index}.{ext}"
    filepath = os.path.join(local_assets_dir, filename)

    with open(filepath, "wb") as f:
        f.write(base64.b64decode(data))

    return filename

# ------------------ HTML → MD ------------------
def convert_html_file(html_file, md_file, chapter_name, local_assets_dir):
    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["style", "script"]):
        tag.decompose()

    # Extract articles that are not inside a sidebar
    articles = soup.find_all("article")
    if articles:
        non_sidebar_articles = [art for art in articles if not is_inside_sidebar(art)]
        if non_sidebar_articles:
            content_soup = BeautifulSoup("".join(str(art) for art in non_sidebar_articles), "html.parser")
        else:
            content_soup = soup
    else:
        content_soup = soup

    # Decompose any sidebar/TOC elements nested inside the content
    remove_sidebars(content_soup)

    img_index = 1
    
    # Create the local assets directory if needed
    os.makedirs(local_assets_dir, exist_ok=True)

    # Process base64 images in our content scope
    for img in content_soup.find_all("img"):
        src = img.get("src", "")

        if src.startswith("data:image"):
            new_src = save_base64_image(src, img_index, chapter_name, local_assets_dir)
            if new_src:
                img["src"] = f"assets/{new_src}"
                img_index += 1
            else:
                img.decompose()
        else:
            img.decompose()

    markdown = md_custom(str(content_soup))

    # Convert local image links to Obsidian wikilinks, preserving alt text if present
    def replace_image_link(match):
        alt = match.group(1)
        src = match.group(2)
        if "://" in src:
            return match.group(0) # Keep external images as standard markdown links
        
        if alt:
            return f"![[{src}|{alt}]]"
        else:
            return f"![[{src}]]"

    markdown = re.sub(
        r'!\[(.*?)\]\((.*?)\)',
        replace_image_link,
        markdown
    )

    with open(md_file, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✔ Converted: {os.path.basename(html_file)}")
    print(f"  → {os.path.relpath(md_file, os.path.dirname(os.path.dirname(md_file)))}")

# ------------------ Parsing Filename Suffix ------------------
def parse_book_info(filename):
    base = os.path.splitext(filename)[0]
    parts = re.split(r'[|｜]', base)
    if len(parts) < 2:
        return None
    
    chapter_part = parts[0].strip()
    book_part = parts[-1].strip()
    
    # Remove timestamp suffix like (21_06_2026 00:21:56)
    clean_book = re.sub(r'\s*\(\d{2}_\d{2}_\d{4}\s+\d{2}[:：]\d{2}[:：]\d{2}\)\s*$', '', book_part)
    
    return {
        "chapter": sanitize_filename(chapter_part),
        "book": sanitize_filename(clean_book)
    }

# ------------------ Runner ------------------
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python convert.py <arquivo_ou_pasta_html> <pasta_saida_md>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2]

    os.makedirs(output_dir, exist_ok=True)

    if os.path.isfile(input_path):
        filename = os.path.basename(input_path)
        info = parse_book_info(filename)
        if info:
            book_dir = os.path.join(output_dir, info["book"])
            md_file = os.path.join(book_dir, info["chapter"] + ".md")
            local_assets_dir = os.path.join(book_dir, "assets")
            convert_html_file(input_path, md_file, info["chapter"], local_assets_dir)
        else:
            # Fallback if filename structure is not standard
            base_name = os.path.splitext(filename)[0]
            md_file = os.path.join(output_dir, base_name + ".md")
            local_assets_dir = os.path.join(output_dir, "assets")
            convert_html_file(input_path, md_file, base_name, local_assets_dir)

    elif os.path.isdir(input_path):
        # We only process files direct in input_path to avoid processing output directories
        # if input_path and output_dir overlap
        for file in os.listdir(input_path):
            if file.lower().endswith(".html"):
                html_file = os.path.join(input_path, file)
                info = parse_book_info(file)
                if info:
                    book_dir = os.path.join(output_dir, info["book"])
                    md_file = os.path.join(book_dir, info["chapter"] + ".md")
                    local_assets_dir = os.path.join(book_dir, "assets")
                    
                    try:
                        convert_html_file(html_file, md_file, info["chapter"], local_assets_dir)
                        # Remove source HTML after successful conversion
                        os.remove(html_file)
                    except Exception as e:
                        print(f"❌ Error converting {file}: {e}")
                else:
                    print(f"⚠ Skipping {file} (does not match expected name pattern with pipe)")
    else:
        print("❌ Caminho inválido")
