from pathlib import Path
from sequence import Sequence

class Fastaparser(object):
	def __init__(self):
		self.name2id = {}
		self.seqlist = []

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
					sequ = Sequence(bclass, name, counter, comment, line.rstrip(), self, None)
					if sequ.valid:
						self.seqlist.append(sequ)
					counter = counter + 1
		else:
			print("Datei nicht gefunden: " + path)
			quit()


	def generate(self, sequence):
		fasta = ""
		if not sequence.comment == "":
			fasta += ";" + comment + "\n"

		header = sequence.bname.replace(" ", "_") + "_" + sequence.tfname

		fasta += ">" + header + "\n"
		fasta += sequence.sequence + "\n"
		return fasta