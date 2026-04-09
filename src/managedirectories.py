import os
import shutil

def copy_directory(src, dest):
    
    if not os.path.exists(src):
        raise Exception(f"Invalid source: {src}")
    else:
        src_path = os.path.abspath(src)
        print(f"Source found {src_path}")

    
    if os.path.exists(dest):
        shutil.rmtree(dest)       
        pass
    
    if not os.path.exists(dest):
        shutil.copytree(src_path, dest)   
