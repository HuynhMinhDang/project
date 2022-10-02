import csv
import pandas as pd

df = pd.read_csv('RFvalue.csv')
print(df.head)
# print(df['tValue']) 
with open('RFvalue.csv','r') as value_file:
    reader = csv.reader(value_file)
    header = next(reader) #The first line is the header

    data = []
    for row in reader:
        #row = [DID, Description, Length (Byte), Value, ASCII to HEX, Physical Addressing, Functional Addressing ]
        # DID = float(row[1])
        Description = float(row[2])
        Length_Byte = float(row[3])
        ASCII_to_HEX = float(row[4])
        Physical_Addressing = float(row[5])
        Functional_Addressing = float(rowp[6])

        data.append([DID, Discription, Length_Byte, ASCII_to_HEX, Physical_Addressing_Functional_Addressing])

        print(data[0])