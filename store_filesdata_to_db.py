from models import monthlyBillingData

def store_files_data(form_data, db,data):
    # Check if the record already exists in the database
    existing_record = monthlyBillingData.query.filter_by(serial_no=form_data['serial_no'], 
    billing_period=form_data['billing_period'],meter_category=data['meterCategoryFile'],    
    sub_ipp_name = data['subIppNameFile'],node_name=data['nodeNameFile']).first()    
       
    if existing_record:
        # Update existing record
        print("record exists")
        #existing_record.meter_category = form_data['meterCategoryManual']
        #existing_record.node_name = form_data['nodeNameManual']
        existing_record.reading_date = form_data['reading_date']
        existing_record.cumulative_import = form_data['cumulative_import']
        existing_record.cumulative_export = form_data['cumulative_export']
        existing_record.rate1 = form_data['rate1']
        existing_record.rate2 = form_data['rate2']
        existing_record.rate3 = form_data['rate3']
        existing_record.rate4 = form_data['rate4']
        existing_record.rate5 = form_data['rate5']
        existing_record.rate6 = form_data['rate6']
        existing_record.max_dem1 = form_data['max_dem1']
        existing_record.max_dem1_datatime = form_data['max_dem1_datetime']
        existing_record.max_dem2 = form_data['max_dem2']
        existing_record.max_dem2_datatime = form_data['max_dem2_datetime']
        existing_record.max_dem3 = form_data['max_dem3']
        existing_record.max_dem3_datatime = form_data['max_dem3_datetime']
        existing_record.reactive_import = form_data['reactive_import']
        existing_record.reactive_export = form_data['reactive_export']
        existing_record.apparent_import = form_data['apparent_import']
        existing_record.no_of_resets = form_data['no_of_resets']
        existing_record.date_of_last_reset = form_data['date_of_last_reset']
        existing_record.programing_count = form_data['programing_count']
        existing_record.CT_ratio = form_data['ct_ratio']
        existing_record.VT_ratio = form_data['vt_ratio']
        
        message = "Data stored successfully"
    else:
        # Insert new record
        new_billing_data = monthlyBillingData(
            meter_category=data['meterCategoryFile'],
            sub_ipp_name = data['subIppNameFile'],
            node_name=data['nodeNameFile'],
            billing_period=form_data['billing_period'],
            serial_no=form_data['serial_no'],
            reading_date= form_data['reading_date'],
            cumulative_import=form_data['cumulative_import'],
            cumulative_export=form_data['cumulative_export'],
            rate1=form_data['rate1'],
            rate2=form_data['rate2'],
            rate3=form_data['rate3'],
            rate4=form_data['rate4'],
            rate5=form_data['rate5'],
            rate6=form_data['rate6'],
            max_dem1=form_data['max_dem1'],
            max_dem1_datatime=form_data['max_dem1_datetime'],
            max_dem2=form_data['max_dem2'],
            max_dem2_datatime=form_data['max_dem2_datetime'],
            max_dem3=form_data['max_dem3'],
            max_dem3_datatime=form_data['max_dem3_datetime'],
            reactive_import=form_data['reactive_import'],
            reactive_export=form_data['reactive_export'],
            apparent_import=form_data['apparent_import'],
            no_of_resets=form_data['no_of_resets'],
            date_of_last_reset=form_data['date_of_last_reset'],
            programing_count=form_data['programing_count'],
            CT_ratio=form_data['ct_ratio'],
            VT_ratio=form_data['vt_ratio']
        )
        db.session.add(new_billing_data)
        message = "Data stored successfully"

    # Commit the transaction
    db.session.commit()
    return message
