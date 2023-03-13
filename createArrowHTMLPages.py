import json
import glob
import tqdm
import os
from json2html import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def sortFile(file):
    fObj = open(file)
    jsonDict = json.load(fObj)

    try:
        os.mkdir(str(jsonDict['_id']))
    except FileExistsError as e:
        True
    newpath = str(jsonDict['_id']) + '/' + os.path.basename(file)

    with open(newpath, 'w') as f:
        json.dump(jsonDict,f)

def createHTML(file):
    fObj = open(file)
    jsonDict = json.load(fObj)
    Func = open(str(file) + ".html", "w", encoding='utf-8')
    previous, nexts = pointerDict[str(file)] 
    previous = previous + '.html'
    nexts = nexts + ".html"
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .arrow-container {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 200px;
                margin: 0 auto;
            }}
            
            .prev-file, .next-file {{
                font-size: 24px;
                color: #000;
                text-decoration: none;
                margin: 0 10px;
            }}
            
            .prev-file:hover, .next-file:hover {{
                color: #555;
            }}
        </style>
    </head>
    <body>
        <div class="arrow-container">
            <a href="{previous}" class="prev-file">{previous}</a>
            <a href="{nexts}" class="next-file">{nexts}</a>
        </div>
    </body>
    </html>
    """

    rawHtml = json2html.convert(jsonDict)
    rawHtml = html_code + rawHtml

    Func.write(rawHtml)
    Func.close()

def isExtractedText(file):
    fObj = open(file)
    jsonDict = json.load(fObj)
    if 'extractedText' in jsonDict.keys():
        extractedTextFileList.append(file)
    else:
        pointerList.append(file)

if __name__ == "__main__":


        os.makedirs(path, exist_ok=True)


        os.mkdir('html', exist_ok = True)
        os.mkdirs('html\extractedText', exist_ok = True)
        os.mkdirs('html\regularFiles', exist_ok = True)

    fileList = []
    
    previous = ''
    nexts = ''
    pointerList = []
    extractedTextFileList = []

    fileList = []
    newDict = {}

    path = "**\\*.json"

    for file in glob.glob(path, recursive=True):
        fileList.append(file)

    # Serialize data into file:

    #create two lists, one with extracted text, one without
    with tqdm(total=len(fileList)) as pbar:
        with ThreadPoolExecutor(max_workers=os.cpu_count() - 2) as ex:
            futures = [ex.submit(isExtractedText, file) for file in fileList]
            for future in as_completed(futures):
                result = future.result()
                pbar.update(1)



    fileList = extractedTextFileList
    for i in range(len(fileList)):
        fileList[i] = 'html//extractedText//' + fileList[i]
    #create arrow pointers from extractedTextList
    for i in tqdm(range(len(fileList))):
        if (i > 0 and i < len(fileList)-2):
            newDict[fileList[i]] = (fileList[i-1], fileList[i+1])
        if i == 0:
            newDict[fileList[i]] = ('tableOfContents', fileList[i+1])
        if i == len(fileList) - 1:
            newDict[fileList[i]] = (fileList[i-1], 'tableOfContents')

    json.dump( newDict, open( "extractedTextFilePointers.json", 'w' ) )

    newDict = {} # reset dictionary

    # create non-extractedTextFileList
    fileList = pointerList
    for i in range(len(fileList)):
        fileList[i] = 'html//regularFiles//' + fileList[i]
    for i in tqdm(range(len(fileList))):
        if (i > 0 and i < len(fileList)-2):
            newDict[fileList[i]] = (fileList[i-1], fileList[i+1])
        if i == 0:
            newDict[fileList[i]] = ('tableOfContents', fileList[i+1])
        if i == len(fileList) - 1:
            newDict[fileList[i]] = (fileList[i-1], 'tableOfContents')

    json.dump(newDict, open( "regularPointerList.json", 'w' ) )

    # Create ExtractedPointer HTML Files
    pointerDict = json.load('extractedTextFilePointers.json')

    with tqdm(total=len(fileList)) as pbar:
        with ThreadPoolExecutor(max_workers=os.cpu_count() - 2) as ex:
            futures = [ex.submit(createHTML, file) for file in fileList]
            for future in as_completed(futures):
                result = future.result()
                pbar.update(1)
    # Create RegularPointerFiles 

    pointerDict = json.load('regularPointerList.json')
    with tqdm(total=len(fileList)) as pbar:
        with ThreadPoolExecutor(max_workers=os.cpu_count() - 2) as ex:
            futures = [ex.submit(createHTML, file) for file in fileList]
            for future in as_completed(futures):
                result = future.result()
                pbar.update(1)


        
