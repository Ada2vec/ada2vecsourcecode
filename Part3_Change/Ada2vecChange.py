import sys
import os
import random
from collections import Counter
import re
from hoeffdingbound import hoeffding_bound
#import numpy as np
from numpy import mean
#from numpy import dtype

datasetdir = "Ada2vecCodeData/Part1_Dynamic_(Processed_Datasets)/2013/Part3_Change_Input_Files"
neighbourlistdatasetname = "/AMiner2011V1.w50.l20.neighbourlist.txt"
connectionTdatasetname = "/object_connection_2011.txt"
connectionT1datasetname = "/object_connection_2013.txt"
testingfilename = "/testingoutputconfidence0.3.txt"
changedobjectsfilename = "/changedobjectsconfidence0.3.txt"
confidencevalue = 0.3


class DatasetMapping:
	def __init__(self):
		self.id_neighbour_T = dict()
		self.id_objectconnection_T = dict()
		self.id_objectconnection_T1 = dict()
		self.binary_object_neighbourconnection_T = dict()
		self.binary_object_neighbourconnection_T1 = dict()
		self.changedobjects = []

	def map_write_data(self):
		linenumber = 1
		linenumber1 = 1
		linenumber2 = 1

		# read and map data for object neighbourlist
		with open(datasetdir + neighbourlistdatasetname) as neighbourlistfile:
			for line in neighbourlistfile:
				#if (linenumber > 1):
				sline = line.strip()
				if (linenumber % 2 != 0 and sline not in self.id_neighbour_T):
					self.id_neighbour_T[sline] = []
					currentkey = sline
				if (linenumber % 2 == 0):
					currentneighbourlist = sline.split(" ")
					for currentneighbour in currentneighbourlist:
						if currentneighbour not in self.id_neighbour_T[currentkey]:
							self.id_neighbour_T[currentkey].append(currentneighbour)
				linenumber += 1
		print "neighbourlist read"

		# read and map data for object connection Time Stamp T
		with open(datasetdir + connectionTdatasetname) as connectionTfile:
			for line in connectionTfile:
				sline = line.strip()
				if (linenumber1 % 2 != 0 and sline not in self.id_objectconnection_T):
						self.id_objectconnection_T[sline] = []
						currentkey = sline
				if (linenumber1 % 2 == 0):
					currentconnectionlist = sline.split(" ")
					for currentconnection in currentconnectionlist:
						if currentconnection not in self.id_objectconnection_T[currentkey]:
							self.id_objectconnection_T[currentkey].append(currentconnection)
				linenumber1 += 1
		print "object connection Time Stamp T read"

		# read and map data for object connection Time Stamp T1
		with open(datasetdir + connectionT1datasetname) as connectionT1file:
			for line in connectionT1file:
				sline = line.strip()
				if (linenumber2 % 2 != 0 and sline not in self.id_objectconnection_T1):
						self.id_objectconnection_T1[sline] = []
						currentkey = sline
				if (linenumber2 % 2 == 0):
					currentconnectionlist = sline.split(" ")
					for currentconnection in currentconnectionlist:
						if currentconnection not in self.id_objectconnection_T1[currentkey]:
							self.id_objectconnection_T1[currentkey].append(currentconnection)
				linenumber2 += 1
		print "object connection Time Stamp T1 read"

		# change detection based on metapath guided neighbour connection across two consecutive timestamps
		for currentobject in self.id_neighbour_T:
			for currentneighbourobject in self.id_neighbour_T[currentobject]:
				if (currentobject not in self.binary_object_neighbourconnection_T):
					self.binary_object_neighbourconnection_T[currentobject] = []
				if (currentobject in self.id_objectconnection_T and currentneighbourobject in self.id_objectconnection_T[currentobject]):
					self.binary_object_neighbourconnection_T[currentobject].append(1)
				else:
					self.binary_object_neighbourconnection_T[currentobject].append(0)
				if (currentobject not in self.binary_object_neighbourconnection_T1):
					self.binary_object_neighbourconnection_T1[currentobject] = []
				if (currentobject in self.id_objectconnection_T1 and currentneighbourobject in self.id_objectconnection_T1[currentobject]):
					self.binary_object_neighbourconnection_T1[currentobject].append(1)
				else:
					self.binary_object_neighbourconnection_T1[currentobject].append(0)
		print "binary appending done"

		# write statement for testing
		testingfile = open(datasetdir + testingfilename, 'w')
		testingfile.write("Binary Object Neighbourconnection Timestamp T:" + "\n")
		for eachobject in self.binary_object_neighbourconnection_T:
			outline = ""
			testingfile.write(eachobject + "\n")
			for eachbinary in self.binary_object_neighbourconnection_T[eachobject]:
				outline += str(eachbinary) + " "
			testingfile.write(outline + "\n")
		testingfile.write("Binary Object Neighbourconnection Timestamp T1:" + "\n")
		for eachobject1 in self.binary_object_neighbourconnection_T1:
			outline1 = ""
			testingfile.write(eachobject1 + "\n")
			for eachbinary1 in self.binary_object_neighbourconnection_T1[eachobject1]:
				outline1 += str(eachbinary1) + " "
			testingfile.write(outline1 + "\n")
		print "testing statement done"

		# identify changed objects using Hoeffding bound
		for eachobject in self.binary_object_neighbourconnection_T:
			#print "eachobject: ", eachobject
			if eachobject not in self.binary_object_neighbourconnection_T1: continue
			timestamp_t_mean = mean(self.binary_object_neighbourconnection_T[eachobject])
			#print "mean t: ", timestamp_t_mean
			timestamp_t_len = len(self.binary_object_neighbourconnection_T[eachobject])
			#print "len t: ", timestamp_t_len
			timestamp_t1_mean = mean(self.binary_object_neighbourconnection_T1[eachobject])
			#print "mean t1: ", timestamp_t1_mean
			timestamp_t1_len = len(self.binary_object_neighbourconnection_T1[eachobject])
			#print "len t1: ", timestamp_t1_len
			if (not hoeffding_bound(float(timestamp_t_mean), float(timestamp_t_len), float(timestamp_t1_mean), float(timestamp_t1_len), float(confidencevalue))) and (eachobject not in self.changedobjects):
				self.changedobjects.append(eachobject)

		# write changed objects
		changedobjectsfile = open(datasetdir + changedobjectsfilename, 'w')
		#changedobjectsfile.write("List of changed objects are:" + "\n")
		for currentchangedobject in self.changedobjects:
			changedobjectsfile.write(currentchangedobject + "\n")


#sample cmd run command:
#python Ada2vecChange.py

def main():
	dm = DatasetMapping()
	dm.map_write_data()

if __name__ == "__main__":
	main()

