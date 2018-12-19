class Sequence(object):

	def __init__(self, bclass, name, tfspecies, comment, sequence, parser):
		self.tfspecies = tfspecies
		self.bclass = bclass
		self.bname = ""
		self.tfname = ""

		for element in name.split("_"):
			if any(x.isupper() for x in element):
				if name.find(element) == 0:
					self.bname += element
				else:
					for key in parser.name2id.keys():
						if element.startswith(key):
							self.tfname = key
							break
			else:
				self.bname += " " + element

		if self.tfname == "":
			print(name + " konnte nicht importiert werden, name nicht gefunden.")
			self.valid = False
		else:
			self.valid = True
			idsplit = parser.name2id[self.tfname].split(".")
			self.tfsuperclass = idsplit[0]
			self.tfclass = idsplit[1]
			self.tffamily = idsplit[2]
			self.tfsubfamily = idsplit[3]

			self.tfgenus = parser.name2id[self.tfname].split(".")[-1].rstrip()

		self.comment = comment
		self.sequence = sequence
