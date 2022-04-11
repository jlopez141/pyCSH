seed = 1123
shape = (2,2,2)   # Minimum (1,1,1)
Ca_Si_ratio = 1.9
W_Si_ratio  = 1.4

N_samples = 200
make_independent = True


offset_gaussian = True
width_Ca_Si = 0.05
width_SiOH = 0.08
width_CaOH = 0.04

create = True
check = False


write_lammps = False
write_vasp = True
write_siesta = False




# The input below allows to read a handmade brick code
# If NOT using a surface, remove "surface_separation", or set it to "surface_separation = False"

# Use "surface_from_bulk" to read a handmade code and transform it to a surface
# by adding upper (">Lo", ">Ro") and lower ("<Lo", "<Ro") chains


read_structure = False

surface_from_bulk = False
surface_separation = False


shape_read = (2,2,2)
brick_code = { 
(  0,   0,   0)  :   ['<L', 'CU', 'oMUL', 'oMUR', '<R', 'CII', 'XU', 'XD', 'CIU', 'oDL', 'oXU', 'oXD', '>L', 'SD', '>R'], 
(  0,   0,   1)  :   ['<Lo', 'CU', 'oMUL', 'oMUR', '<Ro', 'CII', 'XU', 'XD', 'oDL', 'oUL', 'oXU', 'oXD', '>L', 'SD', '>R'], 
(  0,   1,   0)  :   ['<L', 'CU', '<R', 'XU', 'oUL', 'oXU', '>L', 'CD', 'oMDL', '>R'], 
(  0,   1,   1)  :   ['<L', 'SU', '<R', 'XU', 'XD', 'CID', 'oDR', 'oUR', 'oXU', 'oXD', '>L', 'CD', 'oMDL', 'oMDR', '>Ro'], 
(  1,   0,   0)  :   ['<L', 'SU', '<R', 'CII', 'XU', 'CID', 'CIU', 'oDL', 'oXU', '>L', '>R'], 
(  1,   0,   1)  :   ['<L', 'SU', '<R', 'CII', 'XU', 'XD', 'CIU', 'oDL', 'oDR', 'oUR', 'oXU', 'oXD', '>L', 'CD', 'oMDL', 'oMDR', '>R'], 
(  1,   1,   0)  :   ['<L', 'CU', 'oMUR', '<R', 'XU', 'oXU', '>L', 'CD', 'oMDL', '>R'], 
(  1,   1,   1)  :   ['<L', 'SU', 'oMUL', '<R', 'CII', 'XU', 'XD', 'CID', 'oDR', 'oXU', 'oXD', '>L', 'CD', 'oMDR', '>R'], 
}

water_code = { 
(  0,   0,  0)  :   ['wIL', 'wUL', 'wIR2', 'wIR', 'wMDL'], 
(  0,   0,  1)  :   ['wMDL', 'wIR2', 'wIL', 'wIR'], 
(  0,   1,  0)  :   ['wIR', 'wXD', 'wMUR', 'wIR2', 'wMUL', 'wDR', 'wIL'], 
(  0,   1,  1)  :   ['wIR2', 'wMUL', 'wIL'], 
(  1,   0,  0)  :   ['wMUL', 'wIR2', 'wXD', 'wIL', 'wIR', 'wDR'], 
(  1,   0,  1)  :   ['wIR2', 'wMUL', 'wIL'], 
(  1,   1,  0)  :   ['wUL', 'wMDR', 'wIL', 'wIR', 'wIR2', 'wXD'], 
(  1,   1,  1)  :   ['wIR2', 'wMDL', 'wIL', 'wIR'], 
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