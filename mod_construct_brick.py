import numpy as np
import ast

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
		self.N_H = 0
		self.N_Hw = 0

		self.species = []
		self.coord = []

		cell = np.array([ [6.7352,    0.0 ,      0.0],
		 		   [-4.071295, 6.209521,  0.0],
				   [0.7037701, -6.2095578, 13.9936836] ])

		cell_inv = np.linalg.inv(cell)

		with open("./Blocks_Renamed/"+file) as f:
			lines = f.readlines()
			self.N_atom = int(len(lines)/2)
			for i in range(self.N_atom):
				aux = lines[i*2].split()
				specie = aux[0]

				aux = lines[i*2+1].split()
				r = np.array([ float(x) for x in aux ])

				if specie == "Ca":
					self.species.append( 1 )
					self.N_Ca += 1
				if specie == "Si": 
					self.species.append( 2 )
					self.N_Si += 1
				if specie == "O" : 
					self.species.append( 3 )
					self.N_O += 1
				if specie == "O(S)" :
					self.species.append( 4 )
					self.N_O_S += 1
				if specie == "Ow" : 
					self.species.append( 5 )
					self.N_Ow += 1

					if r[2] > 0.0:
						self.r_H1 = np.array([0, 0, -1.0])
					else:
						self.r_H1 = np.array([0, 0, 1.0])

					if r[1] > 0.0:
						self.r_H2 = np.array([0, -1.0, 0])
					else:
						self.r_H2 = np.array([0, 1.0, 0])

				if specie == "Oh" : 
					self.species.append( 6 )
					self.N_Oh += 1

					if r[2] > 0.0:
						self.r_H1 = np.array([0, 0, -1.0])
					else:
						self.r_H1 = np.array([0, 0, 1.0])



				frac_r = np.matmul(r, cell_inv) + np.array([0.5, 0.5, 0.5])
				for i in range(3):
					if frac_r[i] > 1:
						frac_r[i]-=1
					if frac_r[i] < 0:
						frac_r[i]+=1
				r = np.matmul(frac_r, cell)
				self.coord.append( r )



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
	def __init__(self, comb, pieces, ind):
		self.ind = ind
		self.comb = comb
		self.charge = 0
		self.N_Si = 0
		self.N_Ca = 0
		self.N_SiO = 0
		self.N_SiOH = 0

		self.N_Oh = 0

		self.N_SUD = 0
		self.N_braket = 0

		list_water = set( ["wDR", "wDR", "wIL", "wIR", "wIR2", "wUL", "wXD", "wXU", "wMDL", "wMUL", "wMDR", "wMUR"] )

		#list_water = set( ["wDR", "wDR", "wIL", "wIR2", "wUL", "wXD", "wXU", "wMDL", "wMUL", "wMDR", "wMUR"] )

		incompatibility = { "oMUL" : ["wMUL"],
							"oMDL" : ["wMDL"],
							"oMDR" : ["wMDR"],
							"oMUR" : ["wMUR"],
							"oDL" : ["wDL"],
							"oDR" : ["wDR"],
							"oUL" : ["wUL"],
							"oXD" : ["wXD"],
							"oXU" : ["wXU"],

							"oUR" : ["wIR"],

							"SD"  : ["wMDR", "wDR"],
							"SDo" : ["wMDR", "wDR"],
							"SU"  : ["wMUR", "wUL"],
							"SUo" : ["wMUR", "wUL"],
		}


		self.elegible_water = []

		self.excluded = set()
		for p in comb:
			if p != None:
				self.charge += pieces[p].charge
				self.N_Si += pieces[p].N_Si
				self.N_Ca += pieces[p].N_Ca
				self.N_Oh += pieces[p].N_Oh

			if p in [ "<Lo", "<Ro", ">Lo", ">Ro", "SUo", "SDo" ]:
				self.N_SiOH += 1

			if p in [ "<Lo", "<Ro", ">Lo", ">Ro", "<L", "<R", ">L", ">R"]:
				self.N_braket += 1

			if p in [ "SU", "SUo", "SD", "SDo" ]:
				self.N_SUD += 1

			if p in incompatibility:
				for w in incompatibility[p]:
					self.excluded.add( w )

		self.elegible_water = np.array( list(list_water.difference(self.excluded) ) )




def above_layer():

	bridging = [["SU"], ["SUo"], ["CU"], [None]]

	combs_above = []
	for i_bridge in bridging:
		if i_bridge in [["SU"], ["SUo"]]:
			for oh_bridge in [ [None], ["oMUL"] ]:
				comb = ["<L"] + i_bridge + oh_bridge + ["<R"]
				combs_above.append( [x for x in comb if x is not None] )

		if i_bridge == [None]:
			for i_left in [["<L"], ["<Lo"]]:
				for i_right in  [["<R"], ["<Ro"]]:
					comb = i_left + i_right
					combs_above.append(comb)

		if i_bridge == ["CU"]:
			for i_left in [["<L"], ["<Lo"]]:
				for i_right in  [["<R"], ["<Ro"]]:
					for oh_bridge_1 in [ [None], ["oMUL"] ]:
						for oh_bridge_2 in [ [None], ["oMUR"] ]:
							comb = i_left + i_bridge + oh_bridge_1 + oh_bridge_2 + i_right

							combs_above.append( [x for x in comb if x is not None] )

	return combs_above


def below_layer():

	bridging = [["SD"], ["SDo"], ["CD"], [None]]

	combs_below = []
	for i_bridge in bridging:
		if i_bridge in [["SD"], ["SDo"]]:
			for oh_bridge in [ [None], ["oMDL"] ]:
				comb = [">L"] + i_bridge + oh_bridge + [">R"]
				combs_below.append( [x for x in comb if x is not None] )

		if i_bridge == [None]:
			for i_left in [[">L"], [">Lo"]]:
				for i_right in  [[">R"], [">Ro"]]:
					comb = i_left + i_right
					combs_below.append(comb)

		if i_bridge == ["CD"]:
			for i_left in [[">L"], [">Lo"]]:
				for i_right in  [[">R"], [">Ro"]]:
					for oh_bridge_1 in [ [None], ["oMDL"] ]:
						for oh_bridge_2 in [ [None], ["oMDR"] ]:
							comb = i_left + i_bridge + oh_bridge_1 + oh_bridge_2 + i_right

							combs_below.append( [x for x in comb if x is not None] )		

	return combs_below



def interlayer():
	inter_Ca_1 = [None, "CII"]
	inter_Ca_2 = [None, "XU"]
	inter_Ca_3 = [None, "XD"]
	inter_Ca_4 = [None, "CID"]
	inter_Ca_5 = [None, "CIU"]

	inter_OH_1 = [None, "oDL"]
	inter_OH_2 = [None, "oDR"]
	inter_OH_3 = [None, "oUL"]
	inter_OH_4 = [None, "oUR"]

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
	satisfy = True
	if "SD" in comb or "SDo" in comb:
		if "oMDR" in comb or "oDR" in comb :
			satisfy =  False
	if "SU" in comb or "SUo" in comb:
		if "oMUR" in comb or "oUL" in comb :
			satisfy =  False

	return satisfy




def get_all_bricks(pieces):
	combs_above = above_layer()
	combs_below = below_layer()
	combs_inter = interlayer()

	combs = []
	for i_above in combs_above:
		for i_inter in combs_inter:
			for i_below in combs_below:
				comb = i_above + i_inter + i_below

				if check_restrictions(comb):
					combs.append(comb)

	sorted_bricks = {}

	ind = 0
	for i_comb in combs:
		b = Brick(i_comb, pieces, ind)

		Ca_Si = round( b.N_Ca/b.N_Si, 15 )
		Q     = b.charge

		SiOH = round( b.N_SiOH/b.N_Si, 4)
		CaOH = round( (b.N_Oh - b.N_SiOH )/b.N_Ca, 4)


		if abs(Q) < 5:

			if Ca_Si in sorted_bricks:
				if Q in sorted_bricks[Ca_Si]:
					if SiOH in sorted_bricks[Ca_Si][Q]:
						if CaOH in sorted_bricks[Ca_Si][Q][SiOH]:
							sorted_bricks[Ca_Si][Q][SiOH][CaOH].append(b)
						else:
							sorted_bricks[Ca_Si][Q][SiOH][CaOH] = [b]
					else:
						sorted_bricks[Ca_Si][Q][SiOH] = {CaOH: [b]}
				else:
					sorted_bricks[Ca_Si][Q] = {SiOH: {CaOH: [b]} }
			else:
				sorted_bricks[Ca_Si] = {Q: {SiOH: {CaOH: [b]} } }

		ind += 1

	return sorted_bricks







# def read_brick(input_file, pieces):

# 	with open(input_file, "r") as f:
# 		lines = f.readlines()

# 		shape = tuple([ int(i) for i in lines[5].split()[1:]])
# 		N_brick = shape[0]*shape[1]*shape[2]

# 		crystal_rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]

# 		water_in_crystal_rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]

# 		N_Si = 0
# 		N_Ca = 0
# 		N_SiOH = 0
# 		N_Oh = 0
# 		N_braket = 0
# 		N_SUD = 0

# 		for i in range( N_brick ):
# 			line = lines[10+2*i]
# 			aux = line.split()
# 			cell = tuple([ int(aux[i]) for i in range(3) ])
# 			ind1 = line.find("[")
# 			comb = ast.literal_eval(line[ind1:])
# 			b = Brick(comb, pieces, i)
# 			crystal_rs[cell[0]][cell[1]][cell[2]] = b

# 			N_Si += b.N_Si
# 			N_Ca += b.N_Ca
# 			N_SiOH += b.N_SiOH
# 			N_Oh += b.N_Oh
# 			N_braket += b.N_braket
# 			N_SUD += b.N_SUD


# 			line = lines[11+2*i]
# 			ind1 = line.find("[")
# 			water_in_crystal_rs[cell[0]][cell[1]][cell[2]] = ast.literal_eval(line[ind1:])

# 	crystal_rs = np.array(crystal_rs)
# 	water_in_crystal_rs = np.array(water_in_crystal_rs,dtype=object)

# 	r_SiOH = N_SiOH/N_Si
# 	r_CaOH = (N_Oh-N_SiOH)/N_Ca
# 	if N_braket != 2*N_SUD:
# 		MCL =  (N_braket+N_SUD)/(0.5*N_braket-N_SUD)
# 	else:
# 		MCL = 0

# 	return shape, crystal_rs, water_in_crystal_rs, N_Ca, N_Si, r_SiOH, r_CaOH, MCL





def read_brick(shape_read, brick_code, water_code, pieces, surface_from_bulk):

	shape = shape_read

	if surface_from_bulk:
		shape = ( shape[0], shape[1], shape[2]+2 )

		new_brick_code = dict()
		new_water_code = dict()

		for cell in brick_code.keys():
			key = (cell[0], cell[1], cell[2]+1)
			new_brick_code[key] = brick_code[cell]
			new_water_code[key] = water_code[cell]

		for i in range(shape[0]):
			for j in range(shape[1]):
				new_brick_code[(i,j,0)] = ["<Lo", "<Ro"]
				new_brick_code[(i,j,shape[2]-1)] = [">Lo", ">Ro"]

				new_water_code[(i,j,0)] = []
				new_water_code[(i,j,shape[2]-1)] = []

		brick_code = new_brick_code
		water_code = new_water_code


	N_brick = shape[0]*shape[1]*shape[2]

	crystal_rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]

	water_in_crystal_rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]

	N_Si = 0
	N_Ca = 0
	N_SiOH = 0
	N_Oh = 0
	N_braket = 0
	N_SUD = 0
	Q = 0

	ind = 0
	for cell in ( brick_code ):

		b = Brick(brick_code[cell], pieces, ind)
		crystal_rs[cell[0]][cell[1]][cell[2]] = b

		Q += b.charge
		N_Si += b.N_Si
		N_Ca += b.N_Ca
		N_SiOH += b.N_SiOH
		N_Oh += b.N_Oh
		N_braket += b.N_braket
		N_SUD += b.N_SUD

		water_in_crystal_rs[cell[0]][cell[1]][cell[2]] = water_code[cell]

		ind += 1

	crystal_rs = np.array(crystal_rs)
	water_in_crystal_rs = np.array(water_in_crystal_rs,dtype=object)

	r_SiOH = N_SiOH/N_Si
	r_CaOH = (N_Oh-N_SiOH)/N_Ca
	if N_braket != 2*N_SUD:
		MCL =  (N_braket+N_SUD)/(0.5*N_braket-N_SUD)
	else:
		MCL = 0


	if Q != 0:
		print("CAUTION! Input brick is not neutral")

	return shape, crystal_rs, water_in_crystal_rs, N_Ca, N_Si, r_SiOH, r_CaOH, MCL