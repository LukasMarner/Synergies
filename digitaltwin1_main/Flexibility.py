import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd




def make_bus_susceptance_matrix(net, congestion_factor, NB):
    net.line = net.line[net.line['in_service']]
    net.trafo = net.trafo[net.trafo['in_service']]
    delta_theta_max_deg = 10  # Example value
    delta_theta_max_rad = np.radians(delta_theta_max_deg) 

    # Iterate over each transformer in the network
    x_trafo = []
    flow_limits_trafo = []
    for i, trafo in net.trafo.iterrows():
        # Retrieve parameters
        u_k_percent = trafo['vk_percent']  # Short-circuit voltage in %
        s_rated_mva = trafo['sn_mva']  # Rated power in MVA
        u_hv_kv = trafo['vn_hv_kv']  # High voltage side voltage in kV
        
        # Convert to SI units
        u_hv_v = u_hv_kv   # Convert kV to V
        s_rated_va = s_rated_mva  # Convert MVA to VA
        
        # Calculate reactance in ohms
        x_ohm = (u_k_percent / 100) * (u_hv_v ** 2)
            # Calculate susceptance in siemens
        if x_ohm != 0:
            susceptance = 1 / x_ohm
            # Calculate power flow limit
            p_max = susceptance * delta_theta_max_rad #*s_rated_mva

        else:
            p_max = 0.5
        flow_limits_trafo.append(p_max)
        x_trafo.append(x_ohm)
    flow_limits_trafo = net.trafo['sn_mva']
    b_trafo = 1/np.array(x_trafo)
    from_bus_trafo = net.trafo['hv_bus']
    to_bus_trafo = net.trafo['lv_bus']
    from_bus = np.array(net.line['from_bus'])
    to_bus = np.array(net.line['to_bus'])
    #flow_limit = np.array(branch['RATE_A'])
    vn_from_kv = net.bus.loc[from_bus, 'vn_kv'].values 
    flow_limit = np.array(net.line['max_i_ka'])*np.array(vn_from_kv)
    b_lines = np.array(1 / (net.line['r_ohm_per_km']*net.line['length_km']))
    parallel_lines = net.line['parallel']
    parallel_lines_trafo = net.trafo['parallel']
    

    # Combine into a DataFrame
    df1 = pd.DataFrame({'from_bus': from_bus, 'to_bus': to_bus, 'flow_limit': flow_limit, 'b': b_lines, 'parallel': parallel_lines })
    df2 = pd.DataFrame({'from_bus': from_bus_trafo, 'to_bus': to_bus_trafo, 'flow_limit': flow_limits_trafo, 'b': b_trafo, 'parallel': parallel_lines_trafo })

    df = pd.concat([df1, df2], ignore_index=True)

    # Remove duplicate rows
    # df.drop_duplicates(subset=['from_bus', 'to_bus'], keep='last', inplace=True)
    duplicate_mask = df.duplicated(subset=['from_bus', 'to_bus'], keep='last')
    df.loc[duplicate_mask, 'parallel'] = 2

    # Initialize matrices
    b = np.zeros((NB, NB))
    branch_cap = np.zeros((NB, NB))

    # Fill matrices
    for i, row in df.iterrows():
        from_bus_idx = int(row['from_bus'])  # Convert to integer index
        to_bus_idx = int(row['to_bus'])      # Convert to integer index
        b_line = row['b']
        flow_lim = row['flow_limit']

        b[from_bus_idx, to_bus_idx] = b_line
        b[to_bus_idx, from_bus_idx] = b_line
        branch_cap[from_bus_idx, to_bus_idx] = congestion_factor*flow_lim
        branch_cap[to_bus_idx, from_bus_idx] = congestion_factor*flow_lim

    # Calculate diagonal elements of b matrix
    np.fill_diagonal(b, -np.sum(b, axis=1))

    return b, branch_cap, df

import numpy as np

def map_generators_to_buses(generators, net):
    generators = generators[generators['in_service']]
    NB = len(net.bus)
    map_generators = np.zeros((len(generators), NB))
    for i, bus in enumerate(generators['bus']):
        map_generators[i, bus] = 1
    return map_generators

def map_loads_to_buses(net):
    NB = len(net.bus)
    map_loads = np.zeros((len(net.load), NB))
    for i, bus in enumerate(net.load['bus']):
        map_loads[i, bus] = 1
    return map_loads

def map_ext_grid_to_bus(net):
    ext_grid = net.ext_grid
    NB = len(net.bus)
    map_ext_grid = np.zeros((len(ext_grid), NB))
    for i, bus in enumerate(ext_grid['bus']):
        map_ext_grid[i, bus] = 1
    return map_ext_grid

def minimize_flexibility(net, branch_cap, b,generators, ref_bus=0):
    loads = net.load['p_mw'].reset_index(drop=True)
    map_generators = map_generators_to_buses(generators, net)
    map_ext_grid = map_ext_grid_to_bus(net)
    map_loads = map_loads_to_buses(net)
    generators = generators[generators['in_service']].reset_index(drop=True)
    NB = len(net.bus)

    model = gp.Model()
    
    theta = [model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=f"theta{bus}") for bus in range(NB)]
    flex = [model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=f"flex{g}") for g in range(NB)]
    ext_grid = [model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=f"ext_grid") for g in range(NB)]
    model.addConstr(theta[ref_bus]==0)
    model.update()
    
    obj = gp.quicksum(flex[n] for n in range(NB))
    model.setObjective(obj, gp.GRB.MINIMIZE)

    bus_ext_grid = net.ext_grid['bus']
    for n in range(NB):
        if (n != bus_ext_grid.any()):
            model.addConstr(ext_grid[n] == 0)


    for n in range(NB):
        for m in range(NB):
            if (n != m):
                if (branch_cap[n][m]>0):
                    model.addConstr(b[n][m]*(theta[n]-theta[m]) == [-branch_cap[n][m], branch_cap[n][m]])


    #Definition of the constraints
    balance_constraint = {n:model.addConstr( # Balance equation expressed in p.u at each node
        -gp.quicksum(generators['p_mw'][g]*map_generators[g][n] for g in range(len(generators)))
        +gp.quicksum(b[n][m]*(theta[n]-theta[m]) for m in range(NB))
        +gp.quicksum(loads[g]*map_loads[g][n] for g in range(len(loads)))
        +flex[n],
        gp.GRB.EQUAL,
        0,name='Balance equation at node {0}'.format(n)) for n in range(NB)}


    model.update()
    model.printStats()
    # model.display()
    model.optimize()    

    return model, theta, flex

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
    df_filled['controllable'].fillna(False, inplace=True)
    # Step 5: Output the filled DataFrame
    net.load = df_filled
    return net.load

def fill_gen(net):
    df = net.res_gen
    df_sgen = net.res_sgen
    df['bus'] = net.gen['bus']
    df_sgen['bus'] = net.sgen['bus']

    # Step 1: Identify all buses (in this case 5 buses: 0, 1, 2, 3, 4)
    total_buses = len(net.bus)
    all_buses = pd.Series(range(total_buses))

    df = df.merge(df_sgen, on ='bus', how ='left')

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

def minimize_flexibility(net, branch_cap, b,generators, ref_bus=0):
    loads = net.load['p_mw'].reset_index(drop=True)
    map_generators = map_generators_to_buses(generators, net)
    map_ext_grid = map_ext_grid_to_bus(net)
    map_loads = map_loads_to_buses(net)
    generators = generators[generators['in_service']].reset_index(drop=True)
    NB = len(net.bus)

    model = gp.Model()
    
    theta = [model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=f"theta{bus}") for bus in range(NB)]
    flex_up = [model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=f"flex_up{g}") for g in range(NB)]
    flex_down = [model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=f"flex_down{g}") for g in range(NB)]
    model.addConstr(theta[ref_bus]==0)
    model.update()
    
    c = 100
    obj = c*gp.quicksum(flex_up[n] for n in range(NB)) + gp.quicksum(flex_down[n] for n in range(NB))
    model.setObjective(obj, gp.GRB.MINIMIZE)

    bus_ext_grid = net.ext_grid['bus']
    ext_grid = np.zeros(NB)
    ext_grid[bus_ext_grid] = net.res_ext_grid['p_mw']

    for n in range(NB):
        for m in range(NB):
            if (n != m):
                if (branch_cap[n][m]>0):
                    model.addConstr(b[n][m]*(theta[n]-theta[m]) == [-branch_cap[n][m], branch_cap[n][m]])


    #Definition of the constraints
    balance_constraint = {n:model.addConstr( # Balance equation expressed in p.u at each node
        -gp.quicksum(generators['p_mw'][g]*map_generators[g][n] for g in range(len(generators)))
        +gp.quicksum(b[n][m]*(theta[n]-theta[m]) for m in range(NB))
        +gp.quicksum(loads[g]*map_loads[g][n] for g in range(len(loads)))
        -flex_up[n]
        +flex_down[n]
        -ext_grid[n],
        gp.GRB.EQUAL,
        0,name='Balance equation at node {0}'.format(n)) for n in range(NB)}


    model.update()
    model.printStats()
    # model.display()
    model.optimize()    

    return model, theta, flex_up, flex_down

def maximize_epsilon_up(net, branch_cap, b,generators, cleared_flex_up, ref_bus=0):
    loads = net.load['p_mw'].reset_index(drop=True)
    map_generators = map_generators_to_buses(generators, net)
    map_ext_grid = map_ext_grid_to_bus(net)
    map_loads = map_loads_to_buses(net)
    generators = generators[generators['in_service']].reset_index(drop=True)
    NB = len(net.bus)

    model = gp.Model()
    
    theta = [model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=f"theta{bus}") for bus in range(NB)]
    # flex_up = [model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=f"flex_up{g}") for g in range(NB)]
    # flex_down = [model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=f"flex_down{g}") for g in range(NB)]
    epsilon_up = [model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=f"epsilon{g}") for g in range(NB)]
    model.addConstr(theta[ref_bus]==0)
    model.update()
    
    obj = gp.quicksum(epsilon_up[n] for n in range(NB))
    model.setObjective(obj, gp.GRB.MINIMIZE)

    model.addConstr(gp.quicksum(epsilon_up[n] for n in range(NB)) <= cleared_flex_up)

    bus_ext_grid = net.ext_grid['bus']
    ext_grid = np.zeros(NB)
    ext_grid[bus_ext_grid] = net.res_ext_grid['p_mw']

    for n in range(NB):
        for m in range(NB):
            if (n != m):
                if (branch_cap[n][m]>0):
                    model.addConstr(b[n][m]*(theta[n]-theta[m]) == [-branch_cap[n][m], branch_cap[n][m]])


    #Definition of the constraints
    balance_constraint = {n:model.addConstr( # Balance equation expressed in p.u at each node
        -gp.quicksum(generators['p_mw'][g]*map_generators[g][n] for g in range(len(generators)))
        +gp.quicksum(b[n][m]*(theta[n]-theta[m]) for m in range(NB))
        +gp.quicksum(loads[g]*map_loads[g][n] for g in range(len(loads)))
        -epsilon_up[n]
        -ext_grid[n],
        gp.GRB.EQUAL,
        0,name='Balance equation at node {0}'.format(n)) for n in range(NB)}


    model.update()
    model.printStats()
    # model.display()
    model.optimize()    

    return model, theta, epsilon_up

def maximize_epsilon_down(net, branch_cap, b,generators, cleared_flex_down, ref_bus=0):
    loads = net.load['p_mw'].reset_index(drop=True)
    map_generators = map_generators_to_buses(generators, net)
    map_ext_grid = map_ext_grid_to_bus(net)
    map_loads = map_loads_to_buses(net)
    generators = generators[generators['in_service']].reset_index(drop=True)
    NB = len(net.bus)

    model = gp.Model()
    
    theta = [model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, name=f"theta{bus}") for bus in range(NB)]
    # flex_up = [model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=f"flex_up{g}") for g in range(NB)]
    # flex_down = [model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=f"flex_down{g}") for g in range(NB)]
    epsilon_down = [model.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name=f"epsilon{g}") for g in range(NB)]
    model.addConstr(theta[ref_bus]==0)
    model.update()
    
    obj = gp.quicksum(epsilon_down[n] for n in range(NB))
    model.setObjective(obj, gp.GRB.MINIMIZE)

    model.addConstr(gp.quicksum(epsilon_down[n] for n in range(NB)) <= cleared_flex_down)

    bus_ext_grid = net.ext_grid['bus']
    ext_grid = np.zeros(NB)
    ext_grid[bus_ext_grid] = net.res_ext_grid['p_mw']

    for n in range(NB):
        for m in range(NB):
            if (n != m):
                if (branch_cap[n][m]>0):
                    model.addConstr(b[n][m]*(theta[n]-theta[m]) == [-branch_cap[n][m], branch_cap[n][m]])


    #Definition of the constraints
    balance_constraint = {n:model.addConstr( # Balance equation expressed in p.u at each node
        -gp.quicksum(generators['p_mw'][g]*map_generators[g][n] for g in range(len(generators)))
        +gp.quicksum(b[n][m]*(theta[n]-theta[m]) for m in range(NB))
        +gp.quicksum(loads[g]*map_loads[g][n] for g in range(len(loads)))
        +epsilon_down[n]
        -ext_grid[n],
        gp.GRB.EQUAL,
        0,name='Balance equation at node {0}'.format(n)) for n in range(NB)}


    model.update()
    model.printStats()
    # model.display()
    model.optimize()    

    return model, theta, epsilon_down
