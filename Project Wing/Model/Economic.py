from pandas import *
from numpy import * 

from datetime import datetime

import progressbar

Scenarios = ['Mopani - UAV',	'Vhembe - UAV',	'Waterberg - UAV',	'Chris-Hani - UAV',	'Frances Baard - UAV',	'Soweto - UAV',	'Khayelitsha - UAV',	'Lulekani - UAV',	'Zeerust - UAV',	'Duduza - UAV',	'Hlankomo - UAV',	'Mandileni - UAV',	'Gon’on’o - UAV']

Nu = [1092507,1294722,679336,795461,382086,1271628,391749,14464,9093,73295,3000,3500,5000]

CAPEX = [6707132.325,7762783.275,4047942.195,4906942.56,2266673.31,13866920.96,4303192.11,65015.11,48514.6,783577.08,1494.87,1544.535,2552.775]

OPEX = [3869445.224,4585941.458,2405989.48,2817243.696,1353787.953,14411566.26,4439717.737,77376.71916,51787.56794,6956.4,15.3,15.3,25.5]

NPV = []
From = 0; To = 1500
IRR = {'Counter' : [fee for fee in range(From, To)]}

DATA = {'Counter' : [fee for fee in range(From, To)]}
NumberOfTerms = 5
Rate = 0.05

Count = 0
with progressbar.ProgressBar(max_value = len(Scenarios)) as bar:
	for Scenario in Scenarios:
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

ScenariosB = ['Mopani - LC',	'Vhembe - LC',	'Waterberg - LC',	'Chris-Hani - LC',	'Frances Baard - LC',	'Soweto - LC',	'Khayelitsha - LC',	'Lulekani - LC',	'Zeerust - LC',	'Duduza - LC',	'Hlankomo - LC',	'Mandileni - LC',	'Gon’on’o - LC']

CAPEX = [7748855.1,8873203.95,4494657.6,5835005.1,2590017.3,15940710.25,5177777.85,88218.8,57182.2,951132,2010.35,2147.85,4130.7]

OPEX = [4013087.314,4756181.423,2496568.726,2923089.579,1404675.342,14947186.34,4604529.564,81512.87412,54973.79883,3480.75,7.65,7.65,15.3]

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

CAPEX = [7748855.1,8873203.95,4494657.6,5835005.1,2590017.3,15940710.25,5177777.85,88218.8,57182.2,951132,2010.35,2147.85,4130.7]

OPEX = [4013087.314,4756181.423,2496568.726,2923089.579,1404675.342,14947186.34,4604529.564,81512.87412,54973.79883,3480.75,7.65,7.65,15.3]

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


Writer = ExcelWriter('./Model/Computed Data/Model-{0}.xlsx'.format(datetime.now().strftime('%Y-%m-%d %H-%M')), engine='xlsxwriter') #Create a Pandas Excel writer using XlsxWriter as the engine.
DataFrames.to_excel(Writer, index=False, sheet_name='NPV')
IRRDataFrames.to_excel(Writer, index=False, sheet_name='IRR')
Writer.save()