import os
from pathlib import Path
import argparse
import logging

from fastaparser import Fastaparser
from database import Database
from sequence import Sequence
from alignment import Alignment

#loglevel
logging.basicConfig(level=logging.WARNING)

#globale variablen
dbfilename = "database.db"
name2idfilename = "name2ID.txt"
pathprefix = "tfc_dbd_lvl4_fasta"
alignprefix = "logoplot_fasta"


#Kommandozeilenargumente verarbeiten usw.
argparser = argparse.ArgumentParser(description='FASTA-Datenbanksoftware für TFC')
argparser.add_argument("--id", "-i", help="ID, für welche eine FASTA-Datei generiert werden soll")
args = argparser.parse_args()


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

	for filename in os.listdir(os.getcwd() + "/" + alignprefix):
		parser.readfile(alignprefix + "/" + filename)
		parser.aligncounter += 1	

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
	parser.write(args.id + "_mammalia_dbd_fasta.fasta", db.getnode(str(args.id)))
	
	for alignment in db.getnodealign(args.id):
		print(alignment.getprobability())
		dummysequence = alignment.sequences[0]
		if alignment.multlevels:
			filename = str(dummysequence.tfsuperclass) + "." + str(dummysequence.tfclass) + "." + str(dummysequence.tffamily) + "_" + dummysequence.bclass + "_dbd_logoplot.fasta"
		else:
			filename = str(dummysequence.tfsuperclass) + "." + str(dummysequence.tfclass) + "." + str(dummysequence.tffamily) + "." + str(dummysequence.tfsubfamily) + "_" + dummysequence.bclass + "_dbd_logoplot.fasta"
		parser.write(filename, alignment.getfasta())
	