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


def map_bus_names_to_lines(net):
    """
    Map bus names to line endpoints in a pandapower network.

    This function adds two new columns to net.line:
        - 'from_bus_name': The name of the bus at the 'from_bus' end of the line
        - 'to_bus_name': The name of the bus at the 'to_bus' end of the line

    It uses the 'from_bus' and 'to_bus' index values in net.line to look up
    corresponding 'name' entries in net.bus.

    Parameters
    ----------
    net : pandapowerNet
        The pandapower network object. Assumes net.bus has a 'name' column.

    Returns
    -------
    net : pandapowerNet
        The updated pandapower network with 'from_bus_name' and 'to_bus_name'
        columns added to net.line.
    """

    # -------------------- Step 1: Verify the 'name' column exists in net.bus --------------------
    if 'name' not in net.bus.columns:
        raise ValueError("The 'net.bus' DataFrame must contain a 'name' column.")

    # -------------------- Step 2: Create a mapping from bus index to bus name --------------------
    bus_name_map = net.bus['name'].to_dict()  # {bus_index: "bus_name"}

    # -------------------- Step 3: Map from_bus and to_bus to their names --------------------
    net.line['from_bus_name'] = net.line['from_bus'].map(bus_name_map)
    net.line['to_bus_name'] = net.line['to_bus'].map(bus_name_map)

    # -------------------- Step 4: Return the updated network --------------------
    return net


# In[3]:


def real_time_security_assessment(net):
    """
    Perform Real-Time Security Assessment (RSA) on a given pandapower network.

    Parameters
    ----------
    net : pandapowerNet
        The pandapower network object with assigned load and generation (p_mw, q_mvar) values.

    Returns
    -------
    net : pandapowerNet
        The updated pandapower network with power flow results after security analysis.

    The assessment includes the following components:
        1. Base Case Power Flow Analysis
        2. Voltage Violation Detection
        3. Thermal Overload Detection
        4. Reporting Dashboard
    """

    print("\n==================== Real-Time Security Assessment Engine (RSAE) ====================\n")

    # -------------------- Step 0: Map Bus Names to Lines --------------------
    print("[0] Mapping bus names to line endpoints...")
    map_bus_names_to_lines(net)

    # -------------------- Step 1: Run Base Case Power Flow Analysis --------------------
    print("[1] Running base case power flow...")
    try:
        pp.runpp(net)
        print("    ✅ Power flow successful.\n")
    except Exception as e:
        print("    ❌ Power flow did not converge.")
        print("    Error:", str(e))
        return net

    # -------------------- Step 2: Voltage Violation Check --------------------
    print("[2] Checking for voltage violations...")
    v_min, v_max = 0.95, 1.05
    voltage_violations = net.res_bus[(net.res_bus.vm_pu < v_min) | (net.res_bus.vm_pu > v_max)]
    print(f"    ⚡ Voltage Violations: {len(voltage_violations)}")

    # -------------------- Step 3: Thermal Overload Check --------------------
    print("[3] Checking for thermal overloads on lines...")
    overloads = net.res_line[net.res_line.loading_percent > 100]
    print(f"    🌡️ Line Overloads: {len(overloads)}")

    # -------------------- Step 4: Reporting Dashboard --------------------
    print("\n📊 ================= Security Assessment Dashboard ================ 📊\n")

    if not voltage_violations.empty:
        print("🔺 Voltage Violations Detected:")
        for idx, row in voltage_violations.iterrows():
            bus_name = net.bus.at[idx, 'name'] if 'name' in net.bus.columns else f"Bus {idx}"
            print(f"    - Bus {idx} ({bus_name}): Voltage = {row.vm_pu:.3f} p.u.")
    else:
        print("✅ No voltage violations.")

    print("\n" + "-"*70 + "\n")

    if not overloads.empty:
        print("🔺 Thermal Overloads Detected:")
        for idx, row in overloads.iterrows():
            line_name = net.line.at[idx, 'name'] if 'name' in net.line.columns else f"Line {idx}"
            from_name = net.line.at[idx, 'from_bus_name'] if 'from_bus_name' in net.line.columns else row.from_bus
            to_name = net.line.at[idx, 'to_bus_name'] if 'to_bus_name' in net.line.columns else row.to_bus
            print(f"    - Line {idx} ({line_name}): {from_name} ➝ {to_name}, Loading = {row.loading_percent:.2f}%")
    else:
        print("✅ No line overloads.")

    print("\n" + "-"*70 + "\n")
    print("\n===============================================================================\n")

    return net


# In[ ]:




