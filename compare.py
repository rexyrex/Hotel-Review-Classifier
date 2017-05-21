import sys

file1 = open(sys.argv[1])
file2 = open(sys.argv[2])

file1Lines = file1.readlines()
file2Lines = file2.readlines()

matchCount =0
totalCount = 0
dtMatchCount =0
pnMatchCount =0
idMatchCount = 0

for it in range(0, len(file1Lines)):
    f1Split = file1Lines[it].split()
    f2Split = file2Lines[it].split()
    
    
    if f1Split[1] == f2Split[1] and f1Split[2] == f2Split[2]:
        matchCount += 1
    if f1Split[0] == f2Split[0]:
        idMatchCount += 1
    if f1Split[1] == f2Split[1]:
        dtMatchCount += 1
    if f1Split[2] == f2Split[2]:
        pnMatchCount += 1
    
    totalCount+=1
    
print('accuracy:' + str(matchCount) + '/' + str(totalCount) + '=' + str(float(matchCount)/totalCount)) 
print('id accuracy:' + str(idMatchCount) + '/' + str(totalCount) + '=' + str(float(idMatchCount)/totalCount)) 
print('accuracy dt:' + str(dtMatchCount) + '/' + str(totalCount) + '=' + str(float(dtMatchCount)/totalCount)) 
print('accuracy pn:' + str(pnMatchCount) + '/' + str(totalCount) + '=' + str(float(pnMatchCount)/totalCount)) 

