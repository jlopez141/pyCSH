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


shape_read = (2,2,2)
brick_code = { 
(  0,   0,   0)  :   ['<L', '<R', 'CII', 'CID', 'oDL', 'oDR', 'oUL', '>L', 'CD', '>R'], 
(  0,   0,   1)  :   ['<L', 'CU', 'oMUL', '<R', 'XU', 'XD', 'CID', 'CIU', 'oDL', 'oUL', 'oXU', 'oXD', '>L', 'SD', '>R'], 
(  0,   1,   0)  :   ['<L', 'CU', '<Ro', 'XU', 'CIU', 'oUR', 'oXU', '>L', '>R'], 
(  0,   1,   1)  :   ['<Lo', 'CU', 'oMUL', '<R', 'CID', '>L', 'CD', 'oMDL', '>R'], 
(  1,   0,   0)  :   ['<L', 'CU', 'oMUL', '<R', 'CII', 'XU', 'XD', 'CID', 'oDL', 'oUR', 'oXU', 'oXD', '>L', 'SD', 'oMDL', '>R'], 
(  1,   0,   1)  :   ['<Lo', 'CU', 'oMUL', '<R', 'XU', 'oDL', 'oUR', 'oXU', '>L', 'CD', '>R'], 
(  1,   1,   0)  :   ['<L', 'CU', '<R', 'XU', 'XD', 'oXU', 'oXD', '>L', '>R'], 
(  1,   1,   1)  :   ['<L', 'SU', 'oMUL', '<R', 'CII', 'XU', 'XD', 'CIU', 'oDL', 'oDR', 'oXU', 'oXD', '>L', 'CD', 'oMDL', 'oMDL', '>R'], 
}
water_code = { 
(  0,   0,  0)  :   ['wIL', 'wMUR', 'wXU', 'wMUL', 'wMDL'], 
(  0,   0,  1)  :   ['wMUR', 'wMDL', 'wMDR', 'wIL', 'wIR2'], 
(  0,   1,  0)  :   ['wXD', 'wDR', 'wIR2', 'wMUR', 'wMUL'], 
(  0,   1,  1)  :   ['wXD', 'wIR2', 'wXU', 'wMDR', 'wDR'], 
(  1,   0,  0)  :   ['wMUR', 'wUL', 'wMDR', 'wIR2', 'wIL'], 
(  1,   0,  1)  :   ['wIL', 'wMUR', 'wUL', 'wMDL', 'wMDR'], 
(  1,   1,  0)  :   ['wMUR', 'wIL', 'wMDL', 'wDR'], 
(  1,   1,  1)  :   ['wMUR', 'wIL', 'wIR2', 'wMDR'], 
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