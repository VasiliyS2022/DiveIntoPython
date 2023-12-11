import argparse
import os
import logging
from collections import namedtuple
from pathlib import Path

MyInfo_ = namedtuple(
    "MyInfo_", ["obj_name", "extension", "is_catalog", "parent_catalog"])

def my_func(path_):
    results = []
    # Рекурсивно обходим директорию и все вложенные директории
    for dir_path, dir_names, file_names in os.walk(path_, topdown=True, onerror=None, followlinks=False):
        
        # добавляем информацию о директории
        obj_name = os.path.basename(dir_path)
        parent_catalog = os.path.dirname(dir_path)
        results.append(MyInfo_(obj_name, None, True, parent_catalog))
        # добавляем информацию о файлах
        for file in file_names:
            
            file_path = os.path.join(dir_path, file)
            parent_catalog = os.path.dirname(file_path)
            
            if "." in file:
                *file_name, file_extension = file.split(".")
                file_name = ".".join(file_name)
            else:
                file_name = file
                file_extension = None
                
            results.append(MyInfo_(file_name, file_extension, False, parent_catalog))

    return results
   
def create_log(path_):
    '''
    лог файл создается рядом с папкой к которой указан путь
    '''
    
    log_file_name=str(os.path.basename(path_)+".log")
    save_logpath = os.path.join(os.path.dirname(path_),log_file_name)
    
    logging.basicConfig(filename=save_logpath, filemode="w",
                    encoding="UTF-8", level=logging.INFO)
    my_logger = logging.getLogger(__name__)
    res = my_func(path_)
    for r in res:
        my_logger.info(r.__str__())
    
    

if __name__ == "__main__":
    '''
    PS  ???\homeworks\homework15> python task01.py "???\Homeworks\homework15\myfiles"
    '''
    parser = argparse.ArgumentParser(description="Собирать информацию о содержимом в виде объектов namedtuple.")
    parser.add_argument("folder", nargs="?", type=str, help="Указать путь к папке")

    args = parser.parse_args()

    if args.folder:
        create_log(args.folder)
    else:
        print("Путь к папке не был передан!")