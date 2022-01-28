import sys
import os
import random
from collections import Counter


#datasetnameT = "AMiner2011V1.w50.l20.neighbourlist.txt"
#datasetnameT1Subset = "AMiner2013SubsetV1.w50.l20.neighbourlist.txt"


class NeighbourListUpdator:
	def __init__(self):
		self.object_neighbour_T = dict()
		self.object_neighbour_T1Subset = dict()
		#self.object_neighbour_Output = dict()


	def update_neighbourlist(self, datasetnameT, datasetnameT1Subset, updatedneighbourfilename):
		counterT = 1
		counterT1Subset = 1
		#read neighbourlist T
		with open(datasetnameT) as tfile:
			for line in tfile:
				toks = line.strip()
				if (counterT % 2 != 0 and toks not in self.object_neighbour_T):
					self.object_neighbour_T[toks] = []
					objectkey = toks
				if counterT % 2 == 0:
					neighbouritems = toks.split()
					for eachitem in neighbouritems:
						self.object_neighbour_T[objectkey].append(eachitem)
				counterT += 1
		print "#objectkeyT", len(self.object_neighbour_T)

		#read neighbourlist T1 Subset
		with open(datasetnameT1Subset) as t1subsetfile:
			for lineT1 in t1subsetfile:
				toksT1 = lineT1.strip()
				if (counterT1Subset % 2 != 0 and toksT1 not in self.object_neighbour_T1Subset):
					self.object_neighbour_T1Subset[toksT1] = []
					objectkeyT1 = toksT1
				if counterT1Subset % 2 == 0:
					neighbouritemsT1 = toksT1.split()
					for eachitemT1 in neighbouritemsT1:
						self.object_neighbour_T1Subset[objectkeyT1].append(eachitemT1)
				counterT1Subset += 1
		print "#objectkeyT1", len(self.object_neighbour_T1Subset)

		#update neighbourlist T1 Operation
		for eachkey in self.object_neighbour_T:
			if eachkey not in self.object_neighbour_T1Subset:
				self.object_neighbour_T1Subset[eachkey] = []
				allneighbouritems = self.object_neighbour_T[eachkey]
				for eachneighbour in allneighbouritems:
					self.object_neighbour_T1Subset[eachkey].append(eachneighbour)

		#write updated neighbourlist T1 Operation
		print "Writing updated neighbourlist   "
		updatedneighbourfile = open(updatedneighbourfilename, 'w')
		for eachkeyT1 in self.object_neighbour_T1Subset:
			allneighbour = ""
			updatedneighbourfile.write(eachkeyT1 + "\n")
			allneighbouritemsT1 = self.object_neighbour_T1Subset[eachkeyT1]
			for neighbour in allneighbouritemsT1:
				allneighbour += neighbour + " "
			updatedneighbourfile.write(allneighbour + "\n")


		updatedneighbourfile.close()
		print "Finished writing updated neighbourlist  "

#sample cmd run command:
#python updateNeighbourList.py AMiner2011V1.w50.l20.neighbourlist.txt AMiner2013SubsetV1.w50.l20.neighbourlist.txt updatedNeighbourList2013V1.w50.l20.txt


datasetnameTFileName = sys.argv[1]
datasetnameT1SubsetFileName = sys.argv[2]
neighbourfilename = sys.argv[3]


def main():
	nlu = NeighbourListUpdator()
	nlu.update_neighbourlist(datasetnameTFileName, datasetnameT1SubsetFileName, neighbourfilename)



if __name__ == "__main__":
	main()




