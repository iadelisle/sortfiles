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

    path = "**\\*.json"
    for file in glob.glob(path, recursive=True):
        fileList.append(file)

    for i in tqdm(range(len(fileList))):
        if (i > 0 and i < len(fileList)-2):
            newDict[fileList[i]] = (fileList[i-1], fileList[i+1])
        if i == 0:
            newDict[fileList[i]] = ('tableOfContents', fileList[i+1])
        if i == len(fileList):
            newDict[fileList[i]] = (fileList[i-1], 'tableOfContents')

    import json

    # Serialize data into file:
    json.dump( newDict, open( "pointerDict.json", 'w' ) )
