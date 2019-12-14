import sys
from sqlobject import *
import os.path

#import my database
from model import*

#first_input, second_input = str(sys.argv[1]), str(sys.argv[2])

try:
	first_input, second_input = str(sys.argv[1]), str(sys.argv[2])

except IndexError:
	print('Need 2 protein accessions', file=sys.stderr)
	sys.exit(1)

try:
	queryID = Protein.selectBy(accession = first_input)[0].id
	alignmentID = Protein.selectBy(accession = second_input)[0].id
except IndexError:
	print('Accession not in database')
	sys.exit(1)
#print('Query ID:', queryID, 'Alignment ID:', alignmentID)


#eliminate the possibility of entering 2 proteins that are not aligned in the database
try:
	#If the accession was not in the database, result would be empty  
	result = Alignment.selectBy(queryID=queryID, alignmentID=alignmentID)[0]
	print('Query:', result.queryID.title)
	print('Alignment:', result.alignmentID.title)
	print('E-value:', result.eValue)
	print('Length:', result.length)
	
	for i in range(((len(result.query)-1) // 100) +1):
		print('-' * 100)
		print(result.query[0 + i*100 : 99 + i*100])
		print(result.alignment[0 + i*100 : 99 + i*100])
		print(result.subject[0 + i*100 : 99 + i*100])
		
except IndexError:
	print('They are not aligned')
	sys.exit(1)






