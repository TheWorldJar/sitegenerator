import os, shutil

PUBLIC = "./public"
STATIC = "./static"

def clear_public():
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.mkdir(PUBLIC)

def find_statics(path: str) -> list[str]:
    files = []
    if os.path.exists(path):
        dirs = os.listdir(path)
        for file in dirs:
            if file == ".DS_Store":
                pass
            elif os.path.isdir(os.path.join(path, file)):
                files.extend(find_statics(os.path.join(path, file)))
            else:
                files.append(os.path.join(path, file))
    return files

def copy_statics(statics: list[str]):
    for file in statics:
        dst_path = PUBLIC + file.split(STATIC, 1)[1]
        shutil.copy(file, dst_path)

def prepare_dir_tree(statics: list[str]):
    for file in statics:
        new_path = os.path.dirname(file)
        os.mkdir(PUBLIC + new_path.split(STATIC, 1)[1])

def copy_static_to_public():
    clear_public()
    statics = find_statics(STATIC)
    prepare_dir_tree(statics)
    copy_statics(statics)