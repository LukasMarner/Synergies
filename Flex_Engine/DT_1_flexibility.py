#!/usr/bin/env python
# coding: utf-8

# Flexibility engine

# In[15]:


# Define timestamp
import Data_preprocessing_BH 
from Data_preprocessing_BH import *
import create_BH_net
from create_BH_net import *
import os
import random as rnd
import pandapower as pp

timestamp = '2022-03-09 17:30:00'
timestamp = pd.to_datetime(timestamp)

base_path = r"C:\Users\lukas\Synergies_Local\digitalwin1-main\digitalwin1-main"

file = 'demo_smart_meter_measurements.csv'
smart_meter_path = os.path.join(base_path, file)
demo_smart_meter_measurements = pd.read_csv(smart_meter_path, sep=';')

print(demo_smart_meter_measurements.head())
print(demo_smart_meter_measurements.columns)



# Create a prod_or_con DataFrame that matches the structure
prod_or_con = pd.DataFrame(index=[0], columns=demo_smart_meter_measurements.columns)

# Mark columns based on whether they are production or consumption
for col in demo_smart_meter_measurements.columns:
    if 'Production' in col:
        prod_or_con.loc[0, col] = -2  # Production marker
    elif 'Consumption' in col:
        prod_or_con.loc[0, col] = -1  # Consumption marker
    else:
        prod_or_con.loc[0, col] = None  # Other columns



measurement_number = rnd.randint(3, len(demo_smart_meter_measurements))
#smart_meter_measurements_sorted = fix_datetime(demo_smart_meter_measurements)
#measurement_number = 6473
# measurement_number = 1
#print('Index of measurement:', (measurement_number+3))
#print('Datetime:', (smart_meter_measurements_sorted['datetime'][measurement_number]))
#measurement_prod_cons = aggregated_measurements_substation(smart_meter_measurements_sorted, measurement_number = measurement_number)
measurement_prod_cons = aggregated_measurements_substation_demo(demo_smart_meter_measurements, prod_or_con,measurement_number = measurement_number)

excel_file = 'Bornholm 20220706.xlsx'
excel_path = os.path.join(base_path, excel_file)

# List of substations with associated CSV and voltage
substations = [
    ('Allinge', 'lok_10kvskinnespend'),
    ('Aakirkeby', 't1s_spending'),
    ('Bodilsker', 'lok_10kvskinnespend'),
    ('Gudhjem', 't1s_10kvskinnespend'),
    ('Hasle', ''),
    ('Nexo', ''),
    ('Olsker', ''),
    ('Osterlars', ''),
    ('Povlsker', ''),
    ('RNO', 'fel_10kvskinnespend'),
    ('RNS', 'lok_10kvskinnespend'),
    ('Snorrebakken', 't1s_10kvskinnespend'),
    ('Svaneke', ''),
    ('Vesthavnen', 'fel_skinnespending'),
    ('Viadukten', 't1s_10kvskinnespend'),
]


net = pp.create_empty_network()
net = load_data(excel_path, net)

smart_meter_measurement_vaerket = measurement_prod_cons

scada_path =r"C:\Users\lukas\OneDrive - Danmarks Tekniske Universitet\SYNERGIES Project -- DTU Team - Lukas Tej Marner_SA Shared Folder\Substations_measurements"


df_SCADA_meas = make_SCADA_df_lukas(timestamp, substations, scada_path)

meas_vaerket = pd.DataFrame({'Substation': ['Vaerket'], 'Active Power': [measurement_prod_cons['Consumption'].values[0]-measurement_prod_cons['Production'].values[0]], 'Reactive Power': [0]})

df_SCADA_meas = pd.concat([df_SCADA_meas, meas_vaerket], ignore_index=True)

net_meas = net_60kV_SCADA_measurements(net, df_SCADA_meas)


# In[16]:


def fill_load(net):
    df = net.load

    # Step 1: Identify all buses (in this case 5 buses: 0, 1, 2, 3, 4)
    total_buses = len(net.bus)
    all_buses = pd.Series(range(total_buses))

    # Step 2: Merge the original DataFrame with a DataFrame containing all buses to identify missing ones
    df_all_buses = pd.DataFrame({'bus': all_buses})

    # Step 3: Perform an outer join to fill missing buses and set the NaN values to 0 for the necessary columns
    df_filled = df_all_buses.merge(df, on='bus', how='left')
    # # Step 4: Replace NaN values with 0 where necessary (or fill with a specific default value)
    df_filled['name'].fillna('Unknown', inplace=True)
    df_filled['p_mw'].fillna(0.0, inplace=True)
    df_filled['q_mvar'].fillna(0.0, inplace=True)
    df_filled['const_z_percent'].fillna(0.0, inplace=True)
    df_filled['const_i_percent'].fillna(0.0, inplace=True)
    df_filled['sn_mva'].fillna(0.0, inplace=True)
    df_filled['scaling'].fillna(1.0, inplace=True)
    df_filled['in_service'].fillna(True, inplace=True)
    df_filled['type'].fillna('Unknown', inplace=True)
    # df_filled['controllable'].fillna(False, inplace=True)
    # Step 5: Output the filled DataFrame
    net.load = df_filled
    return net.load

def fill_gen(net):
    df = net.res_gen
    df['bus'] = net.gen['bus']

    # Step 1: Identify all buses (in this case 5 buses: 0, 1, 2, 3, 4)
    total_buses = len(net.bus)
    all_buses = pd.Series(range(total_buses))
    # print(df_sgen)

    # df = pd.DataFrame(df)

    # df = df.merge(df_sgen, on ='bus', how ='left')
    # print(df)

    # Step 2: Merge the original DataFrame with a DataFrame containing all buses to identify missing ones
    df_all_buses = pd.DataFrame({'bus': all_buses})

    # Step 3: Perform an outer join to fill missing buses and set the NaN values to 0 for the necessary columns
    df_filled = df_all_buses.merge(df, on='bus', how='left')
    # # Step 4: Replace NaN values with 0 where necessary (or fill with a specific default value)
    df_filled['p_mw'].fillna(0.0, inplace=True)
    df_filled['q_mvar'].fillna(0.0, inplace=True)
    df_filled['va_degree'].fillna(0.0, inplace=True)
    df_filled['vm_pu'].fillna(1.0, inplace=True) 
    # Step 5: Output the filled DataFrame
    net.res_gen = df_filled
    return net.res_gen

def fill_sgen(net):
    df = net.res_sgen
    df['bus'] = net.sgen['bus']

    # Step 1: Identify all buses (in this case 5 buses: 0, 1, 2, 3, 4)
    total_buses = len(net.bus)
    all_buses = pd.Series(range(total_buses))
    # print(df_sgen)

    # df = pd.DataFrame(df)

    # df = df.merge(df_sgen, on ='bus', how ='left')
    # print(df)

    # Step 2: Merge the original DataFrame with a DataFrame containing all buses to identify missing ones
    df_all_buses = pd.DataFrame({'bus': all_buses})

    # Step 3: Perform an outer join to fill missing buses and set the NaN values to 0 for the necessary columns
    df_filled = df_all_buses.merge(df, on='bus', how='left')
    # # Step 4: Replace NaN values with 0 where necessary (or fill with a specific default value)
    df_filled['p_mw'].fillna(0.0, inplace=True)
    df_filled['q_mvar'].fillna(0.0, inplace=True)
    # Step 5: Output the filled DataFrame
    net.res_sgen = df_filled
    return net.res_sgen

def fill_ext_grid(net):
    df = net.res_ext_grid
    df['bus'] = net.ext_grid['bus']

    # Step 1: Identify all buses (in this case 5 buses: 0, 1, 2, 3, 4)
    total_buses = len(net.bus)
    all_buses = pd.Series(range(total_buses))
    # print(df_sgen)

    # df = pd.DataFrame(df)

    # df = df.merge(df_sgen, on ='bus', how ='left')
    # print(df)

    # Step 2: Merge the original DataFrame with a DataFrame containing all buses to identify missing ones
    df_all_buses = pd.DataFrame({'bus': all_buses})

    # Step 3: Perform an outer join to fill missing buses and set the NaN values to 0 for the necessary columns
    df_filled = df_all_buses.merge(df, on='bus', how='left')
    # # Step 4: Replace NaN values with 0 where necessary (or fill with a specific default value)
    df_filled['p_mw'].fillna(0.0, inplace=True)
    df_filled['q_mvar'].fillna(0.0, inplace=True)
    # Step 5: Output the filled DataFrame
    net.res_ext_grid = df_filled
    return net.res_ext_grid

def create_Y_bus(net):
    NB = len(net.bus)
    y = np.zeros((NB, NB), dtype=complex)  # Define y as a complex array
    y_shunt = np.zeros((NB, NB), dtype=complex)  # Define y_shunt as a complex array
    for i, row in net.line.iterrows():
        from_bus_idx = int(row['from_bus'])  # Convert to integer index
        to_bus_idx = int(row['to_bus'])      # Convert to integer index
        y[from_bus_idx, to_bus_idx] = -1/(row['length_km']*(row['r_ohm_per_km']+1j*row['x_ohm_per_km']))
        y_shunt[from_bus_idx, to_bus_idx] = 1j*row['c_nf_per_km']/2*1e-9*row['length_km']
        y[to_bus_idx, from_bus_idx] = -1/(row['length_km']*(row['r_ohm_per_km']+1j*row['x_ohm_per_km']))
        y_shunt[to_bus_idx, from_bus_idx] = 1j*row['c_nf_per_km']/2*1e-9*row['length_km']
    
    Y_bus = y
    for i in range(NB):
        y_diag = 0
        for k in range(NB):
            y_diag = y_diag-y[i, k] + y_shunt[i, k]
        Y_bus[i, i] = y_diag

    return Y_bus
    


# In[17]:


# import Flexibility
# from Flexibility import *
# importlib.reload(Flexibility)
import gurobipy as gp
import numpy as np
import pandas as pd

m = gp.Model('flex')

net_meas = net_meas

active_power_bus = {}
reactive_power_bus = {}
voltage_real_bus = {}
voltage_imag_bus = {}
flex_up = {}
flex_down = {}
flex_up_reactive = {}
flex_down_reactive = {}
node_number = len(net_meas.bus)
buses = [str(x) for x in np.arange(node_number)] 
NL = len(net.line)
lines = net.line

for i in range(len(buses)):
    # active_power_bus[i] = m.addVar(lb = 0,name = 'active_power_bus')
    # reactive_power_bus[i] = m.addVar(lb = -99.9,name = 'reactive_power_bus')
    voltage_real_bus[i] = m.addVar(lb = -99.9,name = 'voltage_real_bus')
    voltage_imag_bus[i] = m.addVar(lb = -99.9, name = 'voltage_imag_bus')
    flex_up[i] = m.addVar(name = 'flex_up')
    flex_down[i] = m.addVar(name = 'flex_down')
    flex_down_reactive[i] = m.addVar(name = 'flex_down_reactive')
    flex_up_reactive[i] = m.addVar(name = 'flex_up_reactive')
    

C = {}
S = {}


for i in buses:
    for j in buses:
        C[int(i), int(j)] = m.addVar(lb = -99.9 ,name = 'C')
        S[int(i), int(j)] = m.addVar (lb = -99.9  ,name='S')




# m.addConstrs((active_power_bus[bus] == 0 for bus in non_generate_ac_bus),name="balancePVP")
# m.addConstrs((reactive_power_bus[bus] == 0 for bus in non_generate_reac_bus),name="balancePVQ")

# m.addConstrs((active_power_bus[bus] <= Gupper[bus] for bus in generate_ac_bus),name="active_Capacity_upper")
# m.addConstrs((active_power_bus[bus >= Glower[dbus for busn generate_ac_dbusname="active_Capacity_lower")

# m.addConstrs((reactive_power_bus[bus] <= pvqmax[bus for dbusin generate_reac_bus),name="reactive_Capacity_upper")
# m.addConstrs((reactive_power_busbus >= pvqmin[bus] for busin generate_reac_bus),name="reactive_Capacity_lower")

# m.addConstrs((voltage_real_busbus] == pvv_busbus] for busin generate_reac_bus),name='PV')

# active_load_bus= net.load['p_mw']
# reactive_load_bus = net.load['q_mvar']

net_meas.res_gen = fill_gen(net_meas)
print('net_meas.res_gen', net_meas.res_gen)
net_meas.load = fill_load(net_meas)
net_meas.res_sgen = fill_sgen(net_meas)
net_meas.ext_grid = fill_ext_grid(net_meas)

active_power_bus = net_meas.res_gen['p_mw']
print('active_power_bus', active_power_bus)
active_power_bus_sgen = net_meas.res_sgen['p_mw']
reactive_power_bus = net_meas.res_gen['q_mvar']
reactive_power_bus_sgen = net_meas.res_sgen['q_mvar']
active_power_load_bus = net_meas.load['p_mw']
reactive_power_load_bus = net_meas.load['q_mvar']
active_power_ext_grid = net_meas.res_ext_grid['p_mw']
reactive_power_ext_grid = net_meas.res_ext_grid['q_mvar']

# active_load_bus = dict(zip(buses,powpdi.tolist()))
# reactive_load_bus = dict(zip(buses,powqdj.tolist()))

Y_bus = create_Y_bus(net_meas)

B = np.imag(Y_bus)
G = np.real(Y_bus)

def constrainp(i):
    a = B[i, i] * S[i, i]
    for j in buses:
        j = int(j)
        a += G[i,j]*C[i,j]-B[i,j]*S[i,j]
    return (a)

def constrainq(i):
    a = -G[i, i] * S[i, i]
    for j in buses:
        j = int(j)
        a += -B[i,j]*C[i,j]-G[i,j]*S[i,j]
    return (a)

def fintstr(bus):
    bus = int(bus)
    bus = str (bus)
    return bus

# def lineconstraints(i):
#     for j in buses:
#         (B[i, j]*B[i, j] + G[i, j])(*G[i, j]*C[i, i]-2*C[i, j]+C[j, j])




# m.addConstrs((constrainp(int(i))==active_power_bus[int(i)] - active_load_bus[int(i)]+flex_up[int(i)]-flex_down[int(i)]) for i in buses)
# m.addConstrs((constrainq(int(i))==reactive_power_bus[i] - reactive_load_bus[i]) for i in buses)
m.update()

m.addConstrs((constrainp(int(i))==active_power_bus[int(i)]-active_power_load_bus[int(i)]+active_power_bus_sgen[int(i)]+active_power_ext_grid[int(i)]+flex_up[int(i)]-flex_down[int(i)]) for i in buses)
# m.addConstrs((constrainp(int(i))==active_power_bus[int(i)]) for i in range(len(buses)))
m.addConstrs((constrainq(int(i))==reactive_power_bus[int(i)]-reactive_power_load_bus[int(i)]+reactive_power_bus_sgen[int(i)]+reactive_power_ext_grid[int(i)]+flex_up_reactive[int(i)]-flex_down_reactive[int(i)]) for i in range(len(buses)))
## Put reference bus
# m.addConstr(C[fintstr(data[2][1]),fintstr(data[2][1])]==1)'
m.addConstr(voltage_real_bus[0]==1)
m.addConstr(voltage_imag_bus[0] == 0)
m.addConstrs((C[bus_i, bus_i]<=1.05*1.05 for bus_i in range(len(buses))),name='ClimUP')
m.addConstrs((C[bus_i, bus_i]>=0.95*0.95 for bus_i in range(len(buses))),name='ClimLow')
m.addConstrs((C[bus_i, bus_j]==C[bus_j, bus_i] for bus_j in range(len(buses))  for bus_i in range(len(buses))),name='C_Constrs')
m.addConstrs((S[bus_i, bus_j]==-S[bus_j, bus_i] for bus_j in range(len(buses))  for bus_i in range(len(buses))),name='S_Constrs')



for bus_i in range(len(buses)):
    for bus_j in range(len(buses)):
        m.addQConstr((C[bus_i, bus_j]*C[bus_i, bus_j]+S[bus_i, bus_j]*S[bus_i, bus_j])<=C[bus_i, bus_i]*C[bus_j, bus_j])
c=100
obj = c*gp.quicksum((flex_up[n]-flex_down[n]+flex_up_reactive[n]-flex_down_reactive[n]) for n in range(len(buses)))

# obj = quicksum(Ga_bus[bus * active_power_bus[bus]* active_power_busbus] + Gb_busbus] * active_power_busbus]
#                          + Gc_bus[bus] for busin generate_ac_bus)

m.setObjective(obj, gp.GRB.MINIMIZE)
m.optimize()


# In[18]:


for i in range(len(net.bus)):
    print(f'flex_up_{i}', flex_up[i].X)
    print(f'flex_down_{i}', flex_down[i].X)
    print(f'flex_up_reactive{i}', flex_up_reactive[i].X)
    print(f'flex_down_reactive{i}', flex_down_reactive[i].X)
    print(f'voltage bus', voltage_real_bus[i].X, voltage_imag_bus[i].X)
print('total flex up:', np.sum(flex_up[i].X for i in range(len(net.bus))))
print('total flex down:', np.sum(flex_down[i].X for i in range(len(net.bus))))


# In[19]:


# Assuming `net` and the other variables (`flex_up`, `flex_down`, etc.) are already defined
flex_up_vals = []
flex_down_vals = []
flex_up_reactive_vals = []
flex_down_reactive_vals = []
voltage_real_vals = []
voltage_imag_vals = []

for i in range(len(net.bus)):
    flex_up_vals.append(flex_up[i].X)
    flex_down_vals.append(flex_down[i].X)
    flex_up_reactive_vals.append(flex_up_reactive[i].X)
    flex_down_reactive_vals.append(flex_down_reactive[i].X)
    voltage_real_vals.append(voltage_real_bus[i].X)
    voltage_imag_vals.append(voltage_imag_bus[i].X)

# Create a dictionary to store the data
flex_results = {
    'flex_up': flex_up_vals,
    'flex_down': flex_down_vals,
    'flex_up_reactive': flex_up_reactive_vals,
    'flex_down_reactive': flex_down_reactive_vals
    # 'voltage_real': voltage_real_vals,
    # 'voltage_imag': voltage_imag_vals
}

# Create the dataframe
flex_results_df = pd.DataFrame(flex_results)


# In[20]:


flex_results_df


# In[21]:


total_flex_available_up_active = 20
total_flex_available_up_reactive = 3
total_flex_available_down = 0
total_flex_available_down_reactive = 0


# import Flexibility
# from Flexibility import *
# importlib.reload(Flexibility)
import gurobipy as gp
import numpy as np
import pandas as pd

m = gp.Model('flex')

net_meas = net_meas

active_power_bus = {}
reactive_power_bus = {}
voltage_real_bus = {}
voltage_imag_bus = {}
flex_up = {}
flex_down = {}
flex_up_reactive = {}
flex_down_reactive = {}
node_number = len(net_meas.bus)
buses = [str(x) for x in np.arange(node_number)] 
NL = len(net.line)
lines = net.line

for i in range(len(buses)):
    # active_power_bus[i] = m.addVar(lb = 0,name = 'active_power_bus')
    # reactive_power_bus[i] = m.addVar(lb = -99.9,name = 'reactive_power_bus')
    voltage_real_bus[i] = m.addVar(lb = -99.9,name = 'voltage_real_bus')
    voltage_imag_bus[i] = m.addVar(lb = -99.9, name = 'voltage_imag_bus')
    flex_up[i] = m.addVar(name = 'flex_up')
    flex_down[i] = m.addVar(name = 'flex_down')
    flex_down_reactive[i] = m.addVar(name = 'flex_down_reactive')
    flex_up_reactive[i] = m.addVar(name = 'flex_up_reactive')
    

C = {}
S = {}


for i in buses:
    for j in buses:
        C[int(i), int(j)] = m.addVar(lb = -99.9 ,name = 'C')
        S[int(i), int(j)] = m.addVar (lb = -99.9  ,name='S')




# m.addConstrs((active_power_bus[bus] == 0 for bus in non_generate_ac_bus),name="balancePVP")
# m.addConstrs((reactive_power_bus[bus] == 0 for bus in non_generate_reac_bus),name="balancePVQ")

# m.addConstrs((active_power_bus[bus] <= Gupper[bus] for bus in generate_ac_bus),name="active_Capacity_upper")
# m.addConstrs((active_power_bus[bus >= Glower[dbus for busn generate_ac_dbusname="active_Capacity_lower")

# m.addConstrs((reactive_power_bus[bus] <= pvqmax[bus for dbusin generate_reac_bus),name="reactive_Capacity_upper")
# m.addConstrs((reactive_power_busbus >= pvqmin[bus] for busin generate_reac_bus),name="reactive_Capacity_lower")

# m.addConstrs((voltage_real_busbus] == pvv_busbus] for busin generate_reac_bus),name='PV')

# active_load_bus= net.load['p_mw']
# reactive_load_bus = net.load['q_mvar']

net_meas.res_gen = fill_gen(net_meas)
net_meas.load = fill_load(net_meas)
net_meas.res_sgen = fill_sgen(net_meas)
net_meas.ext_grid = fill_ext_grid(net_meas)

active_power_bus = net_meas.res_gen['p_mw']
active_power_bus_sgen = net_meas.res_sgen['p_mw']
reactive_power_bus = net_meas.res_gen['q_mvar']
reactive_power_bus_sgen = net_meas.res_sgen['q_mvar']
active_power_load_bus = net_meas.load['p_mw']
reactive_power_load_bus = net_meas.load['q_mvar']
active_power_ext_grid = net_meas.res_ext_grid['p_mw']
reactive_power_ext_grid = net_meas.res_ext_grid['q_mvar']

# active_load_bus = dict(zip(buses,powpdi.tolist()))
# reactive_load_bus = dict(zip(buses,powqdj.tolist()))

Y_bus = create_Y_bus(net_meas)

B = np.imag(Y_bus)
G = np.real(Y_bus)

def constrainp(i):
    a = B[i, i] * S[i, i]
    for j in buses:
        j = int(j)
        a += G[i,j]*C[i,j]-B[i,j]*S[i,j]
    return (a)

def constrainq(i):
    a = -G[i, i] * S[i, i]
    for j in buses:
        j = int(j)
        a += -B[i,j]*C[i,j]-G[i,j]*S[i,j]
    return (a)

def fintstr(bus):
    bus = int(bus)
    bus = str (bus)
    return bus

# def lineconstraints(i):
#     for j in buses:
#         (B[i, j]*B[i, j] + G[i, j])(*G[i, j]*C[i, i]-2*C[i, j]+C[j, j])



# m.addConstrs((constrainp(int(i))==active_power_bus[int(i)] - active_load_bus[int(i)]+flex_up[int(i)]-flex_down[int(i)]) for i in buses)
# m.addConstrs((constrainq(int(i))==reactive_power_bus[i] - reactive_load_bus[i]) for i in buses)
m.update()

m.addConstrs((constrainp(int(i))==active_power_bus[int(i)]-active_power_load_bus[int(i)]+active_power_bus_sgen[int(i)]+active_power_ext_grid[int(i)]+flex_up[int(i)]-flex_down[int(i)]) for i in buses)
# m.addConstrs((constrainp(int(i))==active_power_bus[int(i)]) for i in range(len(buses)))
m.addConstrs((constrainq(int(i))==reactive_power_bus[int(i)]-reactive_power_load_bus[int(i)]+reactive_power_bus_sgen[int(i)]+reactive_power_ext_grid[int(i)]+flex_up_reactive[int(i)]-flex_down_reactive[int(i)]) for i in range(len(buses)))
## Put reference bus
# m.addConstr(C[fintstr(data[2][1]),fintstr(data[2][1])]==1)'
m.addConstr(voltage_real_bus[0]==1)
m.addConstr(voltage_imag_bus[0] == 0)
m.addConstrs((C[bus_i, bus_i]<=1.05*1.05 for bus_i in range(len(buses))),name='ClimUP')
m.addConstrs((C[bus_i, bus_i]>=0.95*0.95 for bus_i in range(len(buses))),name='ClimLow')
m.addConstrs((C[bus_i, bus_j]==C[bus_j, bus_i] for bus_j in range(len(buses))  for bus_i in range(len(buses))),name='C_Constrs')
m.addConstrs((S[bus_i, bus_j]==-S[bus_j, bus_i] for bus_j in range(len(buses))  for bus_i in range(len(buses))),name='S_Constrs')



for bus_i in range(len(buses)):
    for bus_j in range(len(buses)):
        m.addQConstr((C[bus_i, bus_j]*C[bus_i, bus_j]+S[bus_i, bus_j]*S[bus_i, bus_j])<=C[bus_i, bus_i]*C[bus_j, bus_j])
c=100
obj = c*gp.quicksum((flex_up[n]-flex_down[n]+flex_up_reactive[n]-flex_down_reactive[n]) for n in range(len(buses)))

# obj = quicksum(Ga_bus[bus * active_power_bus[bus]* active_power_busbus] + Gb_busbus] * active_power_busbus]
#                          + Gc_bus[bus] for busin generate_ac_bus)

m.setObjective(obj, gp.GRB.MINIMIZE)
m.optimize()


# Convertion to Pyomo

# In[22]:


m.write("model.lp")
