# Python 3.10 #
# Can be used to remove duplicate data from a PCAP file #

# Importing Tkinter and tkFileDialog to open "Common Open Dialog" window #
# Importing OS and re #
from tkinter import filedialog as fd
from tkinter import *
import os
import re
import operator
import pandas as pd

# Import CSV File #
file = fd.askopenfile(title='Open CSV File to sort')

# Read column names and data
# Importing columns labeled as: (2)Source, (3)Destination, (4)Protocol, (8)Src. Port 1
# Source, Destination, and Protocol are default Wireshark columns
# Src. Port 1 are custom columns that is in slot 8
ppsm = pd.read_csv(file, usecols=['Source', 'Destination', 'Protocol', 'Src. Port', 'Dst. Port'])
ppsm.drop_duplicates(subset=None, keep="first", inplace=True)
ppsm.to_csv('C:\PPSM\PPSM2.csv', index=False)
