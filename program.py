import os
from pathlib import Path
import argparse

from fastaparser import Fastaparser
from database import Database

#globale variablen
dbfilename = "database.db"
name2idfilename = "name2ID.txt"
pathprefix = "tfc_dbd_lvl4_fasta"


#Kommandozeilenargumente verarbeiten usw.
argparser = argparse.ArgumentParser(description='FASTA-Datenbanksoftware für TFC')
argparser.add_argument("--id", "-i", help="ID, für welche eine FASTA-Datei generiert werden soll")
args = argparser.parse_args()
print(args.id)


parser = Fastaparser()
db = None

#Datenbankstuff
existcheck = Path(dbfilename)
if existcheck.is_file():
	db = Database(dbfilename, parser)
else:
	print("Datenbank nicht gefunden, erzeuge Datenbank...")
	parser.readname2id(name2idfilename)

	for filename in os.listdir(os.getcwd() + "/" + pathprefix):
		parser.readfile(pathprefix + "/" + filename)

	db = Database(dbfilename, parser)
	db.createbasestructure()

	db.insert_bclass("mammalia")
    
	for name, id in parser.name2id.items():
		splitid = id.split(".")
		db.insert_tfname(name, splitid[0], splitid[1], splitid[2], splitid[3], splitid[4])

	for seq in parser.seqlist:
		db.insert_bname(seq)
		db.insert_sequence(seq)

	db.commit()


#Fasta-Datei für ID ausgeben
if not args.id == None:
	print(db.getnode(str(id)))
	