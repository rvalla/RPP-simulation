import pandas as pd
import matplotlib.pyplot as plt

class Visualization:
	"A class to plot Rock, Paper & Probabilities results..."

	defaultfont = "Trebuchet MS"
	legendFont = "Trebuchet MS"
	fontcolor = [0.2, 0.2, 0.2]
	titlesize = 12
	subtitlesize = 10
	axislabelsize = 7
	ticksize = 7
	backgroundPlot = [0.65, 0.75, 0.85]
	backgroundFigure = [0.8, 0.8, 0.8]
	backgroundLegend = [0.6, 0.7, 0.8]
	majorGridColor = [0.3, 0.3, 0.3]
	minorGridColor = [0.5, 0.5, 0.5]
	alphaMGC = 1.0
	alphamGC = 1.0
	imageResolution = 200
	widthbig = 2.5
	widthnormal = 2.0
	widthsmall = 1.5
	plotcolors = [(0.7, 0.0, 0.5), (0.0, 0.5, 0.7), (0.9, 0.75, 0.1)]
	resulttexts = []
	labelstexts = []
	plottitles = []
	facestexts = []

	def __init__(self, lan):
		Visualization.buildTexts(lan)

	def gridsAndBackground():
		plt.grid(which='both', axis='both')
		plt.minorticks_on()
		plt.grid(True, "major", "y", ls="-", lw=0.8, c=Visualization.majorGridColor, alpha=Visualization.alphaMGC)
		plt.grid(True, "minor", "y", ls="--", lw=0.3, c=Visualization.minorGridColor, alpha=Visualization.alphamGC)
		plt.grid(True, "major", "x", ls="-", lw=0.8, c=Visualization.majorGridColor, alpha=Visualization.alphaMGC)
		plt.grid(True, "minor", "x", ls="--", lw=0.3, c=Visualization.minorGridColor, alpha=Visualization.alphamGC)
		plt.xticks(fontsize=Visualization.ticksize)
		plt.yticks(fontsize=Visualization.ticksize)
		plt.gca().set_facecolor(Visualization.backgroundPlot)

	def xgridAndBackground():
		plt.grid(which='both', axis='x')
		plt.minorticks_on()
		plt.grid(True, "major", "x", ls="-", lw=0.8, c=Visualization.majorGridColor, alpha=Visualization.alphaMGC)
		plt.grid(True, "minor", "x", ls="--", lw=0.3, c=Visualization.minorGridColor, alpha=Visualization.alphamGC)
		plt.xticks(fontsize=Visualization.ticksize, color=Visualization.fontcolor)
		plt.yticks(fontsize=Visualization.ticksize, color=Visualization.fontcolor)
		plt.gca().set_facecolor(Visualization.backgroundPlot)

	def background():
		plt.xticks(fontsize=Visualization.ticksize, color=Visualization.fontcolor)
		plt.yticks(fontsize=Visualization.ticksize, color=Visualization.fontcolor)
		plt.gca().set_facecolor(Visualization.backgroundPlot)

	def autoCharts(self, sname, folder, cdice, pdice, data, summary):
		print("-- Plotting the data...", end="\r")
		auxt = Visualization.plottitles[0] + sname + "\n"
		dicet = Visualization.getDiceString(cdice) + " vs. " + Visualization.getDiceString(pdice)
		Visualization.plotHistory(8, 4.5, sname + "_history", folder, data, auxt + dicet)
		auxt = Visualization.plottitles[1] + sname + "\n"
		Visualization.plotRatios(8, 4.5, sname + "_ratios", folder, data, auxt + dicet)
		auxt = Visualization.plottitles[2] + sname + "\n"
		Visualization.plotDifference(8, 4.5, sname + "_difference", folder, data, auxt + dicet)
		auxt = Visualization.plottitles[3] + sname + "\n"
		Visualization.plotMatches(8, 4.5, sname + "_matches", folder, summary, auxt + dicet)
		print("-- Charts were saved!                 ", end="\n")
		print()

	def plotHistory(w, h, sname, folder, data, title):
		figure = plt.figure(num=None, figsize=(w, h), dpi=Visualization.imageResolution, \
							facecolor=Visualization.backgroundFigure, edgecolor='k')
		figure.suptitle(title, fontsize=Visualization.titlesize, fontname=Visualization.defaultfont, \
							color=Visualization.fontcolor)
		history = Visualization.getHistoryPlot(data)
		plt.tight_layout(rect=[0, 0, 1, 1])
		plt.savefig(folder + sname + ".png", facecolor=figure.get_facecolor())

	def plotRatios(w, h, sname, folder, data, title):
		figure = plt.figure(num=None, figsize=(w, h), dpi=Visualization.imageResolution, \
							facecolor=Visualization.backgroundFigure, edgecolor='k')
		figure.suptitle(title, fontsize=Visualization.titlesize, fontname=Visualization.defaultfont, \
							color=Visualization.fontcolor)
		ratios = Visualization.getRatioPlot(data)
		plt.tight_layout(rect=[0, 0, 1, 1])
		plt.savefig(folder + sname + ".png", facecolor=figure.get_facecolor())

	def plotDifference(w, h, sname, folder, data, title):
		figure = plt.figure(num=None, figsize=(w, h), dpi=Visualization.imageResolution, \
							facecolor=Visualization.backgroundFigure, edgecolor='k')
		figure.suptitle(title, fontsize=Visualization.titlesize, fontname=Visualization.defaultfont, \
							color=Visualization.fontcolor)
		difference = Visualization.getDifferencePlot(data)
		plt.tight_layout(rect=[0, 0, 1, 1])
		plt.savefig(folder + sname + ".png", facecolor=figure.get_facecolor())

	def plotMatches(w, h, sname, folder, data, title):
		figure = plt.figure(num=None, figsize=(w, h), dpi=Visualization.imageResolution, \
							facecolor=Visualization.backgroundFigure, edgecolor='k')
		figure.suptitle(title, fontsize=Visualization.titlesize, fontname=Visualization.defaultfont, \
							color=Visualization.fontcolor)
		rolls = plt.subplot2grid((1, 2), (0, 0))
		rolls = data[["Won","Tied","Lost"]][0:data.shape[0]].plot(kind="bar", stacked=True, ax=rolls, rot=0)
		rolls.set_title(Visualization.labelstexts[0], fontsize=Visualization.subtitlesize, \
							fontname=Visualization.defaultfont, color=Visualization.fontcolor)
		l = []
		for i in range(data.shape[0] - 1):
			l.append(i+1)
		l.append(Visualization.labelstexts[2])
		rolls.set_xlabel("")
		rolls.set_xticklabels(l)
		rolls.legend(loc=4, shadow = True, facecolor = Visualization.backgroundLegend, \
						prop={'family' : Visualization.legendFont, 'size' : 8})
		Visualization.background()
		matches = plt.subplot2grid((1, 2), (0, 1))
		matches = data[["Won matches","Lost matches"]][0:data.shape[0]].plot(kind="bar", stacked=True, ax=matches, rot=0)
		matches.set_title(Visualization.labelstexts[1], fontsize=Visualization.subtitlesize, \
							fontname=Visualization.defaultfont, color=Visualization.fontcolor)
		matches.set_xlabel("")
		matches.set_xticklabels(l)
		matches.legend(loc=4, shadow = True, facecolor = Visualization.backgroundLegend, \
						prop={'family' : Visualization.legendFont, 'size' : 8})
		Visualization.background()
		plt.tight_layout(rect=[0, 0, 1, 1])
		plt.savefig(folder + sname + ".png", facecolor=figure.get_facecolor())

	def getHistoryPlot(data):
		history = None
		for c in range(len(data)):
			history = data[c]["Tied"].plot(kind="line", linewidth=Visualization.widthbig, \
									color=Visualization.plotcolors[2], label=Visualization.resulttexts[1], ax=history)
			history = data[c]["Lost"].plot(kind="line", linewidth=Visualization.widthbig, \
									color=Visualization.plotcolors[0], label=Visualization.resulttexts[2], ax=history)
			history = data[c]["Won"].plot(kind="line", linewidth=Visualization.widthbig, \
									color=Visualization.plotcolors[1], label=Visualization.resulttexts[0], ax=history)
		history.legend((Visualization.resulttexts[1], Visualization.resulttexts[2], \
					Visualization.resulttexts[0]), loc=0, shadow = True, facecolor = Visualization.backgroundLegend, \
					prop={'family' : Visualization.legendFont, 'size' : 8})
		history.set_xlabel(Visualization.labelstexts[0])
		Visualization.gridsAndBackground()
		return history

	def getRatioPlot(data):
		ratios = None
		for c in range(len(data)):
			ratios = data[c]["Tied%"].plot(kind="line", linewidth=Visualization.widthbig, \
									color=Visualization.plotcolors[2], label=Visualization.resulttexts[1], ax=ratios)
			ratios = data[c]["Lost%"].plot(kind="line", linewidth=Visualization.widthbig, \
									color=Visualization.plotcolors[0], label=Visualization.resulttexts[2], ax=ratios)
			ratios = data[c]["Won%"].plot(kind="line", linewidth=Visualization.widthbig, \
									color=Visualization.plotcolors[1], label=Visualization.resulttexts[0], ax=ratios)
		ratios.legend((Visualization.resulttexts[1], Visualization.resulttexts[2], \
					Visualization.resulttexts[0]), loc=0, shadow = True, facecolor = Visualization.backgroundLegend, \
					prop={'family' : Visualization.legendFont, 'size' : 8})
		ratios.set_xlabel(Visualization.labelstexts[0])
		Visualization.gridsAndBackground()
		return ratios

	def getDifferencePlot(data):
		difference = None
		for c in range(len(data)):
			difference = data[c]["delta"].plot(kind="line", linewidth=Visualization.widthbig, \
									color=Visualization.plotcolors[0], label=Visualization.resulttexts[1], ax=difference)
		l = plt.ylim()
		if abs(l[0]) < abs(l[1]):
			if l[1] > 0:
				difference.set_ylim(-l[1], l[1])
			else:
				difference.set_ylim(l[1], -l[1])
		else:
			if l[0] > 0:
				difference.set_ylim(-l[0], l[0])
			else:
				difference.set_ylim(l[0], -l[0])
		difference.axhline(y=0, linewidth=4, color=Visualization.plotcolors[2], zorder=0)
		difference.set_xlabel(Visualization.labelstexts[0])
		Visualization.gridsAndBackground()
		return difference

	#Getting string representation of a dice
	def getDiceString(dice):
		n = [0, 0, 0]
		for i in range(len(dice)):
			n[dice[i]] += 1
		s = "(" + str(n[0]) + " " + Visualization.facestexts[0] + ", "
		s += str(n[1]) + " " + Visualization.facestexts[1] + ", "
		s += str(n[2]) + " " + Visualization.facestexts[2] + ")"
		return s

	def buildTexts(lan):
		if lan == "spanish":
			Visualization.plottitles.append("Historia: ")
			Visualization.plottitles.append("Proporción: ")
			Visualization.plottitles.append("Diferencia: ")
			Visualization.plottitles.append("Partidas: ")
			Visualization.resulttexts.append("victorias")
			Visualization.resulttexts.append("empates")
			Visualization.resulttexts.append("derrotas")
			Visualization.labelstexts.append("Tiradas")
			Visualization.labelstexts.append("Partidas")
			Visualization.labelstexts.append("Promedio")
			Visualization.facestexts.append("piedra")
			Visualization.facestexts.append("papel")
			Visualization.facestexts.append("tijera")
		else:
			Visualization.plottitles.append("History: ")
			Visualization.plottitles.append("Ratios: ")
			Visualization.plottitles.append("Difference: ")
			Visualization.plottitles.append("Matches: ")
			Visualization.resulttexts.append("won")
			Visualization.resulttexts.append("tied")
			Visualization.resulttexts.append("lost")
			Visualization.labelstexts.append("Rolls")
			Visualization.labelstexts.append("Matches")
			Visualization.labelstexts.append("Average")
			Visualization.facestexts.append("rock")
			Visualization.facestexts.append("paper")
			Visualization.facestexts.append("scissors")

	def __str__(self):
		return "-- MatEduLab\n" + \
				"-- Rock, Paper & Probabilities\n" + \
				"-- https://gitlab.com/matedulab/rpp-simulation\n" + \
				"-- Making some charts...\n"
