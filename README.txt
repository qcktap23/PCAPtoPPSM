Built in Python 3.11.3
All should be built in modules except pandas, openpyxl, and pyshark.

Converts PCAP to CSV, sorts out all but Source IP, Destination IP, Source Port, Destination Port, 
and Protocol. Once done, it then removes all duplicate rows.

Windows Users:

Install Pip:
1. Run: curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
2. Run: python get-pip.py

Install Modules:
1. pip install tk
2. pip install pandas
3. pip install openpyxl
4. pip install pyshark

Pandas Source:
https://github.com/pandas-dev/pandas

Openpyxl Source:
https://foss.heptapod.net/openpyxl/openpyxl

Pyshark Source:
https://github.com/KimiNewt/pyshark
