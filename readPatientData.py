"""
readPatientData
Logan Manlove
11/16/2017

Used to create the union of two seperate spread sheets (saved as tab delimited text files).

First sheet is a list of cells from patient samples that are currently available
Second sheet is a list of deidentified patient informations

matches the two sets based on arbitrary patient number and outputs a tab delimited text file with select patient information and cell types available.
"""


patientList = {}
with open('~') as f:
    for line in f:
        parts = line.split('\t')
        if parts[4].lower() == 'hasm' and parts[0].isdigit():
            if parts[0] in patientList and 0 not in patientList[parts[0]][0]:
                patientList[parts[0]][0].append(0)
            else:
                patientList[parts[0]] = [[0], parts[1]]
        elif parts[4].lower() == 'fibroblast' and parts[0].isdigit():
            if parts[0] in patientList and 1 not in patientList[parts[0]][0]:
                patientList[parts[0]][0].append(1)
            else:
                patientList[parts[0]] = [[1], parts[1]]
                
patientData = {}
with open('~') as f:
    for line in f:
        parts = line.split('\t')
        if parts[0] in patientList:
            patientData[parts[0]] = [parts[3], parts[2]]
            

w = open('cellsOut.txt', 'w')
w.write('~')
for a in patientList:
    w.write(a + '\t' + patientList[a][1] + '\t' + patientData.get(a, ['',''])[0] + '\t' + patientData.get(a, ['',''])[1].upper() + '\t')
    if 1 in patientList[a][0]:
        w.write('X')
    w.write('\t')
    if 0 in patientList[a][0]:
        w.write('X')
    w.write('\n')
w.close()
 
