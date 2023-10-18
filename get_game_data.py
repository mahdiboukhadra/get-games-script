import os
import json
import shutil
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = "game"

def copy_and_overwrite(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)

def find_game_paths(src):
    game_paths = []

    for root, dirs, files in os.walk(src):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(src, directory)
                game_paths.append(path)
        break
    return game_paths


def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)
    return new_names


def create_dir(tgt):
    if not os.path.exists(tgt):
        os.mkdir(tgt)


def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberOfGames": len(game_dirs)
    }

    with open(path, "w") as f:
        json.dump(data, f)

def main(src, tgt):
    cwd = os.getcwd()
    src_path = os.path.join(cwd, src)
    tgt_path = os.path.join(cwd, tgt)

    game_paths = find_game_paths(src_path)
    
    create_dir(tgt_path)

    new_game_dirs = get_name_from_paths(game_paths, "_game")

    for src, dest in zip(game_paths, new_game_dirs):
        des_path = os.path.join(tgt_path, dest)
        copy_and_overwrite(src, des_path)
    
 

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        raise Exception("you must pass a source and a target dir only.")
    
    src, tgt = args[1:]
    main(src, tgt)