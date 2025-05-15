# smfae_1.py - Security Management and Flexibility Activation Engine
import pandas as pd
import numpy as np
import pyomo.environ as pyo
import pandapower as pp
import warnings
import os
import random as rnd
from Data_preprocessing_BH import *
from create_BH_net import load_data, net_60kV_SCADA_measurements
# Suppress warnings
warnings.filterwarnings('ignore')

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


def create_Y_bus(net):
    """
    Create the Y-bus matrix from a pandapower network
    """
    NB = len(net.bus)
    y = np.zeros((NB, NB), dtype=complex)  # Define y as a complex array
    y_shunt = np.zeros((NB, NB), dtype=complex)  # Define y_shunt as a complex array
    
    for i, row in net.line.iterrows():
        from_bus_idx = int(row['from_bus'])  # Convert to integer index
        to_bus_idx = int(row['to_bus'])      # Convert to integer index
        
        # Calculate admittance
        z_line = row['length_km']*(row['r_ohm_per_km']+1j*row['x_ohm_per_km'])
        if z_line != 0:
            y_line = 1/z_line
        else:
            y_line = 0
            
        y[from_bus_idx, to_bus_idx] = -y_line
        y[to_bus_idx, from_bus_idx] = -y_line
        
        # Calculate shunt admittance
        y_shunt[from_bus_idx, to_bus_idx] = 1j*row['c_nf_per_km']/2*1e-9*row['length_km']
        y_shunt[to_bus_idx, from_bus_idx] = 1j*row['c_nf_per_km']/2*1e-9*row['length_km']
    
    # Calculate diagonal elements
    Y_bus = y.copy()
    for i in range(NB):
        y_diag = 0
        for k in range(NB):
            y_diag -= y[i, k]
            y_diag += y_shunt[i, k]
        Y_bus[i, i] = y_diag

    return Y_bus

def ensure_results_exist(net):
    """
    Ensure all necessary result fields exist in the network model
    """
    # Make sure we have run a power flow
    if not hasattr(net, 'res_bus') or net.res_bus.empty:
        try:
            pp.runpp(net, numba=False)
        except:
            print("Warning: Power flow did not converge. Creating empty result tables.")
    
    # Ensure 'bus' column exists in result DataFrames
    if len(net.gen) > 0:
        if not hasattr(net, 'res_gen') or net.res_gen.empty:
            net.res_gen = pd.DataFrame(index=net.gen.index)
            net.res_gen['p_mw'] = net.gen['p_mw']
            net.res_gen['q_mvar'] = 0.0
        
        if 'bus' not in net.res_gen.columns:
            net.res_gen['bus'] = net.gen['bus']
    else:
        net.res_gen = pd.DataFrame(columns=['p_mw', 'q_mvar', 'bus'])
    
    if len(net.sgen) > 0:
        if not hasattr(net, 'res_sgen') or net.res_sgen.empty:
            net.res_sgen = pd.DataFrame(index=net.sgen.index)
            net.res_sgen['p_mw'] = net.sgen['p_mw']
            net.res_sgen['q_mvar'] = 0.0
        
        if 'bus' not in net.res_sgen.columns:
            net.res_sgen['bus'] = net.sgen['bus']
    else:
        net.res_sgen = pd.DataFrame(columns=['p_mw', 'q_mvar', 'bus'])
    
    if len(net.ext_grid) > 0:
        if not hasattr(net, 'res_ext_grid') or net.res_ext_grid.empty:
            net.res_ext_grid = pd.DataFrame(index=net.ext_grid.index)
            net.res_ext_grid['p_mw'] = 0.0
            net.res_ext_grid['q_mvar'] = 0.0
        
        if 'bus' not in net.res_ext_grid.columns:
            net.res_ext_grid['bus'] = net.ext_grid['bus']
    else:
        net.res_ext_grid = pd.DataFrame(columns=['p_mw', 'q_mvar', 'bus'])
    
    return net

def create_pyomo_model(net_meas, Y_bus):
    """
    Create a Pyomo model for flexibility optimization
    """
    # Ensure required data exists
    net_meas = ensure_results_exist(net_meas)
    
    # Create the model
    model = pyo.ConcreteModel()
    
    # Define the set of buses
    buses = list(range(len(net_meas.bus)))
    model.buses = pyo.Set(initialize=buses)
    
    # Create dictionaries mapping from bus indices to power values using concise approach
    active_power_bus = {bus: float(net_meas.res_gen[net_meas.res_gen['bus'] == bus]['p_mw'].sum()) for bus in buses}
    reactive_power_bus = {bus: float(net_meas.res_gen[net_meas.res_gen['bus'] == bus]['q_mvar'].sum()) for bus in buses}
    
    active_power_bus_sgen = {bus: float(net_meas.res_sgen[net_meas.res_sgen['bus'] == bus]['p_mw'].sum()) for bus in buses}
    reactive_power_bus_sgen = {bus: float(net_meas.res_sgen[net_meas.res_sgen['bus'] == bus]['q_mvar'].sum()) for bus in buses}
    
    active_power_load_bus = {bus: float(net_meas.load[net_meas.load['bus'] == bus]['p_mw'].sum()) for bus in buses}
    reactive_power_load_bus = {bus: float(net_meas.load[net_meas.load['bus'] == bus]['q_mvar'].sum()) for bus in buses}
    
    active_power_ext_grid = {bus: float(net_meas.res_ext_grid[net_meas.res_ext_grid['bus'] == bus]['p_mw'].sum()) for bus in buses}
    reactive_power_ext_grid = {bus: float(net_meas.res_ext_grid[net_meas.res_ext_grid['bus'] == bus]['q_mvar'].sum()) for bus in buses}
    
    # Extract G and B matrices
    G = np.real(Y_bus)
    B = np.imag(Y_bus)
    
    # Define variables
    model.voltage_real_bus = pyo.Var(model.buses, bounds=(-5, 5), initialize=1.0)
    model.voltage_imag_bus = pyo.Var(model.buses, bounds=(-5, 5), initialize=0.0)
    model.flex_up = pyo.Var(model.buses, bounds=(0, None), initialize=0.0)
    model.flex_down = pyo.Var(model.buses, bounds=(0, None), initialize=0.0)
    model.flex_up_reactive = pyo.Var(model.buses, bounds=(0, None), initialize=0.0)
    model.flex_down_reactive = pyo.Var(model.buses, bounds=(0, None), initialize=0.0)
    
    # C and S variables (real and imaginary parts of voltage products)
    model.C = pyo.Var(model.buses, model.buses, bounds=(-10, 10), initialize=1.0)
    model.S = pyo.Var(model.buses, model.buses, bounds=(-10, 10), initialize=0.0)
    
    # Reference bus constraint
    model.ref_real = pyo.Constraint(expr=model.voltage_real_bus[0] == 1.0)
    model.ref_imag = pyo.Constraint(expr=model.voltage_imag_bus[0] == 0.0)
    
    # Definition of C and S in terms of voltage variables
    def c_definition_rule(model, i, j):
        return model.C[i, j] == model.voltage_real_bus[i] * model.voltage_real_bus[j] + model.voltage_imag_bus[i] * model.voltage_imag_bus[j]
    
    def s_definition_rule(model, i, j):
        return model.S[i, j] == model.voltage_real_bus[i] * model.voltage_imag_bus[j] - model.voltage_imag_bus[i] * model.voltage_real_bus[j]
    
    model.c_definition = pyo.Constraint(model.buses, model.buses, rule=c_definition_rule)
    model.s_definition = pyo.Constraint(model.buses, model.buses, rule=s_definition_rule)
    
    # Symmetry and antisymmetry constraints for C and S
    def c_symmetry_rule(model, i, j):
        if i != j:
            return model.C[i, j] == model.C[j, i]
        else:
            return pyo.Constraint.Skip
    
    def s_antisymmetry_rule(model, i, j):
        if i != j:
            return model.S[i, j] == -model.S[j, i]
        else:
            return pyo.Constraint.Skip
    
    model.c_symmetry = pyo.Constraint(model.buses, model.buses, rule=c_symmetry_rule)
    model.s_antisymmetry = pyo.Constraint(model.buses, model.buses, rule=s_antisymmetry_rule)
    
    # Voltage magnitude constraints
    def voltage_limit_rule(model, i):
        return pyo.inequality(0.95**2, model.C[i, i], 1.05**2)
    
    model.voltage_limit = pyo.Constraint(model.buses, rule=voltage_limit_rule)
    
    # Power balance constraints
    def active_power_balance_rule(model, i):
        p_calc = sum(G[i, j] * model.C[i, j] - B[i, j] * model.S[i, j] for j in model.buses)
        
        p_total = (
            active_power_bus.get(i, 0.0) - active_power_load_bus.get(i, 0.0) + 
            active_power_bus_sgen.get(i, 0.0) + active_power_ext_grid.get(i, 0.0) + 
            model.flex_up[i] - model.flex_down[i]
        )
        
        return p_calc == p_total
    
    def reactive_power_balance_rule(model, i):
        q_calc = sum(-B[i, j] * model.C[i, j] - G[i, j] * model.S[i, j] for j in model.buses)
        
        q_total = (
            reactive_power_bus.get(i, 0.0) - reactive_power_load_bus.get(i, 0.0) + 
            reactive_power_bus_sgen.get(i, 0.0) + reactive_power_ext_grid.get(i, 0.0) + 
            model.flex_up_reactive[i] - model.flex_down_reactive[i]
        )
        
        return q_calc == q_total
    
    model.active_power_balance = pyo.Constraint(model.buses, rule=active_power_balance_rule)
    model.reactive_power_balance = pyo.Constraint(model.buses, rule=reactive_power_balance_rule)
    
    # Objective function - minimize total flexibility activation
    weight = 100  # Weight factor for objective
    def objective_rule(model):
        return weight * sum(
            model.flex_up[i] - model.flex_down[i] + 
            model.flex_up_reactive[i] - model.flex_down_reactive[i] 
            for i in model.buses
        )
    
    model.objective = pyo.Objective(rule=objective_rule, sense=pyo.minimize)
    
    return model

def solve_flexibility_model(model):
    """
    Solve the Pyomo optimization model
    """
    # Select solver (IPOPT for nonlinear optimization)
    solver = pyo.SolverFactory('ipopt')
    
    # Set solver options
    solver.options['max_iter'] = 5000
    solver.options['tol'] = 1e-6
    
    # Solve the model
    results = solver.solve(model, tee=True)
    
    # Check solution status
    if results.solver.status == pyo.SolverStatus.ok and results.solver.termination_condition == pyo.TerminationCondition.optimal:
        print("Optimal solution found!")
        return True
    elif results.solver.termination_condition == pyo.TerminationCondition.infeasible:
        print("Model is infeasible!")
        return False
    else:
        print(f"Solver Status: {results.solver.status}")
        print(f"Termination Condition: {results.solver.termination_condition}")
        return False

def extract_flexibility_results(model):
    """
    Extract flexibility values from the solved model
    """
    flex_results = {
        'flex_up': [pyo.value(model.flex_up[i]) for i in model.buses],
        'flex_down': [pyo.value(model.flex_down[i]) for i in model.buses],
        'flex_up_reactive': [pyo.value(model.flex_up_reactive[i]) for i in model.buses],
        'flex_down_reactive': [pyo.value(model.flex_down_reactive[i]) for i in model.buses]
    }
    
    return pd.DataFrame(flex_results)

def run_smfae(net_meas):
    """
    Main function to run the SMFAE module
    """
    # Create Y-bus matrix
    Y_bus = create_Y_bus(net_meas)
    
    # Create and solve the Pyomo model
    pyomo_model = create_pyomo_model(net_meas, Y_bus)
    
    # Solve the model
    solve_success = solve_flexibility_model(pyomo_model)
    
    if solve_success:
        # Extract and return results
        flex_results_df = extract_flexibility_results(pyomo_model)
        return flex_results_df
    else:
        return None

# Run this when the script is executed directly
if __name__ == "__main__":
    # Example usage
    import pandapower as pp
    import os
    from Data_preprocessing_BH import make_SCADA_df
    from create_BH_net import load_data, net_60kV_SCADA_measurements
    
    # Load network data
    net = pp.create_empty_network()
    excel_path = "Bornholm 20220706.xlsx"  # Adjust path as needed
    if os.path.exists(excel_path):
        net = load_data(excel_path, net)
        
        # Example SCADA measurements
        timestamp = '2022-03-09 17:30:00'
        substations = [
            ('Allinge', 'lok_10kvskinnespend'),
            ('Aakirkeby', 't1s_spending'),
            # Add other substations as needed
        ]
        
        # Load SCADA measurements
        df_SCADA_meas = make_SCADA_df(timestamp, substations)
        
        # Create network with measurements
        net_meas = net_60kV_SCADA_measurements(net, df_SCADA_meas)
        
        # Run SMFAE
        flex_results = run_smfae(net_meas)
        
        if flex_results is not None:
            print("Flexibility Results:")
            print(flex_results)
            
            # Calculate total flexibility
            total_flex_up = flex_results['flex_up'].sum()
            total_flex_down = flex_results['flex_down'].sum()
            print(f"Total Flex Up: {total_flex_up:.4f} MW")
            print(f"Total Flex Down: {total_flex_down:.4f} MW")
    else:
        print(f"File not found: {excel_path}")