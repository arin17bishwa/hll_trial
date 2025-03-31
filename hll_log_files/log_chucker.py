import os
from typing import TextIO
import chardet
from pathlib import Path
def main():
    print(os.getcwd())
    for fp in get_file_pointers():
        for line in get_lines(fp):
            print(line)
            break

def get_file_pointers():
    print(os.getcwd())
    pwd, _, filenames=next(os.walk(os.path.dirname(__file__)))
    for filename in sorted(filenames):
        if not filename.endswith('.log'):
            continue
        full_path=os.path.join(pwd, filename)
        print(full_path)
        with open(full_path, encoding=get_encoding(full_path)) as fp:
            yield fp

def get_encoding(file_path:str)->str:
    with open(file_path, 'rb') as fp:
        raw_data=fp.read()
    encoding_data=chardet.detect(raw_data)
    return encoding_data['encoding']

def get_lines(fp:TextIO):
    for line in fp:
        yield line

def get_line_stream():
    print(f'__file__: {__file__}')
    for fp in get_file_pointers():
        for line in get_lines(fp):
            yield line

if __name__ == '__main__':
    main()