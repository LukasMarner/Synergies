## Data processing smart meter measurements BH
import pandas as pd
# from sklearn.neighbors import LocalOutlierFactor

def get_measurement_dfs(smart_meter_measurements, name):
    columns = [col for col in smart_meter_measurements.columns if name in col]
    measurement_df = smart_meter_measurements[columns]
    return measurement_df

def get_measurement_dfs_new(smart_meter_measurements, prod_or_con, name):
    columns = [col for col in smart_meter_measurements.columns if name in col]
    measurement_df = smart_meter_measurements[columns]
    prod_or_con_df = prod_or_con[columns]
    return measurement_df, prod_or_con_df

def processing_measurements(measurement_df, measurement_number):
    # Choose the row index to check for -1 or -2
    # if 'datetime' in measurement_df.columns:
    #     measurement_df= measurement_df.drop(columns='datetime')
    row_index_to_check = 2

    # Create masks to check for -1 and -2 in the chosen row
    mask_minus_one = measurement_df.iloc[row_index_to_check] == '-1'
    mask_minus_two = measurement_df.iloc[row_index_to_check] == '-2'

    # Ensure we do not go out of bounds when checking the next row
    if row_index_to_check + 1 < len(measurement_df):
        # Select the next row
        next_row = measurement_df.iloc[row_index_to_check + measurement_number]

        # Sum the values of the next row where the mask for -1 is True
        sum_next_row_minus_one = next_row[mask_minus_one].sum()
        # print(f"Sum of values in the next row where the current row contains -1: {sum_next_row_minus_one}")

        # Sum the values of the next row where the mask for -2 is True
        sum_next_row_minus_two = next_row[mask_minus_two].sum()
        # print(f"Sum of values in the next row where the current row contains -2: {sum_next_row_minus_two}")
    else:
        # print("There is no next row to sum the values from.")
        sum_next_row_minus_two = 0
        sum_next_row_minus_one = 0
    
    consumption = sum_next_row_minus_one
    production = sum_next_row_minus_two
    return consumption, production



def processing_measurements_new(measurement_df, prod_or_con_df, measurement_number):
    # Choose the row index to check for -1 or -2
    # row_index_to_check = 2

    mask_minus_one = prod_or_con_df.iloc[0] == '-1'
    mask_minus_two = prod_or_con_df.iloc[0] == '-2'

    # # Create masks to check for -1 and -2 in the chosen row
    # mask_minus_one = measurement_df.iloc[row_index_to_check] == '-1'
    # mask_minus_two = measurement_df.iloc[row_index_to_check] == '-2'

    # Ensure we do not go out of bounds when checking the next row
    if measurement_number < len(measurement_df):
        # Select the next row
        next_row = measurement_df.iloc[measurement_number]

        # Sum the values of the next row where the mask for -1 is True
        sum_next_row_minus_one = next_row[mask_minus_one].sum()
        # print(f"Sum of values in the next row where the current row contains -1: {sum_next_row_minus_one}")

        # Sum the values of the next row where the mask for -2 is True
        sum_next_row_minus_two = next_row[mask_minus_two].sum()
        # print(f"Sum of values in the next row where the current row contains -2: {sum_next_row_minus_two}")
    else:
        # print("There is no next row to sum the values from.")
        sum_next_row_minus_two = 0
        sum_next_row_minus_one = 0
    
    consumption = sum_next_row_minus_one
    production = sum_next_row_minus_two
    return consumption, production

def aggregated_measurements_substation_demo(smart_meter_measurements_sorted, prod_or_con, measurement_number = 1):
    substations = ['Åkirkeby', 'Allinge', 'Bodilsker', 'Gudhjem', 'Hasle', 'Nexø','Olsker', 'Østerlars','Povlsker', 'Rønne Nord', 'Rønne Syd', 'Snorrebakken', 'Svaneke', 'Værket', 'Vesthavnen', 'Viadukten']
    
    # measurement_prod_cons = pd.DataFrame()    
    measurement_prod_cons = pd.DataFrame(columns=['Substation', 'Consumption', 'Production'])

    for substation in substations:
        measurement_df, prod_or_con_df = get_measurement_dfs_new(smart_meter_measurements_sorted, prod_or_con, substation)
        consumption, production = processing_measurements_new(measurement_df,prod_or_con_df, measurement_number)
                # Create a DataFrame for the new row
        new_row = pd.DataFrame([{
            'Substation': substation,
            'Consumption': consumption/1000, #convert to MWh,
            'Production': production/1000 #convert to MWh
        }])
    

        # Append the new row to the DataFrame
        # measurement_prod_cons = measurement_prod_cons.append(new_row, ignore_index=True)
        measurement_prod_cons = pd.concat([measurement_prod_cons, new_row], ignore_index=True)

        # Optionally, reset the index if needed
        measurement_prod_cons.reset_index(drop=True, inplace=True)
    return measurement_prod_cons
    


def aggregated_measurements_substation(smart_meter_measurements, measurement_number = 1):
    substations = ['Åkirkeby', 'Allinge', 'Bodilsker', 'Gudhjem', 'Hasle', 'Nexø','Olsker', 'Østerlars','Povlsker', 'Rønne Nord', 'Rønne Syd', 'Snorrebakken', 'Svaneke', 'Værket', 'Vesthavnen', 'Viadukten']


    # measurement_df = get_measurement_dfs(smart_meter_measurements, 'Åkirkeby')
    # consumption, production = processing_measurements(measurement_df)

    # measurement_prod_cons = pd.DataFrame()    
    measurement_prod_cons = pd.DataFrame(columns=['Substation', 'Consumption', 'Production'])

    for substation in substations:
        measurement_df = get_measurement_dfs(smart_meter_measurements, substation)
        consumption, production = processing_measurements(measurement_df, measurement_number)
        # new_row = {
        #     'Substation': substation,
        #     'Consumption': consumption,
        #     'Production': production
        # }

        # Create a DataFrame for the new row
        new_row = pd.DataFrame([{
            'Substation': substation,
            'Consumption': consumption/1000, #convert to MWh,
            'Production': production/1000 #convert to MWh
        }])
    

        # Append the new row to the DataFrame
        # measurement_prod_cons = measurement_prod_cons.append(new_row, ignore_index=True)
        measurement_prod_cons = pd.concat([measurement_prod_cons, new_row], ignore_index=True)

        # Optionally, reset the index if needed
        measurement_prod_cons.reset_index(drop=True, inplace=True)
    return measurement_prod_cons

def fix_datetime(smart_meter_measurements):
    smart_meter_measurements_new = smart_meter_measurements
    smart_meter_measurements_new['datetime'] = pd.to_datetime(smart_meter_measurements['Unnamed: 0'][3:] + ' ' + smart_meter_measurements['60 kV station'][3:], format='%d-%m-%Y %H:%M')
    #  Sort the DataFrame by the new datetime column
    smart_meter_measurements_sorted = smart_meter_measurements_new.sort_values(by='datetime')
    return smart_meter_measurements_sorted

def time_series_per_substation(smart_meter_measurements_sorted, prod_or_con):
    # time_series_substation = pd.DataFrame()
    # time_series_substation['datetime'] = smart_meter_measurements_sorted['datetime'].reset_index(drop=True)
    # substations = ['Åkirkeby', 'Allinge', 'Bodilsker', 'Gudhjem', 'Hasle', 'Nexø','Olsker', 'Østerlars','Povlsker', 'Rønne Nord', 'Rønne Syd', 'Snorrebakken', 'Svaneke', 'Værket', 'Vesthavnen', 'Viadukten']
    # for substation in substations:
    #     production_list = []
    #     consumption_list = []
    #     measurement_df = get_measurement_dfs(smart_meter_measurements_sorted, substation)
    #     for i in range(len(smart_meter_measurements_sorted)):
    #         consumption, production = processing_measurements(measurement_df, i)
    #         production_list.append(production)
    #         consumption_list.append(consumption)

    #     # Combine the results into a list of lists
    #     prod_con = list(zip(production_list, consumption_list))
    #     time_series_substation[substation] = prod_con
    # substation = 'Åkirkeby'
# prod_con = []
    time_series_substation = pd.DataFrame()
    # datetime = pd.to_datetime(smart_meter_measurements_sorted['Unnamed: 0'][:] + ' ' + smart_meter_measurements_sorted['60 kV station'][3:], format='%d-%m-%Y %H:%M')
    # time_series_substation['datetime'] = smart_meter_measurements_sorted['datetime'].reset_index(drop=True)
    time_series_substation['datetime'] = smart_meter_measurements_sorted['datetime'].iloc[:-3].reset_index(drop=True)
    substations = ['Åkirkeby', 'Allinge', 'Bodilsker', 'Gudhjem', 'Hasle', 'Nexø','Olsker', 'Østerlars','Povlsker', 'Rønne Nord', 'Rønne Syd', 'Snorrebakken', 'Svaneke', 'Værket', 'Vesthavnen', 'Viadukten']
    for substation in substations:
        production_list = []
        consumption_list = []
        measurement_df, prod_or_con_df = get_measurement_dfs_new(smart_meter_measurements_sorted, prod_or_con, substation)
        for i in range(len(smart_meter_measurements_sorted)-3):
            consumption, production = processing_measurements_new(measurement_df, prod_or_con_df, i)
            production_list.append(production)
            consumption_list.append(consumption)
        # Combine the results into a list of lists
        prod_con = list(zip(production_list, consumption_list))
        time_series_substation[substation] = prod_con
    
    total_production = []
    total_consumption = []
    # Iterate through each row to calculate the sum of production and consumption
    for index, row in time_series_substation.iterrows():
        prod_sum = 0
        cons_sum = 0
        for substation in substations:
            production, consumption = row[substation]
            prod_sum += production
            cons_sum += consumption
        total_production.append(prod_sum)
        total_consumption.append(cons_sum)
    time_series_substation['Total production'] = total_production
    time_series_substation['Total consumption'] = total_consumption

    return time_series_substation

def get_prod_con_per_substation(time_series_substation):
    # Extract production values for each substation
    substations = ['Åkirkeby','Allinge', 'Bodilsker', 'Gudhjem', 'Hasle', 'Nexø','Olsker', 'Østerlars','Povlsker', 'Rønne Nord', 'Rønne Syd', 'Snorrebakken', 'Svaneke', 'Værket', 'Vesthavnen', 'Viadukten']
    for substation in substations:
        time_series_substation[f'{substation}_production'] = time_series_substation[substation].apply(lambda x: x[0])
        time_series_substation[f'{substation}_consumption'] = time_series_substation[substation].apply(lambda x: x[1])
    time_series_substation_prod_con = time_series_substation
    return time_series_substation_prod_con

def time_series_per_substation_v2(smart_meter_measurements_sorted, prod_or_con):
    # Create the initial DataFrame with datetime column
    time_series_substation = pd.DataFrame()
    time_series_substation['datetime'] = smart_meter_measurements_sorted['datetime'].iloc[:-3].reset_index(drop=True)

    substations = ['A', 'B', 'C']

    # Dictionary to store production and consumption for each substation
    substation_data = {}

    for substation in substations:
        # Get the measurement DataFrame and production/consumption DataFrame
        measurement_df, prod_or_con_df = get_measurement_dfs_new(smart_meter_measurements_sorted, prod_or_con, substation)

        # Use apply to process each row and get production and consumption
        prod_con_list = measurement_df.iloc[:-3].apply(
            lambda row, idx: processing_measurements_new(measurement_df, prod_or_con_df, idx), axis=1, result_type='expand', args=(measurement_df.index,)
        ).tolist()


        # Convert the list of tuples into two separate lists for production and consumption
        production_list, consumption_list = zip(*prod_con_list)

        # Store in the dictionary
        substation_data[substation] = (production_list, consumption_list)

    # Populate the DataFrame with the results
    for substation in substations:
        production_list, consumption_list = substation_data[substation]
        time_series_substation[f'{substation}_production'] = production_list
        time_series_substation[f'{substation}_consumption'] = consumption_list

    # Calculate total production and consumption for each row
    time_series_substation['Total production'] = time_series_substation[[f'{substation}_production' for substation in substations]].sum(axis=1)
    time_series_substation['Total consumption'] = time_series_substation[[f'{substation}_consumption' for substation in substations]].sum(axis=1)

    return time_series_substation

def time_series_per_substation_v3(smart_meter_measurements_sorted, prod_or_con):
    # Create the initial DataFrame with the datetime column, excluding the last 3 rows for alignment
    time_series_substation = pd.DataFrame()
    time_series_substation['datetime'] = smart_meter_measurements_sorted['datetime'].iloc[:-3].reset_index(drop=True)

    substations = ['Åkirkeby', 'Allinge', 'Bodilsker', 'Gudhjem', 'Hasle', 'Nexø','Olsker', 'Østerlars','Povlsker', 'Rønne Nord', 'Rønne Syd', 'Snorrebakken', 'Svaneke', 'Værket', 'Vesthavnen', 'Viadukten']

    # Dictionary to store production and consumption for each substation
    substation_data = {}

    for substation in substations:
        # Get the measurement DataFrame and production/consumption DataFrame for the substation
        measurement_df, prod_or_con_df = get_measurement_dfs_new(smart_meter_measurements_sorted, prod_or_con, substation)

        # Use list comprehension to process each row index and get production and consumption
        prod_con_list = [
            processing_measurements_new(measurement_df, prod_or_con_df, i)
            for i in range(len(measurement_df) - 3)
        ]

        # Convert the list of tuples into two separate lists for production and consumption
        production_list, consumption_list = zip(*prod_con_list)

        # Store in the dictionary
        substation_data[substation] = (production_list, consumption_list)

    # Populate the DataFrame with the results
    for substation in substations:
        production_list, consumption_list = substation_data[substation]
        time_series_substation[f'{substation}_production'] = production_list
        time_series_substation[f'{substation}_consumption'] = consumption_list

    # Calculate total production and consumption for each row
    time_series_substation['Total production'] = time_series_substation[[f'{substation}_production' for substation in substations]].sum(axis=1)
    time_series_substation['Total consumption'] = time_series_substation[[f'{substation}_consumption' for substation in substations]].sum(axis=1)

    return time_series_substation


def get_scada_measurements_transformers(smart_meter_measurements, measurement_number = 1):
    substations = ['Åkirkeby', 'Allinge', 'Bodilsker', 'Gudhjem', 'Hasle', 'Nexø','Olsker', 'Østerlars','Povlsker', 'Rønne Nord', 'Rønne Syd', 'Snorrebakken', 'Svaneke', 'Værket', 'Vesthavnen', 'Viadukten']


    # measurement_df = get_measurement_dfs(smart_meter_measurements, 'Åkirkeby')
    # consumption, production = processing_measurements(measurement_df)

    # measurement_prod_cons = pd.DataFrame()    
    measurement_prod_cons = pd.DataFrame(columns=['Substation', 'Consumption', 'Production'])

    for substation in substations:
        measurement_df = get_measurement_dfs(smart_meter_measurements, substation)
        consumption, production = processing_measurements(measurement_df, measurement_number)
        # new_row = {
        #     'Substation': substation,
        #     'Consumption': consumption,
        #     'Production': production
        # }

        # Create a DataFrame for the new row
        new_row = pd.DataFrame([{
            'Substation': substation,
            'Consumption': consumption/1000, #convert to MWh,
            'Production': production/1000 #convert to MWh
        }])
    

        # Append the new row to the DataFrame
        # measurement_prod_cons = measurement_prod_cons.append(new_row, ignore_index=True)
        measurement_prod_cons = pd.concat([measurement_prod_cons, new_row], ignore_index=True)

        # Optionally, reset the index if needed
        measurement_prod_cons.reset_index(drop=True, inplace=True)
    return measurement_prod_cons

# def find_optimal_k():
#     from sklearn.neighbors import LocalOutlierFactor

# # # Example data with potential outliers
# # data = {
# #     'Feature1': [10, 12, 14, 15, 20, 25, 30, 1000, 1100, 1200],  # Outliers at the end
# #     'Feature2': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# # }
# # df = pd.DataFrame(data)

# # Range of k values to test
# k_values = range(100, 150)

# # List to store mean LOF scores
# lof_scores = []

# # Perform LOF for each k
# for k in k_values:
#     lof = LocalOutlierFactor(n_neighbors=k)
#     lof.fit(df[['TotalLoad']])
#     lof_score = -lof.negative_outlier_factor_
#     lof_scores.append(lof_score.mean())

# # Determine the optimal k
# optimal_k = k_values[np.argmax(lof_scores)]
# print(f"The optimal number of neighbors for LOF is {optimal_k}")

# # Plot mean LOF score for each k
# plt.plot(k_values, lof_scores)
# plt.xlabel('Number of Neighbors (k)')
# plt.ylabel('Mean LOF Score')
# plt.title('LOF Mean Score for Different k values')
# plt.axvline(optimal_k, color='r', linestyle='--')
# plt.show()



# def time_series_per_substation(smart_meter_measurements_sorted):
#     substations = ['Åkirkeby', 'Allinge', 'Bodilsker', 'Gudhjem', 'Hasle', 'Nexø','Olsker', 'Østerlars','Povlsker', 'Rønne Nord', 'Rønne Syd', 'Snorrebakken', 'Svaneke', 'Værket', 'Vesthavnen', 'Viadukten']
#     for substation in substations:
#         for i in range(len(smart_meter_measurements)-3):

#             measurement_df = get_measurement_dfs(smart_meter_measurements, substation)
#             consumption, production = processing_measurements(measurement_df, i)
#             prod_con_data = [production, consumption]
#             prod_con.append(prod_con_data)




#     production_substation = []
#     consumption_substation = []

#                 [consumption, production] 

#     time_series_substation = pd.DataFrame()
#     time_series_substation['datetime'] = smart_measurements_sorted['datetime']
#     for substation, prod_con_data in zip(substations, new_data):
#     time_series_substation[substation] = prod_con_data
#     time_series_substation['substation'] = 

    
import cmath
import math 
import numpy as np
import os
def get_trafo_measurement(timestamp, csv_path, voltage=10.5):
    # Use the provided CSV path instead of constructing it internally
    scada_measurements = pd.read_csv(csv_path)
    scada_measurements['ts'] = pd.to_datetime(scada_measurements['ts'])

    ## Clean column names
    original_columns = scada_measurements.columns

    # Process column names to extract the first part before the first ' | '
    cleaned_columns = [col.split(' | ')[0] for col in original_columns]

    # Assign the cleaned column names back to the DataFrame
    scada_measurements.columns = cleaned_columns

    scada_measurements.fillna(method='ffill', inplace=True)
    scada_measurements.fillna(method='bfill', inplace=True)

    scada_measurements.dropna(axis=1, inplace=True)
    scada_measurements['ts'] = pd.to_datetime(scada_measurements['ts'])

    timestamp = pd.to_datetime(timestamp)

        # Retrieve the row(s) at the specific timestamp
    values_at_timestamp = scada_measurements[scada_measurements['ts'] == timestamp]

    if values_at_timestamp.empty:
        time_diffs = (scada_measurements['ts'] - timestamp).abs()
        # Find the index of the minimum difference
        closest_index = time_diffs.idxmin()
        # Retrieve the row corresponding to the closest timestamp
        closest_values = scada_measurements.loc[closest_index]
        values_at_timestamp = closest_values

    ## Check if current if flowing in which transformer
    if (('t1s_belastning' in values_at_timestamp) and (values_at_timestamp['t1s_belastning'] > 1)).all():
        trafo = 't1s'
    elif (('t2s_belastning' in values_at_timestamp) and (values_at_timestamp['t2s_belastning'] > 1)).all():
        trafo = 't2s'

    # Check for t2s voltage
    if all(key in values_at_timestamp for key in ['t2s_spendingvl1', 't2s_spendingvl2', 't2s_spendingvl3']):
        if ((values_at_timestamp['t2s_spendingvl1'] > 1).all() and (values_at_timestamp['t2s_spendingvl2'] > 1).all() and (values_at_timestamp['t2s_spendingvl3'] > 1).all()):
            voltage = (values_at_timestamp['t2s_spendingvl1'] + values_at_timestamp['t2s_spendingvl2'] + values_at_timestamp['t2s_spendingvl3']) * math.sqrt(3)

    # Check for t1s voltage
    if all(key in values_at_timestamp for key in ['t1s_spendingvl1', 't1s_spendingvl2', 't1s_spendingvl3']):
        if ((values_at_timestamp['t1s_spendingvl1'] > 1).all() and (values_at_timestamp['t1s_spendingvl2'] > 1).all() and (values_at_timestamp['t1s_spendingvl3'] > 1).all()):
            voltage = (values_at_timestamp['t1s_spendingvl1'] + values_at_timestamp['t1s_spendingvl2'] + values_at_timestamp['t1s_spendingvl3']) * math.sqrt(3)
    
    # if all(key in values_at_timestamp for key in [f'{trafo}_reaktiveffekt', f'{trafo}_aktiveffekt']) | all(key in values_at_timestamp for key in [f'{trafo}_reaktiveeffekt', f'{trafo}_aktiveffekt']):
    #     power_meas = True
    #     active_power = values_at_timestamp[f'{trafo}_aktiveffekt']
    #     if all(f'{trafo}_reaktiveffekt' in values_at_timestamp):
    #         reactive_power = values_at_timestamp[f'{trafo}_reaktiveffekt'] 
    #     else:
    #         reactive_power = values_at_timestamp[f'{trafo}_reaktiveeffekt']
    # else:
    #     power_meas = False

        # Define the keys to check
    active_power_key = f'{trafo}_aktiveffekt'
    reactive_power_key1 = f'{trafo}_reaktiveffekt'
    reactive_power_key2 = f'{trafo}_reaktiveeffekt'

    # Check for active and reactive power measurements
    if active_power_key in values_at_timestamp and (reactive_power_key1 in values_at_timestamp or reactive_power_key2 in values_at_timestamp):
        power_meas = True
        active_power = values_at_timestamp[active_power_key]
        
        # Assign the correct reactive power key
        reactive_power = values_at_timestamp.get(reactive_power_key1, values_at_timestamp.get(reactive_power_key2))
    else:
        power_meas = False
        active_power = None
        reactive_power = None


    # if ('t2s_spendingvl1' and 't2s_spendingvl2' and 't2s_spendingvl3') in values_at_timestamp and (values_at_timestamp['t2s_spendingvl1'] and values_at_timestamp['t2s_spendingvl2']  and values_at_timestamp['t2s_spendingvl3']) > 1:
    #     voltage = (values_at_timestamp['t2s_spendingvl1'] + values_at_timestamp['t2s_spendingvl2']  + values_at_timestamp['t2s_spendingvl3'])*math.sqrt(3)
    # if ('t1s_spendingvl1' and 't1s_spendingvl2' and 't1s_spendingvl3') in values_at_timestamp and (values_at_timestamp['t1s_spendingvl1'] and values_at_timestamp['t1s_spendingvl2']  and values_at_timestamp['t1s_spendingvl3']) > 1:
    #     voltage = (values_at_timestamp['t1s_spendingvl1'] + values_at_timestamp['t1s_spendingvl2']  + values_at_timestamp['t1s_spendingvl3'])*math.sqrt(3)



    if (power_meas == False):
        if (f'{trafo}_cosphi' in values_at_timestamp):
            angle_in_degrees = values_at_timestamp[f'{trafo}_cosphi']
        elif(f'{trafo}_cosphitrafo1' in values_at_timestamp) | (f'{trafo}_cosphitrafo2' in values_at_timestamp):
            if trafo == 't1s':
                angle_in_degrees= values_at_timestamp[f'{trafo}_cosphitrafo1']
            else:
                angle_in_degrees = values_at_timestamp[f'{trafo}_cosphitrafo2']
            
        angle = math.radians(angle_in_degrees)


        if isinstance(voltage, float):
            voltage_magnitude = voltage
        elif isinstance(voltage, str):
            voltage_magnitude = values_at_timestamp[voltage]
        else:
            voltage_magnitude = voltage
        current_magnitude = values_at_timestamp[f'{trafo}_belastning']
        # i = cmath.rect(current_magnitude, angle)
        # v = cmath.rect(voltage_magnitude, angle)
        i = current_magnitude
        v = voltage_magnitude
        # i = current_magnitude/np.sqrt(2)#, angle
        # v = voltage_magnitude/np.sqrt(2)#, angle
        apparent_power = cmath.rect(v*i, angle)
        #apparent_power = v*np.conjugate(i)
        active_power = apparent_power.real/1000
        reactive_power = apparent_power.imag/1000



    

    return float(active_power), float(reactive_power)



def make_SCADA_df(timestamp, substations, path):
        # Initialize list to hold data
    data = []
    path = path
    # Loop through each substation and get measurements
    for substation, voltage in substations:
        csv = f'{substation}.csv'
        active_power, reactive_power = get_trafo_measurement(timestamp, csv, voltage)
        active_power = float(active_power) if not isinstance(active_power, (float, int)) else active_power
        reactive_power = float(reactive_power) if not isinstance(reactive_power, (float, int)) else reactive_power

        data.append({
            'Substation': substation,
            'Active Power': active_power,
            'Reactive Power': reactive_power
        })

    df_SCADA_meas = pd.DataFrame(data)

    # Fixing the 'Nexo' row
    # Check if 'Nexo' exists in the DataFrame
    # nexo_index = df_SCADA_meas[df_SCADA_meas['Substation'] == 'Nexo'].index

    # if len(nexo_index) > 0:
    #     # Access the first index (assuming only one 'Nexo' entry is intended)
    #     nexo_index = nexo_index[0]

    #     # Extract and replace the scalar value for 'Active Power'
    #     if isinstance(df_SCADA_meas.at[nexo_index, 'Active Power'], pd.Series):
    #         df_SCADA_meas.at[nexo_index, 'Active Power'] = df_SCADA_meas.at[nexo_index, 'Active Power'].iloc[0]

    #     # Extract and replace the scalar value for 'Reactive Power'
    #     if isinstance(df_SCADA_meas.at[nexo_index, 'Reactive Power'], pd.Series):
    #         df_SCADA_meas.at[nexo_index, 'Reactive Power'] = df_SCADA_meas.at[nexo_index, 'Reactive Power'].iloc[0]
        
    #     nexo_index = df_SCADA_meas[df_SCADA_meas['Substation'] == 'Nexo'].index

    # bod_index = df_SCADA_meas[df_SCADA_meas['Substation'] == 'Bodilsker'].index
    # if len(bod_index) > 0:
    #     # Access the first index (assuming only one 'Nexo' entry is intended)
    #     bod_index = bod_index[0]

    #     # Extract and replace the scalar value for 'Active Power'
    #     if isinstance(df_SCADA_meas.at[bod_index, 'Active Power'], pd.Series):
    #         df_SCADA_meas.at[bod_index, 'Active Power'] = df_SCADA_meas.at[bod_index, 'Active Power'].values[0]

    #     # Extract and replace the scalar value for 'Reactive Power'
    #     if isinstance(df_SCADA_meas.at[bod_index, 'Reactive Power'], pd.Series):
    #         df_SCADA_meas.at[bod_index, 'Reactive Power'] = df_SCADA_meas.at[bod_index, 'Reactive Power'].values[0]

    # Handle specific substations
    for substation in ['Nexo', 'Bodilsker', 'Hasle']:
        sub_index = df_SCADA_meas[df_SCADA_meas['Substation'] == substation].index
        if len(sub_index) > 0:
            index = sub_index[0]

            # Directly assign the values, no additional checks
            active_power = df_SCADA_meas.at[index, 'Active Power']
            reactive_power = df_SCADA_meas.at[index, 'Reactive Power']

            # Debug print to check the types again
            print(f"Before: {substation} Active Power Type: {type(active_power)}, Reactive Power Type: {type(reactive_power)}")

            # If active_power or reactive_power is still a Series, access the first value
            if isinstance(active_power, pd.Series):
                active_power = active_power.iloc[0]
            if isinstance(reactive_power, pd.Series):
                reactive_power = reactive_power.iloc[0]

            df_SCADA_meas.at[index, 'Active Power'] = active_power
            df_SCADA_meas.at[index, 'Reactive Power'] = reactive_power
    
    # for substation in ['Nexo', 'Bodilsker', 'Hasle']:
    #     sub_index = df_SCADA_meas[df_SCADA_meas['Substation'] == substation].index
    #     if len(sub_index) > 0:
    #         index = sub_index[0]
    #         active_power = df_SCADA_meas.at[index, 'Active Power']
    #         reactive_power = df_SCADA_meas.at[index, 'Reactive Power']
            
    #         if isinstance(active_power, (pd.Series, list)):
    #             active_power = active_power[0]  # or .iloc[0]

    #         if isinstance(reactive_power, (pd.Series, list)):
    #             reactive_power = reactive_power[0]  # or .iloc[0]

    #         df_SCADA_meas.at[index, 'Active Power'] = active_power
    #         df_SCADA_meas.at[index, 'Reactive Power'] = reactive_power


    # df_SCADA_meas['Active Power'] = pd.to_numeric(df_SCADA_meas['Active Power'], errors='coerce')
    # df_SCADA_meas['Reactive Power'] = pd.to_numeric(df_SCADA_meas['Reactive Power'], errors='coerce')


    # Nexo_row = all(pd.Series(df_SCADA_meas.loc[df_SCADA_meas['Substation'] == 'Nexo']).to_numpy())
    # print(Nexo_row)

    # # nexo_row = Nexo_row.iloc[0]

    # # Extracting Active and Reactive Power values
    # nexo_active_power = Nexo_row['Active Power']
    # nexo_reactive_power = Nexo_row['Reactive Power']


    # nexo_index = Nexo_row.index[0]

    # # Update the main DataFrame with the extracted values
    # df_SCADA_meas.at[nexo_index, 'Active Power'] = nexo_active_power
    # df_SCADA_meas.at[nexo_index, 'Reactive Power'] = nexo_reactive_power
    return df_SCADA_meas


def make_SCADA_df_lukas(timestamp, substations, scada_path=None):
    # Initialize list to hold data
    data = []

    # Loop through each substation and get measurements
    for substation, voltage in substations:
        csv_file = f'{substation}.csv'
        
        # If scada_path is provided, join it with the CSV filename
        if scada_path:
            csv_path = os.path.join(scada_path, csv_file)
        else:
            csv_path = csv_file  # Use just the filename if no path provided
            
        active_power, reactive_power = get_trafo_measurement(timestamp, csv_path, voltage)
        active_power = float(active_power) if not isinstance(active_power, (float, int)) else active_power
        reactive_power = float(reactive_power) if not isinstance(reactive_power, (float, int)) else reactive_power

        data.append({
            'Substation': substation,
            'Active Power': active_power,
            'Reactive Power': reactive_power
        })

    df_SCADA_meas = pd.DataFrame(data)

    # Handle specific substations
    for substation in ['Nexo', 'Bodilsker', 'Hasle']:
        sub_index = df_SCADA_meas[df_SCADA_meas['Substation'] == substation].index
        if len(sub_index) > 0:
            index = sub_index[0]

            # Directly assign the values, no additional checks
            active_power = df_SCADA_meas.at[index, 'Active Power']
            reactive_power = df_SCADA_meas.at[index, 'Reactive Power']

            # Debug print to check the types again
            print(f"Before: {substation} Active Power Type: {type(active_power)}, Reactive Power Type: {type(reactive_power)}")

            # If active_power or reactive_power is still a Series, access the first value
            if isinstance(active_power, pd.Series):
                active_power = active_power.iloc[0]
            if isinstance(reactive_power, pd.Series):
                reactive_power = reactive_power.iloc[0]

            df_SCADA_meas.at[index, 'Active Power'] = active_power
            df_SCADA_meas.at[index, 'Reactive Power'] = reactive_power
    
    return df_SCADA_meas