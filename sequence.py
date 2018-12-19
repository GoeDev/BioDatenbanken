class Sequence(object):

	def __init__(self, bclass, name, tfspecies, comment, sequence, parser, args):
		self.tfspecies = tfspecies
		self.bclass = bclass
		self.tfname = ""
		self.bname = ""

		found = False

		if args == None:
			for element in name.split("_"):
				if any(x.isupper() for x in element):
					if name.find(element) == 0:
						self.bname += element
					else:
						for key in parser.name2id.keys():
							if element.startswith(key):
								self.tfname = key
								found = True
								break
				else:
					if found:
						break
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
		else:
			self.valid = True
			self.bname = args["bname"]
			self.tfname = args["tfname"]
			self.tfsuperclass = args["tfsuperclass"]
			self.tfclass = args["tfclass"]
			self.tffamily = args["tffamily"]
			self.tfsubfamily = args["tfsubfamily"]
			self.tfgenus = args["tfgenus"]

		self.comment = comment
		self.sequence = sequence

