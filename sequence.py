class Sequence(object):

	def __init__(self, bclass, bname, tfname, tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, comment, sequence, align, parser, valid=True):
		self.valid = valid

		self.bclass = bclass
		self.bname = bname

		self.tfname = tfname
		self.tfsuperclass = tfsuperclass
		self.tfclass = tfclass
		self.tffamily = tffamily
		self.tfsubfamily = tfsubfamily
		self.tfgenus = tfgenus
		self.tfspecies = tfspecies

		self.align = align
		
		self.comment = comment
		self.sequence = sequence