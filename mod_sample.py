import numpy as np


def sample_Ca_Si_ratio(sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths, offset=[0.0,0.0]):
	

	width_Ca_Si = widths[0]
	width_SiOH = widths[1]
	width_CaOH = widths[2]

	keys_Ca_Si = np.array(list(sorted_bricks.keys()))

	brick_Ca_Si = 0.0
	brick_Q = 0.0
	brick_SiOH = 0.0
	brick_CaOH = 0.0

	crystal= []#_rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]

	N_Si = 0
	N_Ca = 0
	N_SiO = 0
	N_SiOH = 0
	N_Oh = 0

	N_braket = 0
	N_SUD = 0

	cont = 0
	while True:
		while len(crystal) != N_brick:

			u1 = np.random.normal(loc = Ca_Si_ratio, scale = width_Ca_Si)
			ind_Ca_Si = np.argmin( np.abs( keys_Ca_Si-u1 ) )
			key_Ca_Si = keys_Ca_Si[ind_Ca_Si]


			keys_Q = np.array( list( sorted_bricks[key_Ca_Si].keys() ) )
			u2 = np.random.normal(loc = 0.0, scale = 1.0)
			ind_Q = np.argmin( np.abs( keys_Q-u2 ) )
			key_Q = keys_Q[ind_Q]


			keys_SiOH = np.array( list( sorted_bricks[key_Ca_Si][key_Q].keys() ) )
			u3 = np.random.normal(loc = exp_SiOH(key_Ca_Si)+offset[0], scale = width_SiOH)
			ind_SiOH = np.argmin( np.abs( keys_SiOH-u3 ) )
			key_SiOH = keys_SiOH[ind_SiOH]


			keys_CaOH = np.array( list( sorted_bricks[key_Ca_Si][key_Q][key_SiOH].keys() ) )
			u4 = np.random.normal(loc = exp_CaOH(key_Ca_Si)+offset[1], scale = width_CaOH)
			ind_CaOH = np.argmin( np.abs( keys_CaOH-u4 ) )
			key_CaOH = keys_CaOH[ind_CaOH]



			if abs(key_Q - u2) < 1.0 and abs(key_SiOH-u3)<0.3 and abs(key_CaOH-u4)<0.3:

				ind = np.random.randint(len(sorted_bricks[key_Ca_Si][key_Q][key_SiOH][key_CaOH]))

				crystal.append( sorted_bricks[key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind] )

				N_Ca += sorted_bricks[key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_Ca
				N_Si += sorted_bricks[key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_Si
				N_SiO += sorted_bricks[key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_SiO
				N_SiOH += sorted_bricks[key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_SiOH
				N_Oh += sorted_bricks[key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_Oh

				N_braket += sorted_bricks[key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_braket	
				N_SUD += sorted_bricks[key_Ca_Si][key_Q][key_SiOH][key_CaOH][ind].N_SUD

				brick_Ca_Si += keys_Ca_Si[ind_Ca_Si]
				brick_Q += keys_Q[ind_Q]


		if brick_Q == 0:
			list_elegible_water = np.array([ len(crystal[i_brick].elegible_water) for i_brick in range(N_brick) ])
			N_water = int(np.rint(N_Si * W_Si_ratio))
			r_2H_Si = W_Si_ratio + 0.5*N_Oh/N_Si

			if np.sum(list_elegible_water) >= N_water:
				break
			elif np.sum(list_elegible_water) >= N_water-1:
				N_water-= 1
				break
			else:
				brick_Ca_Si = 0.0
				brick_Q = 0.0
				crystal = []#_rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]
				N_Si = 0
				N_Ca = 0
				N_SiOH = 0
				N_SiO = 0
				N_braket = 0
				N_SUD = 0
				N_Oh = 0
			
				cont += 1

				if cont >= 5000:
					print("Could not find any structure")
					break

		else:
			brick_Ca_Si = 0.0
			brick_Q = 0.0
			crystal = []#_rs = [ [ [ 0 for k in range(shape[2]) ] for j in range(shape[1]) ] for i in range(shape[0]) ]
			N_Si = 0
			N_Ca = 0
			N_SiOH = 0
			N_SiO = 0
			N_braket = 0
			N_SUD = 0
			N_Oh = 0
		
			cont += 1

			if cont >= 5000:
				print("Could not find any structure")
				break


	r_SiOH = N_SiOH/N_Si
	r_CaOH = (N_Oh-N_SiOH)/N_Ca
	if N_braket != 2*N_SUD:
		MCL =  (N_braket+N_SUD)/(0.5*N_braket-N_SUD)
	else:
		MCL = 0

	return crystal, N_Ca, N_Si, r_SiOH, r_CaOH, MCL, N_water, r_2H_Si



def exp_SiOH(Ca_Si):
	return  0.82 -0.43*Ca_Si
	# return (15-7*Ca_Si)/16

def exp_CaOH(Ca_Si):
	return -0.6 + 0.65*Ca_Si
	# return (5*Ca_Si-4)/9

	



# def fill_water(crystal, N_water):
# 	N_brick = len(crystal)

# 	N_left = N_water
# 	water_distr = np.zeros(N_brick,dtype=int)
# 	list_elegible_water = np.array([ len(crystal[i_brick].elegible_water) for i_brick in range(N_brick) ])
# 	list_elegible_brick = np.array( [True for i in range(N_brick)] )

# 	cont = 0
# 	water_in_crystal = None
# 	while N_left != 0:
# 		#Randomly distribute water 
# 		new_distr = np.random.rand(N_brick) * list_elegible_brick
# 		new_distr = np.rint( new_distr/sum(new_distr) * N_left )
# 		new_distr = new_distr.astype(int)


# 		water_distr += new_distr


# 		# Check if more water tahn intended
# 		while np.sum(water_distr) > N_water:
# 			ind = np.where( water_distr > 0 )[0][0]
# 			water_distr[ind] -= 1


# 		# Check if any brick contains more water than allowed
# 		aux = list_elegible_water - water_distr
# 		aux2 = aux < 0

# 		N_left = N_water - np.sum(water_distr) - np.sum( aux*aux2 )

# 		water_distr += aux*aux2

# 		# Elegible bricks for the next iteration
# 		list_elegible_brick = water_distr < list_elegible_water


# 		cont += 1


# 		# When only a few left insert manually
# 		if N_left <= 5 and N_left != 0:
# 			ind = np.random.choice(np.where( list_elegible_brick == True )[0])

# 			water_distr[ind] += 1
# 			N_left -= 1

# 			list_elegible_brick = water_distr < list_elegible_water

# 		if cont == 100:
# 			print("breaking!!")
# 			print( N_water, N_left )
# 			print(water_distr)
# 			print(list_elegible_water)
# 			print(list_elegible_brick)
# 			break

# 	# Fill each brick
# 	water_in_crystal = []
# 	for i_brick in range(N_brick):
# 		aux = np.random.choice( crystal[i_brick].elegible_water, size=water_distr[i_brick], replace=False )

# 		water_in_crystal.append( list(aux) )


# 	return water_in_crystal



def fill_water(crystal, N_water):

	N_brick = len(crystal)
	water_distr = np.zeros(N_brick,dtype=int)

	N_elegible_brick = N_brick
	N_left = N_water
	list_elegible_water = np.array([ len(crystal[i_brick].elegible_water) for i_brick in range(N_brick) ])
	list_elegible_brick = np.array( [True for i in range(N_brick)] )

	while N_left != 0:
		aux = (list_elegible_water - water_distr)*list_elegible_brick
		N_try = np.min( aux[np.nonzero(aux)] )


		if N_try*N_elegible_brick <= N_left:
			add = np.ones(N_brick,  dtype=int)*N_try * list_elegible_brick

			water_distr += add

			N_left = N_water - np.sum(water_distr)
			list_elegible_brick = water_distr < list_elegible_water
			N_elegible_brick = np.sum(list_elegible_brick)


		else:
			for i in range(N_brick):
				if list_elegible_brick[i]:
					water_distr[i] += 1
					N_left -= 1

					if N_left == 0:
						break

	# Fill each brick
	water_in_crystal = []
	for i_brick in range(N_brick):
		aux = np.random.choice( crystal[i_brick].elegible_water, size=water_distr[i_brick], replace=False )

		water_in_crystal.append( list(aux) )


	return water_in_crystal

