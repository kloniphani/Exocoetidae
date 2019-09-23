from pandas import *
from numpy import * 

from datetime import datetime

import progressbar
import matplotlib.pyplot as plt

linestyle = [(0, (1, 10)),
     (0, (1, 1)),
     (0, (1, 1)),

     (0, (5, 10)),
     (0, (5, 5)),
     (0, (5, 1)),

     (0, (3, 10, 1, 10)),
     (0, (3, 5, 1, 5)),
     (0, (3, 1, 1, 1)),

     (0, (3, 5, 1, 5, 1, 5)),
     (0, (3, 10, 1, 10, 1, 10)),
     (0, (3, 1, 1, 1, 1, 1))]


Scenarios = ['Mopani - UAV',	'Vhembe - UAV',	'Waterberg - UAV',	'Chris-Hani - UAV',	'Frances Baard - UAV',	'Soweto - UAV',	'Khayelitsha - UAV',	'Lulekani - UAV',	'Zeerust - UAV',	'Duduza - UAV',	'Hlankomo - UAV',	'Mandileni - UAV',	'Gon’on’o - UAV']
Scenarios = ['Mopani', 'Vhembe', 'Waterberg', 'Chris-Hani',	'Frances Baard', 'Soweto', 'Khayelitsha', 'Lulekani', 'Zeerust', 'Duduza', 'Hlankomo', 'Mandileni', 'Gon’on’o']

Nu = [1092507,1294722,679336,795461,382086,1271628,391749,14464,9093,73295,3000,3500,5000]

CAPEX = [31214908.58, 39298642.8, 69284186.3, 56954892.77, 19703809.82, 13710804.56, 4303192.11, 65015.11, 49839.68, 783577.08, 1494.87, 1544.535, 2552.775]
OPEX = [196805.6456, 251735.4307, 441718.7702, 358062.477, 126244.603, 151100.0273, 46548.82468, 811.2667401, 562.1375837, 6956.4, 15.3, 15.3, 25.5]

NPV = []
From = 1; To = 2000
IRR = {'Counter' : [fee for fee in range(From, To)]}

DATA = {'Counter' : [fee for fee in range(From, To)]}
NumberOfTerms = 5
Rate = 0.05

Count = 0
with progressbar.ProgressBar(max_value = len(Scenarios)) as bar:
	fig, ax = plt.subplots()

	for Scenario in Scenarios:
		Terms = []	
		IRRTerms = []
		for fee in DATA['Counter']:
			CashFlow = []
			for term in range(NumberOfTerms):
				CashFlow.append((Nu[Count] * 12 * float(fee/1000)) - OPEX[Count])
			Terms.append(npv(Rate, CashFlow) - CAPEX[Count])

			Temp = []; Temp.append((CAPEX[Count]*-1)); 
			IRRTerms.append(round(log(irr(Temp + CashFlow)), 4) * 100)
			#print("{0:10} - Fee: {1:4} CASHFLOW: {2} NPV: {3:.2f} CAPEX: {4:.2f}".format(Scenario, fee, CashFlow[0], (npv(Rate, CashFlow) - CAPEX[Count]), CAPEX[Count]))
	
		line, = ax.plot(DATA['Counter'], IRRTerms , label='{0}'.format(Scenario))
		line.set_dashes([2, Count, 10, Count])
				
		Count += 1 
		DATA[Scenario] = Terms
		IRR[Scenario] = IRRTerms
		bar.update(Count)
		
	ax.legend()
	plt.tight_layout()
	plt.show()

ScenariosB = ['Mopani - LC',	'Vhembe - LC',	'Waterberg - LC',	'Chris-Hani - LC',	'Frances Baard - LC',	'Soweto - LC',	'Khayelitsha - LC',	'Lulekani - LC',	'Zeerust - LC',	'Duduza - LC',	'Hlankomo - LC',	'Mandileni - LC',	'Gon’on’o - LC']
ScenariosB = ['Mopani', 'Vhembe', 'Waterberg', 'Chris-Hani',	'Frances Baard', 'Soweto', 'Khayelitsha', 'Lulekani', 'Zeerust', 'Duduza', 'Hlankomo', 'Mandileni', 'Gon’on’o']

CAPEX = [7326301.9, 8717395.05, 4412871.9, 5463614.4, 2544001.2, 15451051.75, 5026936.95, 85548.5, 55381.3,	922876.5, 1948.25, 2085.75, 4006.5]
OPEX = [24583.01562, 29134.99584, 15293.26007, 17906.00382, 8604.636077, 91562.15313, 28206.02029, 499.3243608, 336.7536387, 3480.75, 7.65, 7.65, 15.3]

Count = 0
NumberOfTerms = 10
with progressbar.ProgressBar(max_value = len(Scenarios)) as bar:
	for Scenario in ScenariosB:
		Terms = []	
		IRRTerms = []
		for fee in DATA['Counter']:
			CashFlow = []
			for term in range(NumberOfTerms):
				CashFlow.append((Nu[Count] * 12 * float(fee/1000)) - OPEX[Count])
			Terms.append(npv(Rate, CashFlow) - CAPEX[Count])

			Temp = []; Temp.append((CAPEX[Count]*-1)); 
			IRRTerms.append(irr(Temp + CashFlow))
			#print("{0:10} - Fee: {1:4} CASHFLOW: {2} NPV: {3:.2f} CAPEX: {4:.2f}".format(Scenario, fee, CashFlow[0], (npv(Rate, CashFlow) - CAPEX[Count]), CAPEX[Count]))
	
		Count += 1 
		DATA[Scenario] = Terms
		IRR[Scenario] = IRRTerms
		bar.update(Count)


ScenariosC = ['Mopani - H',	'Vhembe - H',	'Waterberg - H',	'Chris-Hani - H',	'Frances Baard - H',	'Soweto - H',	'Khayelitsha - H',	'Lulekani - H',	'Zeerust - H',	'Duduza - H',	'Hlankomo - H',	'Mandileni - H',	'Gon’on’o - H']
ScenariosC = ['Mopani', 'Vhembe', 'Waterberg', 'Chris-Hani',	'Frances Baard', 'Soweto', 'Khayelitsha', 'Lulekani', 'Zeerust', 'Duduza', 'Hlankomo', 'Mandileni', 'Gon’on’o']

CAPEX = [38307910.6, 48999907.2, 85979866.6, 69696300.2, 24573314.2, 1058134.6, 326386.3, 6051.65, 51933.2, 44673.2, 440.15, 440.15, 440.15]
OPEX = [209109.4224, 267473.2747, 469333.8781, 380447.6112, 134137.0871, 10275.94747, 3169.661471, 74.66012031, 597.2809625, 448.8, 5.1, 5.1, 5.1]

Count = 0
NumberOfTerms = 10
with progressbar.ProgressBar(max_value = len(Scenarios)) as bar:
	for Scenario in ScenariosC:
		Terms = []	
		IRRTerms = []
		for fee in DATA['Counter']:
			CashFlow = []
			for term in range(NumberOfTerms):
				CashFlow.append((Nu[Count] * 12 * float(fee/1000)) - OPEX[Count])
			Terms.append(npv(Rate, CashFlow) - CAPEX[Count])

			Temp = []; Temp.append((CAPEX[Count]*-1)); 
			IRRTerms.append(irr(Temp + CashFlow))
			#print("{0:10} - Fee: {1:4} CASHFLOW: {2} NPV: {3:.2f} CAPEX: {4:.2f}".format(Scenario, fee, CashFlow[0], (npv(Rate, CashFlow) - CAPEX[Count]), CAPEX[Count]))
	
		Count += 1 
		DATA[Scenario] = Terms
		IRR[Scenario] = IRRTerms
		bar.update(Count)



Columns = ['Counter'] + Scenarios + ScenariosB + ScenariosC
DataFrames = DataFrame(data = DATA, columns = Columns) #Create a Pandas dataframe from some data.
IRRDataFrames = DataFrame(data = IRR, columns = Columns)


Writer = ExcelWriter('./Model/Computed Data/Model NPV-IRR [{0}].xlsx'.format(datetime.now().strftime('%Y-%m-%d %H-%M')), engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
DataFrames.to_excel(Writer, index=False, sheet_name='NPV')
IRRDataFrames.to_excel(Writer, index=False, sheet_name='IRR')
Writer.save()