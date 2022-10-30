import argparse

import os
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument('--source', '-s', required=True, help='Source folder')
parser.add_argument('--output', '-o', default=os.getcwd() + r'\Sorted files', help='Output folder')
ARGS = vars(parser.parse_args())

SOURCE = ARGS.get('source')
OUTPUT = ARGS.get('output')


SOURCE_FOLDER = Path(SOURCE)
OUTPUT_FOLDER = Path(OUTPUT)

UA_ALPHA = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюяАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
ENG_TRANSLIT = ('a', 'b', 'v', 'g', 'g', 'd', 'e', 'ye', 'zh', 'z', 'y', 'i', 'yi', 'y', 'k',
                'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'kh', 'tc', 'ch', 'sh', 'sch', '`', 'yu', 'ya') * 2

TR = {ord(a): b for a, b in zip(UA_ALPHA, ENG_TRANSLIT)}
TR.update({ord(a.upper()): b[0].upper() + b[1:] for a, b in zip(UA_ALPHA, ENG_TRANSLIT)})

EXTENS = [('.JPEG', '.PNG', '.JPG', '.SVG'),
          ('.AVI', '.MP4', '.MOV', '.MKV'),
          ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'),
          ('.MP3', '.OGG', '.WAV', '.AMR'),
          ('.ZIP', '.TAR')]

CATEGORIES = {0: 'Images',
              1: 'Video',
              2: 'Documents',
              3: 'Audio',
              4: 'Unknown extensions',
              5: 'Archives',
              }
founded_ext = []
unknown_ext = []

history = {i: [] for i in CATEGORIES.values()}
history['Unknown'] = []


def normalize(file: Path) -> Path:
    """Rename files with latin latters, change all symbols except letters and digits to "_" """

    file_name = file.name.removesuffix(file.suffix)
    trans_file = file_name.translate(TR)
    new_file_name = ''.join(ch if ch.isalpha() or ch.isdigit() else '_' for ch in trans_file)
    return Path(str(file).removesuffix(file.name)) / (new_file_name + file.suffix)  # returns normalized path


def replace_file(file: Path) -> None:
    """Distribute files to relative categories."""

    ext = file.suffix
    new_path = normalize(OUTPUT_FOLDER)
    norm_file = normalize(file)
    os.rename(file, norm_file)

    if ext.upper() in EXTENS[4]:
        founded_ext.append(ext)
        new_path = new_path / 'Archives'
        new_path.mkdir(exist_ok=True, parents=True)
        try:
            shutil.unpack_archive(norm_file, new_path /
                                  (norm_file.name.replace(norm_file.suffix, '')))
            os.remove(norm_file)
        except:
            print('Fail to unpack', norm_file)

        history['Archives'].append(norm_file.name)

    elif ext.upper() not in ([el for tupple in EXTENS for el in tupple]):
        unknown_ext.append(ext)
        new_path = new_path / 'Unknown extensions'
        new_path.mkdir(exist_ok=True, parents=True)
        try:
            os.replace(norm_file, new_path / norm_file.name)
        except:
            print('Fail to replace', norm_file)
        history['Unknown'].append(norm_file.name)

    for i in range(len(EXTENS) - 1):
        if ext.upper() in EXTENS[i]:
            founded_ext.append(ext)
            new_path = new_path / CATEGORIES[i]
            new_path.mkdir(exist_ok=True, parents=True)
            try:
                os.replace(norm_file, new_path / norm_file.name)
            except:
                print('Fail to replace', norm_file)
            history[CATEGORIES[i]].append(norm_file.name)


def read_folder(path: Path) -> tuple:
    """Walk through directories and apply replace_file function to each file in it.  Returns dict with each file in
    it's category """

    for file in path.iterdir():
        if file.is_dir() and file not in CATEGORIES.values():
            read_folder(file)
        else:
            replace_file(file)
    return (history, founded_ext, unknown_ext)


def main():
    print(read_folder(SOURCE_FOLDER))

    # delete empty folders in source folder
    for el in os.listdir(SOURCE_FOLDER):
        print(el)
        if el not in list(CATEGORIES.values()):
            try:
                shutil.rmtree(SOURCE_FOLDER / el)
            except:
                print('Fail to delete', SOURCE_FOLDER / el)


if __name__ == '__main__':
    main()
