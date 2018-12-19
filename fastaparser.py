from pathlib import Path
from sequence import Sequence

class Fastaparser(object):
	def __init__(self):
		self.name2id = {}
		self.seqlist = []

	def readname2id(self, path):
		path = "../name2ID.txt"
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

			name=""
			comment=""

			for num, line in enumerate(filehandle, 1):
				if line.startswith(">"):
					name=line[1:].rstrip()
				elif line.startswith(";"):
					comment=line[1:].rstrip()
				else:
					sequ = Sequence(bclass, name, num, comment, line.rstrip(), self)
					if sequ.valid:
						self.seqlist.append(sequ)
		else:
			print("Datei nicht gefunden: " + path)
			quit()