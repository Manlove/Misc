"""
readPatientData-v2
Logan Manlove
1/25/2018

Update to readPatientData

takes in a sheet of available cells and a sheet of deidentified patient information and creates a union of the two sheets
with select patient information and blocks for each sample with all available passages underneath.
"""



patientList = {}

cell_label = 0
cell_passage = 3
cell_type = 4
passage_date = 5
rack_number = 6
box_number = 7
number_of_vials = 8
passage_dict = 1
cell_type_list = 0

with open('path/to/cell/sheet.txt') as f:
    for line in f:
        parts = line.split('\t')
        if parts[cell_label] == "Patient Number":
            continue
        if parts[cell_label] in patientList:
            
# if cell line is in the dictionary:

            if parts[cell_type] not in patientList[parts[cell_label]][cell_type_list]:
                patientList[parts[cell_label]][cell_type_list].append(parts[cell_type])
            
            if parts[cell_passage] in patientList[parts[cell_label]][passage_dict]:

# if passage is in the passage dictionary:
#       add increasing numbers to name until a name is not found
            
                count = 1
                name = parts[cell_passage] + "-" + str(count)
                while name in patientList[parts[cell_label]][1]:
                    count += 1
                    name = parts[cell_passage] + "-" + str(count)
                patientList[parts[cell_label]][passage_dict][name] = [parts[cell_type], parts[passage_date], parts[rack_number], parts[box_number], parts[number_of_vials]]
            else:

# if passage is not in the passage dictionary:
#       Add the passage and information to the passage dictionary
                
                patientList[parts[cell_label]][passage_dict][parts[cell_passage]] = [parts[cell_type], parts[passage_date], parts[rack_number], parts[box_number], parts[number_of_vials]]
                                       
        else:

# if cell line is not in dictionary:
#       create new key:value pair with cell line and list with the cell type and
#       a dictionary for each passage
            
            patientList[parts[cell_label]] = [[parts[cell_type]], {}]
            patientList[parts[cell_label]][passage_dict][parts[cell_passage]] = [parts[cell_type], parts[passage_date], parts[rack_number], parts[box_number], parts[number_of_vials]]


patientData = {}
patient_number = 0
harvest_date = 1
patient_age = 3
patient_sex = 2
patient_disease = 5
patient_smoking_history = 11

with open('path/to/patient/information.txt') as f:
    for line in f:
        parts = line.split('\t')
        if parts[patient_number] in patientList:
            patientData[parts[patient_number]] = [parts[harvest_date],parts[patient_age], parts[patient_sex], parts[patient_disease], parts[patient_smoking_history]]

# patientList variables
passage_dict = 1
cell_type_list = 0

# passage dict variables
cell_type = 0
passage_date = 1
rack_number = 2
box_number = 3
number_of_vials = 4

# patientData variables
harvest_date = 0
patient_age = 1
patient_sex = 2
patient_disease = 3
patient_smoking_history = 4

blank = ['','','','','']


# Write information to text document
w = open('cellsOut2.txt', 'w')
w.write('Patient Number/ Sample Label\tIsolation Date\tAge\tSex\tDisease\tSmoking History\tCell Types\n')
for sample in patientList:
    patientList[sample][cell_type_list].sort()
    w.write(sample + '\t' +
            patientData.get(sample, [''])[harvest_date] + '\t' +
            patientData.get(sample, blank)[patient_age] + '\t' +
            patientData.get(sample, blank)[patient_sex] + '\t' +
            patientData.get(sample, blank)[patient_disease] + '\t' +
            patientData.get(sample, blank)[patient_smoking_history] + '\t')
    count = 1
    for item in patientList[sample][cell_type_list]:
        if count > 1:
            w.write(', ')
        w.write(item)
        count += 1
    w.write('\n')
    for passage in patientList[sample][passage_dict]:
        w.write('\t' + passage + '\t' +
                patientList[sample][passage_dict][passage][cell_type] + '\t' +
                patientList[sample][passage_dict][passage][passage_date] + '\t' +
                patientList[sample][passage_dict][passage][rack_number] + '\t' +
                patientList[sample][passage_dict][passage][box_number] + '\t' +
                patientList[sample][passage_dict][passage][number_of_vials] + '\n')
w.close()
