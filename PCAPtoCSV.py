# Python 3.11.3 #
# Can be used to remove duplicate data from a PCAP file #
# Requires pandas, tkinter, and pyshark to be installed # 
import pyshark
import pandas as pd
from tkinter import filedialog
from tkinter import *
import csv

# Prompt user for PCAP file path
pcap_path = filedialog.askopenfilename()

# Open the PCAP file and extract desired fields using a generator expression
packets = (packet for packet in pyshark.FileCapture(pcap_path)
           if 'IP' in packet and packet.transport_layer)

# Write the desired fields to a CSV file using a DictWriter object
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
ppsm = pd.read_csv(csv_path, usecols=['Source IP', 'Destination IP', 'Protocol', 'Source Port', 'Destination Port'])
ppsm.drop_duplicates(subset=None, keep="first", inplace=True)
ppsm.to_csv(csv_path, index=False)

print(f"PPSM completed")