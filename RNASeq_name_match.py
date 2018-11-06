fullData = []
names = []
with open("C:\\Users\\M113455\\Desktop\\Book1.csv", 'r') as file:
    for line in file.readlines():
        line = line.strip()
        parts = line.split(",")
        names.append('"' + parts[0] + '"')
        fullData.append(parts)

with open("C:\\Users\\M113455\\Desktop\\output.csv", 'w') as file2:
    with open("C:\\Users\\M113455\\Desktop\\My Analysis Result Table.csv", 'r') as file:
        for line in file.readlines():
            line = line.strip()
            parts = line.split(",")
            try:
                ind = names.index(parts[1])
                file2.write(parts[1] + "," + fullData[ind][0] + "," +  fullData[ind][1] + "," +  fullData[ind][2] + "," +  parts[2] + "," +  parts[3] + "," +  parts[4] + "," +  parts[5] + "," +  parts[6] + "," +  parts[7] + "," +  parts[8]+"\n")

            except:
                pass
            
 
