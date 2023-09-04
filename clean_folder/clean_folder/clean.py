import re
import shutil
from pathlib import Path
import sys

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")


TRANS = {}

jpeg_files = list()
png_files = list()
jpg_files = list()
svg_files = list()
gif_files = list()
bmp_files = list()
tif_files = list()
tiff_files = list()
txt_files = list()
docx_files = list()
doc_files = list()
pdf_files = list()
xlsx_files = list()
pptx_files = list()
folders = list()
archives = list()
mp3_files = list()
ogg_files = list()
wav_files = list()
amr_files = list()
avi_files = list()
mp4_files = list()
mov_files = list()
mkv_files = list()
others = list()
unknown = set()
extensions = set()


registered_extensions = dict(JPEG=jpeg_files, PNG=png_files, SVG=svg_files, GIF=gif_files, BMP=bmp_files, TIF=tif_files,
                             TIFF=tiff_files, JPG=jpg_files, TXT=txt_files, DOCX=docx_files, DOC=doc_files,
                             PDF=pdf_files, XLSX=xlsx_files, PPTX=pptx_files, ZIP=archives, GZ=archives, TAR=archives,
                             RAR=archives, MP3=mp3_files, OGG=ogg_files, WAV=wav_files, AMR=amr_files, AVI=avi_files,
                             MP4=mp4_files, MOV=mov_files, MKV=mkv_files)

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('JPEG', 'PNG', 'JPG', 'TXT', 'DOCX', 'OTHERS', 'ARCHIVE',
                                 'SVG', 'GIF', 'BMP', 'TIF', 'TIFF', 'DOC', 'PDF', 'XLSX', 'PPTX',
                                 'GZ', 'TAR', 'RAR', 'MP3', 'OGG', 'WAV', 'AMR', 'AVI', 'MP4', 'MOV', 'MKV'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)

def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder / normalize(path.name))


def handle_archive(path, root_folder, dist):

    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)


    new_name = normalize(path.name.replace('.zip', ''))

    new_name = normalize(path.name.replace('.gz', ''))

    new_name = normalize(path.name.replace('.rar', ''))

    new_name = normalize(path.name.replace('.tar', ''))

    archive_folder = root_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(path.resolve()))

    except FileNotFoundError:
        archive_folder.rmdir()
        return

    except shutil.ReadError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass


def main(folder_path):
    scan(folder_path)

    for file in jpeg_files:
        hande_file(file, folder_path, "images")

    for file in jpg_files:
        hande_file(file, folder_path, "images")

    for file in png_files:
        hande_file(file, folder_path, "images")

    for file in svg_files:
        hande_file(file, folder_path, "images")

    for file in gif_files:
        hande_file(file, folder_path, "images")

    for file in bmp_files:
        hande_file(file, folder_path, "images")

    for file in tif_files:
        hande_file(file, folder_path, "images")

    for file in tiff_files:
        hande_file(file, folder_path, "images")

    for file in txt_files:
        hande_file(file, folder_path, "documents")

    for file in docx_files:
        hande_file(file, folder_path, "documents")

    for file in doc_files:
        hande_file(file, folder_path, "documents")

    for file in pdf_files:
        hande_file(file, folder_path, "documents")

    for file in xlsx_files:
        hande_file(file, folder_path, "documents")

    for file in pptx_files:
        hande_file(file, folder_path, "documents")

    for file in mp3_files:
        hande_file(file, folder_path, "audio")

    for file in ogg_files:
        hande_file(file, folder_path, "audio")

    for file in wav_files:
        hande_file(file, folder_path, "audio")

    for file in amr_files:
        hande_file(file, folder_path, "audio")

    for file in avi_files:
        hande_file(file, folder_path, "video")

    for file in mp4_files:
        hande_file(file, folder_path, "video")

    for file in mov_files:
        hande_file(file, folder_path, "video")

    for file in mkv_files:
        hande_file(file, folder_path, "video")

    for file in others:
        hande_file(file, folder_path, "OTHERS")

    for file in archives:
        hande_file(file, folder_path, "archives")

    get_folder_objects(folder_path)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)

    main(arg.resolve())
    #comment