seed = 1123
shape = (2, 2, 2)   # Minimum (1,1,1)
Ca_Si_ratio = 1.75
W_Si_ratio  = 1.1

N_samples = 100
make_independent = True


offset_gaussian = False
width_Ca_Si = 0.1
width_SiOH = 0.08
width_CaOH = 0.04

create = True
check = True


write_lammps = True
write_vasp = True
write_siesta = False




# The input below allows to read a handmade brick code
# If NOT using a surface, remove "surface_separation", or set it to "surface_separation = False"

read_structure = True

shape_read = (1, 1, 4)
surface_separation = 1.0
brick_code = { 
(  0,   0,   0)  :   ['<Lo', '<Ro'], 
(  0,   0,   1)  :   ['<L', 'SUo', '<R', 'CII', '>L', 'SDo', '>R'], 
(  0,   0 ,  2)  :   ['<L', 'SUo', '<R', 'CII', '>L', 'SDo', '>R'], 
(  0,   0 ,  3)  :   ['>L', '>R'], 
}
water_code = { 
(  0  , 0 ,  0)  :   [], 
(  0  , 0 ,  1)  :   [], 
(  0 ,  0,   2)  :   [], 
(  0 ,  0  , 3)  :   [], 
}
