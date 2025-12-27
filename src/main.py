from textnode import TextNode 
from htmlnode import HTMLNode
import sys
import os,shutil
from markdownparser import markdown_to_html_node
def extract_header_from_md(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")
def generate_page(from_path,template_path,dest_path,base_url):
    try:
        markdown_file = open(from_path,'r')
        template_file = open(template_path,'r')
        generated_file = open(dest_path,'w')
        markdown_content = markdown_file.read()
        template_content = template_file.read()
    except Exception as e:
        print(e)
    html_string = markdown_to_html_node(markdown_content).to_html()
    print(from_path)
    header = extract_header_from_md(markdown_content)
    replaced_header = template_content.replace("{{ Title }}",header)
    replaced_content = replaced_header.replace("{{ Content }}",html_string)
    final_contetn = replaced_content.replace('href=/',f'href={base_url}').replace('src=/',f"src={base_url}")
    generated_file.write(final_contetn)
    
def generate_paths_recursive(dir_path_content, template_path, dest_dir_path,base_url):
    # Get all items in the current content directory
    list_of_files = os.listdir(dir_path_content)
    
    for filename in list_of_files:
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            # We only care about markdown files
            if filename.endswith(".md"):
                # Change extension from .md to .html
                # This replaces the last 3 characters (".md") with ".html"
                dest_path = dest_path[:-3] + ".html"
                
                print(f"Generating page: {from_path} -> {dest_path}")
                generate_page(from_path, template_path, dest_path,base_url)
        else:
            # It's a directory! 
            # 1. Create the corresponding directory in the destination
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            
            # 2. Recurse into the subdirectory
            generate_paths_recursive(from_path, template_path, dest_path,base_url)
def copy_files_from(source_dir_path, dest_dir_path):
    # We do NOT delete the folder here, because this function recurses.
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        to_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {to_path}")

        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            # It's a directory, so we recurse
            copy_files_from(from_path, to_path)
def main():
    base_url = "/"

    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    copy_files_from("/home/nabil/Desktop/repos/static-site-generator/static/",
                    "/home/nabil/Desktop/repos/static-site-generator/docs/")
    generate_paths_recursive("content/","template.html","docs/",base_url)

main()
