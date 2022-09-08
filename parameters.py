seed = 1123
shape = (2,2,1)   # Minimum (1,1,1)
Ca_Si_ratio = 1.25
W_Si_ratio  = 0.8

N_samples = 50
make_independent = True

random_water = True


offset_gaussian = True
width_Ca_Si = 0.1
width_SiOH = 0.08
width_CaOH = 0.04

create = True
check = False


write_lammps = True
write_vasp = True
write_siesta = False




# The input below allows to read a handmade brick code
# If NOT using a surface, remove "surface_separation", or set it to "surface_separation = False"

# Use "surface_from_bulk" to read a handmade code and transform it to a surface
# by adding upper (">Lo", ">Ro") and lower ("<Lo", "<Ro") chains


read_structure = False

surface_from_bulk = False
surface_separation = False


shape_read = (1, 1, 1)
brick_code = { 
(  0,   0,   0)  :   ['<Lo', 'CU', 'oMUL', 'oMUR', '<Ro', 'CII', 'XU', 'XD', 'oDL', 'oUL', 'oXU', 'oXD', '>L', 'SD', '>R'],
}

water_code = { 
(  0,   0,  0)  :   [], 
}

# shape_read = (1,1,)
# brick_code = { 
# (  0,   0,   0)  :   ['<Lo', 'CU', 'oMUL', 'oMUR', '<Ro'], 
# (  0,   0,   1)  :   ['<L', 'SUo', '<R', 'CII', '>L', 'SDo', '>R'], 
# (  0,   0 ,  2)  :   ['<L', 'SUo', '<R', 'CII', '>L', 'SDo', '>R'], 
# (  0,   0 ,  3)  :   ['>Lo', '>Ro'], 
# }
# water_code = { 
# (  0  , 0 ,  0)  :   [], 
# (  0  , 0 ,  1)  :   [], 
# (  0 ,  0,   2)  :   [], 
# (  0 ,  0  , 3)  :   [], 
# }
