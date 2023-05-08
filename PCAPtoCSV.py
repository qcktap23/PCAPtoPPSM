# Python 3.11.3 #
# Can be used to remove duplicate data from a PCAP file #
# Requires pandas, tkinter, openpyxl, and pyshark to be installed # 
import pyshark
import pandas as pd
from tkinter import filedialog
from tkinter import *
import csv
import os
import openpyxl
import shutil

# Prompt user for PCAP file path
pcap_path = filedialog.askopenfilename()

# Create a copy of the template and establish our var
print("Preparing PPSM sheet")
shutil.copy('PPSM Template.xlsx', 'PPSM.xlsx')
ppsm = 'PPSM.xlsx'

# Open the PCAP file and extract desired fields using a generator expression
packets = (packet for packet in pyshark.FileCapture(pcap_path)
           if 'IP' in packet and packet.transport_layer)

# Write the desired fields to a CSV file using a DictWriter object
print("Reading PCAP file out to csv")
csv_path = 'output.csv'
with open(csv_path, 'w', newline='') as csvfile:
    fieldnames = ['Source IP', 'Destination IP', 'Protocol', 'Source Port', 'Destination Port']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for packet in packets:
        row = {
            'Source IP': packet.ip.src,
            'Destination IP': packet.ip.dst,
            'Protocol': packet.transport_layer,
            'Source Port': packet[packet.transport_layer].srcport,
            'Destination Port': packet[packet.transport_layer].dstport
        }
        writer.writerow(row)

# Read column names and data
# Remove duplicates
print("Removing moving data from CSV to PPSM")
csv_sorted = pd.read_csv(csv_path, usecols=['Source IP', 'Destination IP', 'Protocol', 'Source Port', 'Destination Port'])
csv_sorted.drop_duplicates(subset=None, keep="first", inplace=True)
csv_sorted.to_csv(csv_path, index=False)

# Load the CSV file into a pandas dataframe, specifying the columns to include
cols_to_include = ['Source IP','Protocol','Source Port']
df = pd.read_csv(csv_path, usecols=cols_to_include)

# Create a new Excel workbook
writer = pd.ExcelWriter(ppsm, engine='openpyxl', mode='a', if_sheet_exists='overlay')

# Write the dataframe to the Excel worksheet, specifying destination column names
df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=1, columns={
    'Source Port': 'A',
    'Protocol': 'B'  
})

df.to_excel(writer, sheet_name='Sheet1', index=False, startrow=1, startcol=3, columns={
    'Source IP': 'D'      
})

# Save the Excel workbook
writer._save()

wb = openpyxl.load_workbook(ppsm)

# Remove the second row from each worksheet
for ws in wb.worksheets:
    ws.delete_rows(2)

wb.save(ppsm)

print(f"PPSM completed")
print(f"Save both files, your csv will have extra data that may be useful")
