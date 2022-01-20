from mod_construct_brick import *
from mod_sample import *
from mod_construct_supercell import *
from mod_write import *
from mod_check import *
from parameters import *
from mod_make_graphs import *
import os

# Check input parameters:
glob = blobals()
if seed not in glob:
	seed = 1123


np.random.seed(seed)


mypath = os.path.abspath(".")
path = os.path.join(mypath, "output/")


if create or check:
	# Get all possible bricks
	sorted_bricks = get_all_bricks(pieces)


if create or read_from_file:
	if not os.path.isdir("./output"):
		os.makedirs('./output')


list_properties = []

if create:
	N_brick = shape[0]*shape[1]*shape[2]
	for isample in range(N_samples):
		crystal, N_Ca, N_Si, r_SiOH, r_CaOH, MCL = sample_Ca_Si_ratio(sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick )

		N_water = int(np.rint(N_Si * W_Si_ratio))

		fmt = "Sample: {: 5d}     Ca/Si: {: 8.6f}     SiOH/Si: {: 8.6f}    CaOH/Ca: {: 8.6f}    MCL: {: 8.6f}"
		#print( fmt.format(isample+1, N_Ca/N_Si, r_SiOH, r_CaOH, MCL))

		list_properties.append( [N_Ca/N_Si, r_SiOH, r_CaOH, MCL, isample+1] )

		water_in_crystal = fill_water(crystal, N_water = N_water)
		crystal_rs, water_in_crystal_rs =  reshape_crystal(crystal, water_in_crystal, shape)
		entries_crystal, entries_bonds, crystal_dict, water_dict = get_full_coordinates( crystal_rs, water_in_crystal_rs, shape, pieces )

		entries_angle = get_angles(crystal_dict, water_dict, shape)

		if write_lammps:
			name = "input"+str(isample+1)+".data"
			name = os.path.join(path, name)
			get_lammps_input(name, entries_crystal, entries_bonds, entries_angle, shape) 

		name = "input"+str(isample+1)+".log"
		name = os.path.join(path, name)
		get_log(name, shape, crystal_rs, water_in_crystal_rs, N_Ca, N_Si, r_SiOH, r_CaOH, MCL )

		if write_vasp:
			name = "input"+str(isample+1)+".vasp"
			name = os.path.join(path, name)
			get_vasp_input(name, entries_crystal, shape)

		if write_siesta:
			name = "input"+str(isample+1)+".fdf"
			name = os.path.join(path, name)
			get_siesta_input(name, entries_crystal, shape)


	list_properties = np.array(list_properties)	
	plot_XOH_X(list_properties)
	plot_distributions(list_properties)

	get_sorted_log(list_properties)


if check:
	check_SiOH_CaOH_MCL(sorted_bricks, shape)
	plot_experimental()



if read_from_file:
	shape, crystal_rs, water_in_crystal_rs, N_Si, N_Ca, r_SiOH, r_CaOH, MCL = read_brick(input_file, pieces)
	entries_crystal, entries_bonds, crystal_dict, water_dict = get_full_coordinates( crystal_rs, water_in_crystal_rs, shape, pieces )

	entries_angle = get_angles(crystal_dict, water_dict, shape)

	name = "input_fromManualCode.data"
	name = os.path.join(path, name)
	get_lammps_input(name, entries_crystal, entries_bonds, entries_angle, shape) 
	name = "input_fromManualCode.log"
	name = os.path.join(path, name)
	get_log(name, shape, crystal_rs, water_in_crystal_rs, N_Ca, N_Si, r_SiOH, r_CaOH, MCL )

	name = "input_fromManualCode.vasp"
	name = os.path.join(path, name)
	get_vasp_input(name, entries_crystal, shape)

	name = "input_fromManualCode.fdf"
	name = os.path.join(path, name)
	get_siesta_input(name, entries_crystal, shape)