from os.path import exists
from pathlib import Path

from block_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.split("# ", 1)[1].strip()
    raise ValueError("No Title found")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not exists(from_path):
        raise FileNotFoundError
    with open(from_path, "r") as f:
        markdownContent = f.read()
    with open(template_path, "r") as f:
        templateContent = f.read()
    html = templateContent.replace(
        "{{ Title }}", extract_title(markdownContent)
    ).replace("{{ Content }}", markdown_to_html_node(markdownContent).to_html())
    Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html)
