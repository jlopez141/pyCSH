import numpy as np
from mod_sample import *



def get_offset(N_samples, sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths):
	aux_SiOH = np.zeros(N_samples)
	aux_CaOH = np.zeros(N_samples)
	aux_MCL = np.zeros(N_samples)
	for isample in range(N_samples):
		crystal, N_Ca, N_Si, r_SiOH, r_CaOH, MCL,_,_ = sample_Ca_Si_ratio(sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths )

		aux_SiOH[isample] = r_SiOH
		aux_CaOH[isample] = r_CaOH
		aux_MCL[isample]  = MCL

	return exp_SiOH(Ca_Si_ratio)-np.mean(aux_SiOH), exp_CaOH(Ca_Si_ratio)-np.mean(aux_CaOH)


def check_SiOH_CaOH_MCL(sorted_bricks, widths, shape):

	compute_offset = True

	N_samples = 100
	W_Si_ratio = 0.0

	list_target_ratios = [0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.1]
	offset_SiOH = []
	offset_CaOH = []
	list_MCL = []

	N_brick = shape[0]*shape[1]*shape[2]

	if compute_offset:

		for Ca_Si_ratio in list_target_ratios:
			off_Si, off_Ca = get_offset(N_samples, sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths)
			
			offset_SiOH.append(off_Si)
			offset_CaOH.append(off_Ca)

	else:
		offset_SiOH = [0.0 for i in range(len(list_target_ratios))]
		offset_CaOH = [0.0 for i in range(len(list_target_ratios))]



	list_CaSi = []
	list_SiOH = []
	list_CaOH = []
	list_MCL = []


	ind = 0
	for Ca_Si_ratio in list_target_ratios:
		aux_CaSi = np.zeros(N_samples)
		aux_SiOH = np.zeros(N_samples)
		aux_CaOH = np.zeros(N_samples)
		aux_MCL = np.zeros(N_samples)
		for isample in range(N_samples):
			offset = [offset_SiOH[ind], offset_CaOH[ind]]
			crystal, N_Ca, N_Si, r_SiOH, r_CaOH, MCL,_,_ = sample_Ca_Si_ratio(sorted_bricks, Ca_Si_ratio, W_Si_ratio, N_brick, widths, offset=offset )

			aux_CaSi[isample] = N_Ca/N_Si
			aux_SiOH[isample] = r_SiOH
			aux_CaOH[isample] = r_CaOH
			aux_MCL[isample]  = MCL

		#print( Ca_Si_ratio, np.mean(aux_SiOH), np.mean(aux_CaOH), np.mean(aux_MCL) )
		list_CaSi.append( [np.mean(aux_CaSi), np.std(aux_CaSi)] )
		list_SiOH.append( [np.mean(aux_SiOH), np.std(aux_SiOH)] )
		list_CaOH.append( [np.mean(aux_CaOH), np.std(aux_CaOH)] )
		list_MCL.append( [np.mean(aux_MCL), np.std(aux_MCL)] )

		ind += 1


	# for i in range(len(list_ratios)):
	# 	print(list_ratios[i], offset_CaOH[i], offset_SiOH[i])

	with open( "check_exp.dat", "w" ) as f:
		for i in range( len(list_target_ratios) ):
			fmt = "{: 12.6f} {: 12.6f}   {: 12.6f} {: 12.6f}    {: 12.6f} {: 12.6f}     {: 12.6f} {: 12.6f}  \n"
			f.write( fmt.format(*list_CaSi[i], *list_SiOH[i], *list_CaOH[i], *list_MCL[i]) )

