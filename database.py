import sqlite3

from sequence import Sequence

class Database(object):
	def __init__(self, dbfile, parser):
		self.conn = sqlite3.connect(dbfile)
		self.cursor = self.conn.cursor()

	def createbasestructure(self):
		self.cursor.execute('''CREATE TABLE bclasses 
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, bclass TEXT)''')
		self.cursor.execute('''CREATE TABLE bnames 
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, bname TEXT,
		UNIQUE(name))''')
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
		query = "INSERT INTO sequences (tfnameid, bclassid, bnameid, tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, comment, sequence)"
		query += " VALUES ('" + str(tfnid) + "', '" + str(bclid) + "', '" + str(bnid) + "', '" + str(sequence.tfsuperclass) + "', '" + str(sequence.tfclass) + "', '" + str(sequence.tffamily) + "', '" + str(sequence.tfsubfamily) + "', '" + str(sequence.tfgenus) + "', '" + str(sequence.tfspecies) + "', '" + sequence.comment + "', '" + sequence.sequence + "')" 
		self.cursor.execute(query)

	def commit(self):
		self.conn.commit()

	def getnode(self, id):
		
		idsplit = id.split(".")
		level = len(idsplit)
		
		query = "SELECT tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, tfname, bclass, bname, sequence, comment FROM sequences "
		query += "INNER JOIN bclasses ON bclasses.id = sequences.bclassid INNER JOIN bnames ON bnames.id = sequences.bnameid INNER JOIN tfnames ON tfnames.ID = sequences.tfnameid "
		query += "WHERE tfsuperclass=" + idsplit[0]
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
			args = {"bname": sequencedata[8],
			"tfname": sequencedata[6],
			"tfsuperclass": sequencedata[0],
			"tfclass": sequencedata[1],
			"tffamily": sequencedata[2],
			"tfsubfamily": sequencedata[3],
			"tfgenus": sequencedata[4]}
			sequence = Sequence(bclass, "", tfspecies, comment, seq, self.parser, args)
			fasta += self.parser.generate(sequence)

		return fasta