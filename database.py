import sqlite3
import os

from sequence import Sequence
from alignment import Alignment

class Database(object):
	def __init__(self, dbfile, parser):
		self.conn = sqlite3.connect(dbfile)
		self.cursor = self.conn.cursor()
		self.parser = parser

	def createbasestructure(self):
		self.cursor.execute('''CREATE TABLE bclasses 
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, bclass TEXT)''')
		self.cursor.execute('''CREATE TABLE bnames 
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, bname TEXT,
		UNIQUE(bname))''')
		self.cursor.execute('''CREATE TABLE tfnames 
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
		tfname TEXT,
		superclass INTEGER NOT NULL,
		class INTEGER NOT NULL,
		family INTEGER NOT NULL,
		subfamily INTEGER NOT NULL,
		genus INTEGER NOT NULL)''')
		self.cursor.execute('''CREATE TABLE sequences 
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
		tfnameid INTEGER NOT NULL,
		bclassid INTEGER NOT NULL,
		bnameid INTEGER NOT NULL,
		tfsuperclass INTEGER NOT NULL,
		tfclass INTEGER NOT NULL,
		tffamily INTEGER NOT NULL,
		tfsubfamily INTEGER NOT NULL,
		tfgenus INTEGER NOT NULL,
		tfspecies INTEGER NOT NULL,
		comment TEXT,
		sequence TEXT,
		alignment INTEGER,
		FOREIGN KEY (tfnameid) REFERENCES tfnames(id),
		FOREIGN KEY (bclassid) REFERENCES bclasses(id),
		FOREIGN KEY (bnameid) REFERENCES bnames(id))''')

	def insert_bclass(self, name):
		self.cursor.execute("INSERT INTO bclasses (bclass) VALUES ('" + name + "')")

	def insert_bname(self, sequence):
		self.cursor.execute("INSERT OR IGNORE INTO bnames (bname) VALUES ('" + sequence.bname + "')")

	def insert_tfname(self, name, superclass, tfclass, family, subfamily, genus):
		self.cursor.execute("INSERT INTO tfnames (tfname, superclass, class, family, subfamily, genus) VALUES ('" + name + "', '" + superclass + "', '"+ tfclass+"', '"+ family +"', '"+subfamily+"', '"+genus+"')")

	def insert_sequence(self, sequence):
		self.cursor.execute("SELECT id FROM bclasses WHERE bclass='" + sequence.bclass+"'")
		bclid = self.cursor.fetchone()[0]
		self.cursor.execute("SELECT id FROM bnames WHERE bname='" + sequence.bname+"'")
		bnid = self.cursor.fetchone()[0]
		self.cursor.execute("SELECT id FROM tfnames WHERE tfname='" + sequence.tfname+"'")
		tfnid = self.cursor.fetchone()[0]
		query = "INSERT INTO sequences (tfnameid, bclassid, bnameid, tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, comment, sequence, alignment)"
		query += " VALUES ('" + str(tfnid) + "', '" + str(bclid) + "', '" + str(bnid) + "', '" + str(sequence.tfsuperclass) + "', '" + str(sequence.tfclass) + "', '" + str(sequence.tffamily) + "', '" + str(sequence.tfsubfamily) + "', '" + str(sequence.tfgenus) + "', '" + str(sequence.tfspecies) + "', '" + sequence.comment + "', '" + sequence.sequence + "', '" + str(sequence.align) + "')" 
		self.cursor.execute(query)

	def commit(self):
		self.conn.commit()

	def getnode(self, id):
		idsplit = id.split(".")
		level = len(idsplit)
		
		query = "SELECT tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, tfname, bclass, bname, sequence, comment FROM sequences "
		query += "INNER JOIN bclasses ON bclasses.id = sequences.bclassid INNER JOIN bnames ON bnames.id = sequences.bnameid INNER JOIN tfnames ON tfnames.ID = sequences.tfnameid "
		query += "WHERE alignment=0 AND tfsuperclass=" + idsplit[0]
		if level > 1:
			query += " AND tfclass=" + idsplit[1]
		if level > 2:
			query += " AND tffamily=" + idsplit[2]
		if level > 3:
			query += " AND tfsubfamily=" + idsplit[3]
		if level > 4:
			query += " AND tfgenus=" + idsplit[4]
		if level > 5:
			query += " AND tfspecies=" + idsplit[5]

		self.cursor.execute(query)

		fasta = ""

		for sequencedata in self.cursor.fetchall():
			bclass = sequencedata[7]
			tfspecies = sequencedata[5]
			comment = sequencedata[10]
			seq = sequencedata[9]
			bname = sequencedata[8]
			tfname = sequencedata[6]
			tfsuperclass = sequencedata[0]
			tfclass = sequencedata[1]
			tffamily = sequencedata[2]
			tfsubfamily = sequencedata[3]
			tfgenus = sequencedata[4]
			#sequence = Sequence(bclass, "", tfspecies, comment, seq, 0, self.parser, args)
			sequence = Sequence(bclass, bname, tfname, tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, comment, seq, 0, self.parser)
			fasta += self.parser.generate(sequence)

		return fasta

	def getspecies(self, species):
		query = "SELECT tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, tfname, bclass, bname, sequence, comment FROM sequences "
		query += "INNER JOIN bclasses ON bclasses.id = sequences.bclassid INNER JOIN bnames ON bnames.id = sequences.bnameid INNER JOIN tfnames ON tfnames.ID = sequences.tfnameid "
		query += 'WHERE alignment=0 AND bnameid=(SELECT id from bnames WHERE bname LIKE "' + species +  '")'

		self.cursor.execute(query)
		fasta = ""

		for sequencedata in self.cursor.fetchall():
			bclass = sequencedata[7]
			tfspecies = sequencedata[5]
			comment = sequencedata[10]
			seq = sequencedata[9]
			bname = sequencedata[8]
			tfname = sequencedata[6]
			tfsuperclass = sequencedata[0]
			tfclass = sequencedata[1]
			tffamily = sequencedata[2]
			tfsubfamily = sequencedata[3]
			tfgenus = sequencedata[4]
			#sequence = Sequence(bclass, "", tfspecies, comment, seq, 0, self.parser, args)
			sequence = Sequence(bclass, bname, tfname, tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, comment, seq, 0, self.parser)
			fasta += self.parser.generate(sequence)

		return fasta

	def gettf(self, tfname):
		query = "SELECT tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, tfname, bclass, bname, sequence, comment FROM sequences "
		query += "INNER JOIN bclasses ON bclasses.id = sequences.bclassid INNER JOIN bnames ON bnames.id = sequences.bnameid INNER JOIN tfnames ON tfnames.ID = sequences.tfnameid "
		query += 'WHERE alignment=0 AND tfnameid=(SELECT id from tfnames WHERE tfname LIKE "' + tfname +  '")'

		self.cursor.execute(query)
		fasta = ""

		for sequencedata in self.cursor.fetchall():
			bclass = sequencedata[7]
			tfspecies = sequencedata[5]
			comment = sequencedata[10]
			seq = sequencedata[9]
			bname = sequencedata[8]
			tfname = sequencedata[6]
			tfsuperclass = sequencedata[0]
			tfclass = sequencedata[1]
			tffamily = sequencedata[2]
			tfsubfamily = sequencedata[3]
			tfgenus = sequencedata[4]
			#sequence = Sequence(bclass, "", tfspecies, comment, seq, 0, self.parser, args)
			sequence = Sequence(bclass, bname, tfname, tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, comment, seq, 0, self.parser)
			fasta += self.parser.generate(sequence)

		return fasta

	def getnodealign(self, id):
		idsplit = id.split(".")
		level = len(idsplit)
		
		query = "SELECT tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, tfname, bclass, bname, sequence, comment, alignment FROM sequences "
		query += "INNER JOIN bclasses ON bclasses.id = sequences.bclassid INNER JOIN bnames ON bnames.id = sequences.bnameid INNER JOIN tfnames ON tfnames.ID = sequences.tfnameid "
		query += "WHERE alignment > 0 AND tfsuperclass=" + idsplit[0]
		if level > 1:
			query += " AND tfclass=" + idsplit[1]
		if level > 2:
			query += " AND tffamily=" + idsplit[2]
		if level > 3:
			query += " AND tfsubfamily=" + idsplit[3]
		if level > 4:
			query += " AND tfgenus=" + idsplit[4]
		if level > 5:
			query += " AND tfspecies=" + idsplit[5]

		self.cursor.execute(query)
		
		alignments = []

		align = -1
		level4 = -1
		levelchanged = False
		alignobj = Alignment(self.parser)

		for sequencedata in self.cursor.fetchall():
			if level4 == -1:
				level4 = sequencedata[3]

			if align == -1:
				align = sequencedata[11]

			if not sequencedata[11] == align:
				if levelchanged:
					alignobj.multlevels = True
					alignments.append(alignobj)
					alignobj = Alignment(self.parser)
				else:
					alignments.append(alignobj)
					alignobj = Alignment(self.parser)
				align = sequencedata[11]
				level4 = sequencedata[3]
				levelchanged = False
			
			if not level4 == sequencedata[3]:
				levelchanged = True

			bclass = sequencedata[7]
			tfspecies = sequencedata[5]
			comment = sequencedata[10]
			seq = sequencedata[9]
			alignment = sequencedata[11]
			bname = sequencedata[8]
			tfname = sequencedata[6]
			tfsuperclass = sequencedata[0]
			tfclass = sequencedata[1]
			tffamily = sequencedata[2]
			tfsubfamily = sequencedata[3]
			tfgenus = sequencedata[4]
			#sequence = Sequence(bclass, "", tfspecies, comment, seq, alignment, self.parser, args)
			sequence = Sequence(bclass, bname, tfname, tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, comment, seq, alignment, self.parser)
			alignobj.addsequence(sequence)

		return alignments