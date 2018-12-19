import os
from pathlib import Path

from fastaparser import Fastaparser
from database import Database

dbfilename = "database.db"
name2idfilename = "../name2ID.txt"
pathprefix = "tfc_dbd_lvl4_fasta"

existcheck = Path(dbfilename)
if existcheck.is_file():
	pass
else:
	parser = Fastaparser()
	parser.readname2id(name2idfilename)

	for filename in os.listdir(os.getcwd() + "/" + pathprefix):
		parser.readfile(pathprefix + "/" + filename)

	db = Database(dbfilename)
	db.createbasestructure()

	db.insert_bclass("mammalia")
    
	for name, id in parser.name2id.items():
		splitid = id.split(".")
		db.insert_tfname(name, splitid[0], splitid[1], splitid[2], splitid[3], splitid[4])

	for seq in parser.seqlist:
		db.insert_bname(seq)
		db.insert_sequence(seq)

	db.commit()
#for seq in parser.seqlist:
#	print("Genus:" + seq.tfgenus + " Name:" + seq.bname + " TFName:" + seq.tfname + " Sequenz:" + seq.sequence)