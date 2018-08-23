from os import listdir
from os.path import isfile, isdir, join
mypath = '/home/au/example_code/image'
files = listdir(mypath)

for f in files:
    fullpath = join(mypath, f)
    print (f)