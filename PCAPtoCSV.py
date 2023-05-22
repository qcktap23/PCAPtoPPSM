# Python 3.11.3 #
# Can be used to remove duplicate data from a PCAP file #
# Requires pandas, tkinter, openpyxl, and pyshark, scapy, tqdm, magic to be installed #
import configparser
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
import openpyxl
import shutil
import time
import sys
import scapy.error
from scapy.all import IP
from datetime import datetime
import logging.config
from scapy.utils import PcapReader
from tqdm import tqdm
# ======================================================================================================================
# ============================= Pre-checks // Set up logging and debugging information =================================
# Checks if .ini file exits locally and exits if it doesn't
if not os.path.exists('config.ini'):
    messagebox.showerror("No Config file", "Config.ini file does not exist\nPlace config.ini in: " + str(os.getcwd()) +
                         "\nRe-run program")
    sys.exit()

# Read log directory from .ini and if directory structure doesn't, exist create it.
config = configparser.ConfigParser()
config.read("config.ini")

try:
    log_dir = config.get("handler_fileHandler", "logdir")
except (configparser.NoOptionError, configparser.NoSectionError, configparser.MissingSectionHeaderError):
    messagebox.showerror("Invalid file", "Incompatible config.ini file.")
    sys.exit()
try:
    if os.path.exists(log_dir) is False:
        os.makedirs(log_dir)
except PermissionError:
    messagebox.showerror("Cannot create log directory\nChange 'agrs' and 'logdir' in config.ini "
                         "path to a path with permissions")
    sys.exit()

# load logging configuration file
try:
    logging.config.fileConfig('config.ini')
    logger = logging.getLogger()
except ValueError:
    messagebox.showerror("Invalid file",  "Invalid config.ini")
    sys.exit()

title_name = "PCAP to CSV"
os.system("title " + title_name)
version = "1.2.0"
current_dir = os.getcwd()
log_version = "PCAP to CSV Version: " + version
runtime = datetime.now()
current_time = runtime.strftime("%m%d%Y::%H:%M:%S")
username = os.getlogin()

logger.info(log_version)
logger.debug("Ran from: " + current_dir)
logger.debug("Ran by: " + username)
logger.debug("Ran at: " + str(current_time))


# ======================================================================================================================
# ===================================================== FUNCTIONS ======================================================
def check_path(path):  # Check if path exists return bool and log
    if os.path.exists(path):
        return True
    else:
        logger.warning("Path doesn't exist: " + path)
        return False


def bool_box(title, message):  # present yes or no prompt
    res = messagebox.askquestion(title, message)
    if res == "yes":
        return True
    else:
        return False


def check_write_permission(path):
    if os.path.exists(path):
        write_permission = os.access(path, os.W_OK)
        logger.debug("write permission: " + str(write_permission) + " | " + path)
        return write_permission
    else:
        return None


def check_read_permission(path):
    if os.path.exists(path):
        read_permission = os.access(path, os.R_OK)
        logger.debug("read permission: " + str(read_permission) + " | " + path)
        return read_permission
    else:
        return None


def check_execute_permission(path):
    if os.path.exists(path):
        execute_permission = os.access(path, os.X_OK)
        logger.debug("execute permission: " + str(execute_permission) + " | " + path)
        return execute_permission
    else:
        return None


# ======================================================================================================================
# ===================================================== Pre-checks =====================================================
csv_path = 'raw_output.csv'
ppsm_output = 'PPSM.xlsx'
ppsm_template = 'PPSM Template.xlsx'
root = tk.Tk()
root.withdraw()
# x = log_dir + csv_path

# Prompt user for file path for PCAP
pcap_path = filedialog.askopenfilename()
logger.info("opened file: " + pcap_path)

# Check if handling files exists
csv_exists = check_path(csv_path)
excel_template_exists = check_path(ppsm_template)
excel_exists = check_path(ppsm_output)

# Check permissions for needed files and folders
csv_read_perm_value = check_read_permission(csv_path)
csv_write_perm_value = check_write_permission(csv_path)
csv_ex_perm_value = check_execute_permission(csv_path)
xcel_read_perm_value = check_read_permission(pcap_path)
xcel_write_perm_value = check_write_permission(pcap_path)
xcel_ex_perm_value = check_execute_permission(pcap_path)
current_dir_write_perm = check_write_permission(current_dir)
current_dir_ex_perm = check_execute_permission(current_dir)

# if current directory doesn't have write or execute permission
if not current_dir_write_perm or not current_dir_ex_perm:
    messagebox.showerror("Permission error", current_dir + ": Does not have write and/or execute permission.\n "
                                                           "Move folder to a path with permission.")
    logger.error(current_dir + ": Does not have write or execute permission.")
    sys.exit()

# If file selection is cancelled, exit
if not pcap_path:
    logger.warning("No file selected, exiting.")
    messagebox.showwarning("Exiting", "No file selected, exiting.")
    sys.exit()

# Check file extension on user selection
file_extension = os.path.splitext(pcap_path)[1].lower()
if file_extension not in ['.pcap', '.pcapng']:
    logger.error("User selected file type is invalid.")
    logger.debug(file_extension)
    messagebox.showerror("Invalid File type", "Invalid file type selected. Only PCAP and PCAPNG files.")
    sys.exit()

# gives user selection to overwrite ppsm file if it already exists, if not it copies template
logger.info("Preparing PPSM sheet")
if excel_exists:
    result = bool_box("File overwrite", "File overwrite" + ppsm_output + " exists do you want to overwrite?")
    if result is True:
        logger.info("Overwriting " + ppsm_output)
        shutil.copy(ppsm_template, ppsm_output)
    else:
        logger.warning(ppsm_output + " file already exists")
        logger.warning("user selected cancel overwrite")
        logger.info("exiting")
        messagebox.showwarning("File overwrite cancelled.", "Exiting Program.")
        sys.exit()

# Copy ppsm template for ppsm output
if not excel_exists:
    if excel_template_exists:
        shutil.copy(ppsm_template, ppsm_output)
    else:  # If no ppsm template is found, program exits
        logger.error("No PPSM template found" " | " + ppsm_template + " file not found. Exiting.")
        messagebox.showerror("No file found", "No PPSM template file found!")
        sys.exit()

# gives user selection to overwrite CSV file if it already exists
if csv_exists:
    result = bool_box("File Overwrite", "CSV Path exists: " + csv_path + " | " + "Do you want to overwrite?")
    if result is True:
        try:
            os.remove(csv_path)
        except PermissionError:
            if csv_write_perm_value or xcel_write_perm_value is False:
                logger.error("Program cannot write to file, CSV file is open. Close and re-run.")
                messagebox.showerror("File open", "CSV File is open, please close and try again.")
                sys.exit()
    else:
        logger.warning("Overwrite aborted for: " + csv_path)
        logger.warning("exiting program.")
        messagebox.showwarning("Exiting", "File overwrite cancelled, exiting program.")
        sys.exit()
# ======================================================================================================================
# ====================================================== CORE CODE =====================================================
start_time = time.time()
logger.info("Reading capture file: " + pcap_path)

try:
    chunk_value = config.get("defaults", "chunk_size")  # Number of packets to read at a time, configurable in .ini file
except (configparser.NoOptionError, configparser.NoSectionError, configparser.MissingSectionHeaderError):
    logger.error("Chunk value missing from config.ini")
    messagebox.showerror("File error", "value missing in config")
    sys.exit()

# Set chunk size value to value in .ini file
chunk_size = int(chunk_value)
logger.debug("Chunk Size: " + chunk_value)

# Open the PCAP file for reading and write in chunks to CSV
with open(csv_path, 'w', newline='') as csvfile:
    fieldnames = ['Source IP', 'Destination IP', 'Protocol', 'Source Port', 'Destination Port']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    try:
        logger.info("Writing CSV file")
        logger.debug("CSV path: " + csv_path)
        pcap_file_size = os.path.getsize(pcap_path)  # Get the size of the PCAP file in bytes
        pbar = tqdm(total=pcap_file_size, unit='bytes')  # Initialize the progress bar
        with PcapReader(pcap_path) as pcap_reader:
            while True:
                try:
                    chunk = list(pcap_reader.read_packet(chunk_size))  # Read a chunk of packets
                except EOFError:
                    break  # reached end of file
                for packet in chunk:  # Process each packet in the chunk
                    if IP in packet and packet[IP].payload:
                        transport_layer = packet[IP].payload
                        row = {
                            'Source IP': packet[IP].src,
                            'Destination IP': packet[IP].dst,
                            'Protocol': transport_layer.name,
                            'Source Port': transport_layer.sport if hasattr(transport_layer, 'sport') else '',
                            'Destination Port': transport_layer.dport if hasattr(transport_layer, 'dport') else ''
                        }
                        writer.writerow(row)
                        packet_size = len(bytes(packet))
                        pbar.update(packet_size)
            pbar.close()
    except scapy.error.Scapy_Exception:
        logger.error("Not a supported file type.")
        messagebox.showerror("Unsupported file", "File Not supported.")
        sys.exit()

# Remove duplicate rows in the CSV file and write to Excel workbook
logger.info("Writing data to PPSM: " + ppsm_output)
cols_to_include = ['Source IP', 'Protocol', 'Source Port', 'Destination IP']
writer = pd.ExcelWriter(ppsm_output, engine='openpyxl', mode='a', if_sheet_exists='overlay')
total_rows = sum(1 for _ in pd.read_csv(csv_path, usecols=cols_to_include, chunksize=chunk_size))
with tqdm(total=total_rows, unit=' rows') as pbar:
    for df_chunk in pd.read_csv(csv_path, usecols=cols_to_include, chunksize=chunk_size):
        df_chunk.drop_duplicates(subset=None, keep="first", inplace=True)
        df_chunk.to_excel(writer, sheet_name='Sheet1', index=False, startrow=1, columns={
            'Source Port': 'A',
            'Protocol': 'B',
            'Destination IP': 'E'
        })
        df_chunk.to_excel(writer, sheet_name='Sheet1', index=False, startrow=1, startcol=3, columns={
            'Source IP': 'D',
            'Destination IP': 'E'
        })
        pbar.update(len(df_chunk))
writer.close()
pbar.close()

# Remove the second row from each worksheet because it adds header columns
wb = openpyxl.load_workbook(ppsm_output)
for ws in wb.worksheets:
    ws.delete_rows(2)
wb.save(ppsm_output)

end_time = time.time()
# ======================================================================================================================
# ====================================================== Post-checks====================================================
logger.info("PPSM completed.")
logger.info("CSV file contains raw data.")
run_time = end_time - start_time
runtime_seconds = run_time
runtime_minutes = run_time // 60
if runtime_seconds < 60:  # return minutes if runtime is over 60 seconds
    logger.info("Runtime: " + str(runtime_seconds) + " seconds")
else:
    logger.info("Runtime: " + str(runtime_minutes) + " minutes")
logger.debug("Start time: " + str(start_time) + " // End time: " + str(end_time))
messagebox.showinfo("Process Completed", "PPSM creation completed. Files saved successfully.")
