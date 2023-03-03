import json
import glob
import tqdm
import os
from json2html import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


if __name__ == "__main__":
    fileList = []
    newDict = {}

    path = "**\\*.html"
    for file in glob.glob(path, recursive=True):
        fileList.append(file)

    toc_html = '<!DOCTYPE html>\n<html>\n<head>\n\t<title>Table of Contents</title>\n</head>\n<body>\n\t<h1>Table of Contents</h1>\n\t<ul>\n'

    for file_path in tqdm(fileList):
        filename = file_path.split("\\")[-1]
        toc_html += f'\t\t<li><a href="{filename}">{filename}</a></li>\n'

    toc_html += '\t</ul>\n</body>\n</html>'

    with open("tableOfContents.html", "w", encoding="utf-8") as f:
        f.write(toc_html)

