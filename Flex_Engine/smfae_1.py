





# Define timestamp
import Data_preprocessing_BH 
from Data_preprocessing_BH import *
import create_BH_net
from create_BH_net import *
import os
import random as rnd
import pandapower as pp
from Flexibility import *

timestamp = '2022-03-09 17:30:00'
timestamp = pd.to_datetime(timestamp)

base_path = r"C:\Users\lukas\Synergies\digitaltwin1_main"

file = 'demo_smart_meter_measurements.csv'
smart_meter_path = os.path.join(base_path, file)
demo_smart_meter_measurements = pd.read_csv(smart_meter_path, sep=';')


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

scada_path =r"C:\Users\lukas\Synergies\Flex_Engine\Substations_Measurements"


df_SCADA_meas = make_SCADA_df_lukas(timestamp, substations, scada_path)

meas_vaerket = pd.DataFrame({'Substation': ['Vaerket'], 'Active Power': [measurement_prod_cons['Consumption'].values[0]-measurement_prod_cons['Production'].values[0]], 'Reactive Power': [0]})

df_SCADA_meas = pd.concat([df_SCADA_meas, meas_vaerket], ignore_index=True)

net_meas = net_60kV_SCADA_measurements(net, df_SCADA_meas)




# In[16]:

# the load functions will now be called from flexibility.py

Y_bus = create_Y_bus(net)



import pyomo.environ as pyo
import numpy as np

def create_pyomo_model(net_meas, Y_bus):
    # Extract data from network model
    B = np.imag(Y_bus)
    G = np.real(Y_bus)
    node_number = len(net_meas.bus)
    
   
    # Create Pyomo model
    model = pyo.ConcreteModel()
    
    # Define sets
    model.buses = pyo.Set(initialize=range(node_number))
    
    # Define variables
    model.voltage_real_bus = pyo.Var(model.buses, bounds=(-99.9, None))
    model.voltage_imag_bus = pyo.Var(model.buses, bounds=(-99.9, None))
    model.flex_up = pyo.Var(model.buses, bounds=(0, None))
    model.flex_down = pyo.Var(model.buses, bounds=(0, None))
    model.flex_up_reactive = pyo.Var(model.buses, bounds=(0, None))
    model.flex_down_reactive = pyo.Var(model.buses, bounds=(0, None))
   
    # Define C and S as Pyomo variables (not Python dictionaries)
    model.C = pyo.Var(model.buses, model.buses, bounds=(-99.9, None))
    model.S = pyo.Var(model.buses, model.buses, bounds=(-99.9, None))
   

    net_meas.res_gen = fill_gen(net_meas)
  
    net_meas.load = fill_load(net_meas)
    net_meas.res_sgen = fill_sgen(net_meas)
    net_meas.ext_grid = fill_ext_grid(net_meas)


    # Extract power data from network
    active_power_bus = net_meas.res_gen['p_mw'].to_dict()
    active_power_bus_sgen = net_meas.res_sgen['p_mw'].to_dict()
    reactive_power_bus = net_meas.res_gen['q_mvar'].to_dict()
    reactive_power_bus_sgen = net_meas.res_sgen['q_mvar'].to_dict()
    active_power_load_bus = net_meas.load['p_mw'].to_dict()
    reactive_power_load_bus = net_meas.load['q_mvar'].to_dict()
    active_power_ext_grid = net_meas.res_ext_grid['p_mw'].to_dict()
    reactive_power_ext_grid = net_meas.res_ext_grid['q_mvar'].to_dict()
    
    # Active power balance constraints
    def active_power_balance_rule(model, i):
        return (sum(G[i,j]*model.C[i,j] - B[i,j]*model.S[i,j] for j in model.buses) + B[i,i]*model.S[i,i] == 
                active_power_bus[i] - active_power_load_bus[i] + 
                active_power_bus_sgen[i] + active_power_ext_grid[i] + 
                model.flex_up[i] - model.flex_down[i])
    
    model.active_power_balance = pyo.Constraint(model.buses, rule=active_power_balance_rule)
    
    # Reactive power balance constraints
    def reactive_power_balance_rule(model, i):
        return (sum(-B[i,j]*model.C[i,j] - G[i,j]*model.S[i,j] for j in model.buses) - G[i,i]*model.S[i,i] == 
                reactive_power_bus[i] - reactive_power_load_bus[i] + 
                reactive_power_bus_sgen[i] + reactive_power_ext_grid[i] + 
                model.flex_up_reactive[i] - model.flex_down_reactive[i])
    
    model.reactive_power_balance = pyo.Constraint(model.buses, rule=reactive_power_balance_rule)
    
    # Reference bus constraint
    model.ref_bus_real = pyo.Constraint(expr=model.voltage_real_bus[0] == 1)
    model.ref_bus_imag = pyo.Constraint(expr=model.voltage_imag_bus[0] == 0)
    
    # Voltage magnitude constraints
    def voltage_upper_limit_rule(model, i):
        return model.C[i,i] <= 1.05*1.05
    
    def voltage_lower_limit_rule(model, i):
        return model.C[i,i] >= 0.95*0.95
    
    model.voltage_upper_limit = pyo.Constraint(model.buses, rule=voltage_upper_limit_rule)
    model.voltage_lower_limit = pyo.Constraint(model.buses, rule=voltage_lower_limit_rule)
    
    # C and S symmetry constraints
    def C_symmetry_rule(model, i, j):
        return model.C[i,j] == model.C[j,i]
    
    def S_antisymmetry_rule(model, i, j):
        return model.S[i,j] == -model.S[j,i]
    
    model.C_symmetry = pyo.Constraint(model.buses, model.buses, rule=C_symmetry_rule)
    model.S_antisymmetry = pyo.Constraint(model.buses, model.buses, rule=S_antisymmetry_rule)
    
    # Quadratic constraints - need special handling in Pyomo
    model.quad_constraints = pyo.ConstraintList()
    for i in model.buses:
        for j in model.buses:
            expr = model.C[i,j]**2 + model.S[i,j]**2 <= model.C[i,i] * model.C[j,j]
            model.quad_constraints.add(expr)
    
    # Objective function
    c = 100  # Weight coefficient
    model.objective = pyo.Objective(
        expr=c*sum(model.flex_up[n] - model.flex_down[n] + 
                   model.flex_up_reactive[n] - model.flex_down_reactive[n] 
                   for n in model.buses),
        sense=pyo.minimize
    )
    
    return model

# Create and solve the Pyomo model
pyomo_model = create_pyomo_model(net_meas, Y_bus)

# Configure solver - IPOPT for nonlinear problems
solver = pyo.SolverFactory('ipopt')
solver.options['max_iter'] = 5000  # Increase iteration limit for convergence
solver.options['tol'] = 1e-6  # Tighten tolerance for better solution quality

# Solve the model
results = solver.solve(pyomo_model, tee=True)

# Extract solution
solution = {
    'flex_up': [pyo.value(pyomo_model.flex_up[i]) for i in pyomo_model.buses],
    'flex_down': [pyo.value(pyomo_model.flex_down[i]) for i in pyomo_model.buses],
    'flex_up_reactive': [pyo.value(pyomo_model.flex_up_reactive[i]) for i in pyomo_model.buses],
    'flex_down_reactive': [pyo.value(pyomo_model.flex_down_reactive[i]) for i in pyomo_model.buses]
}

# Create a DataFrame with the results
flex_results_df = pd.DataFrame(solution)
print(flex_results_df)

