import pandas as pd
import numpy as np
import openpyxl
from datetime import datetime
import gc
from models import energyMeters


def store_pro100_data(files, db):
    serial_no = files[0].split("-")[0].strip()
    df = pd.read_excel(files[0])
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

    # GET RATES
    df2 = pd.read_excel(files[1])
    df2 = df2.drop(index=[0, 1]).reset_index(drop=True) #drop the first two rows

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

    columns_to_assign_na = ['vt_ratio', 'ct_ratio', 'no_of_resets', 'date_of_last_reset', 'programing_count',
                        'max_dem1','max_dem1_datetime','max_dem2','max_dem2_datetime','max_dem3','max_dem3_datetime']

    for column in columns_to_assign_na:
        df[column] = pd.NA


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
    
def process_landis_data(filepath,data, db,filename):
    # Read the Excel file
    serial_no = filename[3:].split("-")[0].strip()
    serial_no
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
    new_df_columns = ['rate1','rate2','rate3','rate4','rate5','rate6','cumulative_export','apparent_export', 
                    'reactive_export','cumulative_import','apparent_import','reactive_import', 
                    'max_dem1','max_dem1_datetime','max_dem2','max_dem2_datetime','max_dem3','max_dem3_datetime']
    df = df[new_df_columns]

    df['serial_no'] = serial_no 
    df['reading_date'] = datetime.now().replace(second=0, microsecond=0)
    df['vt_ratio'] = pd.NA  
    df['ct_ratio'] = pd.NA  
    df['no_of_resets'] = pd.NA  
    df['date_of_last_reset'] = pd.NA  
    df['programing_count'] = pd.NA  

    return "Data stored successfully"

