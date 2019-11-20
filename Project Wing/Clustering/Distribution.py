"""         
Authors:     Kloni Maluleke (Msc), kloniphani@gmail.com
Date:        December 10, 2017
Copyrights:  2017 ISAT, Department of Computer Science
             University of the Western Cape, Bellville, ZA
"""

from numpy import * 

class Distribution(object):
	"""description of class"""
	
	def LogNormal(ResidualEnergyMean = 9.5,
			ResidualEnergySigma = 0.5,
			ResidualEnergySize = 100000000,
			SNRMean =  2.5,
			SNRSigma = 0.6,
			SNRSize = 100000000,
			TelementrySize = 100000000,
			Size = None):
		"""
		"""
		if Size is not None:
			ResidualEnergySize = Size; SNRSize = Size, TelementrySize = Size

		return random.lognormal(ResidualEnergyMean, ResidualEnergySigma, ResidualEnergySize), random.lognormal(SNRMean, SNRSigma, SNRSize)
	
	def Normal(ResidualEnergyMean = 1340,
			ResidualEnergySigma = 428.547,
			ResidualEnergySize = 100000000,
			SNRMean =  -78,
			SNRSigma = 16.59,
			SNRSize = 100000000,
			TelementrySize = 100000000,
			Size = None):
		"""
		"""
		if Size is not None:
			ResidualEnergySize = Size; SNRSize = Size, TelementrySize = Size

		return random.normal(ResidualEnergyMean, ResidualEnergySigma, ResidualEnergySize), random.normal(SNRMean, SNRSigma, SNRSize)

	def Uniform(ResidualEnergyLow = 0,
			ResidualEnergyHigh = 2400,
			ResidualEnergySize = 100000000,
			SNRLow =  -160,
			SNRHigh = -20,
			SNRSize = 100000000,
			TelementrySize = 100000000,
			Size = None):
		"""
		"""
		if Size is not None:
			ResidualEnergySize = Size; SNRSize = Size, TelementrySize = Size

		return random.uniform(ResidualEnergyLow, ResidualEnergyHigh, ResidualEnergySize), random.uniform(SNRLow, SNRHigh, SNRSize)

	def ChiSquare(ResidualEnergyDF = 1340,
			ResidualEnergySize = 100000000,
			SNRDF=  20,
			SNRSize = 100000000,
			TelementrySize = 100000000,
			Size = None):
		"""
		"""
		if Size is not None:
			ResidualEnergySize = Size; SNRSize = Size, TelementrySize = Size

		return random.chisquare(ResidualEnergyDF, ResidualEnergySize), random.chisquare(SNRDF, SNRSize)
