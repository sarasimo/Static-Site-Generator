from markdown_to_html import markdown_to_title_and_content
import os

def generate_page(md_path, template_path, dest_path, basepath="/"):
    try:
        print(f"generating page from {md_path} to {dest_path}, using {template_path}")
        md_file = open(md_path)
        markdown = md_file.read()
        title, content = markdown_to_title_and_content(markdown)

        tmp_file = open(template_path)
        template = tmp_file.read()

        html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
        html_page = html_page.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
        par_dir = os.path.dirname(dest_path)
        os.makedirs(par_dir, exist_ok=True)
        with open(dest_path, "w") as file:
            file.write(html_page)

    except Exception as e:
        print(e)


def generate_all_pages(src_directory, template_path, dest_directory, basepath="/"):
    
    md_dir_list = os.listdir(src_directory)
    for entry in md_dir_list:
        print(entry)
        src_path = os.path.normpath(os.path.join(src_directory, entry))       
        
        if os.path.isdir(src_path):
            print("Directory found!")
            dest_path = os.path.normpath(os.path.join(dest_directory, entry))
            generate_all_pages(src_path, template_path, dest_path, basepath)           
            
        if os.path.isfile(src_path):
            dest_path = os.path.normpath(os.path.join(dest_directory, "index.html"))
            print(f"Src: {src_path}\n des: {dest_path}")
            generate_page(src_path, template_path, dest_path, basepath)
