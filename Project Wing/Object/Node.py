"""         
Authors:     Kloni Maluleke (Msc), kloniphani@gmail.com
             Emmanuel Tuyishimire (PHD), tuyinuel@gmail.com
Date:        August 31, 2017
Copyrights:  2017 ISAT, Department of Computer Science
             University of the Western Cape, Bellville, ZA
"""

#OOP CLASSES
from Source import API as api

#PACKAGES
import googlemaps

from numpy import *
from geopy import distance
from matplotlib import pyplot as plt
from scipy import constants as constants

class Node(object):
	"""     
	"""
	
	__nodeHeight = float(8); __headHeight = float(10); __hoopHeight = float(9); __memberHeight = float(7); __graphHeight = int(0)

	#INITIALISERS
	def __init__(self, Id, Address = None, Name = None, Provider = None, Position = None, SNR = None, RE = None, MeshNetwork = None, Results = False, Geocode = False):
		"""
		"""	

		if Address is None and Position is None:
			return None

		#NODE IDENTITY
		self.Id = Id; self.Name = Name; self.Type = None; NumberOfMembers = 0

		#CHAINING MEMBERS
		self.MEMBERS = []

		#NETWORK INFORMATION
		if SNR is not None:
			if SNR < 0:
				self.SNR = 0;
			else:
				self.SNR = SNR

		self.Gt = 10 #dBi
		self.Gr = 10 #dBi
		self.Pt = 20 #dBm
		self.Pr = -999 #dBm
		self.Tx = 0 ######
		self.Frequency = 5e5
		self.Channel = 1
		self.VRMS = 10
		self.Bandwidth = 10 #Mb/s

		#CONNECTED NODES
		self.LINKS = [];

		#TELEMETRY 		
		self.ResidualEnergy = random.choice(random.normal(12400, 0.1, 100000))
		if RE is not None:
			if RE < 0:
				self.ResidualEnergy = 0;
			else:
				self.ResidualEnergy = RE

		#COMPUTING THE NODE'S LOCATION
		self.Height = self.__nodeHeight
		self.gmaps = googlemaps.Client(key = api.Google().Geolocation)
		if Address is None and Geocode is True:
			self.Geocode = self.gmaps.reverse_geocode((Position[0], Position[1]))[0] 
			self.Address = self.Geocode['formatted_address']
			if Results is True: print("Address: {}\tPosition{}".format(self.Address, Position));
		else:
			self.Address = Address;
			if Geocode is True: self.Geocode = self.gmaps.geocode(Address)[0];

		if Position is None and Geocode is True:		
			self.Position = [self.Geocode['geometry']['location']['lat'], self.Geocode['geometry']['location']['lng'], self.Height]
		else:
			if len(Position) < 3:
				Position.append(self.Height)
			self.Position = Position
		self.Point = (self.Position[0], self.Position[1])
		self.GraphHeight = self.__graphHeight;
		self.GraphColor = 'red';

		#WIRELESS MESH NETWORK
		if MeshNetwork is not False:
			self.MESH = MeshNetwork;

		#COMPUTING SNR-To-LAP
		if SNR is not None:
			self.SNR = SNR
		elif Provider is not None:
			self.Provider = Provider
			self.SNR = self.ComputeSNR(self.Provider.Position)
		else:
			self.SNR = random.choice(random.normal(90, 0.01, 100000))

		#PRINTING RESULTS
		if Results is True:
			print("Created Node: {}\tPosition: {}\tSNR: {}\tRE: {}".format(self.Id, self.Position, self.SNR, self.ResidualEnergy))

	#FUNCTIONS
	def __str__(self):
		return ("Node:\t{},\tPosition:\t{},\tSignal-to-Noise Ratio:\t{},\tResidual Energy\t{},\tType:\t{}".format(self.Id, self.Position, self.SNR, self.ResidualEnergy, self.Type))

	def ComputePathLoss(self, Point, Gr):
		"""
		"""
		return ((20*(log10(distance.vincenty((self.Position[0], self.Position[1]),(Point[0], Point[1])).kilometers) + (
			log10(self.Frequency) + log10((4*constants.pi)/constants.c)))) - self.Gt - Gr)

	def ComputeFriisTransmission(self, Point, WaveLength = None):
		"""
		"""
		if WaveLength is None:
			value, unit, uncertainty = constants.physical_constants['Compton wavelength']
			WaveLength = value
		return (self.Pt + self.Gt + self.Gr + (20*log10(WaveLength/(4*constants.pi*(distance.vincenty((self.Position[0], self.Position[1]),(Point[0], Point[1])))))))

	def ChangeToBaseStation(self, Results = False):
		"""
		"""
		self.Type = -2
		self.Height = self.__headHeight
		self.Position[2] = self.Height

		#CLUSTER HEADS
		self.CLUSTERHEADS = []

		if Results is True:
			print("Node: {} Changed to be Cluster head".format(self.Id))

	def ChangeToClusterHead(self, Results = False):
		"""
		"""
		self.Type = -1
		self.Height = self.__headHeight
		self.Position[2] = self.Height

		if Results is True:
			print("Node: {} Changed to be Cluster head".format(self.Id))

	def ChangeToNode(self, Results = False):
		"""
		"""
		self.Type = 1
		self.Height = self.__nodeHeight
		self.Position[2] = self.Height
		self.Head = None

		if 'MEMBERS' in locals() or 'MEMBERS' in globals():
			for node in MEMBERS:
				node.ChangeToNode(Results = Results)
			self.MEMBERS.clear() #Removing Cluster Members

		if Results is True:
			print("Node: {} Changed to be Normal Node".format(self.Id))

	def ChangeToRoot(self, Results = False):
		self.Type = -1;
		self.SINKPATHS = []

	def ChangeToClusterMember(self, Head):
		self.Head = Head; 
		if self.Type != -1 and self.Type != -2 and self.Type != 2:
			self.Type = 0;
		self.Height = self.__memberHeight; self.Position[2] = self.Height

	def SetGraphHeight(self, Height):
		self.GraphHeight = Height;

	def SetGraphColor(self, Color):
		self.GraphColor = Color;

	def ChangeToChainNode(self, Results = False):
		if self.Type != -1 and self.Type != -2:
			self.Type = 2

		if Results is True:
			print("Node: {} Changed to be Chaining Node".format(self.Id))

	def AddMember(self, Node):
		if self.Type == None: self.Type = 1;
		if Node not in self.MEMBERS:
			self.MEMBERS.append(Node);
	
	def AddPath(self, Path):
		self.SINKPATHS.append(Path);
		

	def SetHoopHead(self, Head):
		self.Head = Head;  
		if self.Type == None or self.Type == 0:
			self.Type = 3;
	
	def Hoops(self):
		self.Hoops = 0

		if hasattr(self, 'Head'):
			node = self.Head
			while True:
				self.Hoops += 1
				try:
					node = node.Head
				except:
					return self.Hoops	
				
	def RemoveMember(self, Node, Results = False):
		try:
			self.MEMBERS.remove(Node)
			if Results is True: print('Node: #{} was SUCESSFULLY Deleted from the List'.format(Node.Id))
		except:
			print('Failed to delete Node: {}'.format(Node))
	
	def Position(self, Point):
		"""
		"""
		if len(self.Position) is not len(Point): return False
		for i in range(len(Point)):
			if self.Position[i] != Point[i]: return False
		return True

	def setPosition(self, Position, Results = False):
		self.Position = Position;
		self.Point = (Position[0], Position[1])

	def Distance(self, Point, Type = '2D', Results = False):
		"""
		"""
		Adjecent = distance.vincenty((self.Position[0], self.Position[1]),(Point[0], Point[1])).kilometers
		Opposite = abs(self.Position[2] - Point[2])
		Hypotenuse = sqrt(square(Adjecent) + square(Opposite))

		#PRINTING THE RESULTS
		if Results is True:
			print("Distance: {0:8f}\tAdject: {1:8f}\tOpposite: {2:8f}".format(Hypotenuse, Adjecent, Opposite))

		if Type is '2D': return Adjecent
		else: return Hypotenuse

	def addLink(self, Node, Link, Results = False):
		"""
		"""
		self.LINKS.append({str(Node.Id):Node, 'link':Link})

		#PRINTING THE RESULTS
		if Results is True:
			print("Node: {0:8f}\tLink: {1:8f}".format(Node.Id, Link))

	def ReferenceDistance(self, Point):
		"""
		"""
		Vincenty = distance.vincenty((self.Position[0], self.Position[1]),(Point[0], Point[1])).kilometers
		GreatCircle = distance.great_circle((self.Position[0], self.Position[1]),(Point[0], Point[1])).kilometers
		return (Vincenty + GreatCircle)/2

	#CALCULATING THE SIGNAL TO NOISE RATIO
	def FadingModel(self, Time = 1, Graphs = False, Results = False):
		"""
		"""
		from scipy.stats import rice
		from scipy import integrate

		#CALCULATING THE RICE CONTINUOUS DISTIBUTION
		shape = 0.775
		#MeanPowerGain = (1/Time) * integrate(pow(rice.logcdf(t, shape), 2), (t, 0, Time))
		h = lambda x: pow(rice.logpdf(x, shape), 2)
		MeanPowerGain, err = integrate.quad(h, 0, Time)

		#PLOTING THE PROBABILITY DENSITY FUNCTION
		if Graphs is True:
			fig, ax = plt.subplots(1, 1)
			x = linspace(rice.ppf(0.01, shape), rice.ppf(0.99, shape), 100)
			ax.plot(x, rice.pdf(x, shape), 'r-', lw = 5, alpha = 0.6, label = 'Rice PDF')

			rv = rice(shape)
			ax.plot(x, rv.pdf(x), 'k-', lw = 2, label = 'Frozen PDF')

			r = rice.rvs(shape, size=1000)
			ax.hist(r, normed=True, histtype='stepfilled', alpha=0.2)
			ax.legend(loc='best', frameon=False)
		
		#PRINTING RESULTS
		if Results is True:
			print("Fading - Mean Power Gain: {}".format((1/Time) * MeanPowerGain))
		return (1/Time) * MeanPowerGain

	def PeriodogramPowerSpectralDensity(self, TimeSeries = 1, Graphs = False, Results = False):
		"""
		"""
		from scipy import signal
		from scipy import integrate

		#GENERATING TEST SIGNAL
		random.seed(int(self.Frequency))
		fs = 5.2e3 # Sampling Frequency
		N = 1e5
		amp = self.VRMS * sqrt(self.VRMS)
		NoisePower = 0.001 * self.Frequency/self.VRMS		
		time = arange(N) / fs

		x = amp*sin(self.VRMS * pi * self.Frequency * time)
		x += random.normal(scale=sqrt(NoisePower), size=time.shape)

		#COMPUTE AND PLOT THE POWER SPECTRAL DENSITY
		f, Pxx_den = signal.periodogram(x, fs)
		if Graphs is True:
			plt.figure(1)
			plt.semilogy(f, Pxx_den)
			plt.ylim([1e-7, 1e2])
			plt.xlabel('Frequency in Hz')
			plt.ylabel('PSD (V^2/Hz)')

		#COMPUTE AND PLT POWER SPECTRUM
		f, Pxx_spec = signal.periodogram(x, fs, 'flattop', scaling='spectrum')
		if Graphs is True:
			plt.figure(2)
			plt.semilogy(f, sqrt(Pxx_spec))
			plt.ylim([1e-4, 1e1])
			plt.xlabel('Frequency in Hz')
			plt.ylabel('Linear spectrum in V RMS')
		
		#PRINTING RESULTS
		if Results is True:
			print("Power Spectral Density - Peak: {}\t Mean: {}".format(sqrt(Pxx_spec.max()), mean(Pxx_den[25000:])))

		#The peak height and mean in the power spectrum is an estimate of the RMS amplitude.
		return [sqrt(Pxx_spec.max()), mean(Pxx_den[25000:])]

	def ComputeProportionPathLoss(self, Point, Proportion = 1, Results = False):
		"""
		"""
		SpeedOfLight = 3 * power(10, 8) #m/s
		FreeSpacePathLoss = power(4 * pi 	* self.Frequency * self.ReferenceDistance(Point), 2)/SpeedOfLight
		ProportionDistance = power((self.Distance(Point)/self.ReferenceDistance(Point)), Proportion)

		#PRINTING THE RESULTS
		if Results is True:
			print("Path Loss: {}".format(FreeSpacePathLoss * ProportionDistance))

		return FreeSpacePathLoss * ProportionDistance

	def ComputeBitEnergy(self, Point, PartialDifferential = 6e8, Results = False):
		"""
		PartialDifferential = Bits per second
		"""
		try:
			BE = (self.Pt * self.Gt * self.Gr)/float(PartialDifferential * self.Distance(Point, Results = Results))
		except ZeroDivisionError:
			BE = 0

		#PRINTING THE RESULTS
		if Results is True:
			print("Bit Energy: {}".format(BE))

		return BE

	def ComputeSNR(self, Point, Results = False):
		"""
		"""
		BitEnergy = self.ComputeBitEnergy(Point, Results = Results) 
		MeanPowerGain = self.FadingModel(Results = Results)
		PowerSpectralDensity = self.PeriodogramPowerSpectralDensity(Results = Results)[1] #Selected the Mean

		Computed_SNR = (BitEnergy * MeanPowerGain)/PowerSpectralDensity
		#PRINTING THE RESULTS
		if Results is True:
			print("SNR: {0}".format(Computed_SNR))

		return Computed_SNR

	def GenerateTransmittedSignal(self, Size = 256, Graph = False, Results = False):
		"""
		"""
		from scipy import signal
		Signal = repeat([0., 1., 1., 0., 1., 0., 0., 1.], Size)
		SignalNoise = Signal + random.randn(len(Signal))

		if Graph is True:
			clock = arange(64, len(Signal), Size)
			fig, (ax_orig, ax_noise) = plt.subplots(2, 1, sharex = True)
			ax_orig.plot(Signal)
			ax_orig.plot(clock, Signal[clock], 'ro')
			ax_orig.set_title('Original Signal')
			ax_noise.plot(SignalNoise)
			ax_noise.set_title('Signal with Noise')
			ax_orig.margins(0, 0.1)
			fig.tight_layout()
			fig.show()

		return Signal, SignalNoise

	def ComputeRS(self, Point, Results = False):
		"""
		Compute Recieved Signal
		"""
		from scipy import signal

		d = sqrt(self.Distance(Point))
		FadingModel = self.FadingModel(Results = Results)
		Noise = random.choice(signal.gaussian(100, std = 5))

		#Generate the Transmitted Signal
		Signal, NoiseSignal = self.GenerateTransmittedSignal(Results = Results)

		Tx = random.choice(NoiseSignal)
		RS = ((FadingModel * Tx)/d) + Noise

		if Results is True:
			print("Corresponding Received Signal: {}".format(RS))

		return RS

	def EnergyConsumption(self, Bandwidth = None, Pt = None, Prcv = 100, Nbpp = 200, Npkt = 10000,  Results = False, ReduceEnergy = True):
		"""
		@Pt: float - Transmission Power
		@Prcv: float - Power required at the receiver for receiving the data, mW
		@Nbpp: int - Number of bits per packet
		@Npkt: int - Total number of transmitted packets
		"""
		if Bandwidth is None:
			Bandwidth = self.Bandwidth
		if Pt is None:
			Pt = self.Pt

		e = ((Pt * Prcv)/Bandwidth) * Nbpp * Npkt
		if Results is True:
			print("Energy Consumption: {}\t Residual Energy: {}\t New Power: {}".format((e/1e7), self.ResidualEnergy, (self.ResidualEnergy - (e/1e7))))

		if ReduceEnergy is True:
			self.ResidualEnergy -= e/1e7
		else:
			return e

	def DelayEnergyConsumption(self, Delay = 5, Results = False):
		"""
		"""
		import time

		print("Delay Energy: {}".format(self.Id))
		while(self.ResidualEnergy > 0):
			time.sleep(random.randint(Delay))
			self.EnergyConsumption

		if Results is True:
			print("!Node: {} Does not have Residual Energy".format(self.Id))

	def ShowGraphs(self):
		"""
		"""
		plt.show();

	def ComputeLinkBudget(self, Point, Results = False):
		"""
		@Pout = power at the received in dBm
		@Pt = power at the transmitter in dBm
		@Gt, @Gr = gains of the transmit and receive antennas respectively
		@Lt, @Lr = losses at the transmit and receive circuits respectively
		@Lfs = free space path loss = 20log10d+20log10f+32.44
		"""

		Pt = self.Pt
		Gt = self.Gt
		Gr = float(self.ComputeRS(Point = Point, Results = Results))
		Lt = 3
		Lr = 2
		Lm = self.FadingModel(Results = Results);
		Lfs = float(self.ComputePathLoss(Point = Point, Gr = Gr))

		Pr = Pt + Gt - Lt - Lfs - Lm + Gr - Lr
		
		if Results is True:
			print("Pt: {0}\tGt: {1}\tLt: {2}\tLfs: {3}\tLm: {4}\tGr: {5}\tLr:{6}\t|Pr: {7}".format(Pt, Gt, Lt, Lfs, Lm, Gr, Lr, Pr))

		return Pr



	def ConfigureNetwork(self, SNR = None, Gt = None, Gr = None, Pt = None, Pr = None, Frequency = None, Channel = None, VRMS = None, Results = False):
		"""
		"""
		if SNR is not None: 
			self.SNR = SNR
			if Results is True:
				print("'SNR' Has Been Changed on Node: {}\t To: {} ".format(self.Id, self.SNR))

		if Gt is not None: 
			self.Gt = Gt
			if Results is True:
				print("'Gt' Has Been Changed on Node: {}\t To: {} ".format(self.Id, self.Gt))

		if Gr is not None: 
			self.Gr = Gr
			if Results is True:
				print("'Gr' Has Been Changed on Node: {}\t To: {} ".format(self.Id, self.Gr))

		if Pt is not None: 
			self.Pt = Pt
			if Results is True:
				print("'Pt' Has Been Changed on Node: {}\t To: {} ".format(self.Id, self.Pt))

		if Pr is not None: 
			self.Pr = Pr
			if Results is True:
				print("'Pr' Has Been Changed on Node: {}\t To: {} ".format(self.Id, self.Pr))

		if Frequency is not None: 
			self.Frequency = Frequency;
			if Results is True:
				print("'Frequency' Has Been Changed on Node: {}\t To: {} ".format(self.Id, self.Frequency))

		if Channel is not None: 
			self.Channel = Channel
			if Results is True:
				print("'Channel' Has Been Changed on Node: {}\t To: {} ".format(self.Id, self.Channel))

		if VRMS is not None: 
			self.VRMS = VRMS
			if Results is True:
				print("'VRMS' Has Been Changed on Node: {}\t To: {} ".format(self.Id, self.VRMS))		

