import numpy as np
from parameters import *

from collections import OrderedDict
import sys


class Piece(object):
	"""docstring for Piece"""
	def __init__(self, charge, file):
		super(Piece, self).__init__()
		self.charge = charge
		self.N_Ca = 0
		self.N_Si = 0
		self.N_O = 0
		self.N_O_S = 0
		self.N_Ow = 0
		self.N_Oh = 0

		self.coord = []
		self.species = []
		self.entries = []

		with open("./Blocks_Renamed/"+file) as f:
			lines = f.readlines()
			self.N_atom = int(len(lines)/2)
			for i in range(self.N_atom):
				aux = lines[i*2].split()
				specie = aux[0]

				aux = lines[i*2+1].split()
				r = [ float(x) for x in aux ]

				if specie == "Ca":
					self.species.append( 1 )
					self.N_Ca += 1
					entries = [ 1, 2.0, r[0], r[1], r[2] ]
				if specie == "Si": 
					self.species.append( 2 )
					self.N_Si += 1
					entries = [ 2, 4.0, r[0], r[1], r[2] ]
				if specie == "O" : 
					self.species.append( 3 )
					self.N_O += 1
					entries = [ 3, 0.848, r[0], r[1], r[2] ]
				if specie == "O(S)" :
					self.species.append( 4 )
					self.N_O_S += 1
					entries = [ 4, -2.848, r[0], r[1], r[2] ]
				if specie == "Ow" : 
					self.species.append( 5 )
					self.N_Ow += 1
					entries = [ 5, -0.82, r[0], r[1], r[2] ]
				if specie == "Oh" : 
					self.species.append( 6 )
					self.N_Oh += 1
					entries = [ 6, -1.4, r[0], r[1], r[2] ]

				self.coord.append( np.array([ float(x) for x in aux ] ))



pieces = { "<L"   : Piece( charge = -2, file = "<L"   ),
		   ">L"   : Piece( charge = 0,  file = ">L"   ),
		   "<R"   : Piece( charge = 0,  file = "<R"   ),
		   ">R"   : Piece( charge = -2, file = ">R"   ),
                                                             
		   "<Lo"  : Piece( charge = -1, file = "<Lo"  ),
		   ">Lo"  : Piece( charge = 1,  file = ">Lo"  ),
		   "<Ro"  : Piece( charge = 1,  file = "<Ro"  ),
		   ">Ro"  : Piece( charge = -1, file = ">Ro"  ),
                                                             
                                                             
		   "SU"   : Piece( charge = 0, file =  "SU"  ),
		   "SD"   : Piece( charge = 0, file =  "SD"  ),
		   "SUo"  : Piece( charge = 1, file =  "SUo" ),
		   "SDo"  : Piece( charge = 1, file =  "SDo" ),
		   "CU"   : Piece( charge = 2, file =  "CU"  ),
		   "CD"   : Piece( charge = 2, file =  "CD"  ),
                                                             
                                                             
		   "CII"  : Piece( charge = 2,  file = "CII" ),
                                                             
		   "CIU"  : Piece( charge = 2,  file = "CIU" ),
		   "CID"  : Piece( charge = 2,  file = "CID" ),
                                                             
		   "XU"   : Piece( charge = 2,  file = "XU"  ),
		   "XD"   : Piece( charge = 2,  file = "XD"  ),
                                                             
                                                             
		   "oDL"  : Piece( charge = -1, file = "oDL" ),
		   "oDR"  : Piece( charge = -1, file = "oDR" ),
		   "oUL"  : Piece( charge = -1, file = "oUL" ),
		   "oUR"  : Piece( charge = -1, file = "oUR" ),
		   "oXU"  : Piece( charge = -1, file = "oXU" ),
		   "oXD"  : Piece( charge = -1, file = "oXD" ),
                                                             
		   "XU"   : Piece( charge = 2,  file = "XU"  ),
		   "XD"   : Piece( charge = 2,  file = "XD"  ),
                                                             
		   "oMDL" : Piece( charge = -1, file = "oMDL"),
		   "oMDR" : Piece( charge = -1, file = "oMDR"),
		   "oMUL" : Piece( charge = -1, file = "oMUL"),
		   "oMUR" : Piece( charge = -1, file = "oMUR"),
                                                             
                                                             
		   "wDR"  : Piece( charge = 0,  file = "wDR" ),
		   "wDL"  : Piece( charge = 0,  file = "wDL" ),
		   "wIL"  : Piece( charge = 0,  file = "wIL" ),
		   "wIR"  : Piece( charge = 0,  file = "wIR" ),
		   "wIR2" : Piece( charge = 0,  file = "wIR2"),
		   "wUL"  : Piece( charge = 0,  file = "wUL" ),
		   "wXD"  : Piece( charge = 0,  file = "wXD" ),
		   "wXU"  : Piece( charge = 0,  file = "wXU" ),
                                                             
		   "wMDL" : Piece( charge = 0,  file = "wMDL"),
		   "wMUL" : Piece( charge = 0,  file = "wMUL"),
		   "wMDR" : Piece( charge = 0,  file = "wMDR"),
		   "wMUR" : Piece( charge = 0,  file = "wMUR"),

}





class Brick(object):
	def __init__(self, comb, pieces):
		self.comb = comb
		self.charge = 0
		self.N_Si = 0
		self.N_Ca = 0

		list_water = set( ["wDR", "wDR", "wIL", "wIR", "wIR2", "wUL", "wXD", "wXU", "wMDL", "wMUL", "wMDR", "wMUR"] )

		incompatibility = { "oMUL" : "wMUL",
							"oMDL" : "wMDL",
							"oMDR" : "wMDR",
							"oMUR" : "wMUR",
							"oDL" : "wDL",
							"oDR" : "wDR",
							"oUL" : "wUL",
							"oXD" : "wXD",
							"oXU" : "wXU",

							"SD" : "wMDR",
							"SDo" : "wMDR",
							"SU" : "wMUR",
							"SUo" : "wMUR",

							"SD" : "wDR",
							"SDo" : "wDR",
							"SU" : "wUL",
							"SUo" : "wUL"
		}

		self.elegible_water = []

		excluded = set()
		for p in comb:
			if p != None:
				self.charge += pieces[p].charge
				self.N_Si += pieces[p].N_Si
				self.N_Ca += pieces[p].N_Ca

			if p in incompatibility:
				excluded.add( incompatibility[p] )

		self.elegible_water = np.array( list(list_water.difference(excluded) ) )



def above_layer():
	above_1 = [["<L"], ["<Lo"]]
	above_2 = [ [None], ["SU"], ["SU", "oUR"], ["SUo"], ["CU"], ["CU","oUL"], ["CU","oUR"] ]
	above_3 = [["<R"], ["<Ro"]]

	combs_above = []

	for i_ab_1 in above_1:
		
		for i_ab_2 in above_2:
			for i_ab_3 in above_3:
				comb = i_ab_1 + i_ab_2 + i_ab_3

				comb = [x for x in comb if x is not None]
				combs_above.append(comb)

	return combs_above


def below_layer():
	below_1 = [[">L"], [">Lo"]]
	below_2 = [ [None], ["SD"], ["SD", "oDR"], ["SDo"], ["CD"], ["CD","oDL"], ["CD","oDR"] ]
	below_3 = [[">R"], [">Ro"]]

	combs_below = []

	for i_ab_1 in below_1:
		
		for i_ab_2 in below_2:
			for i_ab_3 in below_3:
				comb = i_ab_1 + i_ab_2 + i_ab_3

				comb = [x for x in comb if x is not None]
				combs_below.append(comb)

	return combs_below



def interlayer():
	inter_Ca_1 = [None, "CII"]
	inter_Ca_2 = [None, "XU"]
	inter_Ca_3 = [None, "XD"]
	inter_Ca_4 = [None, "CID"]
	inter_Ca_5 = [None, "CIU"]

	inter_OH_1 = [None, "oMDL"]
	inter_OH_2 = [None, "oMDR"]
	inter_OH_3 = [None, "oMUL"]
	inter_OH_4 = [None, "oMUR"]

	combs_inter = []

	for i_Ca_1 in inter_Ca_1:
		for i_Ca_2 in inter_Ca_2:
			for i_Ca_3 in inter_Ca_3:
				for i_Ca_4 in inter_Ca_4:
					for i_Ca_5 in inter_Ca_5:

						for i_OH_1 in inter_OH_1:
							for i_OH_2 in inter_OH_2:
								for i_OH_3 in inter_OH_3:
									for i_OH_4 in inter_OH_4:

										comb = [i_Ca_1, i_Ca_2, i_Ca_3, i_Ca_4, i_Ca_5,
										        i_OH_1, i_OH_2, i_OH_3, i_OH_4]

										comb = [x for x in comb if x is not None]

										if i_Ca_2 == "XU":
											combs_inter.append(comb)
											comb.append( "oXU" )
											combs_inter.append(comb)
										if i_Ca_3 == "XD":
											combs_inter.append(comb)
											comb.append( "oXD" )
											combs_inter.append(comb)
										else:
											combs_inter.append(comb)

	return combs_inter




def check_restrictions(comb):
	if "SD" in comb or "SDo" in comb:
		if "oMDR" in comb or "oDR" in comb :
			return False
	elif "SU" in comb or "SUo" in comb:
		if "oMUR" in comb or "oUL" in comb :
			return False
	else:
		return True




def get_all_bricks(pieces):
	combs_above = above_layer()
	combs_below = below_layer()
	combs_inter = interlayer()

	combs = []
	for i_above in combs_above:
		for i_inter in combs_inter:
			for i_below in combs_below:
				comb = i_above + i_inter + i_below

				if check_restrictions:
					combs.append(comb)

	sorted_bricks = {}

	for i_comb in combs:
		b = Brick(i_comb, pieces)

		Ca_Si = round( b.N_Ca/b.N_Si, 15 )
		Q     = b.charge


		if b.charge < 10:

			if Ca_Si in sorted_bricks:
				if Q in sorted_bricks[Ca_Si]:
					sorted_bricks[Ca_Si][Q].append(b)
				else:
					sorted_bricks[Ca_Si][Q] = [b]
			else:
				sorted_bricks[Ca_Si] = {Q:[b]}

	return sorted_bricks




def sample_Ca_Si_ratio(sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick):
	
	width = 0.2

	keys_ratio = np.array(list(sorted_bricks.keys()))

	brick_ratio = 0.0
	brick_Q = 0.0

	crystal = []

	N_Si = 0
	N_Ca = 0

	cont = 0
	while True:
		while len(crystal) != N_brick:

			u = np.random.normal(loc = Ca_Si_ratio, scale = width)
			ind_ratio = np.argmin( np.abs( keys_ratio-u ) )

			key_ratio = keys_ratio[ind_ratio]

			keys_Q = np.array( list( sorted_bricks[key_ratio].keys() ) )

			u = np.random.normal(loc = 0.0, scale = 1.0)
			ind_Q = np.argmin( np.abs( keys_Q-u ) )


			if abs(keys_Q[ind_Q] - u) < 1.0:

				k1 = keys_ratio[ind_ratio]
				k2 = keys_Q[ind_Q]
				ind = np.random.randint(len(sorted_bricks[k1][k2]))

				crystal.append( sorted_bricks[k1][k2][ind] )

				N_Ca += sorted_bricks[k1][k2][ind].N_Ca
				N_Si += sorted_bricks[k1][k2][ind].N_Si

				brick_ratio += keys_ratio[ind_ratio]
				brick_Q += keys_Q[ind_Q]


		if brick_Q == 0:
			list_elegible_water = np.array([ len(crystal[i_brick].elegible_water) for i_brick in range(N_brick) ])
			N_water = int(np.rint(N_Si * W_Si_ratio))

			if np.sum(list_elegible_water) >= N_water:
				break
			else:
				print("Not enough room for water!")
				print(np.sum(list_elegible_water), N_water)
		else:
			brick_ratio = 0.0
			brick_Q = 0.0
			crystal = []
			N_Si = 0
			N_Ca = 0
		
			cont += 1

			if cont == 50:
				sys.exit("Could not find any structure")


	return crystal, N_Ca, N_Si





def fill_water(crystal, N_water):
	N_brick = len(crystal)

	N_left = N_water
	water_distr = np.zeros(N_brick,dtype=int)
	list_elegible_water = np.array([ len(crystal[i_brick].elegible_water) for i_brick in range(N_brick) ])
	list_elegible_brick = np.array( [True for i in range(N_brick)] )

	cont = 0
	water_in_crystal = None
	while N_left != 0:
		#Randomly distribute water 
		new_distr = np.random.rand(N_brick) * list_elegible_brick
		new_distr = np.rint( new_distr/sum(new_distr) * N_left )
		new_distr = new_distr.astype(int)


		water_distr += new_distr


		# Check if more water tahn intended
		if np.sum(water_distr) > N_water:
			ind = np.where( water_distr > 0 )[0][0]
			water_distr[ind] -= 1


		# Check if any brick contains more water than allowed
		aux = list_elegible_water - water_distr
		aux2 = aux < 0

		N_left = N_water - np.sum(water_distr) - np.sum( aux*aux2 )

		water_distr += aux*aux2

		# Elegible bricks for the next iteration
		list_elegible_brick = water_distr < list_elegible_water


		cont += 1


		# When only a few left insert manually
		if N_left <= 5 and N_left != 0:
			ind = np.random.choice(np.where( list_elegible_brick == True )[0])

			water_distr[ind] += 1
			N_left -= 1

			list_elegible_brick = water_distr < list_elegible_water

		if cont == 20:
			print("breaking!!")
			break

	# Fill each brick
	water_in_crystal = []
	for i_brick in range(N_brick):
		aux = np.random.choice( crystal[i_brick].elegible_water, size=water_distr[i_brick], replace=False )

		water_in_crystal.append( list(aux) )


	return water_in_crystal




def apply_PBC(r, supercell, supercell_inv):
	r_frac = np.matmul(r,supercell_inv)
	for i in range(3):
		if r_frac[i] > 1:
			r_frac[i]-=1
		if r_frac[i] < 0:
			r_frac[i]+=1

	return  np.matmul(r_frac,supercell)




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
			r = apply_PBC(r, supercell, supercell_inv)

			entry = [ atom_index, specie, charges[specie], r[0], r[1], r[2] ]
			at_entries.append(entry)
			atom_index += 1

			piece_entries.append(entry)

			# If "Oh" add hydroxyl "H"
			if specie == 6:
				if r[2] > 0.0:
					r_H = np.array([ r[0], r[1], r[2] - 1.0 ])
				elif r[2] < 0.0:
					r_H = np.array([ r[0], r[1], r[2] + 1.0 ])

				r_H = apply_PBC(r_H, supercell, supercell_inv)

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
		r = apply_PBC(r, supercell, supercell_inv)

		entry = [ atom_index, specie, charges[specie], r[0], r[1], r[2] ]
		at_entries.append(entry)
		piece_entries.append(entry)
		atom_index += 1

		# 1st hydrogen
		if r[2] > 0.0:
			r_H = np.array([ r[0], r[1], r[2] - 1.0 ])
		else:
			r_H = np.array([ r[0], r[1], r[2] + 1.0 ])
		r_H = apply_PBC(r_H, supercell, supercell_inv)
		entry = [ atom_index, 7, charges[7],  r_H[0], r_H[1], r_H[2] ]
		piece_entries.append(entry)
		at_entries.append(entry)

		entry = [ bond_index, 2, atom_index-1, atom_index ]
		bd_entries.append(entry)

		bond_index += 1

		atom_index += 1

		# 2nd hydrogen
		if r[1] > 0.0:
			r_H = np.array([ r[0], r[1] -1.0 , r[2] ])
		else:
			r_H = np.array([ r[0], r[1] + 1.0, r[2] ])
		r_H = apply_PBC(r_H, supercell, supercell_inv)
		entry = [ atom_index, 7, charges[7],  r_H[0], r_H[1], r_H[2] ]
		at_entries.append(entry)
		piece_entries.append(entry)

		entry = [ bond_index, 2, atom_index-2, atom_index ]
		bd_entries.append(entry)

		bond_index += 1
		atom_index += 1

		water_dict[w] = piece_entries

	return at_entries, atom_index, bd_entries, bond_index, brick_dict, water_dict



def get_full_coordinates(crystal, water_in_crystal, shape, pieces):

	crystal_rs = np.reshape( np.array(crystal), shape )


	water_in_crystal_rs = np.reshape( np.array(water_in_crystal, dtype=object), shape )


	cell = np.array([ [6.7352, -4.071295, 0.7037701],
					  [0.0, 6.209521, -6.2095578],
					  [0.0, 0.0, 13.9936836] ])

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


	return angle_entries




def get_lammps_input(input_file, entries_crystal, entries_bonds, entries_angle, shape):

	unit_cell = np.array([ [6.7352, -4.071295, 0.7037701],
				  [0.0, 6.209521, -6.2095578],
				  [0.0, 0.0, 13.9936836] ])

	cell = np.zeros((3,3))
	for i in range(3):
		cell[i,:] = unit_cell[i,:]*shape[i]
	cell_inv = np.linalg.inv(cell)

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
		f.write( "{: 12.6f} {: 12.6f} xlo xhi \n".format(0.0, cell[0,0]) )
		f.write( "{: 12.6f} {: 12.6f} ylo yhi \n".format(0.0, cell[1,1]) )
		f.write( "{: 12.6f} {: 12.6f} zlo zhi \n".format(0.0, cell[2,2]) )
		f.write( "{: 12.6f} {: 12.6f} {: 12.6f} xy xz yz \n".format( cell[0,1], cell[0,2], cell[1,2] ) )
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




def get_vasp_input(entries_crystal, shape):

	N_atoms_specie = np.zeros(8,dtype=int)

	coords = [ [] for i in range(8) ]

	coords_Ca = []
	coords_Si = []
	coords_O1 = []
	coords_O2 = []
	coords_Ow = []
	coords_Oh = []
	coords_Hw = []
	coords_H = []


	unit_cell = np.array([ [6.7352, -4.071295, 0.7037701],
				  [0.0, 6.209521, -6.2095578],
				  [0.0, 0.0, 13.9936836] ])

	cell = np.zeros((3,3))
	for i in range(3):
		cell[i,:] = unit_cell[i,:]*shape[i]
	cell_inv = np.linalg.inv(cell)

	for entry in entries_crystal:
		N_atoms_specie[ entry[1]-1 ] += 1
		r = np.array( entry[3:] )
		r = apply_PBC(r, cell, cell_inv)
		coords[  entry[1]-1 ].append( r )




	#f.write( " \n" )
	with open( "kk.vasp", "w" ) as f:
		f.write( "kk \n" )
		f.write( "1.0 \n" )
		for i in cell:
			f.write( "{: 12.6f} {: 12.6f} {: 12.6f} \n".format(*i) )
		f.write( "Ca  Si  O1  O2  Ow  Oh  Hw  H \n" )
		f.write( "{: 5d} {: 5d} {: 5d} {: 5d} {: 5d} {: 5d} {: 5d} {: 5d} \n".format(*N_atoms_specie) )
		f.write("Cartesian\n")
		fmt = "{: 12.6f} {: 12.6f} {: 12.6f} \n"
		
		for i in range(8):
			for j in coords[i]:
				f.write( fmt.format(*j) )








np.random.seed(seed)


# Get all possible bricks
sorted_bricks = get_all_bricks(pieces)

N_brick = shape[0]*shape[1]*shape[2]


for isample in range(N_samples):
	crystal, N_Ca, N_Si = sample_Ca_Si_ratio(sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick )

	N_water = int(np.rint(N_Si * W_Si_ratio))

	print( "Sample:{: 5d}    Ca/Si ratio: {: 10.6f}". format(isample+1, N_Ca/N_Si) )

	water_in_crystal = fill_water(crystal, N_water = N_water)

	entries_crystal, entries_bonds, crystal_dict, water_dict = get_full_coordinates( crystal, water_in_crystal, shape, pieces )

	entries_angle = get_angles(crystal_dict, water_dict, shape)

	name = "input"+str(isample+1)+".data"
	get_lammps_input(name, entries_crystal, entries_bonds, entries_angle, shape) 

	#get_vasp_input(entries_crystal, shape)