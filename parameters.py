seed = 1123
shape = (2, 2, 2)   # Minimum (1,1,1)
Ca_Si_ratio = 1.75
W_Si_ratio  = 1.0

N_samples = 100
make_independent = True


offset_gaussian = False
width_Ca_Si = 0.05
width_SiOH = 0.08
width_CaOH = 0.04

create = True
check = True


write_lammps = True
write_vasp = True
write_siesta = False





read_from_file = True
input_file = "pruebas.log"


shape_read = (1, 1, 4)
surface_separation = 20.0
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