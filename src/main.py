from textnode import TextNode 
from htmlnode import HTMLNode
import os,shutil
from markdownparser import markdown_to_html_node
def extract_header_from_md(markdown):
    markdown_lines = markdown.strip().splitlines()
    if len(markdown_lines) == 0:
        raise Exception("markdown file is empty")
    print(markdown_lines[0])
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
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        markdown_file = open(from_path,'r')
        template_file = open(template_path,'r')
        generated_file = open(dest_path,'w')
        markdown_content = markdown_file.read()
        template_content = template_file.read()
    except Exception as e:
        print(e)
    html_string = markdown_to_html_node(markdown_content).to_html()
    header = extract_header_from_md(markdown_content)
    replaced_header = template_content.replace("{{ Title }}",header)
    replaced_content = replaced_header.replace("{{ Content }}",html_string)
    print(html_string)

    generated_file.write(replaced_content)
    
def main():

    copy_files_from("/home/nabil/Desktop/repos/static-site-generator/static/",
                    "/home/nabil/Desktop/repos/static-site-generator/public/",os.listdir("static"))
    generate_page("content/index.md","template.html","public/index.html")

main()
