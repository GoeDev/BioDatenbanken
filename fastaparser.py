from pathlib import Path
import logging

from sequence import Sequence
from sequencefromfile import Sequencefromfile

class Fastaparser(object):
	def __init__(self):
		self.name2id = {}
		self.seqlist = []
		self.aligncounter = 1

	def readname2id(self, path):
		existcheck = Path(path)
		if existcheck.is_file():
			filehandle=open(path, "r")
			for line in filehandle:
				splitted = line.split(";")
				name = splitted[0]
				id = splitted[1]
				self.name2id[name] = id
				
	def readfile(self, path):
		existcheck = Path(path)
		if existcheck.is_file():
			filehandle=open(path, "r")

			align = 0
			if "logoplot" in path:
				align = self.aligncounter

			bclass = path.split("/")[-1].split("_")[1]

			name = ""
			comment = ""
			counter = 1
			for line in filehandle:
				if line.startswith(">"):
					name=line[1:].rstrip()
				elif line.startswith(";"):
					comment=line[1:].rstrip()
				else:
					#sequ = Sequence(bclass, name, counter, comment, line.rstrip(), align, self, None)
					sequ = Sequencefromfile(bclass, name, counter, comment, line.rstrip(), align, self)
					if sequ.valid:
						self.seqlist.append(sequ)
					counter = counter + 1
		else:
			print("Datei nicht gefunden: " + path)
			quit()


	def generate(self, sequence):
		fasta = ""
		if not sequence.comment == "":
			fasta += ";" + sequence.comment + "\n"

		header = sequence.bname.replace(" ", "_") + "_" + sequence.tfname

		fasta += ">" + header + "\n"
		fasta += sequence.sequence + "\n"
		return fasta

	def write(self, filename, fasta):
		outfile = open(filename, "w+")
		outfile.write(fasta)
		outfile.close()