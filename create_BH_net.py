## Creating Bornholm network
## Author: Emilie Jong (Technical University of Denmark)

# Inside create_BH_net.py
import pandas as pd
# Import only what you need from pandapower instead of the whole module
from pandapower import create_empty_network, create_bus, create_gen
import pandapower as pp
# Add other specific imports as needed
### BASE CASE
# path = "C:/Users/emijo/OneDrive - Danmarks Tekniske Universitet/Dokumenter/SYNERGIES/Data BH"
# file = 'Bornholm 20220706.xlsx'

def load_data(path, net):
        ## Load data
    std_types_lines = pd.read_excel(path, sheet_name = 'line_std_types')
    std_types_trafo = pd.read_excel(path, sheet_name = 'trafo_std_types')
    net_bh = pp.from_excel(path, convert=True)
    std_types_lines.set_index('Unnamed: 0', inplace=True)
    std_types_dict = {}

    # Iterate over the rows of the DataFrame
    for index, row in std_types_lines.iterrows():
        # Create a dictionary for the current row
        row_dict = row.to_dict()
        # Use the index as the key for the outer dictionary
        std_types_dict[index] = row_dict

    for key, attributes in std_types_dict.items():
        pp.create_std_type(net, data=attributes, name=key, element='line')

    std_types_trafo.set_index('Unnamed: 0', inplace=True)
    std_types_dict = {}
    # Iterate over the rows of the DataFrame
    for index, row in std_types_trafo.iterrows():
        # Create a dictionary for the current row
        row_dict = row.to_dict()
        # Use the index as the key for the outer dictionary
        std_types_dict[index] = row_dict

    for key, attributes in std_types_dict.items():
        pp.create_std_type(net, data=attributes, name=key, element='trafo')

    ## Create missing std line types
    #c_nf_per_km, r_ohm_per_km, x_ohm_per_km and max_i_ka (for lines)
    line_parameters = {
    'r_ohm_per_km': 0.32,  # Resistance in ohms per kilometer
    'x_ohm_per_km': 0.098,  # Reactance in ohms per kilometer
    'c_nf_per_km': 0.241,  # Capacitance in nanofarads per kilometer
    'max_i_ka': 310  # Maximum current carrying capacity in kiloamps
    }
    pp.create_std_type(net, data=line_parameters,name='3x95 PEX AL + 25 CU', element='line', overwrite=True, check_required=True)
    line_parameters = {
    'r_ohm_per_km': 0.32,  # Resistance in ohms per kilometer
    'x_ohm_per_km': 0.641,  # Reactance in ohms per kilometer
    'c_nf_per_km': 0.107,  # Capacitance in nanofarads per kilometer
    'max_i_ka': 250  # Maximum current carrying capacity in kiloamps
    }
    pp.create_std_type(net, data=line_parameters,name='3x50 PEX AL + 16 CU', element='line', overwrite=True, check_required=True)
    # pp.create_std_type(net, data=[250, 0.32, 0.641, 0.107],name='3x50 PEX AL + 16 CU', element='line', overwrite=True, check_required=True)
    

    return net

## Net based on available measurements
def net_60kV(net):
    vn_kv = 63
    max_vm_pu = 1.05
    min_vm_pu = 0.95


    ## Create substations Net 60 kv
    bus_HAS_A = pp.create_bus(net, vn_kv, name='Hasle A', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_HAS_B = pp.create_bus(net, vn_kv, name='Hasle B', index=None, geodata=None, type='b', zone=None, in_service=False,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SNO = pp.create_bus(net, vn_kv, name='Snorrebakken', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OLS = pp.create_bus(net, vn_kv, name='Olsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_RNO = pp.create_bus(net, vn_kv, name='Ronne Nord', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOR_HAS = pp.create_bus(net, vn_kv, name='BOR-HAS split 3', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    bus_ALL = pp.create_bus(net, vn_kv, name='Allinge', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SVA = pp.create_bus(net, vn_kv, name='Svaneke', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_NEX = pp.create_bus(net, vn_kv, name='Nexo', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOD = pp.create_bus(net, vn_kv, name='Bodilsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_POU = pp.create_bus(net, vn_kv, name='Poulsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_AAK = pp.create_bus(net, vn_kv, name='Aakirkeby', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_DAL = pp.create_bus(net, vn_kv, name='Dalslunde', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OST = pp.create_bus(net, vn_kv, name='Osterlars', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OLS = pp.create_bus(net, vn_kv, name='Olsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_GUD = pp.create_bus(net, vn_kv, name='Gudhjem', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VIA_A = pp.create_bus(net, vn_kv, name='Viadukten A', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VIA_B = pp.create_bus(net, vn_kv, name='Viadukten B', index=None, geodata=None, type='b', zone=None, in_service=False,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_RNS = pp.create_bus(net, vn_kv, name='Ronne Syd', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VAE_A = pp.create_bus(net, vn_kv, name='Vaerket A', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VAE_B = pp.create_bus(net, vn_kv, name='Vaerket B', index=None, geodata=None, type='b', zone=None, in_service=False, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VES = pp.create_bus(net, vn_kv, name='Vesthavnen', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    aux_bus_VIA_1 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 1', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_2 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 2', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_3 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 3', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    ## Create lines 60 kV side
    line_HAS_A_SNO = pp.create_line(net, from_bus=bus_HAS_A, to_bus = bus_SNO, std_type = 'OHL 3x1x130StAl+50Fe', length_km=5.217 )
    line_SNO_VAE_A = pp.create_line(net, from_bus=bus_SNO, to_bus = bus_VAE_A, std_type = 'APBF 1x3x95 Cu', length_km=3.453)
    line_VAE_A_VES = pp.create_line(net, from_bus=bus_VES, to_bus = bus_VAE_A, std_type = 'PEX 3x1x300Al+35Cu', length_km=1.8)
    line_VAE_A_VIA_A = pp.create_line(net, from_bus=aux_bus_VIA_1, to_bus = bus_VAE_A, std_type = 'PEX 3x1x300Al+35Cu', length_km=1.481)
    line_VAE_A_RNS = pp.create_line(net, from_bus=bus_VAE_A, to_bus=bus_RNS, std_type = 'APBF 1x3x95 Cu', length_km=2.861)
    line_VES_RNO = pp.create_line(net, from_bus=bus_RNO, to_bus = bus_VES, std_type = 'PEX 3x1x300Al+35Cu', length_km=2.2)
    line_HAS_A_RNO = pp.create_line(net, from_bus=bus_HAS_A, to_bus = bus_RNO, std_type = 'PEX 3x1x240Al+35Cu', length_km=7.434)
    line_VIA_A_RNO = pp.create_line(net, from_bus=aux_bus_VIA_2, to_bus = bus_RNO, std_type = 'PEX 3x1x240Al+35Cu', length_km=1.834)
    line_VIA_A_RNS = pp.create_line(net, from_bus=aux_bus_VIA_3, to_bus = bus_RNS, std_type = 'PEX 3x1x240Al+35Cu', length_km=1.674)
    line_RNS_AAK = pp.create_line(net, from_bus=bus_AAK, to_bus = bus_RNS, std_type = 'OHL 3x1x130StAl+50Fe', length_km=10.995)
    line_BOD_AAK = pp.create_line(net, from_bus=bus_AAK, to_bus = bus_BOD, std_type = 'OHL 3x1x130StAl+50Fe', length_km=10.891)
    line_BOD_POU = pp.create_line(net, from_bus=bus_POU, to_bus = bus_BOD, std_type = 'PEX 3x1x150Al+25Cu', length_km=5.95)
    line_BOD_NEX = pp.create_line(net, from_bus=bus_NEX, to_bus = bus_BOD, std_type = 'PEX 3x1x95Al+25Cu', length_km=3.477)
    line_BOD_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_BOD, std_type = 'OHL 3x1x130StAl+50Fe', length_km=4.138)
    line_SVA_NEX = pp.create_line(net, from_bus=bus_NEX, to_bus = bus_SVA, std_type = 'PEX 3x1x150Al+25Cu', length_km=9.78)
    line_SVA_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_SVA, std_type = 'PEX 3x1x150Al+25Cu', length_km=7.531)
    line_OST_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_OST, std_type = 'OHL 3x1x130StAl+50Fe', length_km=9.924)
    line_OST_GUD = pp.create_line(net, from_bus=bus_GUD, to_bus = bus_OST, std_type = 'PEX 3x1x150Al+25Cu', length_km=6.6)
    line_OST_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_OST, std_type = 'OHL 3x1x130StAl+50Fe', length_km=13.05)
    line_ALL_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_ALL, std_type = 'PEX 3x1x150Al+25Cu', length_km=4.276)
    line_HAS_A_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_HAS_A, std_type = 'OHL 3x1x130StAl+50Fe', length_km=6.818)
    line_BOR_HAS_A = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_HAS_A, std_type = 'PEX 3x1x400CuPbAl', length_km=1.4)
    #line_BOR_HAS_3 = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_HAS_A, std_type = 'PEX 3x1x240CuPbAl', length_km=43.5)

    ## Switches

    # switch_VIA_A_1 = pp.create_switch(net, bus_VIA_A, line_VIA_A_RNO, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_A_2 = pp.create_switch(net, bus_VIA_A, line_VAE_A_VIA_A, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_A_3 = pp.create_switch(net, bus_VIA_A, line_VIA_A_RNS, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNO, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, line_VAE_A_VIA_A, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNS, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)

    switch_VIA_A_1 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_1, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_A_2 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_2, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_A_3 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_3, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)

    switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_1, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_2, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_3, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)


    # switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNO, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, line_VAE_A_VIA_A, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNS, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    ## TODO include switches VAE A and B


    ## External grid Sweden
    bus_BOR_HAS_split1 = pp.create_bus(net, vn_kv, name='BOR HAS split 1', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOR_HAS_split2 = pp.create_bus(net, vn_kv, name='BOR HAS split 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_borr = pp.create_bus(net, vn_kv, name='Borrby', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    line_BOR_HAS_2 = pp.create_line(net, from_bus=bus_BOR_HAS_split2, to_bus = bus_BOR_HAS_split1, std_type = 'PEX 3x1x400CuPbAl', length_km=0.7)
    line_BOR_HAS_1 = pp.create_line(net, from_bus=bus_BOR_HAS_split1, to_bus = bus_borr, std_type = 'IBIS 3x1x234', length_km=4.2)
    line_BOR_HAS_3 = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_BOR_HAS_split2, std_type = 'PEX 3x1x240CuPbAl', length_km=43.5)
    bus_tom = pp.create_bus(net, 135, name='Tomelilla', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_borr = pp.create_transformer(net, hv_bus = bus_tom, lv_bus = bus_borr, std_type = 'Trf 135-69 kV')
    # bus_N_punkt_Borr = pp.create_bus(net, vn_kv, name='N punkt Borrby', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    # sw_Borr = pp.create_switch(net, bus, element, et, closed=True, type=None, name=None, index=None, z_ohm=0)
    ext_grid = pp.create_ext_grid(net, bus_tom, vm_pu =0.91, va_degree = 0.0, slack_weight = 1.0)
    net.ext_grid.at[0, 'vm_pu'] = 0.91
    # gen = pp.create_gen(net, bus_VIA_A, p_mw = 0.0001)

    vn_kv = 10.5

    ## Gen Vaerket
    bus_VAE_blok_6 = pp.create_bus(net, vn_kv, name='Vaerket Blok 6', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_blok_6 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_blok_6, name ='Trf blok 6', std_type='Trf-6 45 MVA', in_service=False)
    VAE_gen_blok_6 = pp.create_gen(net, bus_VAE_blok_6, p_mw = 36, vm_pu=1.0, name='Blok 6 gen',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)

    bus_VAE_blok_5 = pp.create_bus(net, vn_kv, name='Vaerket Blok 5', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_blok_6 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_blok_5, name ='Trf blok 5', std_type='Trf-5 29 MVA', in_service=False)
    VAE_gen_blok_5 = pp.create_gen(net, bus_VAE_blok_6, p_mw =23.52, sn_mva=29, vm_pu=1.0, name='Blok 5 gen',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)

    bus_VAE_Diesler = pp.create_bus(net, vn_kv, name='Vaerket Diesler', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_1 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_Diesler, name ='Trf Vaerket 1', std_type='Trf-1 16/20 MVA', in_service=False)
    VAE_Diesel_1 = pp.create_gen(net, bus_VAE_Diesler, p_mw =4.66, sn_mva=5.825, vm_pu=1.0, name='Diesel 1',scaling=1.0, slack=False, cos_phi=0.8, in_service=False)
    VAE_Diesel_2 = pp.create_gen(net, bus_VAE_Diesler, p_mw =4.66, sn_mva=5.825, vm_pu=1.0, name='Diesel 2',scaling=1.0, slack=False, cos_phi=0.8, in_service=False)
    VAE_Diesel_3 = pp.create_gen(net, bus_VAE_Diesler, p_mw =5.068, sn_mva=6.335, vm_pu=1.0, name='Diesel 3',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)
    VAE_Diesel_4 = pp.create_gen(net, bus_VAE_Diesler, p_mw =5.068, sn_mva=6.335, vm_pu=1.0, name='Diesel 4',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)

    bus_VAER_N = pp.create_bus(net, vn_kv, name='Vaer N', type='b', in_service=False, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_1 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAER_N, name ='Trf Vaerket 1 - 1', std_type='Trf-1 16/20 MVA', in_service=False)
    




    ## 00 Dampvaerket

    
    bus_DMP_A = pp.create_bus(net, vn_kv, name='Dampværk A', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_DMP_B = pp.create_bus(net, vn_kv, name='Dampværk B', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_DMP = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # aux_bus_trafo_DMP_2 = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_DMP1 = pp.create_switch(net, aux_bus_DMP, bus_DMP_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_DMP2 = pp.create_switch(net, aux_bus_DMP, bus_DMP_B, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    trafo_DMP = pp.create_transformer(net, hv_bus = bus_VAE_A, lv_bus = aux_bus_DMP, name='Værket Trf 2', std_type='Trf-2 25/31.5 MVA')

    aux_bus_DMP_2 = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_DMP3 = pp.create_switch(net, aux_bus_DMP_2, bus_DMP_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_DMP4 = pp.create_switch(net, aux_bus_DMP_2, bus_DMP_B, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)

    DMP_shunt = pp.create_shunt(net, bus_DMP_A, q_mvar=0.8, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)
    DMP_shunt_var = pp.create_shunt(net, bus_DMP_A, q_mvar=3.2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    DMP_load = pp.create_load(net, aux_bus_DMP_2, p_mw=1.37, q_mvar = 0.26)


    ## 01 Snorrebakken


    bus_SNO_10 = pp.create_bus(net, vn_kv, name='Snorrebakken 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SNO_SMED = pp.create_bus(net, vn_kv, name='94 Smedegaard', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SNO_YPP = pp.create_bus(net, vn_kv, name='566 Ypperne', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SNO_KNUD = pp.create_bus(net, vn_kv, name='995 Knudser VP ', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    line_SNO_10_SMED = pp.create_line(net, from_bus=bus_SNO_10, to_bus = bus_SNO_SMED, std_type = '3x95 PEX AL + 25 CU', length_km=5.751)
    line_YPP_SMED = pp.create_line(net, from_bus=bus_SNO_YPP, to_bus = bus_SNO_SMED, std_type = '3x50 PEX AL + 16 CU', length_km=1.21)
    line_SNO_KNUD = pp.create_line(net, from_bus=bus_SNO_YPP, to_bus = bus_SNO_SMED, std_type = '3x95 PEX AL + 25 CU', length_km=0.452)

    trafo_SNO = pp.create_transformer(net, hv_bus = bus_SNO, lv_bus = bus_SNO_10, name='Snorrebakken Trf', std_type='Trf 10 MVA ek 8.5 er 0.62')

    # ## Create loads
    # load_VIA_A = pp.create_load(net, bus_VIA_A,p_mw=0.929, q_mvar=0.478)
    SNO_load = pp.create_load(net, bus_SNO_10,p_mw=0.883, q_mvar=0.129)

    ## Create generators
    SNO_husstandsmoller = pp.create_sgen(net, bus_SNO_10, p_mw=2, q_mvar = 0, slack=True)
    SNO_WTG566 = pp.create_sgen(net, bus_SNO_YPP, p_mw=0.26, q_mvar = 0)
    SNO_WT955 = pp.create_sgen(net, bus_SNO_YPP, p_mw=2.4, q_mvar = 0)

    ## Hasle
    # aux_bus_HAS_A_B_1 = pp.create_bus(net, 63, name='Aux bus Hasle 1', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # aux_bus_HAS_A_B_2 = pp.create_bus(net, 63, name='Aux bus Hasle 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_trafo_HAS_1 = pp.create_bus(net, 63, name='Aux bus trafo HASLE', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_trafo_HAS_2 = pp.create_bus(net, 63, name='Aux bus trafo HASLE', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_1, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_1, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)
    switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)

    bus_HAS_10 = pp.create_bus(net, vn_kv, name='Hasle 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    
    trafo_HAS1 = pp.create_transformer(net, hv_bus = aux_bus_trafo_HAS_1, lv_bus = bus_HAS_10, name='Hasle Trf 1', std_type='Trf 10 MVA ek 8.87 er 0.54', in_service=False)
    trafo_HAS2 = pp.create_transformer(net, hv_bus = aux_bus_trafo_HAS_2, lv_bus = bus_HAS_10, name='Hasle Trf 2', std_type='Trf 10 MVA ek 8.87 er 0.54')

    bus_HAS_TOR = pp.create_bus(net, vn_kv, name='1042 Tornby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_HAS_VYS = pp.create_bus(net, vn_kv, name='1020 Vysteby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_HAS_HAS = pp.create_bus(net, vn_kv, name='851 Hasle VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    HAS_husstandsmoller = pp.create_sgen(net, bus_HAS_10, p_mw=2, q_mvar = 0, slack=True)
    HAS_load = pp.create_load(net, bus_HAS_10,p_mw=0.641, q_mvar=-0.437)


    HAS_WTG1042 = pp.create_sgen(net, bus_HAS_TOR, p_mw=6.9, q_mvar = 0)
    HAS_WTG1020 = pp.create_sgen(net, bus_HAS_VYS, p_mw=5.25, q_mvar = 0)
    HAS_WTG851 = pp.create_sgen(net, bus_HAS_HAS, p_mw=3.9, q_mvar = 0)

    line_HAS_10_TOR = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_TOR, std_type = '3x150 PEX AL+25 CU', length_km=2.944, parallel=2)
    line_HAS_10_VYS = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_VYS, std_type = '3x 240 PEX AL + 35 CU', length_km=5.293, parallel=1)
    line_HAS_10_HAS = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_HAS, std_type = '3x150 PEX AL+25 CU', length_km=3.9, parallel=1)
    
    ## OLSKER

    bus_OLS_10 = pp.create_bus(net, vn_kv, name='Olsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    trafo_OLS1 = pp.create_transformer(net, hv_bus = bus_OLS, lv_bus = bus_OLS_10, name='Olsker Trf 1', std_type='Trf 4 MVA ek 7.4 er 0.3')
    trafo_OLS2 = pp.create_transformer(net, hv_bus = bus_OLS, lv_bus = bus_OLS_10, name='Olsker Trf 2', std_type='Trf 4 MVA ek 7.4 er 0.3', in_service=False)

    OLS_husstandsmoller = pp.create_sgen(net, bus_OLS_10, p_mw=2, q_mvar = 0, slack=True)
    OLS_load = pp.create_load(net, bus_OLS_10,p_mw=0.615, q_mvar=-0.354)

    ## Østerlars
    bus_OST_10 = pp.create_bus(net, vn_kv, name='Østerlars 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_OST = pp.create_transformer(net, hv_bus = bus_OST, lv_bus = bus_OST_10, name='Østerlars Trf 1', std_type='Trf 16 MVA ek 8.8 er 0.3')
    OST_husstandsmoller = pp.create_sgen(net, bus_OST_10, p_mw=2, q_mvar = 0, slack=True)
    OST_load = pp.create_load(net, bus_OST_10,p_mw=0.922, q_mvar=-0.109)

    ## Åkirkeby
    bus_AAK_10 = pp.create_bus(net, vn_kv, name='Åkirkeby 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # trafo_AAK22 = pp.create_transformer(net, hv_bus = bus_AAK, lv_bus = bus_AAK_10, name='Aakirkeby Trf 21', std_type='Trf 16 MVA ek 8.8 er 0.', in_service=False)
    trafo_AAK21 = pp.create_transformer(net, hv_bus = bus_AAK, lv_bus = bus_AAK_10, name='Aakirkeby Trf 22', std_type='Trf 25/31.5 MVA ek 10%', in_service=True)
    AAK_husstandsmoller = pp.create_sgen(net, bus_AAK_10, p_mw=2, q_mvar = 0, slack=True)
    AAK_load = pp.create_load(net, bus_AAK_10,p_mw=1.587, q_mvar=-0.578)

    bus_AAK_BOD = pp.create_bus(net, vn_kv, name='Bodelyngsvejen 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    line_AAK_10_BOD = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_BOD, std_type = '3x150 PEX AL+25 CU', length_km=1.25, parallel=2)
    AAK_PV = pp.create_sgen(net, bus_AAK_BOD, p_mw=7.5, q_mvar = 0, slack=True)

    bus_AAK_KAL = pp.create_bus(net, vn_kv, name='Kalby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    line_AAK_10_BOD = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_KAL, std_type = '3x150 PEX AL+25 CU', length_km=0.516, parallel=2)
    AAK_WTG965 = pp.create_sgen(net, bus_AAK_KAL, p_mw=6, q_mvar = 0, slack=True)

    bus_AAK_SOS = pp.create_bus(net, vn_kv, name='Sose VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    line_AAK_10_SOS = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_SOS, std_type = '3x150 PEX AL+25 CU', length_km=3.24, parallel=2)
    AAK_WTG1004 = pp.create_sgen(net, bus_AAK_KAL, p_mw=6.5, q_mvar = 0, slack=True)

    bus_AAK_BIO = pp.create_bus(net, vn_kv, name='Biogas', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    line_AAK_10_BIO = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_BIO, std_type = '3x95 PEX AL + 25 CU', length_km=2.314, parallel=1)
    AAK_BIO1 = pp.create_gen(net, bus_AAK_BIO, p_mw = 1.521,sn_mva=1.981, vm_pu=1.0, name='Biogas gen 1',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)
    AAK_BIO2 = pp.create_gen(net, bus_AAK_BIO, p_mw = 1.521,sn_mva=1.981, vm_pu=1.0, name='Biogas gen 1',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)

    ## Nexø
    bus_NEX_10 = pp.create_bus(net, vn_kv, name='Nexø 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_NEX1 = pp.create_transformer(net, hv_bus = bus_NEX, lv_bus = bus_NEX_10, name='Nexø Trf 1', std_type='SEA 63/11 10 MVA NEXØ', in_service=True)
    trafo_NEX2 = pp.create_transformer(net, hv_bus = bus_NEX, lv_bus = bus_NEX_10, name='Nexø Trf 2', std_type='Trf 10 MVA ek 8.4 er 0.61', in_service=False)
    NEX_husstandsmoller = pp.create_sgen(net, bus_NEX_10, p_mw=2, q_mvar = 0, slack=True)
    NEX_load = pp.create_load(net, bus_NEX_10,p_mw=1.079, q_mvar=0.137)

    ## Bodilsker
    bus_BOD_10 = pp.create_bus(net, vn_kv, name='Bodilsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_BOD = pp.create_transformer(net, hv_bus = bus_BOD, lv_bus = bus_BOD_10, name='Bodilsker Trf 1', std_type='Trf 10/12 MVA ek 8.87 er 0.54', in_service=True)
    BOD_husstandsmoller = pp.create_sgen(net, bus_BOD_10, p_mw=2, q_mvar = 0, slack=True)
    BOD_load = pp.create_load(net, bus_BOD_10,p_mw=0.618, q_mvar=-0.026)
    BOD_shunt = pp.create_shunt(net, bus_BOD_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)
    bus_BOD_GAD = pp.create_bus(net, vn_kv, name='Gadeby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    line_BOD_GAD = pp.create_line(net, from_bus=bus_BOD_10, to_bus = bus_BOD_GAD, std_type = '3x95 PEX AL + 25 CU', length_km=2.48, parallel=1)
    BOD_WTG1001 = pp.create_sgen(net, bus_BOD_GAD, p_mw=2.7, q_mvar = 0, slack=True)

    ## Rønne Syd
    bus_RNS_10 = pp.create_bus(net, vn_kv, name='Rønne Syd 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_RNS1 = pp.create_transformer(net, hv_bus = bus_RNS, lv_bus = bus_RNS_10, name='Nexø Trf 1', std_type='Trf 10 MVA ek 8.3 er 0.62', in_service=True)
    RNS_husstandsmoller = pp.create_sgen(net, bus_RNS_10, p_mw=2, q_mvar = 0, slack=True)
    RNS_load = pp.create_load(net, bus_RNS_10,p_mw=1.128, q_mvar=-0.124)
    RNS_shunt = pp.create_shunt(net, bus_RNS_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    ## Allinge
    bus_ALL_10 = pp.create_bus(net, vn_kv, name='Allinge 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_ALL1 = pp.create_transformer(net, hv_bus = bus_ALL, lv_bus = bus_ALL_10, name='Allinge Trf 1', std_type='Trf 10 MVA ek 8.4 er 0.61', in_service=True)
    trafo_ALL2 = pp.create_transformer(net, hv_bus = bus_ALL, lv_bus = bus_ALL_10, name='Allinge Trf 2', std_type='Trf 10 MVA ek 8.04 er 0.53', in_service=False)
    ALL_husstandsmoller = pp.create_sgen(net, bus_ALL_10, p_mw=2, q_mvar = 0, slack=True)
    ALL_load = pp.create_load(net, bus_ALL_10,p_mw=0.78, q_mvar=-0.266)

    ## Svaneke
    bus_SVAN_10 = pp.create_bus(net, vn_kv, name='Svaneke 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_SVAN1 = pp.create_transformer(net, hv_bus = bus_SVA, lv_bus = bus_SVAN_10, name='Allinge Trf 1', std_type='Trf 10 MVA ek 8.3 er 0.54', in_service=True)
    SVAN_husstandsmoller = pp.create_sgen(net, bus_SVAN_10, p_mw=2, q_mvar = 0, slack=True)
    SVAN_load = pp.create_load(net, bus_SVAN_10,p_mw=0.923, q_mvar=0.043)
    SVAN_shunt = pp.create_shunt(net, bus_RNS_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    ## Viadukten
    bus_VIA_10 = pp.create_bus(net, vn_kv, name='Viadukten 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_4 = pp.create_bus(net, 63, name='Auxiliary bus Viadukten 4', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_VIA_A_4 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_4, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_4 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_4, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)
    trafo_VIA1 = pp.create_transformer(net, hv_bus = aux_bus_VIA_4, lv_bus = bus_VIA_10, name='Viadukten Trf 1', std_type='Trf 10 MVA ek 7.9 er 0.54', in_service=True)
    VIA_husstandsmoller = pp.create_sgen(net, bus_VIA_10, p_mw=2, q_mvar = 0, slack=True)
    VIA_load = pp.create_load(net, bus_VIA_10,p_mw=0.929, q_mvar=0.478)

    ## Rønne Nord
    bus_RNO_10 = pp.create_bus(net, vn_kv, name='Rønne Nord 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_RNO = pp.create_transformer(net, hv_bus = bus_RNO, lv_bus = bus_RNO_10, name='Rønne Nord Trf 1', std_type='Trf 10 MVA ek 7.94 er 0.58', in_service=True)
    RNO_husstandsmoller = pp.create_sgen(net, bus_RNO_10, p_mw=2, q_mvar = 0, slack=True)
    RNO_load = pp.create_load(net, bus_RNO_10,p_mw=0.866, q_mvar=0.58)

    ## Poulsker
    bus_POU_10 = pp.create_bus(net, vn_kv, name='Poulsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_POU = pp.create_transformer(net, hv_bus = bus_POU, lv_bus = bus_POU_10, name='Poulsker Trf 1', std_type='Trf 10 MVA ek 8.14 er 0.59', in_service=True)
    POU_husstandsmoller = pp.create_sgen(net, bus_POU_10, p_mw=2, q_mvar = 0, slack=True)
    POU_load = pp.create_load(net, bus_POU_10,p_mw=0.405, q_mvar=-0.546)

    ## Vesthavnen
    bus_VES_10 = pp.create_bus(net, vn_kv, name='Vesthavnen 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VES = pp.create_transformer(net, hv_bus = bus_VES, lv_bus = bus_VES_10, name='Vesthavnen Trf 1', std_type='Trf 10 MVA ek 8.1 er 0.54', in_service=True)
    VES_husstandsmoller = pp.create_sgen(net, bus_VES_10, p_mw=2, q_mvar = 0, slack=True)
    VES_load = pp.create_load(net, bus_VES_10,p_mw=0.317, q_mvar=-0.154)

    ## Gudhjem
    bus_GUD_10 = pp.create_bus(net, vn_kv, name='Gudhjem 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_GUD = pp.create_transformer(net, hv_bus = bus_GUD, lv_bus = bus_GUD_10, name='Gudhjem Trf 1', std_type='Trf 4 MVA ek 7.3 er 0.3 N.2', in_service=True)
    GUD_husstandsmoller = pp.create_sgen(net, bus_GUD_10, p_mw=2, q_mvar = 0, slack=True)
    GUD_load = pp.create_load(net, bus_GUD_10,p_mw=0.608, q_mvar=-0.143)


    return net


## More detailed version
def net_60kV_10kV(net):
    vn_kv = 63
    max_vm_pu = 1.05
    min_vm_pu = 0.95


    ## Create substations Net 60 kv
    bus_HAS_A = pp.create_bus(net, vn_kv, name='Hasle A', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_HAS_B = pp.create_bus(net, vn_kv, name='Hasle B', index=None, geodata=None, type='b', zone=None, in_service=False,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SNO = pp.create_bus(net, vn_kv, name='Snorrebakken', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OLS = pp.create_bus(net, vn_kv, name='Olsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_RNO = pp.create_bus(net, vn_kv, name='Ronne Nord', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOR_HAS = pp.create_bus(net, vn_kv, name='BOR-HAS split 3', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    bus_ALL = pp.create_bus(net, vn_kv, name='Allinge', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SVA = pp.create_bus(net, vn_kv, name='Svaneke', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_NEX = pp.create_bus(net, vn_kv, name='Nexo', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOD = pp.create_bus(net, vn_kv, name='Bodilsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_POU = pp.create_bus(net, vn_kv, name='Poulsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_AAK = pp.create_bus(net, vn_kv, name='Aakirkeby', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_DAL = pp.create_bus(net, vn_kv, name='Dalslunde', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OST = pp.create_bus(net, vn_kv, name='Osterlars', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OLS = pp.create_bus(net, vn_kv, name='Olsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_GUD = pp.create_bus(net, vn_kv, name='Gudhjem', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VIA_A = pp.create_bus(net, vn_kv, name='Viadukten A', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VIA_B = pp.create_bus(net, vn_kv, name='Viadukten B', index=None, geodata=None, type='b', zone=None, in_service=False,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_RNS = pp.create_bus(net, vn_kv, name='Ronne Syd', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VAE_A = pp.create_bus(net, vn_kv, name='Vaerket A', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VAE_B = pp.create_bus(net, vn_kv, name='Vaerket B', index=None, geodata=None, type='b', zone=None, in_service=False, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VES = pp.create_bus(net, vn_kv, name='Vesthavnen', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    ## Create lines 60 kV side
    line_HAS_A_SNO = pp.create_line(net, from_bus=bus_HAS_A, to_bus = bus_SNO, std_type = 'OHL 3x1x130StAl+50Fe', length_km=5.217 )
    line_SNO_VAE_A = pp.create_line(net, from_bus=bus_SNO, to_bus = bus_VAE_A, std_type = 'APBF 1x3x95 Cu', length_km=3.453)
    line_VAE_A_VES = pp.create_line(net, from_bus=bus_VES, to_bus = bus_VAE_A, std_type = 'PEX 3x1x300Al+35Cu', length_km=1.8)
    line_VAE_A_VIA_A = pp.create_line(net, from_bus=bus_VIA_A, to_bus = bus_VAE_A, std_type = 'PEX 3x1x300Al+35Cu', length_km=1.481)
    line_VAE_A_RNS = pp.create_line(net, from_bus=bus_VAE_A, to_bus=bus_RNS, std_type = 'APBF 1x3x95 Cu', length_km=2.861)
    line_VES_RNO = pp.create_line(net, from_bus=bus_RNO, to_bus = bus_VES, std_type = 'PEX 3x1x300Al+35Cu', length_km=2.2)
    line_HAS_A_RNO = pp.create_line(net, from_bus=bus_HAS_A, to_bus = bus_RNO, std_type = 'PEX 3x1x240Al+35Cu', length_km=7.434)
    line_VIA_A_RNO = pp.create_line(net, from_bus=bus_VIA_A, to_bus = bus_RNO, std_type = 'PEX 3x1x240Al+35Cu', length_km=1.834)
    line_VIA_A_RNS = pp.create_line(net, from_bus=bus_VIA_A, to_bus = bus_RNS, std_type = 'PEX 3x1x240Al+35Cu', length_km=1.674)
    line_RNS_AAK = pp.create_line(net, from_bus=bus_AAK, to_bus = bus_RNS, std_type = 'OHL 3x1x130StAl+50Fe', length_km=10.995)
    line_BOD_AAK = pp.create_line(net, from_bus=bus_AAK, to_bus = bus_BOD, std_type = 'OHL 3x1x130StAl+50Fe', length_km=10.891)
    line_BOD_POU = pp.create_line(net, from_bus=bus_POU, to_bus = bus_BOD, std_type = 'PEX 3x1x150Al+25Cu', length_km=5.95)
    line_BOD_NEX = pp.create_line(net, from_bus=bus_NEX, to_bus = bus_BOD, std_type = 'PEX 3x1x95Al+25Cu', length_km=3.477)
    line_BOD_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_BOD, std_type = 'OHL 3x1x130StAl+50Fe', length_km=4.138)
    line_SVA_NEX = pp.create_line(net, from_bus=bus_NEX, to_bus = bus_SVA, std_type = 'PEX 3x1x150Al+25Cu', length_km=9.78)
    line_SVA_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_SVA, std_type = 'PEX 3x1x150Al+25Cu', length_km=7.531)
    line_OST_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_OST, std_type = 'OHL 3x1x130StAl+50Fe', length_km=9.924)
    line_OST_GUD = pp.create_line(net, from_bus=bus_GUD, to_bus = bus_OST, std_type = 'PEX 3x1x150Al+25Cu', length_km=6.6)
    line_OST_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_OST, std_type = 'OHL 3x1x130StAl+50Fe', length_km=13.05)
    line_ALL_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_ALL, std_type = 'PEX 3x1x150Al+25Cu', length_km=4.276)
    line_HAS_A_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_HAS_A, std_type = 'OHL 3x1x130StAl+50Fe', length_km=6.818)
    line_BOR_HAS_A = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_HAS_A, std_type = 'PEX 3x1x400CuPbAl', length_km=1.4)
    line_BOR_HAS_3 = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_HAS_A, std_type = 'PEX 3x1x240CuPbAl', length_km=43.5)


    ## External grid Sweden
    bus_BOR_HAS_split1 = pp.create_bus(net, vn_kv, name='BOR HAS split 1', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOR_HAS_split2 = pp.create_bus(net, vn_kv, name='BOR HAS split 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_borr = pp.create_bus(net, vn_kv, name='Borrby', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    line_BOR_HAS_2 = pp.create_line(net, from_bus=bus_BOR_HAS_split2, to_bus = bus_BOR_HAS_split1, std_type = 'PEX 3x1x400CuPbAl', length_km=0.7)
    line_BOR_HAS_1 = pp.create_line(net, from_bus=bus_BOR_HAS_split1, to_bus = bus_borr, std_type = 'IBIS 3x1x234', length_km=4.2)
    line_BOR_HAS_3 = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_BOR_HAS_split2, std_type = 'PEX 3x1x240CuPbAl', length_km=43.5)
    bus_tom = pp.create_bus(net, 135, name='Tomelilla', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_borr = pp.create_transformer(net, hv_bus = bus_tom, lv_bus = bus_borr, std_type = 'Trf 135-69 kV')
    # bus_N_punkt_Borr = pp.create_bus(net, vn_kv, name='N punkt Borrby', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    # sw_Borr = pp.create_switch(net, bus, element, et, closed=True, type=None, name=None, index=None, z_ohm=0)
    ext_grid = pp.create_ext_grid(net, bus_tom, vm_pu =0.91, va_degree = 0.0, slack_weight = 1.0)
    net.ext_grid.at[0, 'vm_pu'] = 0.91
    # gen = pp.create_gen(net, bus_VIA_A, p_mw = 0.0001)

    vn_kv = 10.5

    ## Gen Vaerket
    bus_VAE_blok_6 = pp.create_bus(net, vn_kv, name='Vaerket Blok 6', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_blok_6 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_blok_6, name ='Trf blok 6', std_type='Trf-6 45 MVA', in_service=False)
    VAE_gen_blok_6 = pp.create_gen(net, bus_VAE_blok_6, p_mw = 36, vm_pu=1.0, name='Blok 6 gen',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)

    bus_VAE_blok_5 = pp.create_bus(net, vn_kv, name='Vaerket Blok 5', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_blok_6 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_blok_5, name ='Trf blok 5', std_type='Trf-5 29 MVA', in_service=False)
    VAE_gen_blok_5 = pp.create_gen(net, bus_VAE_blok_6, p_mw =23.52, sn_mva=29, vm_pu=1.0, name='Blok 5 gen',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)

    bus_VAE_Diesler = pp.create_bus(net, vn_kv, name='Vaerket Diesler', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_1 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_Diesler, name ='Trf Vaerket 1', std_type='Trf-1 16/20 MVA', in_service=False)
    VAE_Diesel_1 = pp.create_gen(net, bus_VAE_Diesler, p_mw =4.66, sn_mva=5.825, vm_pu=1.0, name='Diesel 1',scaling=1.0, slack=False, cos_phi=0.8, in_service=False)
    VAE_Diesel_2 = pp.create_gen(net, bus_VAE_Diesler, p_mw =4.66, sn_mva=5.825, vm_pu=1.0, name='Diesel 2',scaling=1.0, slack=False, cos_phi=0.8, in_service=False)
    VAE_Diesel_3 = pp.create_gen(net, bus_VAE_Diesler, p_mw =5.068, sn_mva=6.335, vm_pu=1.0, name='Diesel 3',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)
    VAE_Diesel_4 = pp.create_gen(net, bus_VAE_Diesler, p_mw =5.068, sn_mva=6.335, vm_pu=1.0, name='Diesel 4',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)

    bus_VAER_N = pp.create_bus(net, vn_kv, name='Vaer N', type='b', in_service=False, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_1 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAER_N, name ='Trf Vaerket 1 - 1', std_type='Trf-1 16/20 MVA', in_service=False)
    




    ## 00 Dampvaerket

    ## 01 Snorrebakken


    bus_SNO_10 = pp.create_bus(net, vn_kv, name='Snorrebakken 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SNO_SMED = pp.create_bus(net, vn_kv, name='94 Smedegaard', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SNO_YPP = pp.create_bus(net, vn_kv, name='566 Ypperne', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SNO_YPP = pp.create_bus(net, vn_kv, name='566 Ypperne', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    line_SNO_10_SMED = pp.create_line(net, from_bus=bus_SNO_10, to_bus = bus_SNO_SMED, std_type = '3x95 PEX AL + 25 CU', length_km=5.751)
    line_YPP_SMED = pp.create_line(net, from_bus=bus_SNO_YPP, to_bus = bus_SNO_SMED, std_type = '3x50 PEX AL + 16 CU', length_km=1.21)

    trafo_SNO = pp.create_transformer(net, hv_bus = bus_SNO, lv_bus = bus_SNO_10, name='Snorrebakken Trf', std_type='Trf 10 MVA ek 8.5 er 0.62')

    # ## Create loads
    # load_VIA_A = pp.create_load(net, bus_VIA_A,p_mw=0.929, q_mvar=0.478)
    SNO_load = pp.create_load(net, bus_SNO_10,p_mw=0.883, q_mvar=0.129)

    ## Create generators
    SNO_husstandsmoller = pp.create_sgen(net, bus_SNO_10, p_mw=2, q_mvar = 0, slack=True)
    SNO_WTG566 = pp.create_sgen(net, bus_SNO_YPP, p_mw=0.26, q_mvar = 0)

    ## Hasle
    # aux_bus_HAS_A_B_1 = pp.create_bus(net, 63, name='Aux bus Hasle 1', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # aux_bus_HAS_A_B_2 = pp.create_bus(net, 63, name='Aux bus Hasle 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_trafo_HAS_1 = pp.create_bus(net, 63, name='Aux bus trafo HASLE', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_trafo_HAS_2 = pp.create_bus(net, 63, name='Aux bus trafo HASLE', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_1, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_1, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)
    switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)

    bus_HAS_10 = pp.create_bus(net, vn_kv, name='Hasle 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    
    trafo_HAS1 = pp.create_transformer(net, hv_bus = aux_bus_trafo_HAS_1, lv_bus = bus_HAS_10, name='Hasle Trf 1', std_type='Trf 10 MVA ek 8.87 er 0.54', in_service=False)
    trafo_HAS2 = pp.create_transformer(net, hv_bus = aux_bus_trafo_HAS_2, lv_bus = bus_HAS_10, name='Hasle Trf 2', std_type='Trf 10 MVA ek 8.87 er 0.54')

    bus_HAS_TOR = pp.create_bus(net, vn_kv, name='1042 Tornby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_HAS_VYS = pp.create_bus(net, vn_kv, name='1020 Vysteby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_HAS_HAS = pp.create_bus(net, vn_kv, name='851 Hasle VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    HAS_husstandsmoller = pp.create_sgen(net, bus_HAS_10, p_mw=2, q_mvar = 0, slack=True)
    HAS_load = pp.create_load(net, bus_HAS_10,p_mw=0.641, q_mvar=-0.437)


    HAS_WTG1042 = pp.create_sgen(net, bus_HAS_TOR, p_mw=6.9, q_mvar = 0)
    HAS_WTG1020 = pp.create_sgen(net, bus_HAS_VYS, p_mw=5.25, q_mvar = 0)
    HAS_WTG851 = pp.create_sgen(net, bus_HAS_HAS, p_mw=3.9, q_mvar = 0)

    line_HAS_10_TOR = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_TOR, std_type = '3x150 PEX AL+25 CU', length_km=2.944, parallel=2)
    line_HAS_10_VYS = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_VYS, std_type = '3x 240 PEX AL + 35 CU', length_km=5.293, parallel=1)
    line_HAS_10_HAS = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_HAS, std_type = '3x150 PEX AL+25 CU', length_km=3.9, parallel=1)
    
    ## OLSKER

    bus_OLS_10 = pp.create_bus(net, vn_kv, name='Olsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    trafo_OLS1 = pp.create_transformer(net, hv_bus = bus_OLS, lv_bus = bus_OLS_10, name='Olsker Trf 1', std_type='Trf 4 MVA ek 7.4 er 0.3')
    trafo_OLS2 = pp.create_transformer(net, hv_bus = bus_OLS, lv_bus = bus_OLS_10, name='Olsker Trf 2', std_type='Trf 4 MVA ek 7.4 er 0.3', in_service=False)

    OLS_husstandsmoller = pp.create_sgen(net, bus_OLS_10, p_mw=2, q_mvar = 0, slack=True)
    OLS_load = pp.create_load(net, bus_OLS_10,p_mw=0.615, q_mvar=-0.354)
      

    return net

## Net based on available measurements
def net_60kV_measurements(net, measurements):
    vn_kv = 63
    max_vm_pu = 1.05
    min_vm_pu = 0.95


    ## Create substations Net 60 kv
    bus_HAS_A = pp.create_bus(net, vn_kv, name='Hasle A', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_HAS_B = pp.create_bus(net, vn_kv, name='Hasle B', index=None, geodata=None, type='b', zone=None, in_service=False,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SNO = pp.create_bus(net, vn_kv, name='Snorrebakken', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OLS = pp.create_bus(net, vn_kv, name='Olsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_RNO = pp.create_bus(net, vn_kv, name='Ronne Nord', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOR_HAS = pp.create_bus(net, vn_kv, name='BOR-HAS split 3', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    bus_ALL = pp.create_bus(net, vn_kv, name='Allinge', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SVA = pp.create_bus(net, vn_kv, name='Svaneke', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_NEX = pp.create_bus(net, vn_kv, name='Nexo', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOD = pp.create_bus(net, vn_kv, name='Bodilsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_POU = pp.create_bus(net, vn_kv, name='Poulsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_AAK = pp.create_bus(net, vn_kv, name='Aakirkeby', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_DAL = pp.create_bus(net, vn_kv, name='Dalslunde', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OST = pp.create_bus(net, vn_kv, name='Osterlars', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OLS = pp.create_bus(net, vn_kv, name='Olsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_GUD = pp.create_bus(net, vn_kv, name='Gudhjem', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VIA_A = pp.create_bus(net, vn_kv, name='Viadukten A', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VIA_B = pp.create_bus(net, vn_kv, name='Viadukten B', index=None, geodata=None, type='b', zone=None, in_service=False,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_RNS = pp.create_bus(net, vn_kv, name='Ronne Syd', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VAE_A = pp.create_bus(net, vn_kv, name='Vaerket A', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VAE_B = pp.create_bus(net, vn_kv, name='Vaerket B', index=None, geodata=None, type='b', zone=None, in_service=False, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VES = pp.create_bus(net, vn_kv, name='Vesthavnen', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    aux_bus_VIA_1 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 1', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_2 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 2', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_3 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 3', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    ## Create lines 60 kV side
    line_HAS_A_SNO = pp.create_line(net, from_bus=bus_HAS_A, to_bus = bus_SNO, std_type = 'OHL 3x1x130StAl+50Fe', length_km=5.217 )
    line_SNO_VAE_A = pp.create_line(net, from_bus=bus_SNO, to_bus = bus_VAE_A, std_type = 'APBF 1x3x95 Cu', length_km=3.453)
    line_VAE_A_VES = pp.create_line(net, from_bus=bus_VES, to_bus = bus_VAE_A, std_type = 'PEX 3x1x300Al+35Cu', length_km=1.8)
    line_VAE_A_VIA_A = pp.create_line(net, from_bus=aux_bus_VIA_1, to_bus = bus_VAE_A, std_type = 'PEX 3x1x300Al+35Cu', length_km=1.481)
    line_VAE_A_RNS = pp.create_line(net, from_bus=bus_VAE_A, to_bus=bus_RNS, std_type = 'APBF 1x3x95 Cu', length_km=2.861)
    line_VES_RNO = pp.create_line(net, from_bus=bus_RNO, to_bus = bus_VES, std_type = 'PEX 3x1x300Al+35Cu', length_km=2.2)
    line_HAS_A_RNO = pp.create_line(net, from_bus=bus_HAS_A, to_bus = bus_RNO, std_type = 'PEX 3x1x240Al+35Cu', length_km=7.434)
    line_VIA_A_RNO = pp.create_line(net, from_bus=aux_bus_VIA_2, to_bus = bus_RNO, std_type = 'PEX 3x1x240Al+35Cu', length_km=1.834)
    line_VIA_A_RNS = pp.create_line(net, from_bus=aux_bus_VIA_3, to_bus = bus_RNS, std_type = 'PEX 3x1x240Al+35Cu', length_km=1.674)
    line_RNS_AAK = pp.create_line(net, from_bus=bus_AAK, to_bus = bus_RNS, std_type = 'OHL 3x1x130StAl+50Fe', length_km=10.995)
    line_BOD_AAK = pp.create_line(net, from_bus=bus_AAK, to_bus = bus_BOD, std_type = 'OHL 3x1x130StAl+50Fe', length_km=10.891)
    line_BOD_POU = pp.create_line(net, from_bus=bus_POU, to_bus = bus_BOD, std_type = 'PEX 3x1x150Al+25Cu', length_km=5.95)
    line_BOD_NEX = pp.create_line(net, from_bus=bus_NEX, to_bus = bus_BOD, std_type = 'PEX 3x1x95Al+25Cu', length_km=3.477)
    line_BOD_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_BOD, std_type = 'OHL 3x1x130StAl+50Fe', length_km=4.138)
    line_SVA_NEX = pp.create_line(net, from_bus=bus_NEX, to_bus = bus_SVA, std_type = 'PEX 3x1x150Al+25Cu', length_km=9.78)
    line_SVA_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_SVA, std_type = 'PEX 3x1x150Al+25Cu', length_km=7.531)
    line_OST_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_OST, std_type = 'OHL 3x1x130StAl+50Fe', length_km=9.924)
    line_OST_GUD = pp.create_line(net, from_bus=bus_GUD, to_bus = bus_OST, std_type = 'PEX 3x1x150Al+25Cu', length_km=6.6)
    line_OST_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_OST, std_type = 'OHL 3x1x130StAl+50Fe', length_km=13.05)
    line_ALL_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_ALL, std_type = 'PEX 3x1x150Al+25Cu', length_km=4.276)
    line_HAS_A_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_HAS_A, std_type = 'OHL 3x1x130StAl+50Fe', length_km=6.818)
    line_BOR_HAS_A = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_HAS_A, std_type = 'PEX 3x1x400CuPbAl', length_km=1.4)
    #line_BOR_HAS_3 = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_HAS_A, std_type = 'PEX 3x1x240CuPbAl', length_km=43.5)

    ## Switches

    # switch_VIA_A_1 = pp.create_switch(net, bus_VIA_A, line_VIA_A_RNO, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_A_2 = pp.create_switch(net, bus_VIA_A, line_VAE_A_VIA_A, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_A_3 = pp.create_switch(net, bus_VIA_A, line_VIA_A_RNS, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNO, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, line_VAE_A_VIA_A, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNS, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)

    switch_VIA_A_1 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_1, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_A_2 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_2, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_A_3 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_3, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)

    switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_1, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_2, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_3, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)


    # switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNO, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, line_VAE_A_VIA_A, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNS, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    ## TODO include switches VAE A and B


    ## External grid Sweden
    bus_BOR_HAS_split1 = pp.create_bus(net, vn_kv, name='BOR HAS split 1', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOR_HAS_split2 = pp.create_bus(net, vn_kv, name='BOR HAS split 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_borr = pp.create_bus(net, vn_kv, name='Borrby', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    line_BOR_HAS_2 = pp.create_line(net, from_bus=bus_BOR_HAS_split2, to_bus = bus_BOR_HAS_split1, std_type = 'PEX 3x1x400CuPbAl', length_km=0.7)
    line_BOR_HAS_1 = pp.create_line(net, from_bus=bus_BOR_HAS_split1, to_bus = bus_borr, std_type = 'IBIS 3x1x234', length_km=4.2)
    line_BOR_HAS_3 = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_BOR_HAS_split2, std_type = 'PEX 3x1x240CuPbAl', length_km=43.5)
    bus_tom = pp.create_bus(net, 135, name='Tomelilla', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_borr = pp.create_transformer(net, hv_bus = bus_tom, lv_bus = bus_borr, name = 'Borrby',std_type = 'Trf 135-69 kV')
    # bus_N_punkt_Borr = pp.create_bus(net, vn_kv, name='N punkt Borrby', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    # sw_Borr = pp.create_switch(net, bus, element, et, closed=True, type=None, name=None, index=None, z_ohm=0)
    ext_grid = pp.create_ext_grid(net, bus_tom, vm_pu =0.91, va_degree = 0.0, slack_weight = 1.0)
    net.ext_grid.at[0, 'vm_pu'] = 0.91
    # gen = pp.create_gen(net, bus_VIA_A, p_mw = 0.0001)

    vn_kv = 10.5

    ## Gen Vaerket
    bus_VAE_blok_6 = pp.create_bus(net, vn_kv, name='Vaerket Blok 6', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_blok_6 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_blok_6, name ='Trf blok 6', std_type='Trf-6 45 MVA', in_service=False)
    VAE_gen_blok_6 = pp.create_gen(net, bus_VAE_blok_6, p_mw = 36, vm_pu=1.0, name='Blok 6 gen',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)

    bus_VAE_blok_5 = pp.create_bus(net, vn_kv, name='Vaerket Blok 5', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_blok_6 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_blok_5, name ='Trf blok 5', std_type='Trf-5 29 MVA', in_service=False)
    VAE_gen_blok_5 = pp.create_gen(net, bus_VAE_blok_6, p_mw =23.52, sn_mva=29, vm_pu=1.0, name='Blok 5 gen',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)

    bus_VAE_Diesler = pp.create_bus(net, vn_kv, name='Vaerket Diesler', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_1 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_Diesler, name ='Trf Vaerket 1', std_type='Trf-1 16/20 MVA', in_service=False)
    VAE_Diesel_1 = pp.create_gen(net, bus_VAE_Diesler, p_mw =4.66, sn_mva=5.825, vm_pu=1.0, name='Diesel 1',scaling=1.0, slack=False, cos_phi=0.8, in_service=False)
    VAE_Diesel_2 = pp.create_gen(net, bus_VAE_Diesler, p_mw =4.66, sn_mva=5.825, vm_pu=1.0, name='Diesel 2',scaling=1.0, slack=False, cos_phi=0.8, in_service=False)
    VAE_Diesel_3 = pp.create_gen(net, bus_VAE_Diesler, p_mw =5.068, sn_mva=6.335, vm_pu=1.0, name='Diesel 3',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)
    VAE_Diesel_4 = pp.create_gen(net, bus_VAE_Diesler, p_mw =5.068, sn_mva=6.335, vm_pu=1.0, name='Diesel 4',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)

    bus_VAER_N = pp.create_bus(net, vn_kv, name='Vaer N', type='b', in_service=False, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_1 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAER_N, name ='Trf Vaerket 1 - 1', std_type='Trf-1 16/20 MVA', in_service=False)
    




    ## 00 Dampvaerket

    bus_DMP_A = pp.create_bus(net, vn_kv, name='Dampværk A', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_DMP_B = pp.create_bus(net, vn_kv, name='Dampværk B', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_DMP = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # aux_bus_trafo_DMP_2 = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_DMP1 = pp.create_switch(net, aux_bus_DMP, bus_DMP_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_DMP2 = pp.create_switch(net, aux_bus_DMP, bus_DMP_B, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    trafo_DMP = pp.create_transformer(net, hv_bus = bus_VAE_A, lv_bus = aux_bus_DMP, name='Værket Trf 2', std_type='Trf-2 25/31.5 MVA', in_service=True)

    aux_bus_DMP_2 = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_DMP3 = pp.create_switch(net, aux_bus_DMP_2, bus_DMP_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_DMP4 = pp.create_switch(net, aux_bus_DMP_2, bus_DMP_B, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)

    DMP_shunt = pp.create_shunt(net, bus_DMP_A, q_mvar=0.8, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)
    DMP_shunt_var = pp.create_shunt(net, bus_DMP_A, q_mvar=3.2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    # DMP_load = pp.create_load(net, aux_bus_DMP_2, p_mw=1.37, q_mvar = 0.26)
    
    target_substation = "Værket"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    DMP_consumed = pp.create_load(net, aux_bus_DMP_2,p_mw=consumption, q_mvar=0)
    DMP_generated = pp.create_gen(net, aux_bus_DMP_2, p_mw =-1*production, q_mvar=0)

    # switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)


    ## 01 Snorrebakken


    bus_SNO_10 = pp.create_bus(net, vn_kv, name='Snorrebakken 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_SNO_SMED = pp.create_bus(net, vn_kv, name='94 Smedegaard', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_SNO_YPP = pp.create_bus(net, vn_kv, name='566 Ypperne', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_SNO_YPP = pp.create_bus(net, vn_kv, name='566 Ypperne', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # line_SNO_10_SMED = pp.create_line(net, from_bus=bus_SNO_10, to_bus = bus_SNO_SMED, std_type = '3x95 PEX AL + 25 CU', length_km=5.751)
    # line_YPP_SMED = pp.create_line(net, from_bus=bus_SNO_YPP, to_bus = bus_SNO_SMED, std_type = '3x50 PEX AL + 16 CU', length_km=1.21)

    trafo_SNO = pp.create_transformer(net, hv_bus = bus_SNO, lv_bus = bus_SNO_10, name='Snorrebakken Trf', std_type='Trf 10 MVA ek 8.5 er 0.62')

    # ## Create loads
    # load_VIA_A = pp.create_load(net, bus_VIA_A,p_mw=0.929, q_mvar=0.478)
    # SNO_load = pp.create_load(net, bus_SNO_10,p_mw=0.883, q_mvar=0.129)

    ## Create generators
    target_substation = "Snorrebakken"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    SNO_consumed = pp.create_load(net, bus_SNO_10,p_mw=consumption, q_mvar=0)
    SNO_generated = pp.create_gen(net, bus_SNO_10, p_mw =-1*production, q_mvar=0)


    ## Hasle
    # aux_bus_HAS_A_B_1 = pp.create_bus(net, 63, name='Aux bus Hasle 1', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # aux_bus_HAS_A_B_2 = pp.create_bus(net, 63, name='Aux bus Hasle 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_trafo_HAS_1 = pp.create_bus(net, 63, name='Aux bus trafo HASLE', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_trafo_HAS_2 = pp.create_bus(net, 63, name='Aux bus trafo HASLE', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_1, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_1, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)
    switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)

    bus_HAS_10 = pp.create_bus(net, vn_kv, name='Hasle 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    
    trafo_HAS1 = pp.create_transformer(net, hv_bus = aux_bus_trafo_HAS_1, lv_bus = bus_HAS_10, name='Hasle Trf 1', std_type='Trf 10 MVA ek 8.87 er 0.54', in_service=False)
    trafo_HAS2 = pp.create_transformer(net, hv_bus = aux_bus_trafo_HAS_2, lv_bus = bus_HAS_10, name='Hasle Trf 2', std_type='Trf 10 MVA ek 8.87 er 0.54')

    # bus_HAS_TOR = pp.create_bus(net, vn_kv, name='1042 Tornby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_HAS_VYS = pp.create_bus(net, vn_kv, name='1020 Vysteby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_HAS_HAS = pp.create_bus(net, vn_kv, name='851 Hasle VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    # HAS_husstandsmoller = pp.create_sgen(net, bus_HAS_10, p_mw=2, q_mvar = 0, slack=True)
    # HAS_load = pp.create_load(net, bus_HAS_10,p_mw=0.641, q_mvar=-0.437)


    # HAS_WTG1042 = pp.create_sgen(net, bus_HAS_TOR, p_mw=6.9, q_mvar = 0)
    # HAS_WTG1020 = pp.create_sgen(net, bus_HAS_VYS, p_mw=5.25, q_mvar = 0)
    # HAS_WTG851 = pp.create_sgen(net, bus_HAS_HAS, p_mw=3.9, q_mvar = 0)

    # line_HAS_10_TOR = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_TOR, std_type = '3x150 PEX AL+25 CU', length_km=2.944, parallel=2)
    # line_HAS_10_VYS = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_VYS, std_type = '3x 240 PEX AL + 35 CU', length_km=5.293, parallel=1)
    # line_HAS_10_HAS = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_HAS, std_type = '3x150 PEX AL+25 CU', length_km=3.9, parallel=1)

    target_substation = "Hasle"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    HAS_husstandsmoller = pp.create_sgen(net, bus_HAS_10, p_mw=-1*production, q_mvar = 0, slack=True)
    HAS_load = pp.create_load(net, bus_HAS_10,p_mw=consumption)

    
    ## OLSKER
    target_substation = "Olsker"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    bus_OLS_10 = pp.create_bus(net, vn_kv, name='Olsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    trafo_OLS1 = pp.create_transformer(net, hv_bus = bus_OLS, lv_bus = bus_OLS_10, name='Olsker Trf 1', std_type='Trf 4 MVA ek 7.4 er 0.3')
    trafo_OLS2 = pp.create_transformer(net, hv_bus = bus_OLS, lv_bus = bus_OLS_10, name='Olsker Trf 2', std_type='Trf 4 MVA ek 7.4 er 0.3', in_service=False)

    OLS_husstandsmoller = pp.create_sgen(net, bus_OLS_10, p_mw=-1*production, q_mvar = 0, slack=True)
    OLS_load = pp.create_load(net, bus_OLS_10,p_mw=consumption, q_mvar=0)

    ## Østerlars
    bus_OST_10 = pp.create_bus(net, vn_kv, name='Østerlars 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_OST = pp.create_transformer(net, hv_bus = bus_OST, lv_bus = bus_OST_10, name='Østerlars Trf 1', std_type='Trf 16 MVA ek 8.8 er 0.3')
    # OST_husstandsmoller = pp.create_sgen(net, bus_OST_10, p_mw=2, q_mvar = 0, slack=True)
    # OST_load = pp.create_load(net, bus_OST_10,p_mw=0.922, q_mvar=-0.109)

    target_substation = "Østerlars"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    OST_husstandsmoller = pp.create_sgen(net, bus_OST_10, p_mw=-1*production, q_mvar = 0, slack=True)
    OST_load = pp.create_load(net, bus_OST_10,p_mw=consumption, q_mvar=0)

    ## Åkirkeby
    bus_AAK_10 = pp.create_bus(net, vn_kv, name='Åkirkeby 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # trafo_AAK22 = pp.create_transformer(net, hv_bus = bus_AAK, lv_bus = bus_AAK_10, name='Aakirkeby Trf 21', std_type='Trf 16 MVA ek 8.8 er 0.', in_service=False)
    trafo_AAK21 = pp.create_transformer(net, hv_bus = bus_AAK, lv_bus = bus_AAK_10, name='Aakirkeby Trf 22', std_type='Trf 25/31.5 MVA ek 10%', in_service=True)
    # AAK_husstandsmoller = pp.create_sgen(net, bus_AAK_10, p_mw=2, q_mvar = 0, slack=True)
    # AAK_load = pp.create_load(net, bus_AAK_10,p_mw=1.587, q_mvar=-0.578)

    # bus_AAK_BOD = pp.create_bus(net, vn_kv, name='Bodelyngsvejen 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # line_AAK_10_BOD = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_BOD, std_type = '3x150 PEX AL+25 CU', length_km=1.25, parallel=2)
    # # AAK_PV = pp.create_sgen(net, bus_AAK_BOD, p_mw=7.5, q_mvar = 0, slack=True)

    # bus_AAK_KAL = pp.create_bus(net, vn_kv, name='Kalby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    # line_AAK_10_BOD = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_KAL, std_type = '3x150 PEX AL+25 CU', length_km=0.516, parallel=2)
    # # AAK_WTG965 = pp.create_sgen(net, bus_AAK_KAL, p_mw=6, q_mvar = 0, slack=True)

    # bus_AAK_SOS = pp.create_bus(net, vn_kv, name='Sose VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    # line_AAK_10_SOS = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_SOS, std_type = '3x150 PEX AL+25 CU', length_km=3.24, parallel=2)
    # # AAK_WTG1004 = pp.create_sgen(net, bus_AAK_KAL, p_mw=6.5, q_mvar = 0, slack=True)

    # bus_AAK_BIO = pp.create_bus(net, vn_kv, name='Biogas', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    # line_AAK_10_BIO = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_BIO, std_type = '3x95 PEX AL + 25 CU', length_km=2.314, parallel=1)
    # AAK_BIO1 = pp.create_gen(net, bus_AAK_BIO, p_mw = 1.521,sn_mva=1.981, vm_pu=1.0, name='Biogas gen 1',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)
    # AAK_BIO2 = pp.create_gen(net, bus_AAK_BIO, p_mw = 1.521,sn_mva=1.981, vm_pu=1.0, name='Biogas gen 1',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)

    target_substation = "Åkirkeby"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    AAK_husstandsmoller = pp.create_sgen(net, bus_AAK_10, p_mw=-1*production, q_mvar = 0, slack=True)
    AAK_load = pp.create_load(net, bus_AAK_10,p_mw=consumption, q_mvar=0)

    ## Nexø
    bus_NEX_10 = pp.create_bus(net, vn_kv, name='Nexø 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_NEX1 = pp.create_transformer(net, hv_bus = bus_NEX, lv_bus = bus_NEX_10, name='Nexø Trf 1', std_type='SEA 63/11 10 MVA NEXØ', in_service=True)
    trafo_NEX2 = pp.create_transformer(net, hv_bus = bus_NEX, lv_bus = bus_NEX_10, name='Nexø Trf 2', std_type='Trf 10 MVA ek 8.4 er 0.61', in_service=False)

    target_substation = "Nexø"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]
    NEX_husstandsmoller = pp.create_sgen(net, bus_NEX_10, p_mw=-1*production, q_mvar = 0, slack=True)
    NEX_load = pp.create_load(net, bus_NEX_10,p_mw=consumption, q_mvar=0)

    ## Bodilsker
    bus_BOD_10 = pp.create_bus(net, vn_kv, name='Bodilsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_BOD = pp.create_transformer(net, hv_bus = bus_BOD, lv_bus = bus_BOD_10, name='Bodilsker Trf 1', std_type='Trf 10/12 MVA ek 8.87 er 0.54', in_service=True)
    # BOD_husstandsmoller = pp.create_sgen(net, bus_BOD_10, p_mw=2, q_mvar = 0, slack=True)
    # BOD_load = pp.create_load(net, bus_BOD_10,p_mw=0.618, q_mvar=-0.026)

    target_substation = "Bodilsker"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    BOD_husstandsmoller = pp.create_sgen(net, bus_BOD_10, p_mw=-1*production, q_mvar = 0, slack=True)
    BOD_load = pp.create_load(net, bus_BOD_10,p_mw=consumption, q_mvar=0)


    BOD_shunt = pp.create_shunt(net, bus_BOD_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)
    # bus_BOD_GAD = pp.create_bus(net, vn_kv, name='Gadeby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # line_BOD_GAD = pp.create_line(net, from_bus=bus_BOD_10, to_bus = bus_BOD_GAD, std_type = '3x95 PEX AL + 25 CU', length_km=2.48, parallel=1)
    # BOD_WTG1001 = pp.create_sgen(net, bus_BOD_GAD, p_mw=2.7, q_mvar = 0, slack=True)

    ## Rønne Syd
    bus_RNS_10 = pp.create_bus(net, vn_kv, name='Rønne Syd 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_RNS1 = pp.create_transformer(net, hv_bus = bus_RNS, lv_bus = bus_RNS_10, name='Rønne Syd Trf 1', std_type='Trf 10 MVA ek 8.3 er 0.62', in_service=True)
    # RNS_husstandsmoller = pp.create_sgen(net, bus_RNS_10, p_mw=2, q_mvar = 0, slack=True)
    # RNS_load = pp.create_load(net, bus_RNS_10,p_mw=1.128, q_mvar=-0.124)
    RNS_shunt = pp.create_shunt(net, bus_RNS_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    target_substation = "Rønne Syd"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    RNS_husstandsmoller = pp.create_sgen(net, bus_RNS_10, p_mw=-1*production, q_mvar = 0, slack=True)
    RNS_load = pp.create_load(net, bus_RNS_10,p_mw=consumption, q_mvar=0)


    ## Allinge
    bus_ALL_10 = pp.create_bus(net, vn_kv, name='Allinge 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_ALL1 = pp.create_transformer(net, hv_bus = bus_ALL, lv_bus = bus_ALL_10, name='Allinge Trf 1', std_type='Trf 10 MVA ek 8.4 er 0.61', in_service=True)
    trafo_ALL2 = pp.create_transformer(net, hv_bus = bus_ALL, lv_bus = bus_ALL_10, name='Allinge Trf 2', std_type='Trf 10 MVA ek 8.04 er 0.53', in_service=False)
    # ALL_husstandsmoller = pp.create_sgen(net, bus_ALL_10, p_mw=2, q_mvar = 0, slack=True)


    # ALL_load = pp.create_load(net, bus_ALL_10,p_mw=0.78, q_mvar=-0.266)
    target_substation = "Allinge"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    ALL_husstandsmoller = pp.create_sgen(net, bus_ALL_10, p_mw=-1*production, q_mvar = 0, slack=True)
    ALL_load = pp.create_load(net, bus_ALL_10,p_mw=consumption, q_mvar=0)

    ## Svaneke
    bus_SVAN_10 = pp.create_bus(net, vn_kv, name='Svaneke 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_SVAN1 = pp.create_transformer(net, hv_bus = bus_SVA, lv_bus = bus_SVAN_10, name='Svaneke Trf 1', std_type='Trf 10 MVA ek 8.3 er 0.54', in_service=True)
    # SVAN_husstandsmoller = pp.create_sgen(net, bus_SVAN_10, p_mw=2, q_mvar = 0, slack=True)
    # SVAN_load = pp.create_load(net, bus_SVAN_10,p_mw=0.923, q_mvar=0.043)
    SVAN_shunt = pp.create_shunt(net, bus_RNS_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    target_substation = "Svaneke"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]
    SVAN_husstandsmoller = pp.create_sgen(net, bus_SVAN_10, p_mw=-1*production, q_mvar = 0, slack=True)
    SVAN_load = pp.create_load(net, bus_SVAN_10,p_mw=consumption, q_mvar=0)

    ## Viadukten
    bus_VIA_10 = pp.create_bus(net, vn_kv, name='Viadukten 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_4 = pp.create_bus(net, 63, name='Auxiliary bus Viadukten 4', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_VIA_A_4 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_4, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_4 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_4, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)
    trafo_VIA1 = pp.create_transformer(net, hv_bus = aux_bus_VIA_4, lv_bus = bus_VIA_10, name='Viadukten Trf 1', std_type='Trf 10 MVA ek 7.9 er 0.54', in_service=True)
    # VIA_husstandsmoller = pp.create_sgen(net, bus_VIA_10, p_mw=2, q_mvar = 0, slack=True)
    # VIA_load = pp.create_load(net, bus_VIA_10,p_mw=0.929, q_mvar=0.478)

    target_substation = "Viadukten"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    VIA_husstandsmoller = pp.create_sgen(net, bus_VIA_10, p_mw=-1*production, q_mvar = 0, slack=True)
    VIA_load = pp.create_load(net, bus_VIA_10,p_mw=consumption, q_mvar=0)

    ## Rønne Nord
    bus_RNO_10 = pp.create_bus(net, vn_kv, name='Rønne Nord 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_RNO = pp.create_transformer(net, hv_bus = bus_RNO, lv_bus = bus_RNO_10, name='Rønne Nord Trf 1', std_type='Trf 10 MVA ek 7.94 er 0.58', in_service=True)
    # RNO_husstandsmoller = pp.create_sgen(net, bus_RNO_10, p_mw=2, q_mvar = 0, slack=True)
    # RNO_load = pp.create_load(net, bus_RNO_10,p_mw=0.866, q_mvar=0.58)

    target_substation = "Rønne Nord"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    RNO_husstandsmoller = pp.create_sgen(net, bus_RNO_10, p_mw=-1*production, q_mvar = 0, slack=True)
    RNO_load = pp.create_load(net, bus_RNO_10,p_mw=consumption, q_mvar=0)

    ## Poulsker
    bus_POU_10 = pp.create_bus(net, vn_kv, name='Poulsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_POU = pp.create_transformer(net, hv_bus = bus_POU, lv_bus = bus_POU_10, name='Poulsker Trf 1', std_type='Trf 10 MVA ek 8.14 er 0.59', in_service=True)
    # POU_husstandsmoller = pp.create_sgen(net, bus_POU_10, p_mw=2, q_mvar = 0, slack=True)
    # POU_load = pp.create_load(net, bus_POU_10,p_mw=0.405, q_mvar=-0.546)

    target_substation = "Povlsker"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    POU_husstandsmoller = pp.create_sgen(net, bus_POU_10, p_mw=-1*production, q_mvar = 0, slack=True)
    POU_load = pp.create_load(net, bus_POU_10,p_mw=consumption, q_mvar=0)

    ## Vesthavnen
    bus_VES_10 = pp.create_bus(net, vn_kv, name='Vesthavnen 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VES = pp.create_transformer(net, hv_bus = bus_VES, lv_bus = bus_VES_10, name='Vesthavnen Trf 1', std_type='Trf 10 MVA ek 8.1 er 0.54', in_service=True)

    target_substation = "Vesthavnen"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    VES_husstandsmoller = pp.create_sgen(net, bus_VES_10, p_mw=-1*production, q_mvar = 0, slack=True)
    VES_load = pp.create_load(net, bus_VES_10,p_mw=consumption, q_mvar=0)

    ## Gudhjem
    bus_GUD_10 = pp.create_bus(net, vn_kv, name='Gudhjem 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_GUD = pp.create_transformer(net, hv_bus = bus_GUD, lv_bus = bus_GUD_10, name='Gudhjem Trf 1', std_type='Trf 4 MVA ek 7.3 er 0.3 N.2', in_service=True)
    # GUD_husstandsmoller = pp.create_sgen(net, bus_GUD_10, p_mw=2, q_mvar = 0, slack=True)
    # GUD_load = pp.create_load(net, bus_GUD_10,p_mw=0.608, q_mvar=-0.143)
    target_substation = "Gudhjem"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]



    GUD_husstandsmoller = pp.create_sgen(net, bus_GUD_10, p_mw=-1*production, q_mvar = 0, slack=True)
    GUD_load = pp.create_load(net, bus_GUD_10,p_mw=consumption, q_mvar=0)


    return net


## Net based on available measurements
def net_60kV_opf(net, measurements):
    vn_kv = 63
    max_vm_pu = 1.05
    min_vm_pu = 0.95


    ## Create substations Net 60 kv
    bus_HAS_A = pp.create_bus(net, vn_kv, name='Hasle A', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_HAS_B = pp.create_bus(net, vn_kv, name='Hasle B', index=None, geodata=None, type='b', zone=None, in_service=False,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SNO = pp.create_bus(net, vn_kv, name='Snorrebakken', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OLS = pp.create_bus(net, vn_kv, name='Olsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_RNO = pp.create_bus(net, vn_kv, name='Ronne Nord', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOR_HAS = pp.create_bus(net, vn_kv, name='BOR-HAS split 3', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    bus_ALL = pp.create_bus(net, vn_kv, name='Allinge', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SVA = pp.create_bus(net, vn_kv, name='Svaneke', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_NEX = pp.create_bus(net, vn_kv, name='Nexo', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOD = pp.create_bus(net, vn_kv, name='Bodilsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_POU = pp.create_bus(net, vn_kv, name='Poulsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_AAK = pp.create_bus(net, vn_kv, name='Aakirkeby', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_DAL = pp.create_bus(net, vn_kv, name='Dalslunde', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OST = pp.create_bus(net, vn_kv, name='Osterlars', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OLS = pp.create_bus(net, vn_kv, name='Olsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_GUD = pp.create_bus(net, vn_kv, name='Gudhjem', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VIA_A = pp.create_bus(net, vn_kv, name='Viadukten A', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VIA_B = pp.create_bus(net, vn_kv, name='Viadukten B', index=None, geodata=None, type='b', zone=None, in_service=False,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_RNS = pp.create_bus(net, vn_kv, name='Ronne Syd', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VAE_A = pp.create_bus(net, vn_kv, name='Vaerket A', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VAE_B = pp.create_bus(net, vn_kv, name='Vaerket B', index=None, geodata=None, type='b', zone=None, in_service=False, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VES = pp.create_bus(net, vn_kv, name='Vesthavnen', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    aux_bus_VIA_1 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 1', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_2 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 2', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_3 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 3', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    ## Create lines 60 kV side
    line_HAS_A_SNO = pp.create_line(net, from_bus=bus_HAS_A, to_bus = bus_SNO, std_type = 'OHL 3x1x130StAl+50Fe', length_km=5.217 )
    line_SNO_VAE_A = pp.create_line(net, from_bus=bus_SNO, to_bus = bus_VAE_A, std_type = 'APBF 1x3x95 Cu', length_km=3.453)
    line_VAE_A_VES = pp.create_line(net, from_bus=bus_VES, to_bus = bus_VAE_A, std_type = 'PEX 3x1x300Al+35Cu', length_km=1.8)
    line_VAE_A_VIA_A = pp.create_line(net, from_bus=aux_bus_VIA_1, to_bus = bus_VAE_A, std_type = 'PEX 3x1x300Al+35Cu', length_km=1.481)
    line_VAE_A_RNS = pp.create_line(net, from_bus=bus_VAE_A, to_bus=bus_RNS, std_type = 'APBF 1x3x95 Cu', length_km=2.861)
    line_VES_RNO = pp.create_line(net, from_bus=bus_RNO, to_bus = bus_VES, std_type = 'PEX 3x1x300Al+35Cu', length_km=2.2)
    line_HAS_A_RNO = pp.create_line(net, from_bus=bus_HAS_A, to_bus = bus_RNO, std_type = 'PEX 3x1x240Al+35Cu', length_km=7.434)
    line_VIA_A_RNO = pp.create_line(net, from_bus=aux_bus_VIA_2, to_bus = bus_RNO, std_type = 'PEX 3x1x240Al+35Cu', length_km=1.834)
    line_VIA_A_RNS = pp.create_line(net, from_bus=aux_bus_VIA_3, to_bus = bus_RNS, std_type = 'PEX 3x1x240Al+35Cu', length_km=1.674)
    line_RNS_AAK = pp.create_line(net, from_bus=bus_AAK, to_bus = bus_RNS, std_type = 'OHL 3x1x130StAl+50Fe', length_km=10.995)
    line_BOD_AAK = pp.create_line(net, from_bus=bus_AAK, to_bus = bus_BOD, std_type = 'OHL 3x1x130StAl+50Fe', length_km=10.891)
    line_BOD_POU = pp.create_line(net, from_bus=bus_POU, to_bus = bus_BOD, std_type = 'PEX 3x1x150Al+25Cu', length_km=5.95)
    line_BOD_NEX = pp.create_line(net, from_bus=bus_NEX, to_bus = bus_BOD, std_type = 'PEX 3x1x95Al+25Cu', length_km=3.477)
    line_BOD_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_BOD, std_type = 'OHL 3x1x130StAl+50Fe', length_km=4.138)
    line_SVA_NEX = pp.create_line(net, from_bus=bus_NEX, to_bus = bus_SVA, std_type = 'PEX 3x1x150Al+25Cu', length_km=9.78)
    line_SVA_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_SVA, std_type = 'PEX 3x1x150Al+25Cu', length_km=7.531)
    line_OST_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_OST, std_type = 'OHL 3x1x130StAl+50Fe', length_km=9.924)
    line_OST_GUD = pp.create_line(net, from_bus=bus_GUD, to_bus = bus_OST, std_type = 'PEX 3x1x150Al+25Cu', length_km=6.6)
    line_OST_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_OST, std_type = 'OHL 3x1x130StAl+50Fe', length_km=13.05)
    line_ALL_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_ALL, std_type = 'PEX 3x1x150Al+25Cu', length_km=4.276)
    line_HAS_A_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_HAS_A, std_type = 'OHL 3x1x130StAl+50Fe', length_km=6.818)
    line_BOR_HAS_A = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_HAS_A, std_type = 'PEX 3x1x400CuPbAl', length_km=1.4)
    line_BOR_HAS_3 = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_HAS_A, std_type = 'PEX 3x1x240CuPbAl', length_km=43.5)

    ## Switches

    # switch_VIA_A_1 = pp.create_switch(net, bus_VIA_A, line_VIA_A_RNO, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_A_2 = pp.create_switch(net, bus_VIA_A, line_VAE_A_VIA_A, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_A_3 = pp.create_switch(net, bus_VIA_A, line_VIA_A_RNS, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNO, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, line_VAE_A_VIA_A, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNS, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)

    switch_VIA_A_1 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_1, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_A_2 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_2, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_A_3 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_3, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)

    switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_1, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_2, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_3, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)


    # switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNO, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, line_VAE_A_VIA_A, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNS, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    ## TODO include switches VAE A and B


    ## External grid Sweden
    bus_BOR_HAS_split1 = pp.create_bus(net, vn_kv, name='BOR HAS split 1', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOR_HAS_split2 = pp.create_bus(net, vn_kv, name='BOR HAS split 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_borr = pp.create_bus(net, vn_kv, name='Borrby', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    line_BOR_HAS_2 = pp.create_line(net, from_bus=bus_BOR_HAS_split2, to_bus = bus_BOR_HAS_split1, std_type = 'PEX 3x1x400CuPbAl', length_km=0.7)
    line_BOR_HAS_1 = pp.create_line(net, from_bus=bus_BOR_HAS_split1, to_bus = bus_borr, std_type = 'IBIS 3x1x234', length_km=4.2)
    line_BOR_HAS_3 = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_BOR_HAS_split2, std_type = 'PEX 3x1x240CuPbAl', length_km=43.5)
    bus_tom = pp.create_bus(net, 135, name='Tomelilla', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_borr = pp.create_transformer(net, hv_bus = bus_tom, lv_bus = bus_borr, name = 'Borrby',std_type = 'Trf 135-69 kV')
    # bus_N_punkt_Borr = pp.create_bus(net, vn_kv, name='N punkt Borrby', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    # sw_Borr = pp.create_switch(net, bus, element, et, closed=True, type=None, name=None, index=None, z_ohm=0)
    ext_grid = pp.create_ext_grid(net, bus_tom, vm_pu =0.91, va_degree = 0.0, slack_weight = 1.0)
    net.ext_grid.at[0, 'vm_pu'] = 0.91
    # gen = pp.create_gen(net, bus_VIA_A, p_mw = 0.0001)

    vn_kv = 10.5

    ## Gen Vaerket
    bus_VAE_blok_6 = pp.create_bus(net, vn_kv, name='Vaerket Blok 6', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_blok_6 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_blok_6, name ='Trf blok 6', std_type='Trf-6 45 MVA', in_service=False)
    VAE_gen_blok_6 = pp.create_gen(net, bus_VAE_blok_6, p_mw = 36, vm_pu=1.0, name='Blok 6 gen',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)

    bus_VAE_blok_5 = pp.create_bus(net, vn_kv, name='Vaerket Blok 5', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_blok_6 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_blok_5, name ='Trf blok 5', std_type='Trf-5 29 MVA', in_service=False)
    VAE_gen_blok_5 = pp.create_gen(net, bus_VAE_blok_6, p_mw =23.52, sn_mva=29, vm_pu=1.0,name='Blok 5 gen',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)

    bus_VAE_Diesler = pp.create_bus(net, vn_kv, name='Vaerket Diesler', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_1 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_Diesler, name ='Trf Vaerket 1', std_type='Trf-1 16/20 MVA', in_service=False)
    VAE_Diesel_1 = pp.create_gen(net, bus_VAE_Diesler, p_mw =4.66, sn_mva=5.825, vm_pu=1.0, name='Diesel 1',scaling=1.0, slack=False, cos_phi=0.8, in_service=False)
    VAE_Diesel_2 = pp.create_gen(net, bus_VAE_Diesler, p_mw =4.66, sn_mva=5.825, vm_pu=1.0, name='Diesel 2',scaling=1.0, slack=False, cos_phi=0.8, in_service=False)
    VAE_Diesel_3 = pp.create_gen(net, bus_VAE_Diesler, p_mw =5.068, sn_mva=6.335, vm_pu=1.0, name='Diesel 3',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)
    VAE_Diesel_4 = pp.create_gen(net, bus_VAE_Diesler, p_mw =5.068, sn_mva=6.335, vm_pu=1.0, name='Diesel 4',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)

    bus_VAER_N = pp.create_bus(net, vn_kv, name='Vaer N', type='b', in_service=False, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_1 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAER_N, name ='Trf Vaerket 1 - 1', std_type='Trf-1 16/20 MVA', in_service=False)
    




    ## 00 Dampvaerket

    bus_DMP_A = pp.create_bus(net, vn_kv, name='Dampværk A', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_DMP_B = pp.create_bus(net, vn_kv, name='Dampværk B', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_DMP = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # aux_bus_trafo_DMP_2 = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_DMP1 = pp.create_switch(net, aux_bus_DMP, bus_DMP_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_DMP2 = pp.create_switch(net, aux_bus_DMP, bus_DMP_B, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    trafo_DMP = pp.create_transformer(net, hv_bus = bus_VAE_A, lv_bus = aux_bus_DMP, name='Værket Trf 2', std_type='Trf-2 25/31.5 MVA')

    aux_bus_DMP_2 = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_DMP3 = pp.create_switch(net, aux_bus_DMP_2, bus_DMP_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_DMP4 = pp.create_switch(net, aux_bus_DMP_2, bus_DMP_B, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)

    DMP_shunt = pp.create_shunt(net, bus_DMP_A, q_mvar=0.8, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)
    DMP_shunt_var = pp.create_shunt(net, bus_DMP_A, q_mvar=3.2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    # DMP_load = pp.create_load(net, aux_bus_DMP_2, p_mw=1.37, q_mvar = 0.26)
    
    target_substation = "Værket"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    DMP_consumed = pp.create_load(net, aux_bus_DMP_2,p_mw=consumption, q_mvar=0)
    DMP_generated = pp.create_gen(net, aux_bus_DMP_2, p_mw =-1*production, q_mvar=0)

    # switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)


    ## 01 Snorrebakken


    bus_SNO_10 = pp.create_bus(net, vn_kv, name='Snorrebakken 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_SNO_SMED = pp.create_bus(net, vn_kv, name='94 Smedegaard', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_SNO_YPP = pp.create_bus(net, vn_kv, name='566 Ypperne', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_SNO_YPP = pp.create_bus(net, vn_kv, name='566 Ypperne', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # line_SNO_10_SMED = pp.create_line(net, from_bus=bus_SNO_10, to_bus = bus_SNO_SMED, std_type = '3x95 PEX AL + 25 CU', length_km=5.751)
    # line_YPP_SMED = pp.create_line(net, from_bus=bus_SNO_YPP, to_bus = bus_SNO_SMED, std_type = '3x50 PEX AL + 16 CU', length_km=1.21)

    trafo_SNO = pp.create_transformer(net, hv_bus = bus_SNO, lv_bus = bus_SNO_10, name='Snorrebakken Trf', std_type='Trf 10 MVA ek 8.5 er 0.62')

    # ## Create loads
    # load_VIA_A = pp.create_load(net, bus_VIA_A,p_mw=0.929, q_mvar=0.478)
    # SNO_load = pp.create_load(net, bus_SNO_10,p_mw=0.883, q_mvar=0.129)

    ## Create generators
    target_substation = "Snorrebakken"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    SNO_consumed = pp.create_load(net, bus_SNO_10,p_mw=consumption, q_mvar=0)
    # SNO_generated = pp.create_gen(net, bus_SNO_10, p_mw =-1*production, q_mvar=0)
    SNO_generated = pp.create_gen(net, bus_SNO_10, p_mw =-1*production, min_p_mw=0, max_p_mw=1,q_mvar=0)


    ## Hasle
    # aux_bus_HAS_A_B_1 = pp.create_bus(net, 63, name='Aux bus Hasle 1', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # aux_bus_HAS_A_B_2 = pp.create_bus(net, 63, name='Aux bus Hasle 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_trafo_HAS_1 = pp.create_bus(net, 63, name='Aux bus trafo HASLE', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_trafo_HAS_2 = pp.create_bus(net, 63, name='Aux bus trafo HASLE', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_1, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_1, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)
    switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)

    bus_HAS_10 = pp.create_bus(net, vn_kv, name='Hasle 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    
    trafo_HAS1 = pp.create_transformer(net, hv_bus = aux_bus_trafo_HAS_1, lv_bus = bus_HAS_10, name='Hasle Trf 1', std_type='Trf 10 MVA ek 8.87 er 0.54', in_service=False)
    trafo_HAS2 = pp.create_transformer(net, hv_bus = aux_bus_trafo_HAS_2, lv_bus = bus_HAS_10, name='Hasle Trf 2', std_type='Trf 10 MVA ek 8.87 er 0.54')

    # bus_HAS_TOR = pp.create_bus(net, vn_kv, name='1042 Tornby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_HAS_VYS = pp.create_bus(net, vn_kv, name='1020 Vysteby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_HAS_HAS = pp.create_bus(net, vn_kv, name='851 Hasle VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    # HAS_husstandsmoller = pp.create_sgen(net, bus_HAS_10, p_mw=2, q_mvar = 0, slack=True)
    # HAS_load = pp.create_load(net, bus_HAS_10,p_mw=0.641, q_mvar=-0.437)


    # HAS_WTG1042 = pp.create_sgen(net, bus_HAS_TOR, p_mw=6.9, q_mvar = 0)
    # HAS_WTG1020 = pp.create_sgen(net, bus_HAS_VYS, p_mw=5.25, q_mvar = 0)
    # HAS_WTG851 = pp.create_sgen(net, bus_HAS_HAS, p_mw=3.9, q_mvar = 0)

    # line_HAS_10_TOR = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_TOR, std_type = '3x150 PEX AL+25 CU', length_km=2.944, parallel=2)
    # line_HAS_10_VYS = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_VYS, std_type = '3x 240 PEX AL + 35 CU', length_km=5.293, parallel=1)
    # line_HAS_10_HAS = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_HAS, std_type = '3x150 PEX AL+25 CU', length_km=3.9, parallel=1)

    target_substation = "Hasle"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    HAS_husstandsmoller = pp.create_sgen(net, bus_HAS_10, p_mw=-1*production, q_mvar = 0, slack=True)
    HAS_load = pp.create_load(net, bus_HAS_10,p_mw=consumption)

    
    ## OLSKER
    target_substation = "Olsker"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    bus_OLS_10 = pp.create_bus(net, vn_kv, name='Olsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    trafo_OLS1 = pp.create_transformer(net, hv_bus = bus_OLS, lv_bus = bus_OLS_10, name='Olsker Trf 1', std_type='Trf 4 MVA ek 7.4 er 0.3')
    trafo_OLS2 = pp.create_transformer(net, hv_bus = bus_OLS, lv_bus = bus_OLS_10, name='Olsker Trf 2', std_type='Trf 4 MVA ek 7.4 er 0.3', in_service=False)

    OLS_husstandsmoller = pp.create_sgen(net, bus_OLS_10, p_mw=-1*production, q_mvar = 0, slack=True)
    OLS_load = pp.create_load(net, bus_OLS_10,p_mw=consumption, q_mvar=0)

    ## Østerlars
    bus_OST_10 = pp.create_bus(net, vn_kv, name='Østerlars 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_OST = pp.create_transformer(net, hv_bus = bus_OST, lv_bus = bus_OST_10, name='Østerlars Trf 1', std_type='Trf 16 MVA ek 8.8 er 0.3')
    # OST_husstandsmoller = pp.create_sgen(net, bus_OST_10, p_mw=2, q_mvar = 0, slack=True)
    # OST_load = pp.create_load(net, bus_OST_10,p_mw=0.922, q_mvar=-0.109)

    target_substation = "Østerlars"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    OST_husstandsmoller = pp.create_sgen(net, bus_OST_10, p_mw=-1*production, q_mvar = 0, slack=True)
    OST_load = pp.create_load(net, bus_OST_10,p_mw=consumption, q_mvar=0)

    ## Åkirkeby
    bus_AAK_10 = pp.create_bus(net, vn_kv, name='Åkirkeby 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # trafo_AAK22 = pp.create_transformer(net, hv_bus = bus_AAK, lv_bus = bus_AAK_10, name='Aakirkeby Trf 21', std_type='Trf 16 MVA ek 8.8 er 0.', in_service=False)
    trafo_AAK21 = pp.create_transformer(net, hv_bus = bus_AAK, lv_bus = bus_AAK_10, name='Aakirkeby Trf 22', std_type='Trf 25/31.5 MVA ek 10%', in_service=True)
    # AAK_husstandsmoller = pp.create_sgen(net, bus_AAK_10, p_mw=2, q_mvar = 0, slack=True)
    # AAK_load = pp.create_load(net, bus_AAK_10,p_mw=1.587, q_mvar=-0.578)

    # bus_AAK_BOD = pp.create_bus(net, vn_kv, name='Bodelyngsvejen 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # line_AAK_10_BOD = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_BOD, std_type = '3x150 PEX AL+25 CU', length_km=1.25, parallel=2)
    # # AAK_PV = pp.create_sgen(net, bus_AAK_BOD, p_mw=7.5, q_mvar = 0, slack=True)

    # bus_AAK_KAL = pp.create_bus(net, vn_kv, name='Kalby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    # line_AAK_10_BOD = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_KAL, std_type = '3x150 PEX AL+25 CU', length_km=0.516, parallel=2)
    # # AAK_WTG965 = pp.create_sgen(net, bus_AAK_KAL, p_mw=6, q_mvar = 0, slack=True)

    # bus_AAK_SOS = pp.create_bus(net, vn_kv, name='Sose VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    # line_AAK_10_SOS = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_SOS, std_type = '3x150 PEX AL+25 CU', length_km=3.24, parallel=2)
    # # AAK_WTG1004 = pp.create_sgen(net, bus_AAK_KAL, p_mw=6.5, q_mvar = 0, slack=True)

    # bus_AAK_BIO = pp.create_bus(net, vn_kv, name='Biogas', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    # line_AAK_10_BIO = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_BIO, std_type = '3x95 PEX AL + 25 CU', length_km=2.314, parallel=1)
    # AAK_BIO1 = pp.create_gen(net, bus_AAK_BIO, p_mw = 1.521,sn_mva=1.981, vm_pu=1.0, name='Biogas gen 1',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)
    # AAK_BIO2 = pp.create_gen(net, bus_AAK_BIO, p_mw = 1.521,sn_mva=1.981, vm_pu=1.0, name='Biogas gen 1',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)

    target_substation = "Åkirkeby"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    AAK_husstandsmoller = pp.create_sgen(net, bus_AAK_10, p_mw=-1*production, q_mvar = 0, slack=True)
    AAK_load = pp.create_load(net, bus_AAK_10,p_mw=consumption, q_mvar=0)

    ## Nexø
    bus_NEX_10 = pp.create_bus(net, vn_kv, name='Nexø 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_NEX1 = pp.create_transformer(net, hv_bus = bus_NEX, lv_bus = bus_NEX_10, name='Nexø Trf 1', std_type='SEA 63/11 10 MVA NEXØ', in_service=True)
    trafo_NEX2 = pp.create_transformer(net, hv_bus = bus_NEX, lv_bus = bus_NEX_10, name='Nexø Trf 2', std_type='Trf 10 MVA ek 8.4 er 0.61', in_service=False)

    target_substation = "Nexø"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]
    NEX_husstandsmoller = pp.create_sgen(net, bus_NEX_10, p_mw=-1*production, q_mvar = 0, slack=True)
    NEX_load = pp.create_load(net, bus_NEX_10,p_mw=consumption, q_mvar=0)

    ## Bodilsker
    bus_BOD_10 = pp.create_bus(net, vn_kv, name='Bodilsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_BOD = pp.create_transformer(net, hv_bus = bus_BOD, lv_bus = bus_BOD_10, name='Bodilsker Trf 1', std_type='Trf 10/12 MVA ek 8.87 er 0.54', in_service=True)
    # BOD_husstandsmoller = pp.create_sgen(net, bus_BOD_10, p_mw=2, q_mvar = 0, slack=True)
    # BOD_load = pp.create_load(net, bus_BOD_10,p_mw=0.618, q_mvar=-0.026)

    target_substation = "Bodilsker"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    BOD_husstandsmoller = pp.create_sgen(net, bus_BOD_10, p_mw=-1*production, q_mvar = 0, slack=True)
    BOD_load = pp.create_load(net, bus_BOD_10,p_mw=consumption, q_mvar=0)


    BOD_shunt = pp.create_shunt(net, bus_BOD_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)
    # bus_BOD_GAD = pp.create_bus(net, vn_kv, name='Gadeby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # line_BOD_GAD = pp.create_line(net, from_bus=bus_BOD_10, to_bus = bus_BOD_GAD, std_type = '3x95 PEX AL + 25 CU', length_km=2.48, parallel=1)
    # BOD_WTG1001 = pp.create_sgen(net, bus_BOD_GAD, p_mw=2.7, q_mvar = 0, slack=True)

    ## Rønne Syd
    bus_RNS_10 = pp.create_bus(net, vn_kv, name='Rønne Syd 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_RNS1 = pp.create_transformer(net, hv_bus = bus_RNS, lv_bus = bus_RNS_10, name='Rønne Syd Trf 1', std_type='Trf 10 MVA ek 8.3 er 0.62', in_service=True)
    # RNS_husstandsmoller = pp.create_sgen(net, bus_RNS_10, p_mw=2, q_mvar = 0, slack=True)
    # RNS_load = pp.create_load(net, bus_RNS_10,p_mw=1.128, q_mvar=-0.124)
    RNS_shunt = pp.create_shunt(net, bus_RNS_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    target_substation = "Rønne Syd"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    RNS_husstandsmoller = pp.create_sgen(net, bus_RNS_10, p_mw=-1*production, q_mvar = 0, slack=True)
    RNS_load = pp.create_load(net, bus_RNS_10,p_mw=consumption, q_mvar=0)


    ## Allinge
    bus_ALL_10 = pp.create_bus(net, vn_kv, name='Allinge 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_ALL1 = pp.create_transformer(net, hv_bus = bus_ALL, lv_bus = bus_ALL_10, name='Allinge Trf 1', std_type='Trf 10 MVA ek 8.4 er 0.61', in_service=True)
    trafo_ALL2 = pp.create_transformer(net, hv_bus = bus_ALL, lv_bus = bus_ALL_10, name='Allinge Trf 2', std_type='Trf 10 MVA ek 8.04 er 0.53', in_service=False)
    # ALL_husstandsmoller = pp.create_sgen(net, bus_ALL_10, p_mw=2, q_mvar = 0, slack=True)


    # ALL_load = pp.create_load(net, bus_ALL_10,p_mw=0.78, q_mvar=-0.266)
    target_substation = "Allinge"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    ALL_husstandsmoller = pp.create_sgen(net, bus_ALL_10, p_mw=-1*production, q_mvar = 0, slack=True)
    ALL_load = pp.create_load(net, bus_ALL_10,p_mw=consumption, q_mvar=0)

    ## Svaneke
    bus_SVAN_10 = pp.create_bus(net, vn_kv, name='Svaneke 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_SVAN1 = pp.create_transformer(net, hv_bus = bus_SVA, lv_bus = bus_SVAN_10, name='Svaneke Trf 1', std_type='Trf 10 MVA ek 8.3 er 0.54', in_service=True)
    # SVAN_husstandsmoller = pp.create_sgen(net, bus_SVAN_10, p_mw=2, q_mvar = 0, slack=True)
    # SVAN_load = pp.create_load(net, bus_SVAN_10,p_mw=0.923, q_mvar=0.043)
    SVAN_shunt = pp.create_shunt(net, bus_RNS_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    target_substation = "Svaneke"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]
    SVAN_husstandsmoller = pp.create_sgen(net, bus_SVAN_10, p_mw=-1*production, q_mvar = 0, slack=True)
    SVAN_load = pp.create_load(net, bus_SVAN_10,p_mw=consumption, q_mvar=0)

    ## Viadukten
    bus_VIA_10 = pp.create_bus(net, vn_kv, name='Viadukten 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_4 = pp.create_bus(net, 63, name='Auxiliary bus Viadukten 4', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_VIA_A_4 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_4, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_4 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_4, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)
    trafo_VIA1 = pp.create_transformer(net, hv_bus = aux_bus_VIA_4, lv_bus = bus_VIA_10, name='Viadukten Trf 1', std_type='Trf 10 MVA ek 7.9 er 0.54', in_service=True)
    # VIA_husstandsmoller = pp.create_sgen(net, bus_VIA_10, p_mw=2, q_mvar = 0, slack=True)
    # VIA_load = pp.create_load(net, bus_VIA_10,p_mw=0.929, q_mvar=0.478)

    target_substation = "Viadukten"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    VIA_husstandsmoller = pp.create_sgen(net, bus_VIA_10, p_mw=-1*production, q_mvar = 0, slack=True)
    VIA_load = pp.create_load(net, bus_VIA_10,p_mw=consumption, q_mvar=0)

    ## Rønne Nord
    bus_RNO_10 = pp.create_bus(net, vn_kv, name='Rønne Nord 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_RNO = pp.create_transformer(net, hv_bus = bus_RNO, lv_bus = bus_RNO_10, name='Rønne Nord Trf 1', std_type='Trf 10 MVA ek 7.94 er 0.58', in_service=True)
    # RNO_husstandsmoller = pp.create_sgen(net, bus_RNO_10, p_mw=2, q_mvar = 0, slack=True)
    # RNO_load = pp.create_load(net, bus_RNO_10,p_mw=0.866, q_mvar=0.58)

    target_substation = "Rønne Nord"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    RNO_husstandsmoller = pp.create_sgen(net, bus_RNO_10, p_mw=-1*production, q_mvar = 0, slack=True)
    RNO_load = pp.create_load(net, bus_RNO_10,p_mw=consumption, q_mvar=0)

    ## Poulsker
    bus_POU_10 = pp.create_bus(net, vn_kv, name='Poulsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_POU = pp.create_transformer(net, hv_bus = bus_POU, lv_bus = bus_POU_10, name='Poulsker Trf 1', std_type='Trf 10 MVA ek 8.14 er 0.59', in_service=True)
    # POU_husstandsmoller = pp.create_sgen(net, bus_POU_10, p_mw=2, q_mvar = 0, slack=True)
    # POU_load = pp.create_load(net, bus_POU_10,p_mw=0.405, q_mvar=-0.546)

    target_substation = "Povlsker"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    POU_husstandsmoller = pp.create_sgen(net, bus_POU_10, p_mw=-1*production, q_mvar = 0, slack=True)
    POU_load = pp.create_load(net, bus_POU_10,p_mw=consumption, q_mvar=0)

    ## Vesthavnen
    bus_VES_10 = pp.create_bus(net, vn_kv, name='Vesthavnen 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VES = pp.create_transformer(net, hv_bus = bus_VES, lv_bus = bus_VES_10, name='Vesthavnen Trf 1', std_type='Trf 10 MVA ek 8.1 er 0.54', in_service=True)

    target_substation = "Vesthavnen"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]

    VES_husstandsmoller = pp.create_sgen(net, bus_VES_10, p_mw=-1*production, q_mvar = 0, slack=True)
    VES_load = pp.create_load(net, bus_VES_10,p_mw=consumption, q_mvar=0)

    ## Gudhjem
    bus_GUD_10 = pp.create_bus(net, vn_kv, name='Gudhjem 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_GUD = pp.create_transformer(net, hv_bus = bus_GUD, lv_bus = bus_GUD_10, name='Gudhjem Trf 1', std_type='Trf 4 MVA ek 7.3 er 0.3 N.2', in_service=True)
    # GUD_husstandsmoller = pp.create_sgen(net, bus_GUD_10, p_mw=2, q_mvar = 0, slack=True)
    # GUD_load = pp.create_load(net, bus_GUD_10,p_mw=0.608, q_mvar=-0.143)
    target_substation = "Gudhjem"
    substation_data = measurements[measurements['Substation'] == target_substation]
    consumption = substation_data['Consumption'].values[0]
    production = substation_data['Production'].values[0]



    GUD_husstandsmoller = pp.create_sgen(net, bus_GUD_10, p_mw=-1*production, q_mvar = 0, slack=True)
    GUD_load = pp.create_load(net, bus_GUD_10,p_mw=consumption, q_mvar=0)


    return net


## Net based on available measurements
def net_60kV_SCADA_measurements(net, measurements):
    vn_kv = 63
    max_vm_pu = 1.05
    min_vm_pu = 0.95


    ## Create substations Net 60 kv
    bus_HAS_A = pp.create_bus(net, vn_kv, name='Hasle A', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_HAS_B = pp.create_bus(net, vn_kv, name='Hasle B', index=None, geodata=None, type='b', zone=None, in_service=False,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SNO = pp.create_bus(net, vn_kv, name='Snorrebakken', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OLS = pp.create_bus(net, vn_kv, name='Olsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_RNO = pp.create_bus(net, vn_kv, name='Ronne Nord', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOR_HAS = pp.create_bus(net, vn_kv, name='BOR-HAS split 3', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    bus_ALL = pp.create_bus(net, vn_kv, name='Allinge', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_SVA = pp.create_bus(net, vn_kv, name='Svaneke', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_NEX = pp.create_bus(net, vn_kv, name='Nexo', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOD = pp.create_bus(net, vn_kv, name='Bodilsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_POU = pp.create_bus(net, vn_kv, name='Poulsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_AAK = pp.create_bus(net, vn_kv, name='Aakirkeby', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_DAL = pp.create_bus(net, vn_kv, name='Dalslunde', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OST = pp.create_bus(net, vn_kv, name='Osterlars', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_OLS = pp.create_bus(net, vn_kv, name='Olsker', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_GUD = pp.create_bus(net, vn_kv, name='Gudhjem', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VIA_A = pp.create_bus(net, vn_kv, name='Viadukten A', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VIA_B = pp.create_bus(net, vn_kv, name='Viadukten B', index=None, geodata=None, type='b', zone=None, in_service=False,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_RNS = pp.create_bus(net, vn_kv, name='Ronne Syd', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VAE_A = pp.create_bus(net, vn_kv, name='Vaerket A', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VAE_B = pp.create_bus(net, vn_kv, name='Vaerket B', index=None, geodata=None, type='b', zone=None, in_service=False, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_VES = pp.create_bus(net, vn_kv, name='Vesthavnen', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    aux_bus_VIA_1 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 1', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_2 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 2', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_3 = pp.create_bus(net, vn_kv, name='Auxiliary bus Viadukten 3', index=None, geodata=None, type='b', zone=None, in_service=True,  max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    ## Create lines 60 kV side
    line_HAS_A_SNO = pp.create_line(net, from_bus=bus_HAS_A, to_bus = bus_SNO, std_type = 'OHL 3x1x130StAl+50Fe', length_km=5.217 )
    line_SNO_VAE_A = pp.create_line(net, from_bus=bus_SNO, to_bus = bus_VAE_A, std_type = 'APBF 1x3x95 Cu', length_km=3.453)
    line_VAE_A_VES = pp.create_line(net, from_bus=bus_VES, to_bus = bus_VAE_A, std_type = 'PEX 3x1x300Al+35Cu', length_km=1.8)
    line_VAE_A_VIA_A = pp.create_line(net, from_bus=aux_bus_VIA_1, to_bus = bus_VAE_A, std_type = 'PEX 3x1x300Al+35Cu', length_km=1.481)
    line_VAE_A_RNS = pp.create_line(net, from_bus=bus_VAE_A, to_bus=bus_RNS, std_type = 'APBF 1x3x95 Cu', length_km=2.861)
    line_VES_RNO = pp.create_line(net, from_bus=bus_RNO, to_bus = bus_VES, std_type = 'PEX 3x1x300Al+35Cu', length_km=2.2)
    line_HAS_A_RNO = pp.create_line(net, from_bus=bus_HAS_A, to_bus = bus_RNO, std_type = 'PEX 3x1x240Al+35Cu', length_km=7.434)
    line_VIA_A_RNO = pp.create_line(net, from_bus=aux_bus_VIA_2, to_bus = bus_RNO, std_type = 'PEX 3x1x240Al+35Cu', length_km=1.834)
    line_VIA_A_RNS = pp.create_line(net, from_bus=aux_bus_VIA_3, to_bus = bus_RNS, std_type = 'PEX 3x1x240Al+35Cu', length_km=1.674)
    line_RNS_AAK = pp.create_line(net, from_bus=bus_AAK, to_bus = bus_RNS, std_type = 'OHL 3x1x130StAl+50Fe', length_km=10.995)
    line_BOD_AAK = pp.create_line(net, from_bus=bus_AAK, to_bus = bus_BOD, std_type = 'OHL 3x1x130StAl+50Fe', length_km=10.891)
    line_BOD_POU = pp.create_line(net, from_bus=bus_POU, to_bus = bus_BOD, std_type = 'PEX 3x1x150Al+25Cu', length_km=5.95)
    line_BOD_NEX = pp.create_line(net, from_bus=bus_NEX, to_bus = bus_BOD, std_type = 'PEX 3x1x95Al+25Cu', length_km=3.477)
    line_BOD_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_BOD, std_type = 'OHL 3x1x130StAl+50Fe', length_km=4.138)
    line_SVA_NEX = pp.create_line(net, from_bus=bus_NEX, to_bus = bus_SVA, std_type = 'PEX 3x1x150Al+25Cu', length_km=9.78)
    line_SVA_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_SVA, std_type = 'PEX 3x1x150Al+25Cu', length_km=7.531)
    line_OST_DAL = pp.create_line(net, from_bus=bus_DAL, to_bus = bus_OST, std_type = 'OHL 3x1x130StAl+50Fe', length_km=9.924)
    line_OST_GUD = pp.create_line(net, from_bus=bus_GUD, to_bus = bus_OST, std_type = 'PEX 3x1x150Al+25Cu', length_km=6.6)
    line_OST_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_OST, std_type = 'OHL 3x1x130StAl+50Fe', length_km=13.05)
    line_ALL_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_ALL, std_type = 'PEX 3x1x150Al+25Cu', length_km=4.276)
    line_HAS_A_OLS = pp.create_line(net, from_bus=bus_OLS, to_bus = bus_HAS_A, std_type = 'OHL 3x1x130StAl+50Fe', length_km=6.818)
    line_BOR_HAS_A = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_HAS_A, std_type = 'PEX 3x1x400CuPbAl', length_km=1.4)
    # line_BOR_HAS_3 = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_HAS_A, std_type = 'PEX 3x1x240CuPbAl', length_km=43.5)

    ## Switches

    # switch_VIA_A_1 = pp.create_switch(net, bus_VIA_A, line_VIA_A_RNO, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_A_2 = pp.create_switch(net, bus_VIA_A, line_VAE_A_VIA_A, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_A_3 = pp.create_switch(net, bus_VIA_A, line_VIA_A_RNS, et='l', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNO, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, line_VAE_A_VIA_A, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNS, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)

    switch_VIA_A_1 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_1, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_A_2 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_2, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_A_3 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_3, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)

    switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_1, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_2, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_3, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)


    # switch_VIA_B_1 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNO, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_2 = pp.create_switch(net, bus_VIA_B, line_VAE_A_VIA_A, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    # switch_VIA_B_3 = pp.create_switch(net, bus_VIA_B, line_VIA_A_RNS, et='l', closed=False, type=None, name=None, index=None, z_ohm=0)
    ## TODO include switches VAE A and B


    ## External grid Sweden
    bus_BOR_HAS_split1 = pp.create_bus(net, vn_kv, name='BOR HAS split 1', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_BOR_HAS_split2 = pp.create_bus(net, vn_kv, name='BOR HAS split 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_borr = pp.create_bus(net, vn_kv, name='Borrby', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    line_BOR_HAS_2 = pp.create_line(net, from_bus=bus_BOR_HAS_split2, to_bus = bus_BOR_HAS_split1, std_type = 'PEX 3x1x400CuPbAl', length_km=0.7)
    line_BOR_HAS_1 = pp.create_line(net, from_bus=bus_BOR_HAS_split1, to_bus = bus_borr, std_type = 'IBIS 3x1x234', length_km=4.2)
    line_BOR_HAS_3 = pp.create_line(net, from_bus=bus_BOR_HAS, to_bus = bus_BOR_HAS_split2, std_type = 'PEX 3x1x240CuPbAl', length_km=43.5)
    bus_tom = pp.create_bus(net, 135, name='Tomelilla', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_borr = pp.create_transformer(net, hv_bus = bus_tom, lv_bus = bus_borr, name = 'Borrby',std_type = 'Trf 135-69 kV')
    # bus_N_punkt_Borr = pp.create_bus(net, vn_kv, name='N punkt Borrby', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    # sw_Borr = pp.create_switch(net, bus, element, et, closed=True, type=None, name=None, index=None, z_ohm=0)
    ext_grid = pp.create_ext_grid(net, bus_tom, vm_pu =0.91, va_degree = 0.0, slack_weight = 1.0)
    net.ext_grid.at[0, 'vm_pu'] = 0.91
    # gen = pp.create_gen(net, bus_VIA_A, p_mw = 0.0001)

    vn_kv = 10.5

    ## Gen Vaerket
    bus_VAE_blok_6 = pp.create_bus(net, vn_kv, name='Vaerket Blok 6', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_blok_6 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_blok_6, name ='Trf blok 6', std_type='Trf-6 45 MVA', in_service=False)
    VAE_gen_blok_6 = pp.create_gen(net, bus_VAE_blok_6, p_mw = 36, vm_pu=1.0, name='Blok 6 gen',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)

    bus_VAE_blok_5 = pp.create_bus(net, vn_kv, name='Vaerket Blok 5', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_blok_6 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_blok_5, name ='Trf blok 5', std_type='Trf-5 29 MVA', in_service=False)
    VAE_gen_blok_5 = pp.create_gen(net, bus_VAE_blok_6, p_mw =23.52, sn_mva=29, vm_pu=1.0, name='Blok 5 gen',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)

    bus_VAE_Diesler = pp.create_bus(net, vn_kv, name='Vaerket Diesler', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_1 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAE_Diesler, name ='Trf Vaerket 1', std_type='Trf-1 16/20 MVA', in_service=False)
    VAE_Diesel_1 = pp.create_gen(net, bus_VAE_Diesler, p_mw =4.66, sn_mva=5.825, vm_pu=1.0, name='Diesel 1',scaling=1.0, slack=False, cos_phi=0.8, in_service=False)
    VAE_Diesel_2 = pp.create_gen(net, bus_VAE_Diesler, p_mw =4.66, sn_mva=5.825, vm_pu=1.0, name='Diesel 2',scaling=1.0, slack=False, cos_phi=0.8, in_service=False)
    VAE_Diesel_3 = pp.create_gen(net, bus_VAE_Diesler, p_mw =5.068, sn_mva=6.335, vm_pu=1.0, name='Diesel 3',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)
    VAE_Diesel_4 = pp.create_gen(net, bus_VAE_Diesler, p_mw =5.068, sn_mva=6.335, vm_pu=1.0, name='Diesel 4',scaling=1.0, slack=True, cos_phi=0.8, in_service=False)

    bus_VAER_N = pp.create_bus(net, vn_kv, name='Vaer N', type='b', in_service=False, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VAE_1 = pp.create_transformer(net, hv_bus=bus_VAE_A, lv_bus=bus_VAER_N, name ='Trf Vaerket 1 - 1', std_type='Trf-1 16/20 MVA', in_service=False)
    




    ## 00 Dampvaerket

    bus_DMP_A = pp.create_bus(net, vn_kv, name='Dampværk A', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    bus_DMP_B = pp.create_bus(net, vn_kv, name='Dampværk B', type='b', in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_DMP = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # aux_bus_trafo_DMP_2 = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_DMP1 = pp.create_switch(net, aux_bus_DMP, bus_DMP_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_DMP2 = pp.create_switch(net, aux_bus_DMP, bus_DMP_B, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    trafo_DMP = pp.create_transformer(net, hv_bus = bus_VAE_A, lv_bus = aux_bus_DMP, name='Værket Trf 2', std_type='Trf-2 25/31.5 MVA', in_service=True)

    aux_bus_DMP_2 = pp.create_bus(net, vn_kv, name='Aux bus trafo DMP 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_DMP3 = pp.create_switch(net, aux_bus_DMP_2, bus_DMP_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_DMP4 = pp.create_switch(net, aux_bus_DMP_2, bus_DMP_B, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)

    DMP_shunt = pp.create_shunt(net, bus_DMP_A, q_mvar=0.8, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)
    DMP_shunt_var = pp.create_shunt(net, bus_DMP_A, q_mvar=3.2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    # DMP_load = pp.create_load(net, aux_bus_DMP_2, p_mw=1.37, q_mvar = 0.26)

    target_substation = "Vaerket"
    measurements['Active Power'] = pd.to_numeric(measurements['Active Power'], errors='coerce')
    substation_data = measurements[measurements['Substation'] == target_substation]
    # print(substation_data['Active Power'].dtype)

    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]

    if active_power < 0:
        VAE_generated = pp.create_gen(net, aux_bus_DMP_2, p_mw=active_power, q_mvar=reactive_power)
    else:
        VAE_consumed = pp.create_load(net, aux_bus_DMP_2,p_mw=active_power, q_mvar=reactive_power)
    
    # target_substation = "Vaerket"
    # substation_data = smart_meter_measurement_vaerket[smart_meter_measurement_vaerket['Substation'] == target_substation]
    # print(substation_data)
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]

    # DMP_consumed = pp.create_load(net, aux_bus_DMP_2,p_mw=consumption, q_mvar=0)
    # DMP_generated = pp.create_gen(net, aux_bus_DMP_2, p_mw =-1*production, q_mvar=0)

    # switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    # switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)


    ## 01 Snorrebakken


    bus_SNO_10 = pp.create_bus(net, vn_kv, name='Snorrebakken 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_SNO_SMED = pp.create_bus(net, vn_kv, name='94 Smedegaard', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_SNO_YPP = pp.create_bus(net, vn_kv, name='566 Ypperne', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_SNO_YPP = pp.create_bus(net, vn_kv, name='566 Ypperne', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # line_SNO_10_SMED = pp.create_line(net, from_bus=bus_SNO_10, to_bus = bus_SNO_SMED, std_type = '3x95 PEX AL + 25 CU', length_km=5.751)
    # line_YPP_SMED = pp.create_line(net, from_bus=bus_SNO_YPP, to_bus = bus_SNO_SMED, std_type = '3x50 PEX AL + 16 CU', length_km=1.21)

    trafo_SNO = pp.create_transformer(net, hv_bus = bus_SNO, lv_bus = bus_SNO_10, name='Snorrebakken Trf', std_type='Trf 10 MVA ek 8.5 er 0.62')

    # ## Create loads
    # load_VIA_A = pp.create_load(net, bus_VIA_A,p_mw=0.929, q_mvar=0.478)
    # SNO_load = pp.create_load(net, bus_SNO_10,p_mw=0.883, q_mvar=0.129)

    ## Create generators
    target_substation = "Snorrebakken"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    if active_power < 0:
        SNO_generated = pp.create_gen(net, bus_SNO_10, p_mw=active_power, q_mvar=reactive_power)
    else:
        SNO_consumed = pp.create_load(net, bus_SNO_10,p_mw=active_power, q_mvar=reactive_power)



    ## Hasle
    # aux_bus_HAS_A_B_1 = pp.create_bus(net, 63, name='Aux bus Hasle 1', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # aux_bus_HAS_A_B_2 = pp.create_bus(net, 63, name='Aux bus Hasle 2', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_trafo_HAS_1 = pp.create_bus(net, 63, name='Aux bus trafo HASLE', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_trafo_HAS_2 = pp.create_bus(net, 63, name='Aux bus trafo HASLE', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_1, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_1, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)
    switch_HAS1 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_A, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_HAS2 = pp.create_switch(net, aux_bus_trafo_HAS_2, bus_HAS_B, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)

    bus_HAS_10 = pp.create_bus(net, vn_kv, name='Hasle 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    
    trafo_HAS1 = pp.create_transformer(net, hv_bus = aux_bus_trafo_HAS_1, lv_bus = bus_HAS_10, name='Hasle Trf 1', std_type='Trf 10 MVA ek 8.87 er 0.54', in_service=False)
    trafo_HAS2 = pp.create_transformer(net, hv_bus = aux_bus_trafo_HAS_2, lv_bus = bus_HAS_10, name='Hasle Trf 2', std_type='Trf 10 MVA ek 8.87 er 0.54')

    # bus_HAS_TOR = pp.create_bus(net, vn_kv, name='1042 Tornby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_HAS_VYS = pp.create_bus(net, vn_kv, name='1020 Vysteby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # bus_HAS_HAS = pp.create_bus(net, vn_kv, name='851 Hasle VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    # HAS_husstandsmoller = pp.create_sgen(net, bus_HAS_10, p_mw=2, q_mvar = 0, slack=True)
    # HAS_load = pp.create_load(net, bus_HAS_10,p_mw=0.641, q_mvar=-0.437)


    # HAS_WTG1042 = pp.create_sgen(net, bus_HAS_TOR, p_mw=6.9, q_mvar = 0)
    # HAS_WTG1020 = pp.create_sgen(net, bus_HAS_VYS, p_mw=5.25, q_mvar = 0)
    # HAS_WTG851 = pp.create_sgen(net, bus_HAS_HAS, p_mw=3.9, q_mvar = 0)

    # line_HAS_10_TOR = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_TOR, std_type = '3x150 PEX AL+25 CU', length_km=2.944, parallel=2)
    # line_HAS_10_VYS = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_VYS, std_type = '3x 240 PEX AL + 35 CU', length_km=5.293, parallel=1)
    # line_HAS_10_HAS = pp.create_line(net, from_bus=bus_HAS_10, to_bus = bus_HAS_HAS, std_type = '3x150 PEX AL+25 CU', length_km=3.9, parallel=1)

    target_substation = "Hasle"
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    if active_power < 0:
        HAS_generated = pp.create_gen(net, bus_HAS_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        HAS_consumed = pp.create_load(net, bus_HAS_10,p_mw=active_power, q_mvar=reactive_power)

    
    ## OLSKER
    target_substation = "Olsker"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]


    bus_OLS_10 = pp.create_bus(net, vn_kv, name='Olsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)

    trafo_OLS1 = pp.create_transformer(net, hv_bus = bus_OLS, lv_bus = bus_OLS_10, name='Olsker Trf 1', std_type='Trf 4 MVA ek 7.4 er 0.3')
    trafo_OLS2 = pp.create_transformer(net, hv_bus = bus_OLS, lv_bus = bus_OLS_10, name='Olsker Trf 2', std_type='Trf 4 MVA ek 7.4 er 0.3', in_service=False)

    if active_power < 0:
        OLS_generated = pp.create_gen(net, bus_OLS_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        OLS_consumed = pp.create_load(net, bus_OLS_10,p_mw=active_power, q_mvar=reactive_power)


    ## Østerlars
    bus_OST_10 = pp.create_bus(net, vn_kv, name='Østerlars 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_OST = pp.create_transformer(net, hv_bus = bus_OST, lv_bus = bus_OST_10, name='Østerlars Trf 1', std_type='Trf 16 MVA ek 8.8 er 0.3')
    # OST_husstandsmoller = pp.create_sgen(net, bus_OST_10, p_mw=2, q_mvar = 0, slack=True)
    # OST_load = pp.create_load(net, bus_OST_10,p_mw=0.922, q_mvar=-0.109)

    target_substation = "Osterlars"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        OST_generated = pp.create_gen(net, bus_OST_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        OST_consumed = pp.create_load(net, bus_OST_10,p_mw=active_power, q_mvar=reactive_power)

    # OST_husstandsmoller = pp.create_sgen(net, bus_OST_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # OST_load = pp.create_load(net, bus_OST_10,p_mw=consumption, q_mvar=0)

    ## Åkirkeby
    bus_AAK_10 = pp.create_bus(net, vn_kv, name='Åkirkeby 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # trafo_AAK22 = pp.create_transformer(net, hv_bus = bus_AAK, lv_bus = bus_AAK_10, name='Aakirkeby Trf 21', std_type='Trf 16 MVA ek 8.8 er 0.', in_service=False)
    trafo_AAK21 = pp.create_transformer(net, hv_bus = bus_AAK, lv_bus = bus_AAK_10, name='Aakirkeby Trf 22', std_type='Trf 25/31.5 MVA ek 10%', in_service=True)
    # AAK_husstandsmoller = pp.create_sgen(net, bus_AAK_10, p_mw=2, q_mvar = 0, slack=True)
    # AAK_load = pp.create_load(net, bus_AAK_10,p_mw=1.587, q_mvar=-0.578)

    # bus_AAK_BOD = pp.create_bus(net, vn_kv, name='Bodelyngsvejen 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # line_AAK_10_BOD = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_BOD, std_type = '3x150 PEX AL+25 CU', length_km=1.25, parallel=2)
    # # AAK_PV = pp.create_sgen(net, bus_AAK_BOD, p_mw=7.5, q_mvar = 0, slack=True)

    # bus_AAK_KAL = pp.create_bus(net, vn_kv, name='Kalby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    # line_AAK_10_BOD = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_KAL, std_type = '3x150 PEX AL+25 CU', length_km=0.516, parallel=2)
    # # AAK_WTG965 = pp.create_sgen(net, bus_AAK_KAL, p_mw=6, q_mvar = 0, slack=True)

    # bus_AAK_SOS = pp.create_bus(net, vn_kv, name='Sose VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    # line_AAK_10_SOS = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_SOS, std_type = '3x150 PEX AL+25 CU', length_km=3.24, parallel=2)
    # # AAK_WTG1004 = pp.create_sgen(net, bus_AAK_KAL, p_mw=6.5, q_mvar = 0, slack=True)

    # bus_AAK_BIO = pp.create_bus(net, vn_kv, name='Biogas', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu) 
    # line_AAK_10_BIO = pp.create_line(net, from_bus=bus_AAK_10, to_bus = bus_AAK_BIO, std_type = '3x95 PEX AL + 25 CU', length_km=2.314, parallel=1)
    # AAK_BIO1 = pp.create_gen(net, bus_AAK_BIO, p_mw = 1.521,sn_mva=1.981, vm_pu=1.0, name='Biogas gen 1',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)
    # AAK_BIO2 = pp.create_gen(net, bus_AAK_BIO, p_mw = 1.521,sn_mva=1.981, vm_pu=1.0, name='Biogas gen 1',scaling=1.0, slack=True, cos_phi=0.8, in_service=True)

    target_substation = "Aakirkeby"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        AAK_generated = pp.create_gen(net, bus_AAK_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        AAK_consumed = pp.create_load(net, bus_AAK_10,p_mw=active_power, q_mvar=reactive_power)

    # target_substation = "Åkirkeby"
    # substation_data = measurements[measurements['Substation'] == target_substation]
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]

    # AAK_husstandsmoller = pp.create_sgen(net, bus_AAK_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # AAK_load = pp.create_load(net, bus_AAK_10,p_mw=consumption, q_mvar=0)

    ## Nexø
    bus_NEX_10 = pp.create_bus(net, vn_kv, name='Nexø 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_NEX1 = pp.create_transformer(net, hv_bus = bus_NEX, lv_bus = bus_NEX_10, name='Nexø Trf 1', std_type='SEA 63/11 10 MVA NEXØ', in_service=True)
    trafo_NEX2 = pp.create_transformer(net, hv_bus = bus_NEX, lv_bus = bus_NEX_10, name='Nexø Trf 2', std_type='Trf 10 MVA ek 8.4 er 0.61', in_service=False)

    target_substation = "Nexo"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        NEX_generated = pp.create_gen(net, bus_NEX_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        NEX_consumed = pp.create_load(net, bus_NEX_10,p_mw=active_power, q_mvar=reactive_power)

    # target_substation = "Nexø"
    # substation_data = measurements[measurements['Substation'] == target_substation]
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]
    # NEX_husstandsmoller = pp.create_sgen(net, bus_NEX_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # NEX_load = pp.create_load(net, bus_NEX_10,p_mw=consumption, q_mvar=0)

    ## Bodilsker
    bus_BOD_10 = pp.create_bus(net, vn_kv, name='Bodilsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_BOD = pp.create_transformer(net, hv_bus = bus_BOD, lv_bus = bus_BOD_10, name='Bodilsker Trf 1', std_type='Trf 10/12 MVA ek 8.87 er 0.54', in_service=True)
    # BOD_husstandsmoller = pp.create_sgen(net, bus_BOD_10, p_mw=2, q_mvar = 0, slack=True)
    # BOD_load = pp.create_load(net, bus_BOD_10,p_mw=0.618, q_mvar=-0.026)

    target_substation = "Bodilsker"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        BOD_generated = pp.create_gen(net, bus_BOD_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        BOD_consumed = pp.create_load(net, bus_BOD_10,p_mw=active_power, q_mvar=reactive_power)

    # target_substation = "Bodilsker"
    # substation_data = measurements[measurements['Substation'] == target_substation]
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]

    # BOD_husstandsmoller = pp.create_sgen(net, bus_BOD_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # BOD_load = pp.create_load(net, bus_BOD_10,p_mw=consumption, q_mvar=0)


    BOD_shunt = pp.create_shunt(net, bus_BOD_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)
    # bus_BOD_GAD = pp.create_bus(net, vn_kv, name='Gadeby VP', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    # line_BOD_GAD = pp.create_line(net, from_bus=bus_BOD_10, to_bus = bus_BOD_GAD, std_type = '3x95 PEX AL + 25 CU', length_km=2.48, parallel=1)
    # BOD_WTG1001 = pp.create_sgen(net, bus_BOD_GAD, p_mw=2.7, q_mvar = 0, slack=True)

    ## Rønne Syd
    bus_RNS_10 = pp.create_bus(net, vn_kv, name='Rønne Syd 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_RNS1 = pp.create_transformer(net, hv_bus = bus_RNS, lv_bus = bus_RNS_10, name='Rønne Syd Trf 1', std_type='Trf 10 MVA ek 8.3 er 0.62', in_service=True)
    # RNS_husstandsmoller = pp.create_sgen(net, bus_RNS_10, p_mw=2, q_mvar = 0, slack=True)
    # RNS_load = pp.create_load(net, bus_RNS_10,p_mw=1.128, q_mvar=-0.124)
    RNS_shunt = pp.create_shunt(net, bus_RNS_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    target_substation = "RNS"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        RNS_generated = pp.create_gen(net, bus_RNS_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        RNS_consumed = pp.create_load(net, bus_RNS_10,p_mw=active_power, q_mvar=reactive_power)

    # target_substation = "Rønne Syd"
    # substation_data = measurements[measurements['Substation'] == target_substation]
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]

    # RNS_husstandsmoller = pp.create_sgen(net, bus_RNS_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # RNS_load = pp.create_load(net, bus_RNS_10,p_mw=consumption, q_mvar=0)


    ## Allinge
    bus_ALL_10 = pp.create_bus(net, vn_kv, name='Allinge 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_ALL1 = pp.create_transformer(net, hv_bus = bus_ALL, lv_bus = bus_ALL_10, name='Allinge Trf 1', std_type='Trf 10 MVA ek 8.4 er 0.61', in_service=True)
    trafo_ALL2 = pp.create_transformer(net, hv_bus = bus_ALL, lv_bus = bus_ALL_10, name='Allinge Trf 2', std_type='Trf 10 MVA ek 8.04 er 0.53', in_service=False)
    # ALL_husstandsmoller = pp.create_sgen(net, bus_ALL_10, p_mw=2, q_mvar = 0, slack=True)

    target_substation = "Allinge"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        ALL_generated = pp.create_gen(net, bus_ALL_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        ALL_consumed = pp.create_load(net, bus_ALL_10,p_mw=active_power, q_mvar=reactive_power)


    # # ALL_load = pp.create_load(net, bus_ALL_10,p_mw=0.78, q_mvar=-0.266)
    # target_substation = "Allinge"
    # substation_data = measurements[measurements['Substation'] == target_substation]
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]

    # ALL_husstandsmoller = pp.create_sgen(net, bus_ALL_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # ALL_load = pp.create_load(net, bus_ALL_10,p_mw=consumption, q_mvar=0)

    ## Svaneke
    bus_SVAN_10 = pp.create_bus(net, vn_kv, name='Svaneke 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_SVAN1 = pp.create_transformer(net, hv_bus = bus_SVA, lv_bus = bus_SVAN_10, name='Svaneke Trf 1', std_type='Trf 10 MVA ek 8.3 er 0.54', in_service=True)
    # SVAN_husstandsmoller = pp.create_sgen(net, bus_SVAN_10, p_mw=2, q_mvar = 0, slack=True)
    # SVAN_load = pp.create_load(net, bus_SVAN_10,p_mw=0.923, q_mvar=0.043)
    SVAN_shunt = pp.create_shunt(net, bus_RNS_10, q_mvar=2, p_mw=0.0, vn_kv=None, step=1, max_step=1, name=None, in_service=True, index=None)

    target_substation = "Svaneke"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        SVA_generated = pp.create_gen(net, bus_SVAN_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        SVA_consumed = pp.create_load(net, bus_SVAN_10,p_mw=active_power, q_mvar=reactive_power)
    # target_substation = "Svaneke"
    # substation_data = measurements[measurements['Substation'] == target_substation]
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]
    # SVAN_husstandsmoller = pp.create_sgen(net, bus_SVAN_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # SVAN_load = pp.create_load(net, bus_SVAN_10,p_mw=consumption, q_mvar=0)

    ## Viadukten
    bus_VIA_10 = pp.create_bus(net, vn_kv, name='Viadukten 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    aux_bus_VIA_4 = pp.create_bus(net, 63, name='Auxiliary bus Viadukten 4', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    switch_VIA_A_4 = pp.create_switch(net, bus_VIA_A, aux_bus_VIA_4, et='b', closed=True, type=None, name=None, index=None, z_ohm=0)
    switch_VIA_B_4 = pp.create_switch(net, bus_VIA_B, aux_bus_VIA_4, et='b', closed=False, type=None, name=None, index=None, z_ohm=0)
    trafo_VIA1 = pp.create_transformer(net, hv_bus = aux_bus_VIA_4, lv_bus = bus_VIA_10, name='Viadukten Trf 1', std_type='Trf 10 MVA ek 7.9 er 0.54', in_service=True)
    # VIA_husstandsmoller = pp.create_sgen(net, bus_VIA_10, p_mw=2, q_mvar = 0, slack=True)
    # VIA_load = pp.create_load(net, bus_VIA_10,p_mw=0.929, q_mvar=0.478)

    target_substation = "Viadukten"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        VIA_generated = pp.create_gen(net, bus_VIA_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        VIA_consumed = pp.create_load(net, bus_VIA_10,p_mw=active_power, q_mvar=reactive_power)

    # target_substation = "Viadukten"
    # substation_data = measurements[measurements['Substation'] == target_substation]
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]

    # VIA_husstandsmoller = pp.create_sgen(net, bus_VIA_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # VIA_load = pp.create_load(net, bus_VIA_10,p_mw=consumption, q_mvar=0)

    ## Rønne Nord
    bus_RNO_10 = pp.create_bus(net, vn_kv, name='Rønne Nord 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_RNO = pp.create_transformer(net, hv_bus = bus_RNO, lv_bus = bus_RNO_10, name='Rønne Nord Trf 1', std_type='Trf 10 MVA ek 7.94 er 0.58', in_service=True)
    # RNO_husstandsmoller = pp.create_sgen(net, bus_RNO_10, p_mw=2, q_mvar = 0, slack=True)
    # RNO_load = pp.create_load(net, bus_RNO_10,p_mw=0.866, q_mvar=0.58)

    target_substation = "RNO"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        RNS_generated = pp.create_gen(net, bus_RNO_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        RNS_consumed = pp.create_load(net, bus_RNO_10,p_mw=active_power, q_mvar=reactive_power)

    # target_substation = "Rønne Nord"
    # substation_data = measurements[measurements['Substation'] == target_substation]
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]

    # RNO_husstandsmoller = pp.create_sgen(net, bus_RNO_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # RNO_load = pp.create_load(net, bus_RNO_10,p_mw=consumption, q_mvar=0)

    ## Poulsker
    bus_POU_10 = pp.create_bus(net, vn_kv, name='Poulsker 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_POU = pp.create_transformer(net, hv_bus = bus_POU, lv_bus = bus_POU_10, name='Poulsker Trf 1', std_type='Trf 10 MVA ek 8.14 er 0.59', in_service=True)
    # POU_husstandsmoller = pp.create_sgen(net, bus_POU_10, p_mw=2, q_mvar = 0, slack=True)
    # POU_load = pp.create_load(net, bus_POU_10,p_mw=0.405, q_mvar=-0.546)

    target_substation = "Povlsker"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        POU_generated = pp.create_gen(net, bus_POU_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        POU_consumed = pp.create_load(net, bus_POU_10,p_mw=active_power, q_mvar=reactive_power)

    # target_substation = "Povlsker"
    # substation_data = measurements[measurements['Substation'] == target_substation]
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]

    # POU_husstandsmoller = pp.create_sgen(net, bus_POU_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # POU_load = pp.create_load(net, bus_POU_10,p_mw=consumption, q_mvar=0)

    ## Vesthavnen
    bus_VES_10 = pp.create_bus(net, vn_kv, name='Vesthavnen 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_VES = pp.create_transformer(net, hv_bus = bus_VES, lv_bus = bus_VES_10, name='Vesthavnen Trf 1', std_type='Trf 10 MVA ek 8.1 er 0.54', in_service=True)

    target_substation = "Vesthavnen"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        VES_generated = pp.create_gen(net, bus_VES_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        VES_consumed = pp.create_load(net, bus_VES_10,p_mw=active_power, q_mvar=reactive_power)

    # target_substation = "Vesthavnen"
    # substation_data = measurements[measurements['Substation'] == target_substation]
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]

    # VES_husstandsmoller = pp.create_sgen(net, bus_VES_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # VES_load = pp.create_load(net, bus_VES_10,p_mw=consumption, q_mvar=0)

    ## Gudhjem
    bus_GUD_10 = pp.create_bus(net, vn_kv, name='Gudhjem 10 kV', index=None, geodata=None, type='b', zone=None, in_service=True, max_vm_pu=max_vm_pu, min_vm_pu=min_vm_pu)
    trafo_GUD = pp.create_transformer(net, hv_bus = bus_GUD, lv_bus = bus_GUD_10, name='Gudhjem Trf 1', std_type='Trf 4 MVA ek 7.3 er 0.3 N.2', in_service=True)
    # GUD_husstandsmoller = pp.create_sgen(net, bus_GUD_10, p_mw=2, q_mvar = 0, slack=True)
    # GUD_load = pp.create_load(net, bus_GUD_10,p_mw=0.608, q_mvar=-0.143)

    target_substation = "Gudhjem"
    substation_data = measurements[measurements['Substation'] == target_substation]
    active_power = substation_data['Active Power'].values[0]
    reactive_power = substation_data['Reactive Power'].values[0]
    
    if active_power < 0:
        GUD_generated = pp.create_gen(net, bus_GUD_10, p_mw=active_power, q_mvar=reactive_power, slack=True)
    else:
        GUD_consumed = pp.create_load(net, bus_GUD_10,p_mw=active_power, q_mvar=reactive_power)
    # target_substation = "Gudhjem"
    # substation_data = measurements[measurements['Substation'] == target_substation]
    # consumption = substation_data['Consumption'].values[0]
    # production = substation_data['Production'].values[0]



    # GUD_husstandsmoller = pp.create_sgen(net, bus_GUD_10, p_mw=-1*production, q_mvar = 0, slack=True)
    # GUD_load = pp.create_load(net, bus_GUD_10,p_mw=consumption, q_mvar=0)


    return net




