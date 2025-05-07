import pandas as pd
import numpy as np
import openpyxl
from datetime import datetime
import gc, os
from models import energyMeters
from store_filesdata_to_db import store_files_data
from dateutil.relativedelta import relativedelta
import csv

#PROCESS PROMETER 100 FILE DATA
def process_pro100_data(db, files_paths,filename, data):
    serial_no = filename[0].split("-")[0].strip()

    # Assign DFs to TOD and MainEnergy 
    for file_path in files_paths:
        if "TODEnergy" in file_path:
            # GET RATES
            df2 = pd.read_excel(file_path, engine="xlrd")
             #df = pd.read_excel(files_paths[0], engine="xlrd")
            df2 = df2.drop(index=[0, 1]).reset_index(drop=True) #drop the first two rows

        elif "MainEnergy" in file_path:
            df = pd.read_excel(file_path, engine="xlrd")
            df = df.drop(index=[0, 1]).reset_index(drop=True) #drop the first two rows

    # assign values of the third row as column names
    df.columns = df.iloc[0]
    df = df.drop(0).reset_index(drop=True)

    column_list = {"Billing Date":'billing_period',"Active(I) Total":"cumulative_import",
    "Active(E) Total":"cumulative_export","Apparent-Active(I) - type 2":"apparent_import",
    "Reactive(I)":"reactive_import","Reactive(E)":"reactive_export"}

    df = df.rename(columns=column_list)
    df = df[df["History"] != 0] #drop this row because we can not parse its date string (its empty)
    df['billing_period'] = pd.to_datetime(df['billing_period']).dt.normalize()

    # select needed columns
    column_list = ['History', 'billing_period', 'cumulative_import', 'cumulative_export',
        'apparent_import', 'reactive_import', 'reactive_export']
    df = df[column_list]
    df = df[df["History"] == 1]

    

    # assign values of the third row as column names
    df2.columns = df2.iloc[0]
    df2 = df2.drop(0).reset_index(drop=True)
    df2_columns = ['History', 'Billing Date', 'TOD/SLAB', 'Active(I) Total','Active(E) Total']
    df2 = df2[df2_columns]

    df2_columns = {'Billing Date':'billing_period', 'TOD/SLAB':'tou', 'Active(I) Total':'import',
               'Active(E) Total':'export'}
    df2 = df2.rename(columns=df2_columns)
    df = df[df["History"] != 0] #drop the current values. also, we cannot parse its date(empty)
    df['billing_period'] = pd.to_datetime(df['billing_period']).dt.normalize()
    df2 = df2[df2["History"] == 1]

    # getting rates and and assiging them to df
    df['rate1'] = df2[(df2['tou'] == 1) & (df2['History'] == 1)]['import'].values[0]
    df['rate2'] = df2[(df2['tou'] == 2) & (df2['History'] == 1)]['import'].values[0]
    df['rate3'] = df2[(df2['tou'] == 3) & (df2['History'] == 1)]['import'].values[0]

    df['rate4'] = df2[(df2['tou'] == 1) & (df2['History'] == 1)]['export'].values[0]
    df['rate5'] = df2[(df2['tou'] == 2) & (df2['History'] == 1)]['export'].values[0]
    df['rate6'] = df2[(df2['tou'] == 3) & (df2['History'] == 1)]['export'].values[0]
    df['serial_no'] = serial_no
    df['reading_date'] = datetime.now().replace(second=0, microsecond=0)

    columns_to_assign_na = ['vt_ratio', 'ct_ratio', 'no_of_resets', 'date_of_last_reset', 'programing_count',
                        'max_dem1','max_dem1_datetime','max_dem2','max_dem2_datetime','max_dem3','max_dem3_datetime']

    for column in columns_to_assign_na:
        df[column] = pd.NA
    
    billing_values = df.iloc[0].to_dict()
    print(billing_values)
    result = store_files_data(form_data = billing_values, db=db, data=data)

    if result == "Data stored successfully":
        return result
  
def process_prometer_data(db, files_paths,filename, data):
    #files = ['CW001292_hist.xls','CW001292_TOU.xls']
    serial_no = filename.split("_")[0].strip()
    print("serial no: ", serial_no)

    # Assign historica and TOU and MainEnergy 
    for file_path in files_paths:
        if "hist" in file_path:
            # GET RATES
            df = pd.read_table(file_path)
            
        elif "TOU" in file_path:
            df_rates = pd.read_table(file_path)
            df_rates = df_rates.rename(columns={df_rates.columns[0]: 'parameters'})

    # START PROCESSING DATA
    bill_date = str(df.iloc[0]).split(":")[1].strip().split(" ")[0]
    billing_date = datetime.strptime(bill_date, '%Y-%m-%d').date()
    df = df.reset_index().rename(columns={'index': 'parameters',df.columns[0]:'energy_values'})
    df.dropna(inplace=True)
    df['parameters'] = df['parameters'].str.replace(" ","_").str.lower().str.strip().str.split(".", expand=True)[0]
    values_needed = ['active_energy_imp','active_energy_exp','apparent_energy_imp',
                 'reactive_energy_imp','reactive_energy_exp']
    df = df[df['parameters'].isin(values_needed)]

    # GET UNITS AND MULTIPLY
    units = df_rates.loc[0, 'parameters'].split(".")[1].strip().strip("()")
    if units == 'MWh':
        units_multiplier = 1000

    elif units == 'kWh':
        units_multiplier = 1

    elif units == 'GWh':
        units_multiplier = 1000000

    print(units_multiplier)

    df_rates['parameters'] = df_rates['parameters'].str.replace(" ","_").str.lower().str.strip().str.split(".", expand=True)[0]
    df_rates = df_rates.head(2)

    cumulative_import = df.loc[df['parameters'] == 'active_energy_imp', 'energy_values'].values[0]
    cumulative_export = df.loc[df['parameters'] == 'active_energy_exp', 'energy_values'].values[0]
    apparent_import = df.loc[df['parameters'] == 'apparent_energy_imp', 'energy_values'].values[0]
    reactive_import = df.loc[df['parameters'] == 'reactive_energy_imp', 'energy_values'].values[0]
    reactive_export = df.loc[df['parameters'] == 'reactive_energy_exp', 'energy_values'].values[0]

    rate1 = df_rates.loc[0, 'Rate 1']
    rate2 = df_rates.loc[0, 'Rate 2']
    rate3 = df_rates.loc[0, 'Rate 3']

    rate4 = df_rates.loc[1, 'Rate 1']
    rate5 = df_rates.loc[1, 'Rate 2']
    rate6 = df_rates.loc[1, 'Rate 3']

    # billing_values = {'cumulative_import': cumulative_import,'cumulative_export': cumulative_export,'apparent_import': apparent_import,
    # 'reactive_import': reactive_import, 'reactive_export': reactive_export, 'rate1': rate1, 'rate2': rate2, 'rate3': rate3,
    # 'rate4': rate4,'rate5': rate5,'rate6': rate6
    # }
    # # MULTIPLY THE FLOAT VALUES
    # for key, value in billing_values.items():
    #     billing_values[key] = float(value) * units_multiplier

    columns_to_assign_na = ['vt_ratio', 'ct_ratio', 'date_of_last_reset', 
    'max_dem1','max_dem1_datetime','max_dem2','max_dem2_datetime','max_dem3','max_dem3_datetime']

    new_df = pd.DataFrame(columns=['cumulative_import', 'cumulative_export','apparent_import','reactive_import',
    'reactive_export','rate1', 'rate2', 'rate3', 'rate4', 'rate5', 'rate6'])

    row1 = pd.DataFrame({
    'cumulative_import': [cumulative_import],'cumulative_export': [cumulative_export],'apparent_import': [apparent_import],
    'reactive_import': [reactive_import],'reactive_export': [reactive_export],'rate1': [rate1],'rate2': [rate2],
    'rate3': [rate3],'rate4': [rate4],'rate5': [rate5],'rate6': [rate6]})


    new_df = pd.concat([new_df, row1], ignore_index = True)
    new_df = new_df.astype(float) * units_multiplier
    #new_df


    for column in columns_to_assign_na:
        new_df[column] = pd.NA

    new_df['serial_no'] = serial_no
    new_df['reading_date'] = datetime.now().replace(second=0, microsecond=0)
    new_df['no_of_resets'] = 1
    new_df['programing_count'] = 1
    new_df['billing_period'] = billing_date

    billing_values = new_df.iloc[0].to_dict()
    print(cumulative_import, cumulative_export)
    print(billing_values)

    result = store_files_data(form_data = billing_values, db=db, data=data)

    if result == "Data stored successfully":
        return result
  


def confirm_meter_type(db, data, filepath,meter_no):
    meter = db.session.query(energyMeters).filter(energyMeters.serial_no == meter_no).first()
    print("METER: ", meter)
    if meter.meter_type == "LGE650":
        print("meter is Landis and Gyr")
        return "Data stored successfully"

    elif meter.meter_type == "CEWE Prometer 100":
        print("meter is Pro100")
        return "Data stored successfully"

    elif meter.meter_type == "CEWE Prometer":
        print("meter is Pro100")
        return "Data stored successfully"

    elif meter.meter_type == "Elster A1700":
        print("meter is Elster A1700")
        return "Data stored successfully"
    
def process_landis_data(db, filepath,filename, data):
    # Read the Excel file
    serial_no = filename[3:].split("-")[0].strip()
    df = pd.read_excel(filepath)
    df = df.drop(index=0).reset_index(drop=True)
    df = df.drop(df.columns[0], axis=1)
    units = ['kWh', 'kVAh','kvarh','MVA']
    max_dem_time = ['9.6.1;','9.6.2;','9.6.3;']
    #print(df.columns)
    for column in df.columns.to_list()[1:]:
        if any(substring in column for substring in units):
            new_column_name = column.split(":", 1)[1].split(' ')[0].split(';')[0]
            #print(column)
            df = df.rename(columns={column: new_column_name})

        elif any(substring in column for substring in max_dem_time):
            new_column_name = f"{column.split(':', 1)[1].split(';')[0]}_MDT"
            #print(column)
            df = df.rename(columns={column: new_column_name})
        

    df['9.6.3_MDT'] = df['9.6.3_MDT'].str.split('(', n=1).str[0]
    df['9.6.2_MDT'] = df['9.6.2_MDT'].str.split('(', n=1).str[0]
    df['9.6.1_MDT'] = df['9.6.1_MDT'].str.split('(', n=1).str[0]

    df['9.6.3_MDT'] = pd.to_datetime(df['9.6.3_MDT'])
    df['9.6.2_MDT'] = pd.to_datetime(df['9.6.2_MDT'])
    df['9.6.1_MDT'] = pd.to_datetime(df['9.6.1_MDT'])

    new_df_columns = {'1.9.1':'rate1', '1.9.2':'rate2', '1.9.3':'rate3', '2.9.1':'rate4', '2.9.2':'rate5',
       '2.9.3':'rate6', '2.8.0':'cumulative_export', '10.8.0':'apparent_export', 
       '4.8.0':'reactive_export', '1.8.0':'cumulative_import', '9.8.0':'apparent_import', 
       '3.8.0':'reactive_import', '9.6.1':'max_dem1','9.6.1_MDT':'max_dem1_datetime',
         '9.6.2':'max_dem2', '9.6.2_MDT':'max_dem2_datetime', '9.6.3':'max_dem3', 
         '9.6.3_MDT':'max_dem3_datetime'}
    df = df.rename(columns=new_df_columns)
    df = df.rename(columns={'0-0:1.0.0':'billing_period'})
    df['billing_period'] = pd.to_datetime(df['billing_period']).dt.date

    new_df_columns = ['billing_period','cumulative_import','cumulative_export','rate1','rate2','rate3','rate4','rate5','rate6',
                    'apparent_import','reactive_import', 'reactive_export',
                    'max_dem1','max_dem1_datetime','max_dem2','max_dem2_datetime','max_dem3','max_dem3_datetime']
    df = df[new_df_columns]

    df['serial_no'] = serial_no 
    df['reading_date'] = datetime.now().replace(second=0, microsecond=0)
    df['vt_ratio'] = pd.NA
    df['ct_ratio'] = pd.NA 
    df['no_of_resets'] = pd.NA
    df['date_of_last_reset'] = pd.NA 
    df['programing_count'] = pd.NA 

    #df.to_excel("landis.xlsx", index=False)
    billing_values = df.iloc[0].to_dict()

    #print(billing_values)
    result = store_files_data(form_data = billing_values, db=db, data=data)

    if result == "Data stored successfully":
        return result
    

def process_Elster_data(db, filepath,filename, data):
    with open(filepath, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        #Loop through each row and check if any cell contains '----'
        for row in reader:
            if any('----' in cell for cell in row):
                for item in row:
                    if item.startswith("---"):
                        serial_no = item.split(" ")[0].replace("-"," ").strip()
                        #print(row)  # Print the row containing the pattern
                        #print(serial_no)
                        break
                    
    with open(filepath, newline='', encoding='utf-8') as file:    
        reader = csv.reader(file)
        i = 0
        for row in reader:        
            if "Historical Data Set" in row[1]:
                #print(i)
                break
            else:
                i+= 1
    file.close()

    # read csv pandas file
    df = pd.read_csv(filepath, skiprows=range(i))

    df = df[[df.columns[3],df.columns[4],df.columns[5],df.columns[6]]]
    df = df.rename(columns={df.columns[0]:'column1',df.columns[1]:'column2',df.columns[2]:'column3',df.columns[3]:'column4'})

    first_index_imp = df[df['column2'] == 'Import Wh'].index[0] 
    cumulative_import = df.at[first_index_imp, 'column1'].replace(",","")

    first_index_exp = df[df['column2'] == 'Import Wh'].index[0] 
    cumulative_export = df.at[first_index_exp, 'column1'].replace(",","")

    apparent_import_index = df[df['column2'] == 'Total VAh'].index[0] 
    apparent_import = df.at[apparent_import_index, 'column1'].replace(",","")

    first_Q_react_imp = df[df['column2'] == 'Q1 varh'].index[0]
    second_Q_react_imp = df[df['column2'] == 'Q2 varh'].index[0]
    reactive_import = float(df.at[first_Q_react_imp, 'column1'].replace(",","")) + float(df.at[second_Q_react_imp, 'column1'].replace(",",""))

    first_Q_react_exp = df[df['column2'] == 'Q3 varh'].index[0]
    second_Q_react_exp = df[df['column2'] == 'Q4 varh'].index[0]
    reactive_export = float(df.at[first_Q_react_exp, 'column1'].replace(",","")) + float(df.at[second_Q_react_exp, 'column1'].replace(",",""))

    rate1 = df.loc[df['column1'] == 'Rate 1', 'column2'].iloc[0].replace(",","")
    rate2 = df.loc[df['column1'] == 'Rate 2', 'column2'].iloc[0].replace(",","")
    rate3 = df.loc[df['column1'] == 'Rate 3', 'column2'].iloc[0].replace(",","")

    rate4 = df.loc[df['column1'] == 'Rate 4', 'column2'].iloc[0].replace(",","")
    rate5 = df.loc[df['column1'] == 'Rate 5', 'column2'].iloc[0].replace(",","")
    rate6 = df.loc[df['column1'] == 'Rate 6', 'column2'].iloc[0].replace(",","")

    ## MAXIMUM DEMANDS
    max_dem1 = df.loc[df['column1'] == 'MD 1a', 'column2'].iloc[0].replace(",","")
    max_dem1_time = df.loc[df['column1'] == 'MD 1a', 'column4'].iloc[0]

    ## MAXIMUM DEMANDS
    max_dem2 = df.loc[df['column1'] == 'MD 2a', 'column2'].iloc[0].replace(",","")
    max_dem2_time = df.loc[df['column1'] == 'MD 2a', 'column4'].iloc[0]

    max_dem3 = df.loc[df['column1'] == 'MD 3a', 'column2'].iloc[0].replace(",","")
    max_dem3_time = df.loc[df['column1'] == 'MD 3a', 'column4'].iloc[0]

    #COUNT
    billing_count = df.loc[df['column1'] == 'Count', 'column2'].iloc[0]

    #BILLING PERIOD
    billing_end = df.loc[df['column1'] == 'Period End', 'column2'].iloc[0]

    dt1 = datetime.strptime(max_dem1_time, "%A, %B %d, %Y %I:%M:%S %p")
    max_dem1_time = dt1.strftime("%Y-%d-%m %H:%M")

    dt2 = datetime.strptime(max_dem2_time, "%A, %B %d, %Y %I:%M:%S %p")
    max_dem2_time = dt2.strftime("%Y-%d-%m %H:%M")

    dt3 = datetime.strptime(max_dem3_time, "%A, %B %d, %Y %I:%M:%S %p")
    max_dem3_time = dt3.strftime("%Y-%d-%m %H:%M")

    dt = datetime.strptime(billing_end, "%A, %B %d, %Y %I:%M %p")
    billing_period = dt.strftime("%Y-%m-%d")

    billing_values ={'serial_no':serial_no,'billing_period':billing_period,'cumulative_import': cumulative_import,
    'cumulative_export': cumulative_export,'apparent_import':apparent_import,'reactive_import':reactive_import,
    'reactive_export':reactive_export,'rate1': rate1,'rate2': rate2,'rate3': rate3,'rate4': rate4,'rate5': rate5,
    'rate6':rate6,'no_of_resets':billing_count,'max_dem1':max_dem1,'max_dem1_datetime':max_dem1_time,'max_dem2':max_dem2,
    'max_dem2_datetime':max_dem2_time,'max_dem3':max_dem3,'max_dem3_datetime':max_dem3_time,
    'vt_ratio': pd.NA, 'ct_ratio': pd.NA, 'date_of_last_reset': datetime.now().replace(second=0, microsecond=0) , 'programing_count': 1,
    'reading_date':datetime.now().replace(second=0, microsecond=0)}

    #print(billing_values)
    result = store_files_data(form_data = billing_values, db=db, data=data)

    if result == "Data stored successfully":
        return result
  
