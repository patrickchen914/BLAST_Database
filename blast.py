from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast import NCBIXML

from model import *
#create the tables
init()

drosoph = 'blastdb/drosoph-ribosome.fasta'
yeast = 'blastdb/yeast-ribosome.fasta'

#first, store all the protein ids to Protein table
#drosoph
for record in SeqIO.parse(drosoph, "fasta"):
	accession = record.id.split('|')[3]
	p = Protein(accession = accession, title = record.description)
print('drosoph proteins added')

#yeast
for record in SeqIO.parse(yeast, "fasta"):
	accession = record.id.split('|')[3]
	p = Protein(accession = accession, title = record.description)
print('yeast proteins added')


#second, Blast the heck out of it
def addData(blast_query, blast_db):
	blast_prog = '/usr/local/bin/blastp'

	cmdline = NcbiblastpCommandline(cmd=blast_prog,
					query=blast_query,
					db=blast_db,
					outfmt=5,
					out="results.xml")
	stdout, stderr = cmdline()

	result_handle = open('results.xml')

	for blast_result in NCBIXML.parse(result_handle):
		title = blast_result.query
		accession = blast_result.query.split('|')[3]
		#print(accession, title)

		#get the id of the accession which will be 'query_id' later
		query_id = Protein.selectBy(accession = accession)[0].id

		#Add query, alignment, length and eValue to the Alignment table
		for alignment in blast_result.alignments:
			for hsp in alignment.hsps:
				aAccession = alignment.title.split('|')[5]
				aTitle = alignment.title
				length = alignment.length
				eValue = hsp.expect
				queryFull = hsp.query
				alignmentFull = hsp.match
				subject = hsp.sbjct
				#print(accession, aAccession)
				
				#get the id of the aAccession which will be 'alignment_id' later
				alignment_id = Protein.selectBy(accession = aAccession)[0].id
				a = Alignment(queryID = query_id, 
						alignmentID = alignment_id, 
						length = length, eValue = eValue, 
						query = queryFull, alignment = alignmentFull, subject = subject)


#First, add all the data of the blast result of drosoph against yeast		
addData(drosoph, yeast)
print('finished drosoph against yeast')

#Second, the other way around
addData(yeast, drosoph)
print('finished yeast against drosoph')
