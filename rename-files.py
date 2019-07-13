#! python3
# rename-files.py - Renames files according in the format of "name-#", where name uses snake or camel case

import shutil, re, os, argparse

def main(newFileNameLabel, dir):
    allFilesNames = set(os.listdir(dir))
    fileNameRegex = re.compile(r'(.+)-(\d+)(\.[a-zA-Z]+)$')   # file name is in the format of: name-#.(file extension)
    excludedNumbers = set()

    for file in os.listdir(dir):
        if os.path.isdir(file):
            print(f'{file:s} is not a file, skipping')
            allFilesNames.remove(file)
        checkName = fileNameRegex.fullmatch(file)
        if checkName is not None:
            if int(checkName.group(2)) < len(allFilesNames):
                excludedNumbers.add(int(checkName.group(2)))
                print("Skipping file: %s" % file)
                allFilesNames.remove(file)

    number = 0
    renamedFiles = 0

    absWorkingDir = os.path.abspath(dir)
    
    for file in allFilesNames:
        while number in excludedNumbers:
            number = number+1
        newName = newFileNameLabel + "-" + str(number) + os.path.splitext(file)[1];
        number = number+1
        print("Renaming file: " + file + " to " + newName)
        renamedFiles = renamedFiles + 1
        shutil.move(os.path.join(absWorkingDir, file), os.path.join(absWorkingDir, newName))

    print("%d files were renamed!" % renamedFiles)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process arguments to rename files')
    parser.add_argument('--filename', dest='fileNameLabel', required=True, help='name/labels for files')
    parser.add_argument('--dir', dest='directory', required=True, help='directory in which files should be renamed')
    args = parser.parse_args()
    print(f'Attempting to rename files in: {args.directory:s} to label {args.fileNameLabel:s} ')
    if  not (os.path.abspath(args.directory).startswith("V")):
        print("Trying to rename files in disk other than V, aborting!")
        quit()
    else:
        main(args.fileNameLabel, args.directory)
