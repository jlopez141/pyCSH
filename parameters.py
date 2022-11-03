seed = 23137
shape = (4,4,2)   # Minimum (1,1,1)
Ca_Si_ratio = 1.5
W_Si_ratio  = 1.0

prefix = "CaSi1.5"

N_samples = 10
make_independent = True


offset_gaussian = False
width_Ca_Si = 0.01
width_SiOH = 0.05
width_CaOH = 0.05

create =True
check = False


write_lammps = False
write_lammps_erica = True
write_vasp = True
write_siesta = False




# The input below allows to read a handmade brick code
# If NOT using a surface, remove "surface_separation", or set it to "surface_separation = False"

# Use "surface_from_bulk" to read a handmade code and transform it to a surface
# by adding upper (">Lo", ">Ro") and lower ("<Lo", "<Ro") chains


read_structure = False

surface_from_bulk = False
surface_separation = False


# shape_read = (2,2,2)
# brick_code = { 
# (  0,   0,   0)  :   ['<L', 'CU', 'oMUL', 'oMUR', '<R', 'CII', 'XU', 'XD', 'CIU', 'oDL', 'oXU', 'oXD', '>L', 'SD', '>R'], 
# (  0,   0,   1)  :   ['<Lo', 'CU', 'oMUL', 'oMUR', '<Ro', 'CII', 'XU', 'XD', 'oDL', 'oUL', 'oXU', 'oXD', '>L', 'SD', '>R'], 
# (  0,   1,   0)  :   ['<L', 'CU', '<R', 'XU', 'oUL', 'oXU', '>L', 'CD', 'oMDL', '>R'], 
# (  0,   1,   1)  :   ['<L', 'SU', '<R', 'XU', 'XD', 'CID', 'oDR', 'oUR', 'oXU', 'oXD', '>L', 'CD', 'oMDL', 'oMDR', '>Ro'], 
# (  1,   0,   0)  :   ['<L', 'SU', '<R', 'CII', 'XU', 'CID', 'CIU', 'oDL', 'oXU', '>L', '>R'], 
# (  1,   0,   1)  :   ['<L', 'SU', '<R', 'CII', 'XU', 'XD', 'CIU', 'oDL', 'oDR', 'oUR', 'oXU', 'oXD', '>L', 'CD', 'oMDL', 'oMDR', '>R'], 
# (  1,   1,   0)  :   ['<L', 'CU', 'oMUR', '<R', 'XU', 'oXU', '>L', 'CD', 'oMDL', '>R'], 
# (  1,   1,   1)  :   ['<L', 'SU', 'oMUL', '<R', 'CII', 'XU', 'XD', 'CID', 'oDR', 'oXU', 'oXD', '>L', 'CD', 'oMDR', '>R'], 
# }

# water_code = { 
# (  0,   0,  0)  :   ['wIL', 'wUL', 'wIR2', 'wIR', 'wMDL'], 
# (  0,   0,  1)  :   ['wMDL', 'wIR2', 'wIL', 'wIR'], 
# (  0,   1,  0)  :   ['wIR', 'wXD', 'wMUR', 'wIR2', 'wMUL', 'wDR', 'wIL'], 
# (  0,   1,  1)  :   ['wIR2', 'wMUL', 'wIL'], 
# (  1,   0,  0)  :   ['wMUL', 'wIR2', 'wXD', 'wIL', 'wIR', 'wDR'], 
# (  1,   0,  1)  :   ['wIR2', 'wMUL', 'wIL'], 
# (  1,   1,  0)  :   ['wUL', 'wMDR', 'wIL', 'wIR', 'wIR2', 'wXD'], 
# (  1,   1,  1)  :   ['wIR2', 'wMDL', 'wIL', 'wIR'], 
# }
 

shape_read = (3,3,2)
brick_code = { 
(  0,   0,   0)  :   ['<Lo', 'CU', '<R', '>L', 'CD', 'oMDR', '>R'], 
(  0,   0,   1)  :   ['<L', '<R', 'XD', 'CIU', 'oDL', '>Lo', '>R'], 
(  0,   1,   0)  :   ['<L', 'CU', '<R', 'XU', 'oUL', '>L', '>Ro'], 
(  0,   1,   1)  :   ['<L', '<R', 'XU', 'XD', 'oUL', 'oXU', '>Lo', '>R'], 
(  0,   2,   0)  :   ['<L', 'CU', '<R', 'CII', 'oDR', '>Lo', '>R'], 
(  0,   2,   1)  :   ['<Lo', 'CU', 'oMUL', '<R', 'XD', '>L', '>R'], 
(  1,   0,   0)  :   ['<L', 'SU', 'oMUL', '<R', 'CII', 'XU', 'XD', 'CID', 'CIU', 'oDL', 'oUR', 'oXU', '>L', 'SDo', 'oMDL', '>R'], 
(  1,   0,   1)  :   ['<L', '<R', 'XU', 'oDL', '>Lo', 'CD', '>R'], 
(  1,   1,   0)  :   ['<L', 'CU', '<R', '>L', 'CD', 'oMDR', '>R'], 
(  1,   1,   1)  :   ['<L', 'SUo', 'oMUL', '<R', 'CII', 'XU', 'XD', 'CID', 'CIU', 'oDL', 'oUR', 'oXU', '>L', 'SD', 'oMDL', '>R'], 
(  1,   2,   0)  :   ['<L', 'CU', '<R', 'CII', 'oDR', '>Lo', '>R'], 
(  1,   2,   1)  :   ['<Lo', 'CU', 'oMUL', '<R', 'XU', '>L', '>R'], 
(  2,   0,   0)  :   ['<Lo', '<R', 'XD', 'oUL', 'oXD', '>L', 'CD', '>R'], 
(  2,   0,   1)  :   ['<L', 'SU', 'oMUL', '<R', 'CII', 'XU', 'XD', 'CID', 'CIU', 'oDL', 'oUR', 'oXU', '>L', 'SD', 'oMDL', '>R'], 
(  2,   1,   0)  :   ['<Lo', '<R', 'XD', 'CIU', 'oDL', 'oUR', '>L', '>R'], 
(  2,   1,   1)  :   ['<Lo', '<R', 'XD', '>L', 'CD', 'oMDR', '>R'], 
(  2,   2,   0)  :   ['<L', 'CU', 'oMUL', 'oMUR', '<Ro', 'CID', '>L', '>R'], 
(  2,   2,   1)  :   ['<L', 'CU', '<R', 'CII', 'oDL', '>L', '>Ro'], 
}

water_code = { 
(  0,   0,  0)  :   ['wMDL', 'wXD', 'wUL', 'wIR2', 'wIR'], 
(  0,   0,  1)  :   ['wDR', 'wXD', 'wMDR', 'wMUR', 'w15'], 
(  0,   1,  0)  :   ['wMUR', 'wDR', 'wMUL', 'w15', 'wMDR'], 
(  0,   1,  1)  :   ['w16', 'wIR', 'w15', 'wIR2', 'wIL'], 
(  0,   2,  0)  :   ['wXD', 'wIR', 'w16', 'wMUL', 'wIR2'], 
(  0,   2,  1)  :   ['w14', 'wDR', 'wIL', 'wXD', 'wIR'], 
(  1,   0,  0)  :   ['wXD', 'w16', 'w15', 'wIL'], 
(  1,   0,  1)  :   ['wMDR', 'wIL', 'wIR2', 'wIR'], 
(  1,   1,  0)  :   ['wMUR', 'w15', 'wDR', 'w16'], 
(  1,   1,  1)  :   ['wIR2', 'w14', 'w15', 'wXD'], 
(  1,   2,  0)  :   ['wMDL', 'w16', 'wUL', 'wIR2'], 
(  1,   2,  1)  :   ['wIL', 'wXD', 'wIR', 'wMUR'], 
(  2,   0,  0)  :   ['wMDL', 'w14', 'wMUR', 'w15'], 
(  2,   0,  1)  :   ['w16', 'wIR2', 'w14', 'wIL'], 
(  2,   1,  0)  :   ['wXU', 'wMUL', 'wUL', 'w14'], 
(  2,   1,  1)  :   ['wIL', 'wMDL', 'w16', 'wXD'], 
(  2,   2,  0)  :   ['w16', 'w15', 'wXD', 'wIL'], 
(  2,   2,  1)  :   ['wMUR', 'wIR', 'wIL', 'wXD'], 
}

# shape_read = (3,3,1)
# brick_code = { 
# (  0,   0,   0)  :   ['<L', '<R', '>L', '>R'], 
# (  0,   1,   0)  :   ['<L', '<R', '>L', '>R'], 
# (  0,   2,   0)  :   ['<L', '<R', '>L', '>R'], 
# (  1,   0,   0)  :   ['<L', '<R', '>L', '>R'], 
# (  1,   1,   0)  :   ['<L', '<R', "SU", "oMUR" , '>L', '>R'], 
# (  1,   2,   0)  :   ['<L', '<R', '>L', '>R'], 
# (  2,   0,   0)  :   ['<L', '<R', '>L', '>R'], 
# (  2,   1,   0)  :   ['<L', '<R', '>L', '>R'], 
# (  2,   2,   0)  :   ['<L', '<R', '>L', '>R'], 
# }
# water_code = {
# (  0,   0,   0)  :   [], 
# (  0,   1,   0)  :   [], 
# (  0,   2,   0)  :   [], 
# (  1,   0,   0)  :   [], 
# (  1,   1,   0)  :   [], 
# (  1,   2,   0)  :   [], 
# (  2,   0,   0)  :   [], 
# (  2,   1,   0)  :   [], 
# (  2,   2,   0)  :   [], }

