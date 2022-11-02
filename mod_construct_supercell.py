import numpy as np
import mod_construct_brick 



def reshape_crystal(crystal, water_in_crystal, shape):


	crystal_rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]

	water_in_crystal_rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]

	ind = 0
	for i in range(shape[0]):
		for j in range(shape[1]):
			for k in range(shape[2]):
				crystal_rs[i][j][k] = crystal[ind]
				water_in_crystal_rs[i][j][k] = water_in_crystal[ind]
				ind += 1

	return np.array(crystal_rs), np.array(water_in_crystal_rs,dtype=object)

	

def get_coordinates_brick( atom_index, bond_index, pieces, v_cell, supercell, supercell_inv, brick, water_in_brick ):

	charges = { 1: 2.0, 2: 4.0, 3:0.848, 4: -2.848, 5: -0.82, 6: -1.4, 7: 0.41, 8: 0.4 }

	at_entries = []
	bd_entries = []

	brick_dict = dict()
	water_dict = dict()

	for piece in brick.comb:

		piece_entries = []

		for iat in range( pieces[piece].N_atom ):

			specie = pieces[piece].species[iat]
			r = pieces[piece].coord[iat]
			r = r + v_cell
			#r = apply_PBC(r, supercell, supercell_inv)


			entry = [ atom_index, specie, charges[specie], r[0], r[1], r[2] ]
			at_entries.append(entry)
			atom_index += 1

			piece_entries.append(entry)

			# If "Oh" add hydroxyl "H"
			if specie == 6:
				r_H = r + pieces[piece].r_H1

				#r_H = apply_PBC(r_H, supercell, supercell_inv)

				entry = [atom_index, 8, charges[8], r_H[0], r_H[1], r_H[2] ]
				at_entries.append(entry)

				piece_entries.append(entry)

				entry = [ bond_index, 1, atom_index-1, atom_index ]
				bd_entries.append(entry)

				bond_index += 1
				atom_index += 1

			# If "O" add Shell Oxygen "O(S)"
			if specie == 3:
				entry = [ atom_index, 4, charges[4], r[0], r[1], r[2]+0.05 ]
				at_entries.append(entry)
				piece_entries.append(entry)

				entry = [ bond_index, 3, atom_index-1, atom_index ]
				bd_entries.append(entry)

				bond_index += 1
				atom_index +=1

		brick_dict[piece] = piece_entries

	# Water
	for w in water_in_brick:

		piece_entries = []

		iat = 0
		specie = pieces[w].species[iat]
		r = pieces[w].coord[iat]
		r = r + v_cell
		#r = apply_PBC(r, supercell, supercell_inv)


		entry = [ atom_index, specie, charges[specie], r[0], r[1], r[2] ]
		at_entries.append(entry)
		piece_entries.append(entry)
		atom_index += 1

		# 1st hydrogen
		r_H = r + pieces[w].r_H1
		#r_H = apply_PBC(r_H, supercell, supercell_inv)
		entry = [ atom_index, 7, charges[7],  r_H[0], r_H[1], r_H[2] ]
		piece_entries.append(entry)
		at_entries.append(entry)

		entry = [ bond_index, 2, atom_index-1, atom_index ]
		bd_entries.append(entry)

		bond_index += 1

		atom_index += 1

		# 2nd hydrogen
		r_H = r + pieces[w].r_H2
		#r_H = apply_PBC(r_H, supercell, supercell_inv)
		entry = [ atom_index, 7, charges[7],  r_H[0], r_H[1], r_H[2] ]
		at_entries.append(entry)
		piece_entries.append(entry)

		entry = [ bond_index, 2, atom_index-2, atom_index ]
		bd_entries.append(entry)

		bond_index += 1
		atom_index += 1

		water_dict[w] = piece_entries

	return at_entries, atom_index, bd_entries, bond_index, brick_dict, water_dict



def get_full_coordinates(crystal_rs, water_in_crystal_rs, shape, pieces):

	cell = np.array([ [6.7352,    0.0 ,      0.0],
			 		   [-4.071295, 6.209521,  0.0],
					   [0.7037701, -6.2095578, 13.9936836] ])

	supercell = np.zeros((3,3))
	for i in range(3):
		supercell[i,:] = cell[i,:]*shape[i]

	supercell_inv = np.linalg.inv(supercell)


	atom_entries = []
	bond_entries = []
	atom_index = 1
	bond_index = 1


	crystal_dict = dict()
	water_dict = dict()

	for i in range(shape[0]):
		for j in range(shape[1]):
			for k in range(shape[2]):
				v_cell = i*cell[0] + j*cell[1] + k*cell[2] 

				at_entry_b, atom_index, bd_entry_b, bond_index, brick_dict, brick_water_dict =  get_coordinates_brick( 
											atom_index, bond_index, pieces, v_cell, supercell, supercell_inv, 
											crystal_rs[i,j,k], water_in_crystal_rs[i,j,k] )


				atom_entries = atom_entries + at_entry_b
				bond_entries = bond_entries + bd_entry_b

				crystal_dict[(i,j,k)] = brick_dict
				water_dict[(i,j,k)] = brick_water_dict


	return atom_entries, bond_entries, crystal_dict, water_dict




def get_angles(crystal_dict, water_dict, shape):
	angle_index = 1
	angle_entries = []
	for cell in crystal_dict.keys():

		# Upper "<L" or "<Lo"
		if "<Lo" in crystal_dict[cell] or "<L" in  crystal_dict[cell]:
			piece = "<Lo"
			if "<L" in crystal_dict[cell]: piece = "<L"

			ind_Si = crystal_dict[cell][piece][1][0]
			ind_O = [ crystal_dict[cell][piece][i][0] for i in [2,4,6,8] ]

			for i_O in range(len(ind_O)):
				for j_O in range( i_O+1, len(ind_O) ):
					angle_entries.append( [angle_index, 2, ind_O[i_O], ind_Si, ind_O[j_O]] )
					angle_index += 1

			if piece == "<Lo":
				ind_Oh  = crystal_dict[cell][piece][8][0]
				angle_entries.append( [angle_index, 3, ind_Si, ind_Oh, ind_Oh+1] )
				angle_index += 1



		# Upper "<R" or "<Ro"
		if "<Ro" in crystal_dict[cell] or "<R" in  crystal_dict[cell]:
			piece = "<Ro"
			if "<R" in crystal_dict[cell]: piece = "<R"

			ind_Si = crystal_dict[cell][piece][1][0]
			ind_O = [ crystal_dict[cell][piece][i][0] for i in [2,4,6] ]

			# Pick 3th oxygen in the next cell
			next_cell = [cell[0], cell[1]+1,cell[2]]
			if next_cell[1] == shape[1]: next_cell[1] = 0
			next_cell = tuple(next_cell)

			next_piece = "<Lo"
			if "<L" in crystal_dict[next_cell]: next_piece = "<L"
			ind_O_next = crystal_dict[next_cell][next_piece][6][0]


			ind_O.append(ind_O_next)

			for i_O in range(len(ind_O)):
				for j_O in range( i_O+1, len(ind_O) ):
					angle_entries.append( [angle_index, 2, ind_O[i_O], ind_Si, ind_O[j_O]] )
					angle_index += 1

			if piece == "<Ro":
				ind_Oh  = crystal_dict[cell][piece][6][0]
				angle_entries.append( [angle_index, 3, ind_Si, ind_Oh, ind_Oh+1] )
				angle_index += 1



		# Upper "SU" or "SUo"
		if "SU" in crystal_dict[cell] or "SUo" in crystal_dict[cell]:
			piece = "SU"
			if "SUo" in crystal_dict[cell]: piece = "SUo"

			ind_Si = crystal_dict[cell][piece][0][0]
			ind_O = [ crystal_dict[cell][piece][i][0] for i in [1,3] ]

			# Pick 4th oxygen from "<L"
			piece2 = "<Lo"
			if "<L" in crystal_dict[cell]: piece2 = "<L"
			ind_O.append( crystal_dict[cell][piece2][8][0] )
			# Pick 3rd oxygen from "<R"
			piece2 = "<Ro"
			if "<R" in crystal_dict[cell]: piece2 = "<R"
			ind_O.append( crystal_dict[cell][piece2][6][0] )


			for i_O in range(len(ind_O)):
				for j_O in range( i_O+1, len(ind_O) ):
					angle_entries.append( [angle_index, 2, ind_O[i_O], ind_Si, ind_O[j_O]] )
					angle_index += 1

			if piece == "SUo":
				ind_Oh  = crystal_dict[cell][piece][1][0]
				angle_entries.append( [angle_index, 3, ind_Si, ind_Oh, ind_Oh+1] )
				angle_index += 1




			

		# Bellow ">R" or ">Ro"
		if ">Ro" in crystal_dict[cell] or ">R" in  crystal_dict[cell]:
			piece = ">Ro"
			if ">R" in crystal_dict[cell]: piece = ">R"

			ind_Si = crystal_dict[cell][piece][1][0]
			ind_O = [ crystal_dict[cell][piece][i][0] for i in [2,4,6,8] ]


			for i_O in range(len(ind_O)):
				for j_O in range( i_O+1, len(ind_O) ):
					angle_entries.append( [angle_index, 2, ind_O[i_O], ind_Si, ind_O[j_O]] )
					angle_index += 1

			if piece == ">Ro":
				ind_Oh  = crystal_dict[cell][piece][8][0]
				angle_entries.append( [angle_index, 3, ind_Si, ind_Oh, ind_Oh+1] )
				angle_index += 1


		# Bellow ">L" or ">Lo"
		if ">Lo" in crystal_dict[cell] or ">L" in  crystal_dict[cell]:
			piece = ">Lo"
			if ">L" in crystal_dict[cell]: piece = ">L"

			ind_Si = crystal_dict[cell][piece][1][0]
			ind_O = [ crystal_dict[cell][piece][i][0] for i in [2,4,6] ]

			# Pick 3th oxygen in the previous cell
			prev_cell = [cell[0], cell[1]-1,cell[2]]
			if prev_cell[1] == -1: prev_cell[1] = shape[1]-1
			prev_cell = tuple(prev_cell)

			prev_piece = ">Ro"
			if ">R" in crystal_dict[prev_cell]: prev_piece = ">R"
			ind_O_prev = crystal_dict[prev_cell][prev_piece][6][0]


			ind_O.append(ind_O_prev)

			for i_O in range(len(ind_O)):
				for j_O in range( i_O+1, len(ind_O) ):
					angle_entries.append( [angle_index, 2, ind_O[i_O], ind_Si, ind_O[j_O]] )
					angle_index += 1

			if piece == ">Lo":
				ind_Oh  = crystal_dict[cell][piece][6][0]
				angle_entries.append( [angle_index, 3, ind_Si, ind_Oh, ind_Oh+1] )
				angle_index += 1





		# Bellow "SD" or "SDo"
		if "SD" in crystal_dict[cell] or "SDo" in crystal_dict[cell]:
			piece = "SD"
			if "SDo" in crystal_dict[cell]: piece = "SDo"

			ind_Si = crystal_dict[cell][piece][0][0]
			ind_O = [ crystal_dict[cell][piece][i][0] for i in [1,3] ]

			# Pick 4th oxygen from ">R"
			piece2 = ">Ro"
			if ">R" in crystal_dict[cell]: piece2 = ">R"
			ind_O.append( crystal_dict[cell][piece2][8][0] )
			# Pick 3rd oxygen from ">L"
			piece2 = ">Lo"
			if ">L" in crystal_dict[cell]: piece2 = ">L"
			ind_O.append( crystal_dict[cell][piece2][6][0] )


			for i_O in range(len(ind_O)):
				for j_O in range( i_O+1, len(ind_O) ):
					angle_entries.append( [angle_index, 2, ind_O[i_O], ind_Si, ind_O[j_O]] )
					angle_index += 1

			if piece == "SDo":
				ind_Oh  = crystal_dict[cell][piece][1][0]
				angle_entries.append( [angle_index, 3, ind_Si, ind_Oh, ind_Oh+1] )
				angle_index += 1


		for w in water_dict[cell]:
			angle_entries.append( [angle_index, 1, water_dict[cell][w][1][0],  water_dict[cell][w][0][0],  water_dict[cell][w][2][0] ] )		
			angle_index += 1

	return angle_entries




def transform_surface_separation(crystal_entries, supercell, unitcell, surface_separation):

	vec_c = unitcell[2]
	c = np.linalg.norm(vec_c)
	vec_d = vec_c*surface_separation/c


	new_entries = []
	for entry in crystal_entries:
		r = np.array(entry[3:])
		r = r +0.5*(vec_d - vec_c)

		new_entries.append( [ entry[0], entry[1], entry[2], r[0],  r[1],  r[2] ] )

	supercell[2,:] = supercell[2,:] + vec_d - vec_c

	return new_entries, supercell


def check_move_water_hydrogens(crystal_entries):
	aux_entries = crystal_entries# np.array(crystal_entries)
	# List of Hw and H
	list_Hw = []
	list_Ow = []
	list_oH = []
	list_O  = []
	for i in range(len(aux_entries)):
		# If Ow
		if int(aux_entries[i][1]) == 5:
			list_Ow.append(i)
		# If O
		if int(aux_entries[i][1]) == 3 or int(aux_entries[i][1]) == 6:
			list_O.append(i)
		# If Hw
		if int(aux_entries[i][1]) == 7:
			list_Hw.append(i)
		# If Ho
		if int(aux_entries[i][1]) == 8:
			list_oH.append(i)

	N_water = len(list_Ow)
	N_not_ok = 0

	if N_water == 0:
		return aux_entries, 0, 1

	for itry in range(10):
		N_not_ok = 0
		for iwater in range(len(list_Ow)):
			# Check distance of the Hw in the molecule to every other H
			ok_struc = False
			new_molecule_coordinates(iwater, list_Hw, list_Ow, aux_entries)
			for i in range(100):
				#print(iwater, i)
				ok_molecule = check_new_molecule(iwater, list_Hw, list_Ow, list_oH, list_O, aux_entries,
					                             min_dist_H=0.8, min_dist_O=0.7)
				if ok_molecule:
					ok_struc = True
					break
				else:
					# Change the coordinates of the new molecule
					#print("change molecule", iwater)
					new_molecule_coordinates(iwater, list_Hw, list_Ow, aux_entries)

			if not ok_struc: N_not_ok += 1

		if ok_struc:
			N_not_ok = 0
			itry += 1
			break

	return aux_entries, N_not_ok, itry


# def new_molecule_coordinates(iwater, list_Hw, list_Ow, aux_entries):

# 	iHw1 = list_Hw[2*iwater]
# 	iHw2 = list_Hw[2*iwater+1]

# 	u = np.random.rand(3)-0.5
# 	u = u/np.linalg.norm(u)

# 	v = np.random.rand(3)-0.5
# 	v = v/np.linalg.norm(v)

# 	v[2] = (np.cos(107*np.pi/180) - u[0]*v[0] - u[1]*v[1])/u[2]
# 	v = v/np.linalg.norm(v)

# 	aux_entries[iHw1][3:] = np.array(aux_entries[list_Ow[iwater]][3:]) + u
# 	aux_entries[iHw2][3:] = np.array(aux_entries[list_Ow[iwater]][3:]) + v



def new_molecule_coordinates(iwater, list_Hw, list_Ow, aux_entries):

	iHw1 = list_Hw[2*iwater]
	iHw2 = list_Hw[2*iwater+1]

	r_H1 = np.random.rand(3)-0.5
	r_H1 = r_H1/np.linalg.norm(r_H1)


	# Second water molecule
	# In the reference system where Z' axis is oriented in the direction 
	# that joins the Oxygen and H1 atoms, and Oxygen is the origin
	# x'**2 + y'**2 = cos(104-90)**2
	# z' = -sin(104-90)
	# x' and y' are randomly chosen in that circunference
	ang = np.random.rand()*2*np.pi
	x_p = np.cos(14.5*np.pi/180)*np.sin(ang)
	y_p = np.cos(14.5*np.pi/180)*np.cos(ang)
	z_p = -np.sin(14.5*np.pi/180)

	r_H2_p = np.array([x_p, y_p, z_p])


	# Now we have to rotate that vector to the original cartesian reference
	theta = np.arccos( r_H1[2]/np.linalg.norm(r_H1) )
	u_rot = np.cross(np.array([0,0,1]), r_H1)
	u_rot = u_rot/np.linalg.norm(u_rot)

	mat_rot = np.zeros((3,3))
	mat_rot[0,0] = np.cos(theta) + u_rot[0]**2*(1-np.cos(theta))
	mat_rot[1,1] = np.cos(theta) + u_rot[1]**2*(1-np.cos(theta))
	mat_rot[2,2] = np.cos(theta)
	mat_rot[0,1] = u_rot[0]*u_rot[1]*(1-np.cos(theta))
	mat_rot[0,2] = u_rot[1]*np.sin(theta)
	mat_rot[1,2] = -u_rot[0]*np.sin(theta)

	mat_rot[1,0] = mat_rot[0,1]
	mat_rot[2,0] = -mat_rot[0,2]
	mat_rot[2,1] = -mat_rot[1,2]

	r_H2 = np.dot(mat_rot, r_H2_p)

	# Finaly we change the origin from the Oxygen to the cartesian center

	aux_entries[iHw1][3:] = np.array(aux_entries[list_Ow[iwater]][3:]) + r_H1
	aux_entries[iHw2][3:] = np.array(aux_entries[list_Ow[iwater]][3:]) + r_H2





def check_new_molecule(iwater, list_Hw, list_Ow, list_oH, list_O, aux_entries, min_dist_H=0.8, min_dist_O=1.0):
	# Check distance wrt Oh
	aux = np.zeros((0,3),dtype=float)
	for iH in range(len(list_oH)):
		iHw = 2*iwater
		iHw = list_Hw[iHw]
		aux = np.concatenate(( aux, [np.array(aux_entries[list_oH[iH]][3:]) - np.array(aux_entries[iHw][3:])] ))


		iHw = 2*iwater + 1
		iHw = list_Hw[iHw]
		aux = np.concatenate(( aux, [np.array(aux_entries[list_oH[iH]][3:]) - np.array(aux_entries[iHw][3:])] ))

	dist = check_distance_PBC(aux)
	if np.any( dist < min_dist_H ):
		return False

	# Check distance wrt previous water molecules
	aux = np.zeros((0,3),dtype=float)
	for iw in range(2*(iwater-1)):
		iHw = 2*iwater
		iHw = list_Hw[iHw]

		aux = np.concatenate(( aux, [np.array(aux_entries[list_Hw[iw]][3:]) - np.array(aux_entries[iHw][3:])] ))


		iHw = 2*iwater + 1
		iHw = list_Hw[iHw]
		aux = np.concatenate(( aux, [np.array(aux_entries[list_Hw[iw]][3:]) - np.array(aux_entries[iHw][3:])] ))


	dist = check_distance_PBC(aux)
	if np.any( dist < min_dist_H ):
		return False

	# Check distance wrt other oxygen atoms
	aux = np.zeros((0,3),dtype=float)
	for iO in range(len(list_O)):
		iHw = 2*iwater
		iHw = list_Hw[iHw]
		aux = np.concatenate(( aux, [np.array(aux_entries[list_O[iO]][3:]) - np.array(aux_entries[iHw][3:])] ))

	for iO in range(len(list_Ow)):
		if iO == iwater: continue

		iHw = 2*iwater
		iHw = list_Hw[iHw]
		aux = np.concatenate(( aux, [np.array(aux_entries[list_Ow[iO]][3:]) - np.array(aux_entries[iHw][3:])] ))


	dist = check_distance_PBC(aux)
	if np.any( dist < min_dist_O ):
		return False

	return True


def check_distance_PBC(v1_v2):
	cell = np.array([ [6.7352,    0.0 ,      0.0],
				 		   [-4.071295, 6.209521,  0.0],
						   [0.7037701, -6.2095578, 13.9936836] ])

	invcell = np.linalg.inv(cell)

	aux = v1_v2

	aux2 = np.array(np.dot(aux, invcell),dtype=int)

	if np.any( np.abs(aux2) ) >= 1:
		aux = aux - np.dot(aux2,cell)


	return np.linalg.norm(aux,axis=1)




def check_new_molecule_old(iwater, list_Hw, list_Ow, list_oH, list_O, aux_entries, min_dist_H=0.8, min_dist_O=1.0):
	# Check distance wrt Oh
	for iH in range(len(list_oH)):
		iHw = 2*iwater
		iHw = list_Hw[iHw]
		dist = check_distance_PBC_old( np.array(aux_entries[list_oH[iH]][3:]) , np.array(aux_entries[iHw][3:]) )
		if dist < min_dist_H:
			return False
		iHw = 2*iwater + 1
		iHw = list_Hw[iHw]
		dist = check_distance_PBC_old( np.array(aux_entries[list_oH[iH]][3:]) , np.array(aux_entries[iHw][3:]) )
		if dist < min_dist_H:
			return False

	# Check distance wrt previous water molecules
	for iw in range(2*(iwater-1)):
		iHw = 2*iwater
		iHw = list_Hw[iHw]
		dist = check_distance_PBC_old( np.array(aux_entries[list_Hw[iw]][3:]) , np.array(aux_entries[iHw][3:]) )
		if dist < min_dist_H:
			return False
		iHw = 2*iwater + 1
		iHw = list_Hw[iHw]
		dist = check_distance_PBC_old( np.array(aux_entries[list_Hw[iw]][3:]) , np.array(aux_entries[iHw][3:]) )
		if dist < min_dist_H:
			return False


	# Check distance wrt other oxygen atoms
	for iO in range(len(list_O)):
		iHw = 2*iwater
		iHw = list_Hw[iHw]
		dist = check_distance_PBC_old( np.array(aux_entries[list_O[iO]][3:])  , np.array(aux_entries[iHw][3:]) )
		if dist < min_dist_O:
			return False

	for iO in range(len(list_Ow)):
		if iO == iwater: continue

		iHw = 2*iwater
		iHw = list_Hw[iHw]
		dist = check_distance_PBC_old( np.array(aux_entries[list_Ow[iO]][3:]) , np.array(aux_entries[iHw][3:]) )
		if dist < min_dist_O:
			return False


	return True


def check_distance_PBC_old(v1, v2):
	cell = np.array([ [6.7352,    0.0 ,      0.0],
				 		   [-4.071295, 6.209521,  0.0],
						   [0.7037701, -6.2095578, 13.9936836] ])

	invcell = np.linalg.inv(cell)

	aux = v1-v2

	aux2 = np.array(np.dot(aux, invcell),dtype=int)

	if np.any( np.abs(aux2) ) >= 1:
		aux = aux - np.dot(aux2,cell)


	return np.linalg.norm(aux)



# def transform_surface_separation(crystal_entries, supercell, unitcell, surface_separation):

# 	vec_a = supercell[0,:]
# 	vec_b = supercell[1,:]
# 	vec_c = supercell[2,:]

# 	a = np.linalg.norm(vec_a)
# 	b = np.linalg.norm(vec_b)
# 	c = np.linalg.norm(vec_c)

# 	beta = np.arccos( np.dot(vec_a, vec_c)/a/c )
# 	alpha = np.arccos( np.dot(vec_b, vec_c)/b/c ) #100*np.pi/180

# 	c_new_1 = a*c*np.cos(beta)/vec_a[0]
# 	c_new_2 = b*c/vec_b[1]*np.cos(alpha)-vec_b[0]/vec_b[1] * c_new_1
# 	c_new_3 = np.sqrt( c**2 - c_new_1**2 - c_new_2**2 )
# 	vec_c_new = np.array([c_new_1, c_new_2, c_new_3])

# 	print(vec_c_new)

# 	vec_d = vec_c*surface_separation/c

# 	trans_mat = np.eye(3)
# 	trans_mat[0,2] = (vec_c_new[0] - vec_c[0] )/vec_c[2]
# 	trans_mat[1,2] = (vec_c_new[1] - vec_c[1] )/vec_c[2]
# 	trans_mat[2,2] = vec_c_new[2]/vec_c[2]





# 	vec_c =unitcell[2,:]
# 	c = np.linalg.norm(vec_c)
# 	vec_d = vec_c*surface_separation/c


# 	new_entries = []
# 	for entry in crystal_entries:
# 		r = np.array(entry[3:])
# 		#r = r +0.5*(vec_d - vec_c)

# 		r = np.dot(trans_mat, r)

# 		new_entries.append( [ entry[0], entry[1], entry[2], r[0],  r[1],  r[2] ] )

# 	#supercell[2,:] = supercell[2,:] + vec_d - vec_c

# 	for i in range(3):
# 		supercell[i,:] = np.dot(trans_mat, supercell[i,:])

# 	return new_entries, supercell


# def reshape_unitcell(crystal_entries, supercell, cell):
# 	vec_a = supercell[0,:]
# 	vec_b = supercell[1,:]
# 	vec_c = supercell[2,:]

# 	a = np.linalg.norm(vec_a)
# 	b = np.linalg.norm(vec_b)
# 	c = np.linalg.norm(vec_c)

# 	beta = np.arccos( np.dot(vec_a, vec_c)/a/c )
# 	alpha = 100*np.pi/180

# 	c_new_1 = a*c*np.cos(beta)/vec_a[0]
# 	c_new_2 = b*c/vec_b[1]*np.cos(alpha)-vec_b[0]/vec_b[1] * c_new_1
# 	c_new_3 = np.sqrt( c**2 - c_new_1**2 - c_new_2**2 )
# 	vec_c_new = np.array([c_new_1, c_new_2, c_new_3])

# 	print(vec_c_new)

# 	vec_d = vec_c*surface_separation/c

# 	trans_mat = np.eye(3)
# 	trans_mat[0,2] = (vec_c_new[0] - vec_c[0] )/vec_c[2]
# 	trans_mat[1,2] = (vec_c_new[1] - vec_c[1] )/vec_c[2]
# 	trans_mat[2,2] = vec_c_new[2]/vec_c[2]
