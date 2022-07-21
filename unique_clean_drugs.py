import xlrd

import xlwt

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from pandas import *

from googletrans import Translator

from numba import jit

import time

start = time.time()

# open the CleanDataBase
file = xlrd.open_workbook("/home/larrychen/MSFinance/summer2022/MLMapping/MLMapping/localmapping/CleanDataBase.xls")

# Get and print the number of sheets
print( "sheet number:", file.nsheets)

# Get and print the names of sheets
print( "sheet name:", file.sheet_names())

# Get the related information about the first sheet 
sh1 = file.sheet_by_index(0)


print( u"sheet %s has %d rows %d columns." % (sh1.name, sh1.nrows, sh1.ncols))

# Get and print a specific value in one cell
# print( "第一行第二列的值为:", sh1.cell_value(0, 1))

# Get all values in one row or column.
row0 = sh1.row_values(0) # row of all titles of columns
col12 = sh1.col_values(12) # column of catalog names

print(type(row0), type(col12))

unique_catalog_names = sorted(list(set(col12)))[1:]

print(len(unique_catalog_names), len(col12))

new_wb = xlwt.Workbook()

sheet = new_wb.add_sheet("drugs")

sheet.write(0, 0, 'catalog of drugs')
sheet.write(0, 1, 'República de Chile original')
sheet.write(0, 2, 'República de Chile matched with catalog')
sheet.write(0, 3, 'República de Chile original en ingles')

# this is a helper function
@jit

def list_to_col(l, n):
    for i in range(len(l)):
        sheet.write(i + 1, n, l[i])

# for i in range(len(unique_catalog_names)):
#     sheet.write(i + 1, 0, unique_catalog_names[i])
list_to_col(unique_catalog_names, 0)
    
# new_wb.save("unique_drug_compared_list.xls")

print(fuzz.ratio("123","1234"))

print(fuzz.partial_ratio("123","1234"))


# Now we deal with drugs in the first file, from Chile

# Note: this is a csv file.


file_chile_1 = read_csv("CHLDiab1.csv", encoding='latin-1')



col11_chile_1 = file_chile_1["Descripcion linea Adquisicion"].tolist() # column "L"



unique_chile_1 = list(filter(None, sorted(list(set(col11_chile_1)))))

print(len(sorted(list(set(col11_chile_1))))) # A unique list of catalog of drugs from Chile

# store them in the second colum in unique_drug_compared_list.xls, under title República de Chile original

# car; cat --> lexi. corrspondence note.
# cat; dog 

list_to_col(unique_chile_1, 1)
# for i in range(len(unique_chile_1)):
#     sheet.write(i + 1, 1, unique_chile_1[i])
print(len(unique_chile_1))
    
    
# espanol to english
english_unique_chile_1 = []
translator = Translator(service_urls=['translate.googleapis.com']) 
# discarded

def translist(l1, l2):
    for x in l1:
        l2.append(translator.translate(x, dest='en').text)

# for x in unique_chile_1:
#     english_unique_chile_1.append(translator.translate(x, dest='en').text)
translist(unique_chile_1, english_unique_chile_1)
    
print(len(english_unique_chile_1))




chile1_drug_catalog = []



# query = 'My name is Ali'
# choices = ['My name Ali', 'My name is Ali', 'My Ali']  
# # Get a list of matches ordered by score, default limit to 5
# print(process.extractOne(query, choices)[0], type(process.extract(query, choices)))


def listmatch(lx, ly, lz):
    for x in lx:
        ly.append(process.extractOne(x, lz)[0])

# for x in english_unique_chile_1:
#     chile1_drug_catalog.append(process.extractOne(x, unique_catalog_names)[0])
listmatch(english_unique_chile_1, chile1_drug_catalog, unique_catalog_names)
    
print(len(chile1_drug_catalog))

# for i in range(len(chile1_drug_catalog)):
#     sheet.write(i + 1, 2, chile1_drug_catalog[i])
list_to_col(chile1_drug_catalog, 2)
    
# for i in range(len(english_unique_chile_1)):
#     sheet.write(i + 1, 3, english_unique_chile_1[i])
list_to_col(english_unique_chile_1, 3)

new_wb.save("unique_drug_compared_list.xls")

end = time.time()

print(f"This program runs for {end - start} seconds, which means {(end - start) / 60} minutes")











