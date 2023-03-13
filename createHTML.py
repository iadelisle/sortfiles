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
    jsonDict = jsonDict[0]
    Func = open(str(file) + ".html", "w")
    previous, nexts = pointerDict[file]
    Func.write(json2html.convert(jsonDict))
    Func.close()




if __name__ == "__main__":
    fileList = []

previous = ''
nexts = ''

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
		<a href="#" class="prev-file">f{previous};</a>
		<a href="#" class="next-file">f{nexts};</a>
	</div>
</body>
</html>
"""



    path = "**\\*.json"
    for file in glob.glob(path, recursive=True):
        fileList.append(file)

    pointerDict = json.loads('pointerDict.json')



    with tqdm(total=len(fileList)) as pbar:
        with ThreadPoolExecutor(max_workers=os.cpu_count() - 2) as ex:
            futures = [ex.submit(createHTML, file) for file in fileList]
            for future in as_completed(futures):
                result = future.result()
                pbar.update(1)
