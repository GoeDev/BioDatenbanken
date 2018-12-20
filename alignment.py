import math

from sequence import Sequence
from fastaparser import Fastaparser

class Alignment(object):
	def __init__(self, parser):
		self.sequences = []
		self.multlevels = False
		self.parser = parser
		self.alphabet = ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V", "X", "-"]

	def addsequence(self, sequence):
		self.sequences.append(sequence)

	def getfasta(self):
		fasta = ""
		for sequence in self.sequences:
			fasta += self.parser.generate(sequence)
		return fasta

	def getentropy(self):
		probabilities = []
		counter = 0
		for x in self.sequences[0].sequence:
			probabilities.append({})
			for letter in self.alphabet:
				probabilities[counter][letter] = 0
			counter += 1

		for seq in self.sequences:
			counter = 0
			for x in seq.sequence:
				probabilities[counter][x] +=1
				counter += 1

		seqcount = len(self.sequences)

		counter = 0
		for column in probabilities:
			for key, value in column.items():
				if not key == "-":
					if (seqcount - column["-"]) == 0:
						probabilities[counter][key] = 0
					else:
						probabilities[counter][key] = value / (seqcount - column["-"])
			counter += 1

		counter = 0
		for column in probabilities:
			entropy = 0
			for key, value in column.items():
				if not key == "-":
					if value == 0:
						entropy = 0
					else:
						entropy += -(value * math.log(value, 2))
				else:
					probabilities[counter]["-"] = entropy
			counter += 1

		returnstring = ""
		for column in probabilities:
			returnstring += str(column["-"]) + ", "

		return returnstring[:-2]