import pandas as pd
import xlrd
import openpyxl

data = pd.read_excel("File_Uploads\CEWE Prometer 100\WP020204 - 20-Feb-2025 12-22-34-000 PM - TODEnergy.xls", engine="xlrd")
print(data)