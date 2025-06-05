import os
import shutil
from textnode import *

def main():
    os_copy("static", "public")


def os_copy(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    copy_data(src, dst)

def copy_data(src, dst):
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)

        if os.path.isfile(src_item):
            shutil.copy(src_item, dst_item)
            print(f"Copied File {dst_item}")
        elif os.path.isdir(src_item):
            os.mkdir(dst_item)
            print(f"Created directory: {dst_item}")
            copy_data(src_item, dst_item)





    




if __name__ == "__main__":

    main()