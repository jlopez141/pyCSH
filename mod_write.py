import numpy as np
import os



def get_lammps_input(input_file, entries_crystal, entries_bonds, entries_angle, supercell):

	N_atom = len(entries_crystal)
	N_bond = len(entries_bonds)
	N_angle = len(entries_angle)

	with open(input_file, "w") as f:
		f.write( "Generated with Brickcode \n\n" )
		f.write( "{: 8d} atoms \n".format(N_atom) )
		f.write( "{: 8d} bonds \n".format(N_bond) )
		f.write( "{: 8d} angles \n".format(N_angle) )
		f.write( "{: 8d} atom types \n".format(8) )
		f.write( "{: 8d} bond types \n".format(3) )
		f.write( "{: 8d} angle types \n".format(3) )
		f.write( " \n" )
		f.write( "{: 12.6f} {: 12.6f} xlo xhi \n".format(0.0, supercell[0,0]) )
		f.write( "{: 12.6f} {: 12.6f} ylo yhi \n".format(0.0, supercell[1,1]) )
		f.write( "{: 12.6f} {: 12.6f} zlo zhi \n".format(0.0, supercell[2,2]) )
		f.write( "{: 12.6f} {: 12.6f} {: 12.6f} xy xz yz \n".format( supercell[1,0], supercell[2,0], supercell[2,1] ) )
		f.write( " \n" )
		f.write( "Masses \n" )
		f.write( " \n" )
		f.write( "1 40.08  #Ca  \n" )
		f.write( "2 28.10  #Si \n" )
		f.write( "3 15.79  #O \n" )
		f.write( "4 0.20   #O(S) \n" )
		f.write( "5 16.00  #Ow \n" )
		f.write( "6 16.00  #Oh \n" )
		f.write( "7 1.00   #Hw \n" )
		f.write( "8 1.00   #H \n" )
		f.write( " \n" )
		f.write( "Atoms \n" )
		f.write( " \n" )
		fmt = "{: 8d} {: 8d} {: 8d} {: 8.3f} {: 12.6f} {: 12.6f} {: 12.6f}\n"
		for i in entries_crystal:
			f.write( fmt.format(i[0], 1, *i[1:]) )
		f.write( " \n" )

		f.write( "Bonds \n" )
		f.write( " \n" )
		fmt = "{: 8d} {: 8d} {: 8d} {: 8d} \n"
		for i in entries_bonds:
			f.write( fmt.format(*i) )
		f.write( " \n" )

		f.write( "Angles \n" )
		f.write( " \n" )
		fmt = "{: 8d} {: 8d} {: 8d} {: 8d} {: 8d} \n"
		for i in entries_angle:
			f.write( fmt.format(*i) )





def get_vasp_input(name, entries_crystal, supercell):

	N_atoms_specie = np.zeros(6,dtype=int)

	coords = [ [] for i in range(8) ]

	coords_Ca = []
	coords_Si = []
	coords_O1 = []
	#coords_O2 = []
	coords_Ow = []
	coords_Oh = []
	coords_Hw = []
	coords_H = []

	for entry in entries_crystal:
		specie = entry[1]
		r = np.array( entry[3:] )

		if specie == 1:
			coords_Ca.append(r)
			N_atoms_specie[0] += 1
		elif specie == 2:
			coords_Si.append(r)
			N_atoms_specie[1] += 1
		elif specie == 3:
			coords_O1.append(r)
			N_atoms_specie[2] += 1
		elif specie == 5:
			coords_Ow.append(r)
			N_atoms_specie[3] += 1
		elif specie == 6:
			coords_O1.append(r)
			N_atoms_specie[2] += 1
		elif specie == 7:
			coords_Hw.append(r)
			N_atoms_specie[4] += 1
		elif specie == 8:
			coords_H.append(r)
			N_atoms_specie[5] += 1

		coords[  entry[1]-1 ].append( r )


	together = True
	if together:
		coords_O1 = coords_O1 + coords_Ow
		N_atoms_specie[2] += N_atoms_specie[3]
		N_atoms_specie[3] = 0
		coords_Ow = []

		coords_H = coords_H + coords_Hw
		N_atoms_specie[5] += N_atoms_specie[4]
		N_atoms_specie[4] = 0
		coords_Hw = []

	#print(np.sum(N_atoms_specie))

	#f.write( " \n" )
	with open( name, "w" ) as f:
		f.write( "kk \n" )
		f.write( "1.0 \n" )
		for i in supercell:
			f.write( "{: 12.6f} {: 12.6f} {: 12.6f} \n".format(*i) )
		f.write( "Ca  Si  O  Ow   Hw  H \n" )
		f.write( "{: 5d} {: 5d} {: 5d} {: 5d} {: 5d} {: 5d} \n".format(*N_atoms_specie) )
		f.write("Cartesian\n")
		fmt = "{: 12.6f} {: 12.6f} {: 12.6f} \n"
		
		# for i in range(8):
		# #for i in [4, 6]:
		# 	for j in coords[i]:
		# 		f.write( fmt.format(*j) )

		for i in coords_Ca:
			f.write( fmt.format(*i) )
		for i in coords_Si:
			f.write( fmt.format(*i) )
		for i in coords_O1:
			f.write( fmt.format(*i) )
		for i in coords_Ow:
			f.write( fmt.format(*i) )
		for i in coords_Oh:
			f.write( fmt.format(*i) )
		for i in coords_Hw:
			f.write( fmt.format(*i) )
		for i in coords_H:
			f.write( fmt.format(*i) )


def get_xyz_input(name, entries_crystal, supercell):

	N_atoms_specie = np.zeros(6,dtype=int)

	coords = [ [] for i in range(8) ]

	coords_Ca = []
	coords_Si = []
	coords_O1 = []
	#coords_O2 = []
	coords_Ow = []
	coords_Oh = []
	coords_Hw = []
	coords_H = []

	for entry in entries_crystal:
		specie = entry[1]
		r = np.array( entry[3:] )

		if specie == 1:
			coords_Ca.append(r)
			N_atoms_specie[0] += 1
		elif specie == 2:
			coords_Si.append(r)
			N_atoms_specie[1] += 1
		elif specie == 3:
			coords_O1.append(r)
			N_atoms_specie[2] += 1
		elif specie == 5:
			coords_Ow.append(r)
			N_atoms_specie[3] += 1
		elif specie == 6:
			coords_O1.append(r)
			N_atoms_specie[2] += 1
		elif specie == 7:
			coords_Hw.append(r)
			N_atoms_specie[4] += 1
		elif specie == 8:
			coords_H.append(r)
			N_atoms_specie[5] += 1

		coords[  entry[1]-1 ].append( r )


	together = True
	if together:
		coords_O1 = coords_O1 + coords_Ow
		N_atoms_specie[2] += N_atoms_specie[3]
		N_atoms_specie[3] = 0
		coords_Ow = []

		coords_H = coords_H + coords_Hw
		N_atoms_specie[5] += N_atoms_specie[4]
		N_atoms_specie[4] = 0
		coords_Hw = []


	#f.write( " \n" )
	with open( name, "w" ) as f:
		f.write( "{: 12d} \n".format(np.sum(N_atoms_specie)) )
		fmt = "{:} {: 12.6f} {: 12.6f} {: 12.6f} \n"
		
		# for i in range(8):
		# #for i in [4, 6]:
		# 	for j in coords[i]:
		# 		f.write( fmt.format(*j) )

		for i in coords_Ca:
			f.write( fmt.format("Ca", *i) )
		for i in coords_Si:
			f.write( fmt.format("Si", *i) )
		for i in coords_O1:
			f.write( fmt.format("O",*i) )
		for i in coords_Ow:
			f.write( fmt.format("O",*i) )
		for i in coords_Oh:
			f.write( fmt.format("O", *i) )
		for i in coords_Hw:
			f.write( fmt.format("H",*i) )
		for i in coords_H:
			f.write( fmt.format("H",*i) )


def get_log(log_file, shape, crystal_rs, water_in_crystal_rs, N_Ca, N_Si, r_SiOH, r_CaOH, MCL ):

	N_Oh = 0
	for i in range(shape[0]):
		for j in range(shape[1]):
			for k in range(shape[2]):
				N_Oh+= crystal_rs[i,j,k].N_Oh

	with open(log_file, "w") as f:
		f.write( "Ca/Si ratio:   {: 8.6f} \n".format(N_Ca/N_Si) )
		f.write( "SiOH/Si ratio: {: 8.6f} \n".format(r_SiOH) )
		f.write( "CaOH/Ca ratio: {: 8.6f} \n".format(r_CaOH) )
		f.write( "MCL:           {: 8.6f} \n".format(MCL) )
		f.write( " \n" )
		f.write( "Shape: {: 3d} {: 3d} {: 3d} \n".format(*shape) )
		f.write( " \n" )
		f.write( "Supecell Brick Code: \n" )
		f.write( " Na  Nb  Nc  :   Brick Code \n\n" )
		f.write( "brick_code = { \n" )
		for i in range(shape[0]):
			for j in range(shape[1]):
				for k in range(shape[2]):
					f.write( "({: 3d}, {: 3d}, {: 3d})  :   {:}, \n".format(i, j, k, crystal_rs[i,j, k].comb) )
		f.write("}\n\n")
		f.write( "water_code = { \n" )
		for i in range(shape[0]):
			for j in range(shape[1]):
				for k in range(shape[2]):
					f.write( "({: 3d}, {: 3d},{: 3d})  :   {:}, \n".format(i, j, k, water_in_crystal_rs[i,j, k]) )
		f.write("}\n")

		f.write( " \n" )
		f.write( "Charge Distribution: \n" )
		for i in range(shape[0]):
			for j in range(shape[1]):
				for k in range(shape[2]):

					f.write( "{: 3d} {: 3d} {: 3d}  :   {:} \n".format(i, j, k, crystal_rs[i,j, k].charge) )




def get_siesta_input(name, entries_crystal, supercell):

	N_atoms_specie = np.zeros(4,dtype=int)

	coords_Ca = []
	coords_Si = []
	coords_O = []
	coords_H = []



	for entry in entries_crystal:
		specie = entry[1]
		r = np.array( entry[3:] )
		#r = apply_PBC(r, cell, cell_inv)

		if specie == 1:
			coords_Ca.append(r)
			N_atoms_specie[0] += 1
		elif specie == 2:
			coords_Si.append(r)
			N_atoms_specie[1] += 1
		elif specie in [3, 5, 6]:
			coords_O.append(r)
			N_atoms_specie[2] += 1
		elif specie in [7, 8]:
			coords_H.append(r)
			N_atoms_specie[3] += 1




	#f.write( " \n" )
	with open( name, "w" ) as f:
		f.write( "SystemName        {:} \n".format(name[:-4]) )
		f.write( "SystemLabel       {:} \n".format(name[:-4]) )
		f.write( "NumberOfAtoms     {: 5d} \n".format(np.sum(N_atoms_specie)) )
		f.write( "NumberOfSpecies   {: 5d} \n".format(4) )
		f.write( "NetCharge         {: 5d} \n".format(0) )
		f.write( " \n" )
		f.write( " \n" )
		f.write( "%block ChemicalSpeciesLabel \n" )
		f.write( "1   20   Ca \n" )
		f.write( "2   14   Si \n" )
		f.write( "3   8    O \n" )
		f.write( "4   1    H \n" )
		f.write( "%endblock ChemicalSpeciesLabel \n" )
		f.write( " \n" )
		f.write( " \n" )
		f.write( "%block PAO.BasisSizes \n" )
		f.write( "Ca    DZP \n" )
		f.write( "Si    DZP \n" )
		f.write( "O     DZP \n" )
		f.write( "H     DZP \n" )
		f.write( "%endblock PAO.BasisSizes \n" )
		f.write( " \n" )
		f.write( " \n" )
		f.write( "%block PAO.Basis \n" )
		f.write( "Ca   5      1.90213 \n" )
		f.write( "n=3   0   1   E    61.56667     4.61281 \n" )
		f.write( "    5.29940 \n" )
		f.write( "          1.00000 \n" )
		f.write( "n=4   0   2   E   164.86383     5.38785 \n" )
		f.write( "      6.76569     4.96452 \n" )
		f.write( "           1.00000     1.00000 \n" )
		f.write( "n=3   1   1   E    86.94959     3.48034 \n" )
		f.write( "        6.32716 \n" )
		f.write( "     1.00000 \n" )
		f.write( "n=4   1   1   E   112.03339     4.98424 \n" )
		f.write( "        7.49434 \n" )
		f.write( "        1.00000 \n" )
		f.write( "n=3   2   1   E    87.65847    5.83989 \n" )
		f.write( "        6.49046 \n" )
		f.write( "         1.00000 \n" )
		f.write( "%endblock PAO.Basis \n" )
		f.write( " \n" )
		f.write( " \n" )
		f.write( "xc.functional          GGA \n" )
		f.write( "xc.authors             PBE \n" )
		f.write( " \n" )
		f.write( "SolutionMethod         diagon \n" )
		f.write( "DM.Tolerance           1.E-4 \n" )
		f.write( "MaxSCFIterations       500 \n" )
		f.write( " \n" )
		f.write( "DM.NumberPulay         5 \n" )
		f.write( "DM.MixingWeight        0.05 \n" )
		f.write( "DM.NumberKick          20 \n" )
		f.write( "DM.KickMixingWeight    0.1 \n" )
		f.write( "DM.MixSCF1            .false. \n" )
		f.write( " \n" )
		f.write( "MeshCutoff             400  Ry \n" )
		f.write( "kgrid_cutoff           25  Bohr \n" )
		f.write( " \n" )
		f.write( " \n" )
		f.write( "%block LatticeVectors \n" )
		for i in range(3):
			f.write( "{: 12.6f} {: 12.6f} {: 12.6f} \n".format( *supercell[i,:] ) )
		f.write( "%endblock LatticeVectors \n" )
		f.write( " \n" )
		f.write( " \n" )
		f.write( "AtomicCoordinatesFormat Ang \n" )
		f.write( "%block AtomicCoordinatesAndAtomicSpecies \n" )
		fmt = "{: 12.6f} {: 12.6f} {: 12.6f} {: 5d} {:} \n"
		for i in coords_Ca:
			f.write( fmt.format(*i, 1, "Ca") )
		for i in coords_Si:
			f.write( fmt.format(*i, 2, "Si") )
		for i in coords_O:
			f.write( fmt.format(*i, 3, "O") )
		for i in coords_H:
			f.write( fmt.format(*i, 4, "H") )
		f.write( "%endblock AtomicCoordinatesAndAtomicSpecies \n" )



def get_sorted_log(list_properties):

	sorted_properties = {}
	for i in list_properties:
		Ca_Si = round(i[0], 4)
		SiOH  = round(i[1], 4)
		CaOH  = round(i[2], 4)
		MCL   = round(i[3], 4)

		if Ca_Si in sorted_properties:
			if SiOH in sorted_properties[Ca_Si]:
				if CaOH in sorted_properties[Ca_Si][SiOH]:
					if MCL in sorted_properties[Ca_Si][SiOH][CaOH]:
						sorted_properties[Ca_Si][SiOH][CaOH][MCL].append(i[4])
					else:
						sorted_properties[Ca_Si][SiOH][CaOH][MCL] = [i[4]]
				else:
					sorted_properties[Ca_Si][SiOH][CaOH] = {MCL: [i[4]]}
			else:
				sorted_properties[Ca_Si][SiOH] = {CaOH: {MCL: [i[4]]}}
		else:
			sorted_properties[Ca_Si] = {SiOH: {CaOH: {MCL: [i[4]]} } }


	with open("created_samples.log", "w") as f:
		fmt = "Sample: {: 5d}     Ca/Si: {: 8.6f}     SiOH/Si: {: 8.6f}    CaOH/Ca: {: 8.6f}    MCL: {: 8.6f} \n"

		sorted_Ca_Si = sorted(sorted_properties.keys())
		for Ca_Si in sorted_Ca_Si:
			sorted_SiOH = sorted(sorted_properties[Ca_Si].keys())
			for SiOH in sorted_SiOH:
				sorted_CaOH = sorted(sorted_properties[Ca_Si][SiOH].keys())
				for CaOH in sorted_CaOH:
					sorted_MCL = sorted(sorted_properties[Ca_Si][SiOH][CaOH].keys())
					for MCL in sorted_MCL:
						for i in sorted(sorted_properties[Ca_Si][SiOH][CaOH][MCL]):
							f.write( fmt.format(int(i), Ca_Si, SiOH, CaOH, MCL) )



def write_output( isample, entries_crystal, entries_bonds, entries_angle, shape, crystal_rs, water_in_crystal_rs,
				  supercell, N_Ca, N_Si, r_SiOH, r_CaOH, MCL, write_lammps, write_vasp, write_siesta):

	mypath = os.path.abspath(".")
	path = os.path.join(mypath, "output/")

	if write_lammps:
		name = "input"+str(isample+1)+".data"
		name = os.path.join(path, name)
		get_lammps_input(name, entries_crystal, entries_bonds, entries_angle, supercell) 

	name = "input"+str(isample+1)+".log"
	name = os.path.join(path, name)
	get_log(name, shape, crystal_rs, water_in_crystal_rs, N_Ca, N_Si, r_SiOH, r_CaOH, MCL )

	if write_vasp:
		name = "input"+str(isample+1)+".vasp"
		name = os.path.join(path, name)
		get_vasp_input(name, entries_crystal, supercell)

	if write_siesta:
		name = "input"+str(isample+1)+".fdf"
		name = os.path.join(path, name)
		get_siesta_input(name, entries_crystal, supercell)