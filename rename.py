import os
import shutil
import subprocess

def get_git_tags():
    try:
        result = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True, check=True)
        tag = result.stdout.splitlines()
        return tag
    except subprocess.CalledProcessError as e:
        print(f"Error while running git command: {e}")
        return []

tag = get_git_tags()[0]

if os.path.exists('./masa-mods-chinese.zip'):
    file_path = './masa-mods-chinese.zip'
    shutil.move(file_path, './[1.21]MASA全家桶汉化包' + '-' + tag + '.zip')