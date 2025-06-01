#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import pandas as pd
import numpy as np
import pandapower.networks
import pandapower as pp
import os
import copy
import unicodedata


# In[2]:


def normalize(text):
    """
    Normalize a string by removing diacritics and converting to lowercase.

    Parameters:
    -----------
    text : str
        The string to normalize.

    Returns:
    --------
    str
        Normalized version of the input string.
    """
    return unicodedata.normalize('NFKC', text).strip().lower()


# In[3]:


def match_substation(name, substations):
    """
    Match a bus name to its corresponding substation name based on exact match, 
    prefix match, or fallback on partial component match.

    Parameters:
    -----------
    name : str
        The bus name to match.

    substations : list of str
        A list of known substation names.

    Returns:
    --------
    str or None
        The matched substation name, or None if no match is found.
    """
    normalized_subs = [normalize(s) for s in substations]
    name_norm = normalize(name)

    for i, sub in enumerate(normalized_subs):
        if name_norm == sub:
            return substations[i]
    for i, sub in enumerate(normalized_subs):
        if name_norm.startswith(sub + " ") or name_norm.startswith(sub + "-"):
            return substations[i]
    parts = re.split(r'[\s\-()]', name_norm)
    for part in parts:
        for i, sub in enumerate(normalized_subs):
            if part[:3] == sub[:3]:
                return substations[i]
    return None


# In[4]:


def aggregated_measurements_substation(timestamp_input):
    """
    Function to aggregate smart meter data for different substations on Bornholm Island.
    The function reads the data from an Excel file, processes it by combining columns, 
    filtering data based on a given timestamp, and calculates the total production and 
    consumption for each substation.

    Parameters:
    -----------
    timestamp_input : str
        A string representing the timestamp (in a format convertible by pandas to datetime) 
        for which the measurements need to be aggregated.

    Returns:
    --------
    pd.DataFrame
        A DataFrame containing aggregated production and consumption values for each substation 
        at the specified timestamp. Columns include 'Station', 'Consumption', and 'Production'.
    """
    
    # Get the current working directory to locate the data file
    current_directory = os.getcwd()
    
    # Define the file path for the smart meter data
    smart_meter_data = os.path.join(current_directory, 'CDK_Data_Bornholm_Sample.xlsx')
    
    # Step 1: Load the data from the Excel file into a pandas DataFrame
    df = pd.read_excel(smart_meter_data, engine='calamine', header=[0])

    # Step 2: Remove the first two rows to clean up the data (skip irrelevant data)
    df = df.iloc[2:]

    # Step 3: Extract new column names from the second row onward and append them to the existing columns
    new_col_parts = df.iloc[0, 1:].astype(str).tolist()
    df.columns = [df.columns[0]] + [f"{df.columns[i]}+{new_col_parts[i-1]}" for i in range(1, len(df.columns))]
    
    # Step 4: Drop the first row now that its information has been incorporated into column names
    df = df.iloc[1:].reset_index(drop=True)

    # Step 5: Combine the 'Date' and 'Time' columns into a single 'Date&time' column
    df['Date&time'] = pd.to_datetime(df.iloc[:, 0].astype(str) + ' ' + df.iloc[:, 1].astype(str), errors='coerce')
    
    # Step 6: Drop the original 'Date' and 'Time' columns after combining them
    df.drop(df.columns[[0, 1]], axis=1, inplace=True)
    
    # Step 7: Reorder columns so 'Date&time' appears first
    cols = ['Date&time'] + [col for col in df.columns if col != 'Date&time']
    df = df[cols]
    
    # Step 8: Set 'Date&time' as the DataFrame index for easy filtering
    df.set_index('Date&time', inplace=True)

    # Step 9: Convert the input timestamp to a pandas datetime object
    timestamp = pd.to_datetime(timestamp_input)

    # Step 10: Filter the data to obtain the row corresponding to the input timestamp
    row = df.loc[[timestamp]]

    # Step 11: Define the names of all substations for which data will be aggregated
    station_names = ['Åkirkeby', 'Allinge', 'Bodilsker', 'Gudhjem', 'Hasle', 'Nexø',
                     'Olsker', 'Østerlars', 'Povlsker', 'Rønne Nord', 'Rønne Syd',
                     'Snorrebakken', 'Svaneke', 'Værket', 'Vesthavnen', 'Viadukten']

    # Step 12: Prepare a list to store the results for each station
    results = []
    
    # Step 13: Loop over each station and calculate the production and consumption sums
    for station in station_names:
        # Step 13.1: Find all columns associated with the current station
        station_cols = [col for col in row.columns if str(col).startswith(station)]
    
        # Step 13.2: Calculate the sum of production values (columns ending with '-2')
        production_cols = [col for col in station_cols if str(col).endswith('-2')]
        sum_of_prod_values = np.nansum(row[production_cols].values)
    
        # Step 13.3: Calculate the sum of consumption values (columns ending with '-1')
        consumption_cols = [col for col in station_cols if str(col).endswith('-1')]
        sum_of_cons_values = np.nansum(row[consumption_cols].values)
    
        # Step 13.4: Convert the production and consumption sums to kWh (dividing by 1000)
        production_sum = sum_of_prod_values / 1000
        consumption_sum = sum_of_cons_values / 1000
    
        # Step 13.5: Store the results for the current station
        results.append({'substation_name': station, 'consumption': consumption_sum, 'production': production_sum})
    
    # Step 14: Convert the results list to a DataFrame
    measurement_prod_cons = pd.DataFrame(results)

    # Step 15: Rename 'Povlsker' to 'Poulsker'
    measurement_prod_cons['substation_name'] = measurement_prod_cons['substation_name'].replace('Povlsker', 'Poulsker')
    
    # Step 15: Return the final DataFrame containing the aggregated production and consumption
    return measurement_prod_cons


# In[5]:


def assign_load_values_from_measurements(net, measurement_prod_cons, substations):
    """
    Assigns active (p_mw) and reactive (q_mvar) power values to loads in a pandapower network
    based on substation-level consumption measurements.

    Steps:
    1. Normalize names in bus and load tables.
    2. Drop unwanted load entries by name.
    3. Map bus indices to bus names.
    4. Match loads to substations.
    5. Assign active power (p_mw) using substation consumption.
    6. Calculate reactive power (q_mvar) assuming a power factor of 0.95 (lagging).
    7. Drop temporary columns and retain original indices.

    Parameters:
    -----------
    net : pandapowerNet
        The pandapower network object to be updated.

    measurement_prod_cons : pandas.DataFrame
        DataFrame containing substation-level 'substation_name' and 'consumption' columns.

    substations : list of str
        List of valid substation names used for matching.

    Returns:
    --------
    net : pandapowerNet
        The updated pandapower network with p_mw and q_mvar assigned to net.load.
    """

    # -------- Step 1: Standardize names in bus and load --------
    net.bus['name'] = net.bus['name'].replace({'Gl Dampværket C afg Load': 'Værket 10kV'})
    net.load['name'] = net.load['name'].replace({'00 Gl Dampværk Load': '00 Værket Load'})

    # -------- Step 2: Drop unwanted load entries --------
    names_to_drop = ['Blok 5', 'Blok 6', 'Diesel generatorer']
    net.load = net.load[~net.load['name'].isin(names_to_drop)].copy()

    # -------- Step 3: Map bus index to bus name --------
    bus_name_map = net.bus['name'].to_dict()
    net.load['bus_name'] = net.load['bus'].map(bus_name_map)

    # -------- Step 4: Assign substation names using helper function --------
    net.load['substation_name'] = net.load['bus_name'].apply(lambda name: match_substation(name, substations))

    # -------- Step 5: Assign active power (p_mw) using external measurement data --------
    # Preserve the original index
    original_index = net.load.index

    # Create a mapping from substation name to consumption value
    consumption_map = measurement_prod_cons.set_index('substation_name')['consumption']
    net.load['consumption'] = net.load['substation_name'].map(consumption_map)

    net.load['p_mw'] = net.load['consumption']

    # -------- Step 6: Calculate reactive power (q_mvar) based on 0.95 lagging power factor --------
    power_factor = 0.95
    net.load['q_mvar'] = net.load['p_mw'] * np.tan(np.arccos(power_factor))

    # -------- Step 7: Clean up --------
    net.load.drop(columns=['consumption'], inplace=True)
    net.load.index = original_index  # Restore original indices

    return net


# In[6]:


def assign_generators_values_from_measurements(net, measurement_prod_cons, substations):
    """
    Assign static generator (sgen) data in a pandapower network using measured production data.

    This function populates the net.sgen DataFrame by copying bus and name information from net.load,
    replaces load names with generator names, and assigns active (p_mw) and reactive (q_mvar) power values 
    based on measured production data from the measurement_prod_cons DataFrame. It assumes a lagging 
    power factor of 0.95 for q_mvar calculation.

    Parameters:
    -----------
    net : pandapowerNet
        The pandapower network object to which sgens will be added.

    measurement_prod_cons : pandas.DataFrame
        A DataFrame containing at least the columns 'substation_name' and 'production' (in MW).
        This is used to assign active power (p_mw) values to the generators.

    substations : list of str
        List of known substation names used for validation or reference, not directly modified here.

    Returns:
    --------
    net : pandapowerNet
        The updated pandapower network with net.sgen populated with generator values.
    """

    # --- Step 0: Initialize empty net.sgen DataFrame with appropriate structure
    net.sgen = pd.DataFrame(columns=[
        'name', 'bus', 'p_mw', 'q_mvar', 'sn_mva', 'scaling', 'in_service', 'type'
    ])

    # Enforce correct datatypes
    net.sgen = net.sgen.astype({
        'name': 'str',
        'bus': 'int',
        'p_mw': 'float',
        'q_mvar': 'float',
        'sn_mva': 'float',
        'scaling': 'float',
        'in_service': 'bool',
        'type': 'str'
    })

    # --- Step 1: Generate 'name' column for sgen from load names
    sgen_name = net.load['name'].str.replace('Load', 'Sgen', case=False)

    # --- Step 2: Copy 'bus' and optional 'substation_name' columns from net.load
    sgen_bus = net.load['bus']
    sgen_substation_name = net.load['substation_name'] if 'substation_name' in net.load.columns else None

    # --- Step 3: Set default values for new sgen fields
    sgen_scaling = 1.0
    sgen_in_service = True

    # --- Step 4: Create net.sgen with initial values
    net.sgen = pd.DataFrame({
        'name': sgen_name,
        'bus': sgen_bus,
        'p_mw': np.nan,       # Placeholder for active power
        'q_mvar': np.nan,     # Placeholder for reactive power
        'sn_mva': np.nan,     # Optional; can be filled if known
        'scaling': sgen_scaling,
        'in_service': sgen_in_service,
        'type': 'static'
    })

    # --- Step 5: Add substation_name if available
    if sgen_substation_name is not None:
        net.sgen['substation_name'] = sgen_substation_name

    # --- Step 6: Merge production data based on substation_name
    net.sgen = net.sgen.merge(
        measurement_prod_cons[['substation_name', 'production']],
        on='substation_name',
        how='left'
    )

    # --- Step 7: Assign p_mw (note: sign convention; sgens inject power → positive)
    net.sgen['p_mw'] = -1 * net.sgen['production']

    # --- Step 8: Calculate q_mvar assuming power factor 0.95 lagging
    power_factor = 0.95
    net.sgen['q_mvar'] = net.sgen['p_mw'] * np.tan(np.arccos(power_factor))

    # --- Step 9: Clean up
    net.sgen.drop(columns=['production'], inplace=True)

    return net


# In[ ]:





# In[ ]:




