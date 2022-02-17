from mod_construct_brick import *
from mod_sample import *
from mod_construct_supercell import *
from mod_write import *
from mod_check import *
from parameters import *
from mod_make_graphs import *


# Check input parameters:
try: seed
except NameError: seed = 1123

try: width_Ca_Si
except NameError: width_Ca_Si = 0.1

try: width_SiOH
except NameError: width_SiOH = 0.08

try: width_CaOH
except NameError: width_CaOH = 0.04

try: offset_gaussian
except NameError: offset_gaussian = False

try: make_independent
except NameError: make_independent = False

try: create
except NameError: create = False

try: check
except NameError: check = False

try: write_lammps
except NameError: write_lammps = True

try: write_vasp
except NameError: write_vasp = False

try: write_siesta
except NameError: write_siesta = False

try: read_structure
except NameError: read_structure = False

try: surface_separation
except NameError: surface_separation = False



widths = [width_Ca_Si, width_SiOH, width_CaOH]


np.random.seed(seed)





if create or check:
	# Get all possible bricks
	sorted_bricks = get_all_bricks(pieces)


if create or read_structure:
	if not os.path.isdir("./output"):
		os.makedirs('./output')


list_properties = []

if create:

	unitcell = np.array([ [6.7352,    0.0 ,      0.0],
				 		   [-4.071295, 6.209521,  0.0],
						   [0.7037701, -6.2095578, 13.9936836] ])

	supercell = np.zeros((3,3))
	for i in range(3):
		supercell[i,:] = unitcell[i,:]*shape[i]



	N_brick = shape[0]*shape[1]*shape[2]

	offset = [0.0, 0.0]
	if offset_gaussian:
		off_Si, off_Ca = get_offset(500, sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths)
		offset = [off_Si, off_Ca]


	list_crystals = []
	cont = 0



	for isample in range(N_samples):
		crystal, N_Ca, N_Si, r_SiOH, r_CaOH, MCL, N_water, r_2H_Si = sample_Ca_Si_ratio(
													sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths, offset=offset )


		crystal_index = [ brick.ind for brick in crystal ] 

		new = False

		if make_independent and set(crystal_index) not in list_crystals:
			new = True
			list_crystals.append(set(crystal_index))
		elif not make_independent and crystal_index not in list_crystals:
			new = True
			list_crystals.append(crystal_index)

		if new:
			list_properties.append( [N_Ca/N_Si, r_SiOH, r_CaOH, MCL, isample+1, r_2H_Si] )

			water_in_crystal = fill_water(crystal, N_water = N_water)
			crystal_rs, water_in_crystal_rs =  reshape_crystal(crystal, water_in_crystal, shape)
			entries_crystal, entries_bonds, crystal_dict, water_dict = get_full_coordinates( crystal_rs, water_in_crystal_rs, shape, pieces )

			entries_angle = get_angles(crystal_dict, water_dict, shape)

			write_output( isample, entries_crystal, entries_bonds, entries_angle, shape, crystal_rs, water_in_crystal_rs,
					 	  supercell, N_Ca, N_Si, r_SiOH, r_CaOH, MCL, write_lammps, write_vasp, write_siesta)


	list_properties = np.array(list_properties)	
	plot_XOH_X(list_properties)
	plot_MCL(list_properties)
	plot_distributions(list_properties)
	plot_water(list_properties)

	get_sorted_log(list_properties)



if check:
	check_SiOH_CaOH_MCL(sorted_bricks, widths, shape)
	plot_experimental()





if read_structure:

	shape, crystal_rs, water_in_crystal_rs, N_Si, N_Ca, r_SiOH, r_CaOH, MCL = read_brick(shape_read, brick_code, water_code, pieces, surface_from_bulk)
	
	entries_crystal, entries_bonds, crystal_dict, water_dict = get_full_coordinates( crystal_rs, water_in_crystal_rs, shape, pieces )

	entries_angle = get_angles(crystal_dict, water_dict, shape)



	unitcell = np.array([ [6.7352,    0.0 ,      0.0],
				 		   [-4.071295, 6.209521,  0.0],
						   [0.7037701, -6.2095578, 13.9936836] ])

	supercell = np.zeros((3,3))
	for i in range(3):
		supercell[i,:] = unitcell[i,:]*shape[i]


	if surface_separation:
		entries_crystal, supercell = transform_surface_separation(entries_crystal, supercell, unitcell, surface_separation)		

	mypath = os.path.abspath(".")
	path = os.path.join(mypath, "output/")

	name = "input_fromManualCode.data"
	name = os.path.join(path, name)
	get_lammps_input(name, entries_crystal, entries_bonds, entries_angle, supercell) 
	name = "input_fromManualCode.log"
	name = os.path.join(path, name)
	get_log(name, shape, crystal_rs, water_in_crystal_rs, N_Ca, N_Si, r_SiOH, r_CaOH, MCL )

	name = "input_fromManualCode.vasp"
	name = os.path.join(path, name)
	get_vasp_input(name, entries_crystal, supercell)

	name = "input_fromManualCode.fdf"
	name = os.path.join(path, name)
	get_siesta_input(name, entries_crystal, supercell)