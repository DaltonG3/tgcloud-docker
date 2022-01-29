from scripts import *
listoffiles = getListOfFiles(dirName)
for line in listoffiles:
    md5 = get_md5(line)
    epoch = get_last_time_modified(line)
    print(">>element<<"+line+">>md5<<"+md5+">>epoch<<"+str(epoch)+">>end_of_line<<",file=open("list2.txt", "a"))
               