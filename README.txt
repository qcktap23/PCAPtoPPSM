Built in Python 3.10.4
Requires pandas, os, re, operator, and tkinter modules
All should be built in modules except pandas.

Does not sort a PCAP, but sorts a CSV generated from PCAP. In wireshark with the PCAP file, create 1 extra column for SRC port resolved.
You should have a total of 9 columns with the following being the needed order:
Column 3: Source
Column 4: Destination
Column 5: Protocol
Column 9: Src. Port 1 (Resolved)