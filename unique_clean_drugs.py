import xlrd

import xlwt

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from pandas import *

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

print(len(unique_catalog_names), len(col12), unique_catalog_names)

new_wb = xlwt.Workbook()

sheet = new_wb.add_sheet("drugs")

sheet.write(0, 0, 'catalog of drugs')
sheet.write(0, 1, 'República de Chile original')
sheet.write(0, 2, 'República de Chile matched with catalog')

for i in range(len(unique_catalog_names)):
    sheet.write(i + 1, 0, unique_catalog_names[i])
    
# new_wb.save("unique_drug_compared_list.xls")

print(fuzz.ratio("123","1234"))

print(fuzz.partial_ratio("123","1234"), fuzz.token_sort_ratio("114514", "114514810"))


# Now we deal with drugs in the first file, from Chile

# Note: this is a csv file.


file_chile_1 = read_csv("CHLDiab1.csv", encoding='latin-1')

# sh1_chile_1 = file_chile_1.sheet_by_index(0)

col11_chile_1 = file_chile_1["Descripcion linea Adquisicion"].tolist() # column "L"

# print(type(col11_chile_1), col11_chile_1)

unique_chile_1 = list(filter(None, sorted(list(set(col11_chile_1)))))

print(len(unique_chile_1), len(sorted(list(set(col11_chile_1))))) # A unique list of catalog of drugs from Chile

# store them in the second colum in unique_drug_compared_list.xls, under title República de Chile original



for i in range(len(unique_chile_1)):
    sheet.write(i + 1, 1, unique_chile_1[i])
    
chile1_drug_catalog = []



# query = 'My name is Ali'
# choices = ['My name Ali', 'My name is Ali', 'My Ali']  
# # Get a list of matches ordered by score, default limit to 5
# print(process.extractOne(query, choices)[0], type(process.extract(query, choices)))

for x in unique_chile_1:
    chile1_drug_catalog.append(process.extractOne(x, unique_catalog_names)[0])
    
print(len(chile1_drug_catalog))

for i in range(len(chile1_drug_catalog)):
    sheet.write(i + 1, 2, chile1_drug_catalog[i])

new_wb.save("unique_drug_compared_list.xls")











