import sys
from filemanip import copy_static_to_public
from page import find_pages


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_static_to_public()
    find_pages("./content", "template.html", "./public", basepath)


if __name__ == "__main__":
    main()
