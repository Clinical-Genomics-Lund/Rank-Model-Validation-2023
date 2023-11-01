import os
import re

def find_unzipped_filename(id, path): #For VCF_files.
    dir_list = os.listdir(path)
    our_filename = "placeholder"
    filename_pattern = re.compile(f"^{id}.*.vcf$")
    for filename in dir_list:
        is_match = re.findall(filename_pattern, filename) #Produces a list of all matches in the current file name.
        if len(is_match) > 0: #If there is a match.
            our_filename = filename
            break
    return our_filename

def find_filename(id, path): #For VCF_files.
    #We only want to identify a file based on path and ID, and we want to disregard anything in the file name like rescored.sorted etc.
    #Note that we use regex to ensure that the input file is a VCF file!
    dir_list = os.listdir(path)
    our_filename = "placeholder"
    filename_pattern = re.compile(f"^{id}.*.vcf.gz")
    for filename in dir_list:
        is_match = re.findall(filename_pattern, filename) #Produces a list of all matches in the current file name.
        if len(is_match) > 0: #If there is a match.
            our_filename = filename
            break
    return our_filename

def find_textfile(id, path):
    dir_list = os.listdir(path)
    our_filename = "placeholder"
    filename_pattern = re.compile(f"^{id}_data.txt")
    for filename in dir_list:
        is_match = re.findall(filename_pattern, filename) #Produces a list of all matches in the current file name.
        if len(is_match) > 0: #If there is a match.
            our_filename = filename
            break
    return our_filename