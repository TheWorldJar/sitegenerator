import os, re
from splitter import extract_title
from conversion import markdown_to_html_node
from htmlnode import LeafNode


def find_pages(content_path: str, template_path: str, dest_path: str, basepath: str):
    for dir in os.listdir(content_path):
        full_path = os.path.join(content_path, dir)
        if os.path.isfile(full_path) and dir.endswith(".md"):
            generate_page(
                full_path,
                template_path,
                dest_path
                + full_path.split(".md")[0].split("./content", 1)[1]
                + ".html",
                basepath,
            )
        elif os.path.isdir(full_path):
            find_pages(full_path, template_path, dest_path, basepath)
        else:
            raise Exception("Invalid file type found in the contents folder!")


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    if os.path.isfile(from_path):
        print(f"Generating page from {from_path} to {dest_path} using {template_path}")
        with open(from_path) as file:
            read_file = file.read()
        with open(template_path) as template:
            read_template = template.read()
        split_file = extract_title(read_file)
        html_body = markdown_to_html_node(split_file[1]).to_html()
        html_title = LeafNode("h1", split_file[0]).to_html()
        full_html = re.sub(
            r"\{\{\sTitle\s\}\}",
            re.sub(r"^\<h1\>", "", re.sub(r"\<\/h1\>", "", html_title)),
            re.sub(r"\{\{\sContent\s\}\}", html_title + html_body, read_template),
        )
        full_html = re.sub(r"href=\"\/", 'href="' + basepath, full_html)
        full_html = re.sub(r"src=\"\/", 'src="' + basepath, full_html)
        prepare_dest(dest_path)
        with open(dest_path, "w") as dest:
            dest.write(full_html)


def prepare_dest(dest_path: str):
    if not os.path.isdir(dest_path):
        print(f"Preparing destination directory {dest_path}")
        try:
            os.makedirs(os.path.dirname(dest_path))
        except FileExistsError:
            pass
