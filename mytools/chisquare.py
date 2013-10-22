def chisquare(observe,expect,error,ddof):
	for i,el in enumerate(observe):
		chisq = chisq + np.power((el-expect[i])/error[i],2)

	red_chisq = chisq[0]/(observe.shape[1]-ddof)
	print 'Chi-Squared is {}.'.format(chisq)
	print 'Reduced Chi-Squared is {}.'.format(red_chisq)

	return red_chisq
