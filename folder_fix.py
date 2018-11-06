from os import chdir, rename, removedirs, listdir
from os.path import join, exists, isdir
from shutil import rmtree

basepath = "C:\\Users\\M113455\\Desktop\\empty"

while listdir(basepath) != []:
    path = basepath
    j=0
    while True:
        if exists(join(basepath,str(j))):
            j += 1
        else:
            for i in range(1,10):
                dr = listdir(path)
                for i in dr:
                    if isdir(join(path,i)):
                        path = join(path,i)
                        print(path)
            if path == join(basepath, str(j-1)):
                break
            rename(path, join(basepath, str(j)))
            path = join(basepath, str(j))
            j += 1

    for i in listdir(basepath):
        try:
            rmtree(join(basepath,i))
        except:
            print("skipped {}".format(i))
    
        





    
    
