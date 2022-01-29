from scripts import *
md51 = get_md5("list1.txt")
md52 = get_md5("list2.txt")
print(md51,md52)
founded = []
with open("list1.txt") as search:
    for line in search:
        with open("list2.txt") as search1:
            found = 0
            for line_tmp in search1:
                if line == line_tmp:
                    found = 1
        print (found, line)
        if found == 0:
            founded.append(line)
print ("founded == 0",founded)
                