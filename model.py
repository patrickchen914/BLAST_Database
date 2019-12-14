from sqlobject import *
import os.path, sys

dbfile = 'Blast.db3'

def init(new=False):
	conn_str = os.path.abspath(dbfile)
	conn_str = 'sqlite:'+ conn_str
	
	sqlhub.processConnection = connectionForURI(conn_str)
	if new:
		Protein.dropTable(ifExists=True)
		Alignment.dropTable(ifExists=True)
		Protein.createTable()
		Alignment.createTable()

class Protein(SQLObject):
	class sqlmeta:
		idName = 'protein_id'
	accession = StringCol(alternateID=True)
	title = StringCol()
	queryID = MultipleJoin('Alignment', joinColumn= 'protein_id')
	alignmentID = MultipleJoin('Alignment', joinColumn = 'protein_id')

class Alignment(SQLObject):
	queryID = ForeignKey('Protein', dbName='query_id')
	alignmentID = ForeignKey('Protein', dbName='alignment_id')

	eValue = FloatCol()
	length = IntCol()

	query = StringCol()
	alignment = StringCol()
	subject = StringCol()

init()
