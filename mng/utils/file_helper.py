import os


def cp(source_file, target_file):
    open(target_file, "wb").write(open(source_file, "rb").read())

def safe_rm(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print('no file' + path)

if __name__ == '__main__':
    cp('file_helper.py', 'pythonfile')
    safe_rm('pythonfile')