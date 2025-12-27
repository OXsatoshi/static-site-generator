from textnode import TextNode 
from htmlnode import HTMLNode
import os,shutil
from markdownparser import markdown_to_html_node
def extract_header_from_md(markdown):
    lines = markdown.split("\n")
    for line in lines:
        print(line)
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")
def extract_header_from_mds(markdown):
    markdown_lines = markdown.strip().splitlines()
    if len(markdown_lines) == 0:
        raise Exception("markdown file is empty")
    if markdown_lines[0].strip().count("#") != 1:
        raise Exception("must start with a header")
    return markdown_lines[0].strip("#").strip()
def copy_files_from(src,dst,list_of_files):
    if not os.path.exists(dst):
        os.mkdir(dst)
    else:
        shutil.rmtree(dst)
        os.mkdir(dst)
    for file in list_of_files:
        src_path = os.path.join(src,file)
        if os.path.isfile(src_path):
            shutil.copy(src_path,dst)
            continue
        inner_list = os.listdir(src_path)
        rel_dire = os.path.join(dst,file)
        if not os.path.exists(os.path.join(dst,file)):
            os.mkdir(os.path.join(dst,file))
        copy_files_from(src_path,rel_dire,inner_list)
def generate_page(from_path,template_path,dest_path):
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

    generated_file.write(replaced_content)
def generatesiii_paths_recursive(dir_path_content,template_path,des_dir_path):
    list_of_files = os.listdir(dir_path_content)
    for file in list_of_files:
        src_file_path = os.path.join(dir_path_content,file)
        if os.path.isfile(src_file_path):
            des_file_path = os.path.join(des_dir_path,file[-2:]+".html")
            generate_page(src_file_path,template_path,des_file_path)
            continue
        inner_list = os.listdir(src_file_path)
        des_file_path = os.path.join(des_dir_path,file)
        if not os.path.exists(des_file_path):
            os.mkdir(des_file_path)
        generate_paths_recursive(src_file_path,template_path,des_file_path)

def generate_paths_recursive(dir_path_content, template_path, dest_dir_path):
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
                generate_page(from_path, template_path, dest_path)
        else:
            # It's a directory! 
            # 1. Create the corresponding directory in the destination
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            
            # 2. Recurse into the subdirectory
            generate_paths_recursive(from_path, template_path, dest_path)
def main():

    copy_files_from("/home/nabil/Desktop/repos/static-site-generator/static/",
                    "/home/nabil/Desktop/repos/static-site-generator/public/",os.listdir("static"))
    generate_paths_recursive("content/","template.html","public/")

main()
