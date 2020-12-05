import os
import time as tm
import json as js
import random as rd
import pandas as pd
from visualization import Visualization

class PPP():
	"Simulating Rock, Paper & Probabilities game"

	def __init__(self, configpath):
		self.config = js.load(open(configpath))
		self.vz = Visualization(self.config["language"])
		self.n = None #Number of simulated rolls
		self.i = None #Number of iterations
		self.ai = None #Active iteration
		self.ms = None #Match size in rolls
		self.discardtieds = None #Decide if tied rolls are part of a match
		self.starttime = None
		self.sname = None
		self.rollresult = []
		self.simulationdata = []
		self.summarydata = None
		self.dicefaces = ["rock", "paper", "scissors"]
		self.cdice = [-1,-1,-1,-1,-1,-1]
		self.pdice = [-1,-1,-1,-1,-1,-1]
		PPP.setConfig(self, self.config)
		print()
		print(self)
		PPP.run(self)
		PPP.exportRawData(self)
		self.summarydata = PPP.buildSummary(self)
		self.vz.autoCharts(self.sname, self.config["cPath"], self.cdice, self.pdice, self.simulationdata, self.summarydata)
		PPP.exportSummary(self)

	def run(self):
		for d in range(self.i):
			self.starttime = tm.time()
			self.rollresult = [0, "?", "?", 0, 0, 0, 0, 0.0, 0.0, 0.0, 0, 0.0]
			self.simulationdata.append(PPP.buildSimulationDataFrame())
			print("-- Simulation number: " + str(d) + "   ", end="\n")
			PPP.simulation(self)
			print("-- Time needed: " + \
					PPP.getSimulationTime(self.starttime, tm.time()) + "                 ", end="\n")
			print("-- The data was saved!", end="\n")
			print()
			self.ai += 1

	def simulation(self):
		for d in range(self.n):
			print("-- Roll " + str(d) + ":", end=" ")
			r = PPP.play(self)
			PPP.updateRoll(self, d+1, r)
			print("W: " + str(self.rollresult[7]), end=" ")
			print("T: " + str(self.rollresult[8]), end=" ")
			print("L: " + str(self.rollresult[9]) + "     ", end="\r")
			PPP.saveRoll(self, self.ai)

	def play(self):
		c = rd.choice(self.cdice)
		p = rd.choice(self.pdice)
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

	def updateRoll(self, n, results):
		self.rollresult[0] = n
		self.rollresult[1] = self.dicefaces[results[0]]
		self.rollresult[2] = self.dicefaces[results[1]]
		self.rollresult[3] = results[2]
		PPP.updateRCounts(self, self.rollresult[3])
		self.rollresult[7] = round(self.rollresult[4] / self.rollresult[0], 2)
		self.rollresult[8] = round(self.rollresult[5] / self.rollresult[0], 2)
		self.rollresult[9] = round(self.rollresult[6] / self.rollresult[0], 2)
		self.rollresult[10] = self.rollresult[4] - self.rollresult[6]
		self.rollresult[11] = round(self.rollresult[10] / self.rollresult[0], 2)

	def updateRCounts(self, result):
		if result == 1:
			self.rollresult[4] += 1
		if result == 0:
			self.rollresult[5] += 1
		if result == -1:
			self.rollresult[6] += 1

	def saveRoll(self, i):
		row = pd.DataFrame([self.rollresult], columns = PPP.buildDataFrameColumns())
		self.simulationdata[self.ai] = pd.concat([self.simulationdata[self.ai], row])

	def exportRawData(self):
		for i in range(self.i):
			self.simulationdata[i].set_index("n", inplace = True)
			self.simulationdata[i].to_csv(self.config["dPath"] + self.sname + "_" + str(i) + ".csv")

	def buildSummary(self):
		d = PPP.buildSummaryDataFrame(self)
		for i in range(self.i):
			mr = self.getMatchesResults(self.simulationdata[i])
			d.loc[d.index[i], "Won"] = self.simulationdata[i].loc[self.simulationdata[i].index[self.n - 1], "Won"]
			d.loc[d.index[i], "Tied"] = self.simulationdata[i].loc[self.simulationdata[i].index[self.n - 1], "Tied"]
			d.loc[d.index[i], "Lost"] = self.simulationdata[i].loc[self.simulationdata[i].index[self.n - 1], "Lost"]
			d.loc[d.index[i], "Won matches"] = mr[0]
			d.loc[d.index[i], "Lost matches"] = mr[1]
		d.loc[d.index[self.i], "Won"] = round(d["Won"].mean(), 2)
		d.loc[d.index[self.i], "Tied"] = round(d["Tied"].mean(), 2)
		d.loc[d.index[self.i], "Lost"] = round(d["Lost"].mean(), 2)
		d.loc[d.index[self.i], "Won matches"] = round(d["Won matches"].mean(), 2)
		d.loc[d.index[self.i], "Lost matches"] = round(d["Lost matches"].mean(), 2)
		return d

	def getMatchesResults(self, data):
		if self.discardtieds == True:
			rolls = data[data["Result"] != 0]
			rolls.reset_index(inplace=True)
		else:
			rolls = data
		p = self.ms
		mr = [0, 0]
		while p < rolls.shape[0]:
			r = rolls.loc[p - self.ms:p, "Result"].sum()
			if  r > 0:
				mr[0] += 1
			elif r < 0:
				mr[1] += 1
			p += self.ms
		return mr

	def exportSummary(self):
		self.summarydata.to_csv(self.config["dPath"] + self.sname + "_S" + ".csv")

	def printRoll(self, results):
		return "-- The dice rolled:\n" + \
				"-- " + self.dicefaces[results[0]] + "vs. " + self.dicefaces[results[1]] + \
				"--> " + str(results[2])

	def setConfig(self, data):
		self.n = data["rollcount"]
		self.i = data["iterations"]
		self.ai = 0
		self.ms = data["matchsize"]
		self.discardtieds = data["discardtieds"]
		self.sname = data["name"]
		PPP.buildDices(self, data["computerdice"], data["playerdice"])

	def buildDices(self, cd, pd):
		c = cd.split(",")
		p = pd.split(",")
		l = len(c)
		if l == 6:
			for f in range(l):
				self.cdice[f] = PPP.setDiceFace(c[f])
				self.pdice[f] =PPP.setDiceFace(p[f])
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
		columns = PPP.buildDataFrameColumns()
		p = pd.DataFrame(columns=columns)
		p.index.name = "n"
		return p

	def buildDataFrameColumns():
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
		return columns

	def buildSummaryDataFrame(self):
		columns = []
		columns.append("Won")
		columns.append("Tied")
		columns.append("Lost")
		columns.append("Won matches")
		columns.append("Lost matches")
		p = pd.DataFrame(index=range(self.i + 1), columns=columns)
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
				"-- https://gitlab.com/matedulab/rpp-simulation\n" + \
				"-- version: 0.90\n" + \
				"-- Simulating the game...\n"
