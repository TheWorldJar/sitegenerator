import os, re
from splitter import extract_title
from conversion import markdown_to_html_node
from htmlnode import LeafNode

def generate_page(from_path: str, template_path: str, dest_path: str):
    if os.path.isfile(from_path):
        print(f"Generating page from {from_path} to {dest_path} using {template_path}")
        with open(from_path) as file:
            read_file = file.read()
        with open(template_path) as template:
            read_template = template.read()
        split_file = extract_title(read_file)
        html_body = markdown_to_html_node(split_file[1]).to_html()
        html_title = LeafNode("h1", split_file[0]).to_html()
        full_html = re.sub(r"\{\{\sTitle\s\}\}", 
                           html_title, 
                           re.sub(r"\{\{\sContent\s\}\}", 
                                  html_body, 
                                  read_template)
                            )
        with open(dest_path, "w") as dest:
            dest.write(full_html)

