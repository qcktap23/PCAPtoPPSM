Built in Python 3.11.3

uses libraries: pandas, tkinter, openpyxl, and pyshark, scapy, tqdm, magic

Converts PCAP or PCAPNG to CSV, sorts out all but Source IP, Destination IP, Source Port, Destination Port, 
and Protocol. Once done, it then removes all duplicate rows and puts unique rows in excel file.


needed files:
config.ini
PPSM Template.xlsx

launch .exe from same directory as config.ini and PPSM Template.xlsx
Output is saved in same directory .exe is run from.
log default location is: C:\pcap2csv\log