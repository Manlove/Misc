from os import chdir, rename, removedirs, listdir
from os.path import join, exists, isdir
from shutil import rmtree

basepath = "X:\\LABORATORY\\JCMS\\"

# Runs until all folders within the basepath directory have been removed
while listdir(basepath) != []:
    path = basepath
    j=0
    while True:
        # checks to see if a folder exists with the current integer name and increments by one if it does
        if exists(join(basepath,str(j))):
            j += 1
        else:
        # Steps through
            for i in range(1,10):
                dr = listdir(path)
                # !!! This will probably break if there are more than 1 directory in the current folder
                # adds the two folders in series instead of working through them in parallel
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
