import os
import time as tm
import json as js
import random as rd
import pandas as pd

class PPP():
	"Simulating Rock, Paper & Probabilities game"

	config = None
	n = None #Number of simulated rolls
	i = None #Number of iterations
	ai = None #Active iteration
	ms = None #Match size in rolls
	starttime = None
	sname = None
	rollresult = []
	simulationdata = []
	summarydata = None
	rpath = None
	dicefaces = ["rock", "paper", "scissors"]
	cdice = [-1,-1,-1,-1,-1,-1]
	pdice = [-1,-1,-1,-1,-1,-1]

	def __init__(self, configpath):
		PPP.config = js.load(open(configpath))
		PPP.setConfig(PPP.config)
		print(self)
		PPP.run()
		PPP.exportRawData()
		PPP.summarydata = PPP.buildSummary()
		PPP.exportSummary()

	def run():
		for d in range(PPP.i):
			PPP.starttime = tm.time()
			PPP.rollresult = [0, "?", "?", 0, 0, 0, 0, 0.0, 0.0, 0.0, 0, 0.0]
			PPP.simulationdata.append(PPP.buildSimulationDataFrame())
			print("-- Simulation number: " + str(d) + "   ", end="\n")
			PPP.simulation()
			print("-- Time needed: " + \
					PPP.getSimulationTime(PPP.starttime, tm.time()))
			print("-- The data was saved!             ", end="\n")
			PPP.ai += 1

	def simulation():
		for d in range(PPP.n):
			print("-- Rolling the dice: " + str(d) + "   ", end="\r")
			r = PPP.play()
			PPP.updateRoll(d+1, r)
			PPP.saveRoll(PPP.ai)

	def play():
		c = rd.choice(PPP.cdice)
		p = rd.choice(PPP.pdice)
		r = PPP.decide(c, p)
		return [c, p, r]

	def decide(c, p):
		r = 0;
		if c == 0:
			if p == 1:
				r = 1
			elif p == 2:
				r = -1;
		if c == 1:
			if p == 2:
				r = 1
			elif p == 0:
				r = -1;
		if c == 2:
			if p == 0:
				r = 1
			elif p == 1:
				r = -1;
		if c == -1 or p == -1:
			print("-- Dice has strange faces...")
		return r

	def updateRoll(n, results):
		PPP.rollresult[0] = n
		PPP.rollresult[1] = PPP.dicefaces[results[0]]
		PPP.rollresult[2] = PPP.dicefaces[results[1]]
		PPP.rollresult[3] = results[2]
		PPP.updateRCounts(PPP.rollresult[3])
		PPP.rollresult[7] = round(PPP.rollresult[4] / PPP.rollresult[0], 2)
		PPP.rollresult[8] = round(PPP.rollresult[5] / PPP.rollresult[0], 2)
		PPP.rollresult[9] = round(PPP.rollresult[6] / PPP.rollresult[0], 2)
		PPP.rollresult[10] = PPP.rollresult[4] - PPP.rollresult[6]
		PPP.rollresult[11] = round(PPP.rollresult[10] / PPP.rollresult[0], 2)

	def updateRCounts(result):
		if result == 1:
			PPP.rollresult[4] += 1
		if result == 0:
			PPP.rollresult[5] += 1
		if result == -1:
			PPP.rollresult[6] += 1

	def saveRoll(i):
		row = pd.DataFrame([PPP.rollresult], columns = PPP.simulationdata[0].columns)
		PPP.simulationdata[PPP.ai] = pd.concat([PPP.simulationdata[PPP.ai], row])

	def exportRawData():
		for i in range(PPP.i):
			PPP.simulationdata[i].set_index("n", inplace = True)
			PPP.simulationdata[i].to_csv(PPP.config["oPath"] + PPP.sname + "_" + str(i) + ".csv")

	def buildSummary():
		d = PPP.buildSummaryDataFrame()
		for i in range(PPP.i):
			mr = PPP.getMatchesResults(PPP.simulationdata[i])
			d.loc[d.index[i], "Won"] = PPP.simulationdata[i].loc[PPP.simulationdata[i].index[PPP.n - 1], "Won"]
			d.loc[d.index[i], "Tied"] = PPP.simulationdata[i].loc[PPP.simulationdata[i].index[PPP.n - 1], "Tied"]
			d.loc[d.index[i], "Lost"] = PPP.simulationdata[i].loc[PPP.simulationdata[i].index[PPP.n - 1], "Lost"]
			d.loc[d.index[i], "Won matches"] = mr[0]
			d.loc[d.index[i], "Lost matches"] = mr[1]
		d.loc[d.index[PPP.i], "Won"] = round(d["Won"].mean(), 2)
		d.loc[d.index[PPP.i], "Tied"] = round(d["Tied"].mean(), 2)
		d.loc[d.index[PPP.i], "Lost"] = round(d["Lost"].mean(), 2)
		d.loc[d.index[PPP.i], "Won matches"] = round(d["Won matches"].mean(), 2)
		d.loc[d.index[PPP.i], "Lost matches"] = round(d["Lost matches"].mean(), 2)
		return d

	def getMatchesResults(data):
		rolls = data[data["Result"] != 0]
		rolls.reset_index(inplace=True)
		p = PPP.ms
		mr = [0, 0]
		while p < rolls.shape[0]:
			if rolls.loc[p - PPP.ms:p, "Result"].sum() > 0:
				mr[0] += 1
			else:
				mr[1] += 1
			p += PPP.ms
		return mr

	def exportSummary():
		#PPP.summarydata.set_index("n", inplace = True)
		PPP.summarydata.to_csv(PPP.config["oPath"] + PPP.sname + "_S" + ".csv")

	def printRoll(results):
		return "-- The dice rolled:\n" + \
				"-- " + dicefaces[results[0]] + "vs. " + dicefaces[results[1]] + \
				"--> " + str(results[2])

	def setConfig(data):
		PPP.n = data["rollcount"]
		PPP.i = data["iterations"]
		PPP.ai = 0
		PPP.ms = data["matchsize"]
		PPP.sname = data["name"]
		PPP.buildDices(data["computerdice"], data["playerdice"])

	def buildDices(cd, pd):
		c = cd.split(",")
		p = cd.split(",")
		l = len(c)
		if l == 6:
			for f in range(l):
				PPP.cdice[f] = PPP.setDiceFace(c[f])
				PPP.pdice[f] =PPP.setDiceFace(p[f])
		else:
			print("-- Configuration data is strange...")

	def setDiceFace(s):
		n = -1
		if s == "rock":
			n = 0
		elif s == "paper":
			n = 1
		elif s == "scissors":
			n = 2
		return n

	def buildSimulationDataFrame():
		columns = []
		columns.append("n")
		columns.append("Computer")
		columns.append("Player")
		columns.append("Result")
		columns.append("Won")
		columns.append("Tied")
		columns.append("Lost")
		columns.append("Won%")
		columns.append("Tied%")
		columns.append("Lost%")
		columns.append("delta")
		columns.append("delta%")
		p = pd.DataFrame(columns=columns)
		p.index = p["n"]
		p.index.name = "n"
		return p

	def buildSummaryDataFrame():
		columns = []
		columns.append("Won")
		columns.append("Tied")
		columns.append("Lost")
		columns.append("Won matches")
		columns.append("Lost matches")
		p = pd.DataFrame(index=range(PPP.i + 1), columns=columns)
		p.index.name = "n"
		return p

	#Calculating time needed for simulation to finish...
	def getSimulationTime(startTime, endTime):
		time = endTime - startTime
		formatedTime = PPP.formatTime(time)
		return formatedTime

	def formatTime(time):
		ms = ""
		minutes = time // 60
		seconds = time - minutes * 60
		seconds = round(seconds, 2)
		ms = "{:02d}".format(int(minutes))
		ms += ":"
		ms += "{:05.2f}".format(seconds)
		return ms

	def __str__(self):
		return "-- MatEduLab\n" + \
				"-- Rock, Paper & Probabilities\n" + \
				"-- Simulating the game..."
