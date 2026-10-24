""" 
Steady-State Heat Transfer Analysis - Winter External Thermal Load 
Case Study A) Traditional Thermostat vs. Human-Centered AI Control 
""" 
import sys 
# Set up the path to the PMV calculation 
cale_functie_calcul = r"D:\2_Occupants Comfort and Health\App2.2_PMV-PPD" 
sys.path.append(cale_functie_calcul) 
from Calcul_PMV_PPD import calculate_pmv_ppd 
import pandas as pd 
# ========================================== 
# 1. BOUNDARY CONDITIONS & GEOMETRY 
# ========================================== 
t_E = 5.0           
# Exterior air temperature [°C] 
t_I = 24.0          
t_I_beside=t_I      
t_soil = 11.0       
# Indoor air temperature [°C] 
# Indoor air temperature of the beside rooms [°C] 
# Average soil temperature [°C] (Assumption 10-12°C range) 
# 1.1. Fixed parameters for the winter scenario 
CLO = 1.0       # Winter clothing (e.g., sweater) 
MET = 1.2       # Office work 
v_AIR = 0.1     # Low air velocity (no drafts) 
RH = 40.0       # Typical winter indoor humidity 
t_mr = t_I-2      
# The mean radiant temperature 
# 1.2 WALL 
# Wall geometry 
A_wall_gross = 4 * (3 * 6)  # 4 walls of 3m x 6m [m2] 
A_win_east = 1.0 * 2.0      # East window [m2] 
A_win_south = 1.0 * 2.0     # South window [m2] 
A_win_total = A_win_east + A_win_south 
A_wall_net = A_wall_gross - A_win_total  # Opaque wall area [m2] 
# Wall structure properties (from outside to inside) 
wall_layer = { 
"Layer": ["decorative plaster", "polystyrene EPS", "mortar exterior", "ACC", "mortar interior"], 
"delta_m": [0.005, 0.100, 0.003, 0.250, 0.002], 
"lambda_W_mK": [0.024, 0.040, 0.870, 0.150, 0.870] 
} 
# Data array (DataFrame) 
df_wall = pd.DataFrame(wall_layer) 
# 1.3. FLOOR 
# Floor geometry (derived from four 3x4 walls, yielding a 6x6 plan) 
A_floor = 6.0 * 6.0  # [m2] 
Human centered AI for energy management  
Camelia STANCIU, Iuliana ŞORIGA - POLITEHNICA Bucharest – IAI Master 
# Floor structure properties (from interior down to deep soil) 
floor_layer = { 
"Layer": ["hardwood", "cement screed", "polystyrene XPS", "reinforced concrete", "gravel", 
"soil_3m", "soil_7m"], 
"delta_m": [0.02, 0.05, 0.1, 0.2, 0.2, 2.43, 4], 
"lambda_W_mK": [0.23, 0.93, 0.025, 2.03, 0.7, 2, 4] 
} 
# Data array (DataFrame) 
df_floor = pd.DataFrame(floor_layer) 
# 1.4. CEILING (from interior towards upper floor) 
A_ceiling=A_floor 
ceiling_layer = { 
"Layer": ["mortar interior", "reinforced concrete", "cement screed", "hardwood"], 
"delta_m": [0.002, 0.20, 0.05, 0.02], 
"lambda_W_mK": [0.87, 2.03, 0.93, 0.23] 
} 
# Data array (DataFrame) 
df_ceiling = pd.DataFrame(ceiling_layer) 
# 1.5. WINDOWS 
# Windows properties 
c1, c2, c3 = 0.9, 0.6, 0.6 
window_coef = c1 * c2 * c3 
k_win = 2.56 
# East Window (m=0.3, I_T=55 W/m2) 
m_win_east=0.3 
I_T_east=55 
# South Window (m=0.7, I_T=380 W/m2) 
m_win_south=0.7 
I_T_south=380 
# 1.6. Convection coefficients [W/(m2K)] 
alpha_e = 24.0       
# Exterior convection 
alpha_i_wall = 8.0   # Interior convection (walls) 
alpha_i_floor = 6.0  # Interior convection (heated floor side) 
# ========================================== 
# 2. THERMAL RESISTANCE CALCULATIONS 
# ========================================== 
# 2.1. Wall heat transfer (convection + conduction + convection) 
# ------------------------------------------------- 
# 2.1.1 Insulated wall 
R_si_wall = 1 / alpha_i_wall 
R_se_wall = 1 / alpha_e 
Human centered AI for energy management  
Camelia STANCIU, Iuliana ŞORIGA - POLITEHNICA Bucharest – IAI Master 
# Wall conduction specific thermal resistances R = thickness(m)/lambda(W/mK) 
# (computed once for all layers, in the wall properties array, adding a new column denoted R) 
df_wall["R_m2K_W"] = df_wall["delta_m"] / df_wall["lambda_W_mK"] 
# Compute sum of layers conduction thermal resistances directly from R column 
R_wall_cd = df_wall["R_m2K_W"].sum() 
# Add R_si and R_se 
R_wall_ins = R_si_wall + R_wall_cd + R_se_wall 
k_wall_ins = 1 / R_wall_ins