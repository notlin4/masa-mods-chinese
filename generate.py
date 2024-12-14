import json
import os
import shutil
import subprocess
from typing import Optional
import zipfile

version: Optional[str] = None

def create_resource_pack():
    file_list = [
        'itemscroller.json',
        'litematica.json',
        'malilib.json',
        'minihud.json',
        'syncmatica.json',
        'tweakeroo.json',
        'litematica-printer.json',
    ]
    def write_file(language):
        in_file = os.path.join('masa-mods-chinese', language, file)
        out_file = os.path.join('assets', file.split('.')[0], 'lang', language + '.json')
        with open(in_file, 'r', encoding='utf-8') as f:
            in_file = json.load(f)
        output_dir = os.path.dirname(out_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = open(out_file, 'w', encoding='utf-8')
        output_file.write(json.dumps(in_file, ensure_ascii=False, indent=4))
        output_file.close()

    for file in file_list:
        write_file('zh_cn')
        write_file('zh_tw')
        
        

def rename_mcmeta():
    def get_git_tags():
        try:
            result = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True, check=True)
            tag = result.stdout.splitlines()
            return tag
        except subprocess.CalledProcessError as e:
            print(f"Error while running git command: {e}")
            return []

    tag = get_git_tags()

    with open('pack.mcmeta', 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    data['pack']['pack_format'] = 46
    data['pack']['supported_formats'] = [ 34, 46 ]
    data['pack']['description'] = '§e[1.21]MASA全家桶汉化包' + '-' + tag[0]

    with open('pack.mcmeta', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def zip_files():
    def zip_files_and_folders(zip_filename, items_to_zip):
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in items_to_zip:
                if os.path.isdir(item):
                    for root, dirs, files in os.walk(item):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, os.path.dirname(item))
                            zipf.write(file_path, arcname)
                else:
                    zipf.write(item, os.path.basename(item))
    items_to_zip = [
        'assets',
        'pack.mcmeta',
        'pack.png',
    ]
    zip_filename = './masa-mods-chinese.zip'
    zip_files_and_folders(zip_filename, items_to_zip)

def delete_files():
    shutil.rmtree('./assets')



create_resource_pack()
rename_mcmeta()
zip_files()
delete_files()
print('Done!')


