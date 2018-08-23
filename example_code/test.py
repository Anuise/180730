import os
import sys

fileList = []
fileSize = 0
folderCount = 0
rootdir = '/home/au/example_code/image'

for root, subFolders, files in os.walk(rootdir):
    folderCount += len(subFolders)
    for file in files:
        f = os.path.join(root,file)
        fileSize = fileSize + os.path.getsize(f)
        fileList.append(f)

print('Total Files', type(len(fileList)))

