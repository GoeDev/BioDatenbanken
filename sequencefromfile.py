from sequence import Sequence
import logging

class Sequencefromfile(Sequence):
	def __init__(self, bclass, name, tfspecies, comment, sequence, align, parser):
		bname = ""
		tfname = ""
		tfsuperclass = -1
		tfclass = -1
		tffamily = -1
		tfsubfamily = -1
		tfgenus = -1
		valide = False

		found = False
		for element in name.split("_"):
			if any(x.isupper() for x in element):
				if name.find(element) == 0:
					bname += element
				else:
					for key in parser.name2id.keys():
						if element.startswith(key):
							tfname = key
							found = True
							break
			else:
				if found:
					break
				bname += " " + element
			
		if tfname == "":
			logging.warning(name + " konnte nicht importiert werden, Name in name2ID nicht gefunden.")
			valide = False
		else:
			valide = True
			idsplit = parser.name2id[tfname].split(".")
			tfsuperclass = idsplit[0]
			tfclass = idsplit[1]
			tffamily = idsplit[2]
			tfsubfamily = idsplit[3]

			tfgenus = parser.name2id[tfname].split(".")[-1].rstrip()
		super().__init__(bclass, bname, tfname, tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, comment, sequence, align, parser, valide)