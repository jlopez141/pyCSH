seed = 1123
shape = (2,2,2)   # Minimum (1,1,1)
Ca_Si_ratio = 1.75
W_Si_ratio  = 1.1

N_samples = 100
make_independent = True


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


read_structure = True

surface_from_bulk = True
surface_separation = False #20.0


shape_read = (1, 1, 1)
brick_code = { 
(  0,   0,   0)  :   ['<L', 'SUo', '<R', 'CII', '>L', 'SDo', '>R'],
}

water_code = { 
(  0,   0,  0)  :   [], 
}

#shape_read = (1,1,4)
# brick_code = { 
# (  0,   0,   0)  :   ['<Lo', '<Ro'], 
# (  0,   0,   1)  :   ['<L', 'SUo', '<R', 'CII', '>L', 'SDo', '>R'], 
# (  0,   0 ,  2)  :   ['<L', 'SUo', '<R', 'CII', '>L', 'SDo', '>R'], 
# (  0,   0 ,  3)  :   ['>L', '>R'], 
# }
# water_code = { 
# (  0  , 0 ,  0)  :   [], 
# (  0  , 0 ,  1)  :   [], 
# (  0 ,  0,   2)  :   [], 
# (  0 ,  0  , 3)  :   [], 
# }