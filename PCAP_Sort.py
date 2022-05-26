# Python 3.10 #
# Can be used to remove duplicate data from a PCAP file #

# Importing Tkinter and tkFileDialog to open "Common Open Dialog" window #
# Importing OS and re #
from tkinter import filedialog as fd
from tkinter import *
import os
import re
import operator


# Import and Read PCAP File #
file = fd.askopenfile(mode='r',title='Open PCAP File to sort')
# open(file) uncomment to test 

reader = csv.reader(open(file), delimiter=";")

sortlist = sorted(reader, key=lambda row: row(3), reverse=True) --> sortedfile.csv