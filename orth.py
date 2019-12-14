from sqlobject import *
import os.path

#import my database
from model import*

def getOrtholog(queryID):
	try:
		condition = Alignment.selectBy(queryID=queryID)[0]
	except IndexError:
		print('Protein id "'+ str(queryID)+'" not in database. Or does not have any alignment.')
		return 0
	condition = Alignment.selectBy(queryID=queryID)
	
	#find the best hit by smallest evalue
	eValueList = []
	for row in condition:
		eValueList.append(row.eValue)

	minEValue = min(eValueList)
	#print(minEValue)

	condition = Alignment.selectBy(queryID=queryID, eValue=minEValue)[0]

	orthologID = condition.alignmentID.id
	#print('The best orthologous protein of ' + str(queryID) + ' is', orthologID)
	
	return orthologID

def checkOrtholog(queryID):
	isOrth = False
	orth = getOrtholog(queryID)
	if orth != 0:
		if getOrtholog(orth) == queryID:
			isOrth = True
	
	return isOrth

def main():
	pairs = {}
	#find iterate the proteins in the Pretein table
	for row in Protein.selectBy():
		query = row.id
		if checkOrtholog(row.id) == True:
			alignment = getOrtholog(query)
			#eliminate duplicates
			Min = min(query, alignment)
			Max = max(query, alignment)
			if Min not in pairs:
				pairs[Min] = Max

	print('-' * 100)
	for query, alignment in pairs.items():
		queryAccession = Protein.get(query).accession
		alignmentAccession = Protein.get(alignment).accession
		print(str(queryAccession) + ' and ' + alignmentAccession + ' are mutually best hits')

main()


