import pandas as pd
import numpy as np
import openpyxl
from datetime import datetime
import gc


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


