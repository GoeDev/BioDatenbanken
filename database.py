import sqlite3

from sequence import Sequence

class Database(object):
	def __init__(self, dbfile, parser):
		self.conn = sqlite3.connect(dbfile)
		self.cursor = self.conn.cursor()

	def createbasestructure(self):
		self.cursor.execute('''CREATE TABLE bclasses 
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT)''')
		self.cursor.execute('''CREATE TABLE bnames 
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT,
		UNIQUE(name))''')
		self.cursor.execute('''CREATE TABLE tfnames 
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
		name TEXT,
		superclass INTEGER NOT NULL,
		class INTEGER NOT NULL,
		family INTEGER NOT NULL,
		subfamily INTEGER NOT NULL,
		genus INTEGER NOT NULL)''')
		self.cursor.execute('''CREATE TABLE sequences 
		(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
		tfcname INTEGER NOT NULL,
		bclass INTEGER NOT NULL,
		bname INTEGER NOT NULL,
		tfsuperclass INTEGER NOT NULL,
		tfclass INTEGER NOT NULL,
		tffamily INTEGER NOT NULL,
		tfsubfamily INTEGER NOT NULL,
		tfgenus INTEGER NOT NULL,
		tfspecies INTEGER NOT NULL,
		comment TEXT,
		sequence TEXT,
		FOREIGN KEY (tfcname) REFERENCES tfnames(id),
		FOREIGN KEY (bclass) REFERENCES bclasses(id),
		FOREIGN KEY (bname) REFERENCES bnames(id))''')

	def insert_bclass(self, name):
		self.cursor.execute("INSERT INTO bclasses (name) VALUES ('" + name + "')")

	def insert_bname(self, sequence):
		self.cursor.execute("INSERT OR IGNORE INTO bnames (name) VALUES ('" + sequence.bname + "')")

	def insert_tfname(self, name, superclass, tfclass, family, subfamily, genus):
		self.cursor.execute("INSERT INTO tfnames (name, superclass, class, family, subfamily, genus) VALUES ('" + name + "', '" + superclass + "', '"+ tfclass+"', '"+ family +"', '"+subfamily+"', '"+genus+"')")

	def insert_sequence(self, sequence):
		self.cursor.execute("SELECT id FROM bclasses WHERE name='" + sequence.bclass+"'")
		bclid = self.cursor.fetchone()[0]
		self.cursor.execute("SELECT id FROM bnames WHERE name='" + sequence.bname+"'")
		bnid = self.cursor.fetchone()[0]
		self.cursor.execute("SELECT id FROM tfnames WHERE name='" + sequence.tfname+"'")
		tfnid = self.cursor.fetchone()[0]
		query = "INSERT INTO sequences (tfcname, bclass, bname, tfsuperclass, tfclass, tffamily, tfsubfamily, tfgenus, tfspecies, comment, sequence)"
		query += " VALUES ('" + str(tfnid) + "', '" + str(bclid) + "', '" + str(bnid) + "', '" + str(sequence.tfsuperclass) + "', '" + str(sequence.tfclass) + "', '" + str(sequence.tffamily) + "', '" + str(sequence.tfsubfamily) + "', '" + str(sequence.tfgenus) + "', '" + str(sequence.tfspecies) + "', '" + sequence.comment + "', '" + sequence.sequence + "')" 
		self.cursor.execute(query)

	def commit(self):
		self.conn.commit()

	def getnode(self, id):
		idsplit = id.split(".")