import os.path
from copy import copy
import re
import PyPDF2
from tkinter import filedialog
import glob

from numpy.core.defchararray import isdigit


def is_date(item):
    parts = item.split('/')
    if len(parts) == 3 and isdigit(parts[1]):
        # print(item)
        return True
    return False

def beautify(name):
    if isinstance(name, list):
        new_name = ""
        for item in name:
            new_name = new_name + item.replace(".", " ") + ' '
        return re.sub(' +', ' ', new_name.strip().upper())
    else:
        return re.sub(' +', ' ', name.replace('.', ' ').strip().upper())

def get_date(item):
    parts = item.split('/')
    if isdigit(parts[0][0]):
        return "", item
    else:
        name = ''
        date = ''
        i=0
        while i<len(parts[0]) and (not isdigit(parts[0][i])):
            i+=1
        if i<= len(parts[0]):
            name = parts[0][:i].replace(' ', '')
            date = parts[0][i:]
            for j in range(1,len(parts)):
                date = date+'/'+parts[j]
        return name, date

def get_name_and_date(txt):
    lines = text.split('\n')
    number_of_lines = len(lines)
    p_name = ''
    date = ''
    i=0
    while date == '' and i < number_of_lines:
        p_name_and_date = lines[i].strip().split(' ')
        i+=1
        if len(p_name_and_date) == 1:
            name, date = get_date(p_name_and_date[0])
            p_name = p_name.strip()+' '+name
        else:
            # print("first part:", p_name_and_date[0])
            # print("last part:", p_name_and_date[-11])
            # if not is_date(p_name_and_date[-1]):
            #     p_name = copy(p_name_and_date)
            #     p_name_and_date = lines[1].strip().split(' ')
            if is_date(p_name_and_date[-1]):
                p_name = p_name_and_date[:-1]
                name, date = get_date(p_name_and_date[-1])
                p_name+=name
                # date = p_name_and_date[-1]
            else:
                for item in p_name_and_date:
                    p_name += item


    return p_name, date

def get_age(txt):
    age=""
    lines = txt.split('\n')
    i=1
    number_of_lines = len(lines)
    while i < number_of_lines and (len(lines[i].split(" "))<3 or lines[i].split(" ")[2]!="years"):
        i+=1
    if i>=number_of_lines:
        return ""
    if len(lines[i].split(" "))>=3 and lines[i].split(" ")[2]=="years":
        age = lines[i].split(" ")[1]
    return age

def get_breast_composition(txt):
    lines = txt.split('\n')
    i = 1
    breast_composition = ''
    number_of_lines = len(lines)
    while i < number_of_lines:
        if 'breast composition' in lines[i]:
            break
        i+=1
    if i < number_of_lines and ('breast' in lines[i] and 'composition' in lines[i]):
        items = lines[i].split(' ')
        k=0
        while items[k] != 'composition':
            k+=1
        breast_composition = items[k+1].replace(')', '').replace('.','')
    return breast_composition
    # if i < number_of_lines:
    #     if lines[i].split(" ")[1] == 'Breast'


def get_birads(txt):
    lines = txt.split('\n')
    number_of_lines = len(lines)
    i=0
    bi_rads = ''

    while i < number_of_lines and not('BIRADS:' in lines[i]):
        i+=1
    if i < number_of_lines and 'BIRADS:' in lines[i]:
        items = lines[i].split(' ')
        k=0
        while not ('BIRADS:' in items[k]):
            k+=1
        if len(items[k].split(':'))>1:
            # print(items[k].split(':'))
            bi_rads = items[k].split(':')[1]
            if bi_rads == '':
                bi_rads = items[k+1]

        else:
            bi_rads = items[k+1]

    return bi_rads.replace(')', '').replace(',','')


def greek_to_english_number(greek_number):
    if greek_number == '':
        return ''
    if isdigit(greek_number):
        return str(greek_number)
    valid = ['I', 'V', 'X']
    english_number = 0
    after = 0
    for i in range(len(greek_number)-1, -1, -1):
        if greek_number[i] not in valid:
            continue
        if greek_number[i] == 'I':
            if after > 1:
                english_number -= 1
            else:
                english_number += 1
            after = 1
        elif greek_number[i] == 'V':
            if after> 5:
                english_number = english_number - 5
            else:
                english_number = english_number + 5
            after = 5
        elif greek_number[i] == 'X':
            english_number += 10
            after = 10
    return str(english_number)




pdf_files_path = filedialog.askdirectory(title='Select the folder containing the pdf files to convert', initialdir=r"C:\Users\Admin\Documents\VidaMedicals")
pdf_files = glob.glob(os.path.join(pdf_files_path, "*.pdf"))
csv_file_path = filedialog.asksaveasfilename(initialdir="C:/Users/Admin/Documents/", filetypes=[("csv files", "*.csv")])
# pdf_file_path = r"C:\Users\Admin\Documents\VidaMedicals\Codes\Datasets\MAMMO.G (PDF)\BEHNAZ ROUHI KHORASANI  182074.pdf"
print(pdf_files)
file = open(csv_file_path, 'w')
file.write('Patient Name,Age,Breast Composition, BI_RADS'+'\n')
for pdf in pdf_files:
    pdf_file_obj = open(pdf, 'rb')
    pdfReader = PyPDF2.PdfReader(pdf_file_obj)
    pages = len(pdfReader.pages)

    page_obj = pdfReader.pages[0]
    text = page_obj.extract_text()
    print(text)
    p_name, date = get_name_and_date(text)
    p_name = beautify(p_name)
    # print(p_name)
    # print(date)
    age = get_age(text)
    bi_rads = get_birads(text)
    breast_composition = get_breast_composition(text)
    # print(p_name, bi_rads)
    # print(p_name, date, age)

    # print(text)
    # print("============================================================")
    file.write(p_name + ',' + age + ',' + breast_composition + ',' + greek_to_english_number(bi_rads) + '\n')
file.close()
