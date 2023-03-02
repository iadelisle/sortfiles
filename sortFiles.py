import json
import glob
import tqdm
import os

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




if __name__ == "__main__":
    
    fileList = []


    path = "**/*.json"
    for file in glob.glob(path, recursive=True):
        fileList.append(file)

    with tqdm(total=len(fileList)) as pbar:
        with ThreadPoolExecutor(max_workers=os.cpu_count() - 2) as ex:
            futures = [ex.submit(sortFile, file) for file in fileList]
            for future in as_completed(futures):
                result = future.result()
                pbar.update(1)
