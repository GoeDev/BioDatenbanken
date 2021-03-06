import os
import sys
from pathlib import Path
import argparse
import logging

from fastaparser import Fastaparser
from database import Database
from sequence import Sequence
from alignment import Alignment

#loglevel
logging.basicConfig(level=logging.WARNING)


mypath = sys.path[0]

#globale variablen
dbfilename = mypath + "/database.db"
name2idfilename = mypath + "/name2ID.txt"
dbdpath = mypath + "/tfc_dbd_lvl4_fasta/"
logoplotpath = mypath + "/logoplot_fasta/"

dbdsuff = "_mammalia_dbd_fasta.fasta"
logoplotsuff = "_dbd_logoplot.fasta"


#Kommandozeilenargumente verarbeiten usw.
argparser = argparse.ArgumentParser(description='FASTA-Datenbanksoftware für TFC')
sp = argparser.add_subparsers()

sp_id = sp.add_parser("node", help="FASTA-Dateien für beliebigen TFClass-Knoten generieren und Entropie der Alignments dieses Knotens speichern")
sp_id.add_argument('id', help="ID des Knotens")
sp_species = sp.add_parser("species", help="FASTA-Dateien für beliebige biologische Spezies generieren")
sp_species.add_argument('name', help="Name der Spezies")
sp_tf = sp.add_parser("tf", help="FASTA-Dateien für beliebigen Transkriptionsfaktor generieren")
sp_tf.add_argument('tfname', help="Name des Tranksriptionsfaktors")

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

	for filename in os.listdir(dbdpath):
		parser.readfile(dbdpath + filename)

	for filename in os.listdir(logoplotpath):
		parser.readfile(logoplotpath + filename)
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
if hasattr(args,"id"):
	parser.write(args.id + dbdsuff, db.getnode(str(args.id)))
	
	entropies = ""
	for alignment in db.getnodealign(args.id):
		dummysequence = alignment.sequences[0]
		if alignment.multlevels:
			filename = str(dummysequence.tfsuperclass) + "." + str(dummysequence.tfclass) + "." + str(dummysequence.tffamily) + "_" + dummysequence.bclass + logoplotsuff
		else:
			filename = str(dummysequence.tfsuperclass) + "." + str(dummysequence.tfclass) + "." + str(dummysequence.tffamily) + "." + str(dummysequence.tfsubfamily) + "_" + dummysequence.bclass + logoplotsuff
		parser.write(filename, alignment.getfasta())
		entropies += filename + "\n" + alignment.getentropy() + "\n"
	parser.write("entropies.txt", entropies)
elif hasattr(args,"name"):
	parser.write(args.name + dbdsuff, db.getspecies(args.name))
elif hasattr(args,"tfname"):
	parser.write(args.tfname + dbdsuff, db.gettf(args.tfname))