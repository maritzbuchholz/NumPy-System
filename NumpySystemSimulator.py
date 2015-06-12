###Runs Donchian trading system against SPY ETF data from Yahoo!

import numpy as np

###FUNCTIONS###
##########################################################################################
##########################################################################################



###Data Functions###
def format_yahoo_daily_data():
	data = np.genfromtxt("http://real-chart.finance.yahoo.com/table.csv?s=SPY&d=1&e=5&f=2015&g=d&a=0&b=29&c=1993&ignore=.csv",  dtype="string", delimiter=",", skip_header = 1, usecols = (range(0,7)))

	for row in data:
		row[0] = row[0].replace("-", "")

	data = data.astype(float)
	return data

def abs_percent_change(data, input_loc, loc):
	for i in range(data.shape[0]):
		try:
			data[i][loc] = abs( (data [i][input_loc] - data [i + 1][input_loc]) / data [i + 1][input_loc] )
		except IndexError:
			pass

def stdev(data, input_loc, days, loc):
	for i in range(data.shape[0]):
		try:
			section = []
			for j in range(days):
				section.append(data [i + j][input_loc])
			
			data[i][loc] = np.std(section, ddof=1)
		
		except IndexError:
			pass

def sma(data, input_loc, days, loc):
	for i in range(data.shape[0]):
		try:
			section = []
			for j in range(days):
				section.append(data [i + j][input_loc])
			
			data[i][loc] = np.mean(section)
			
		except IndexError:
			pass

def true_range(data, loc):
	for i in range(data.shape[0]):	
		try:
			data[i][loc] = max(data[i][high]-data[i][low], abs(data[i][high] - data[i + 1][close]), abs(data[i][low] - data[i + 1][close]))
		except IndexError:
			pass
		
def atr(data, days, loc):
	for i in range(data.shape[0]):
		try:
			true_range = 0
			for j in range(days):
				true_range += max(data[i + j][high]-data[i + j][low], abs(data[i][high] - data[i + j + 1][close]), abs(data[i + j][low] - data[i + j + 1][close]))

			data[i][loc] = true_range / j	
		except IndexError:
			pass

def maximum(data, input_loc, days, loc):
	for i in range(data.shape[0]):
		try:
			values =[]
			for j in range(days):
				values.append(data[i + j][input_loc])
			
			data[i][loc] = max(values)
		except IndexError:	
			pass
			
def minimum(data, input_loc, days, loc):
	for i in range(data.shape[0]):
		try:
			values =[]
			for j in range(days):
				values.append(data[i + j][input_loc])
			
			data[i][loc] = min(values)
		except IndexError:	
			pass

		
def returns(data, entry, exit, loc):
	for i in range(data.shape[0]):
		data[i][loc] = (data[i][entry] - data[i][exit]) / data[i][entry]


def cum_returns(data, input_loc):
	cumulative = data[0][input_loc]
	for i in range(data.shape[0]):
		try:
			cumulative *= (1.0 + data[i + 1][input_loc])
		except IndexError:
			pass
	return cumulative
	
		
			
###Trading Functions###
def initiate(data):
	position = None
	if data[i][close] > data[i + 1][close]:
		pos_dir.append(1)
		position = True
	elif data[i][close] < data[i + 1][close]:
		pos_dir.append(-1)
		position = True
	elif data[i][close] == data[i + 1][close]:
		position = False
	else:
		exit("mistake1")
	
	if position == True:
		pos_size.append(1)
		entry_date.append(data[i][date])
		entry_price.append(data[i][close])
	elif position == False:
		pass
	else:
		exit("mistake2")
	
	return position

	
def loss(data, direction):
	if in_pos <= 3:
		shift = 1
	elif in_pos > 3:
		shift = 0
	else:
		exit("whoops")
		
	if direction[-1] == 1:
		if data[i][open] < data[j][close] * (1 - data[j][changem14] * shift):
			exit_price.append(data[i][open])
			exit_date.append(data[i][date])
			return False
		elif data[i][close] < data[j][close] * (1 - data[j][changem14] * shift):
			exit_price.append(data[i][close])
			exit_date.append(data[i][date])
			return False
			
		else:
			return True
	
	elif direction[-1] == -1:
		if data[i][open] > data[j][close] * (1 + data[j][changem14] * shift):
			exit_price.append(data[i][open])
			exit_date.append(data[i][date])
			return False
		elif data[i][close] > data[j][close] * (1 + data[j][changem14] * shift):
			exit_price.append(data[i][close])
			exit_date.append(data[i][date])
			return False
		else:	
			return True
	
	else:
		exit("too bad")
				

def profit(data, direction):
	if direction[-1] == 1:
		if data[i][sma5] < data[i][sma7]:
			exit_price.append(data[i][close])
			exit_date.append(data[i][date])
			return False
		else:
			return True
	elif direction[-1] == -1:
		if data[i][sma5] > data[i][sma7]:
			exit_price.append(data[i][close])
			exit_date.append(data[i][date])
			return False
		else:
			return True


###RUN###
##########################################################################################
##########################################################################################




##########DATA##########

##Build Working Data Matrix Skeleton###
raw_data = format_yahoo_daily_data()

working_data = np.zeros([raw_data.shape[0], 13])
working_data[:, :-6] = raw_data
###Location of Data/Statistics by Column###
#Data#
date = 0 #(YYYYMMDD)
open = 1
high = 2
low = 3
close = 4
vol = 5
adj_close = 6
#Stats#
change = 7
changem14 = 8
sma5 = 9
sma7 = 10
max_high7 = 11
min_low7 = 12


###Calculate Statistics and Input into Working Data Matrix###
abs_percent_change(working_data, close, change)
sma(working_data, change, 14, changem14)
sma(working_data, close, 5, sma5)
sma(working_data, close, 7, sma7)
maximum(working_data, high, 7, max_high7)
minimum(working_data, low, 7, min_low7)

max_lookback = 14

##########TRADING SIMULATION / TRADING LOGIC##########
###long positions = 1, and short positions = -1

pos_dir = []
pos_size = []
entry_date = []
entry_price = []
exit_date = []
exit_price = []

position = False
j = None
in_pos = None #days in position


for i in reversed(range(working_data.shape[0] - max_lookback)):
	if position == False:
		if working_data[i][high] == working_data[i][max_high7] or working_data[i][low] == working_data[i][min_low7]:
			position = initiate(working_data)
			j = i
			in_pos = 1
		else:
			pass
		
	elif position == True:
		position = loss(working_data, pos_dir)
		
		if position == True:
			position = profit(working_data, pos_dir)
		
		if position == True:
			in_pos += 1
		elif position == False:
			j = None
			in_pos = None
		else:
			exit("OH NO!!!")




##########BACKTESTING STATS##########
###Creating array with results###			
if position == True:
	pos_dir.pop()
	pos_size.pop()
	entry_date.pop()
	entry_price.pop()
else:
	pass

pos_dir = np.array(pos_dir)
pos_size = np.array(pos_size)
entry_date = np.array(entry_date)
entry_price = np.array(entry_price)
exit_date = np.array(exit_date)
exit_price = np.array(exit_price)

sim_data = np.zeros([len (entry_date), 7], float)
sim_data [:, 0] = np.transpose (pos_dir)
sim_data [:, 1] = np.transpose (pos_size)
sim_data [:, 2] = np.transpose (entry_date)
sim_data [:, 3] = np.transpose (entry_price)
sim_data [:, 4] = np.transpose (exit_date)
sim_data [:, 5] = np.transpose (exit_price)

pos_dir = 0
pos_size = 1
entry_date = 2
entry_price = 3
exit_date = 4
exit_price = 5
pnl = 6


returns(sim_data, entry_price, exit_price, pnl)	
print cum_returns(sim_data, pnl)
		
