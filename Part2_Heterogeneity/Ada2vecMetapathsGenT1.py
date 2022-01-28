import sys
import os
import random
from collections import Counter

class MetaPathGenerator:
	def __init__(self):
		self.id_author = dict()
		self.id_conf = dict()
		self.author_coauthorlist = dict()
		self.conf_authorlist = dict()
		self.author_conflist = dict()
		self.paper_author = dict()
		self.author_paper = dict()
		self.conf_paper = dict()
		self.paper_conf = dict()
		self.node_neighbourlist = dict()
		self.newchangedexistingauthorlist = []
		self.newchangedexistingconflist = []
		#self.missingconf = 0
		#self.missingauthor = 0

	def read_data(self, dirpath):
		with open(dirpath + "/id_author.txt") as adictfile:
			for line in adictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					self.id_author[toks[0]] = toks[1].replace(" ", "")
		print "#authors (actual)", len(self.id_author)

		with open(dirpath + "/id_conf.txt") as cdictfile:
			for line in cdictfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					newconf = toks[1].replace(" ", "")
					self.id_conf[toks[0]] = newconf
		print "#conf (actual)", len(self.id_conf)

		with open(dirpath + "/paper_author.txt") as pafile:
			for line in pafile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					p, a = toks[0], toks[1]
					if p not in self.paper_author:
						self.paper_author[p] = []
					self.paper_author[p].append(a)
					if a not in self.author_paper:
						self.author_paper[a] = []
					self.author_paper[a].append(p)

		with open(dirpath + "/paper_conf.txt") as pcfile:
			for line in pcfile:
				toks = line.strip().split("\t")
				if len(toks) == 2:
					p, c = toks[0], toks[1]
					self.paper_conf[p] = c 
					if c not in self.conf_paper:
						self.conf_paper[c] = []
					self.conf_paper[c].append(p)

		sumpapersconf, sumauthorsconf = 0, 0
		conf_authors = dict()
		for conf in self.conf_paper:
			papers = self.conf_paper[conf]
			sumpapersconf += len(papers)
			for paper in papers:
				if paper in self.paper_author:
					authors = self.paper_author[paper]
					sumauthorsconf += len(authors)

		print "#confs  ", len(self.conf_paper)
		print "#papers ", sumpapersconf,  "#papers per conf ", sumpapersconf / len(self.conf_paper)
		print "#authors", sumauthorsconf, "#authors per conf", sumauthorsconf / len(self.conf_paper)


		newchangedexistinglist = []
		#newchangedexistingauthorlist = []
		#newchangedexistingconflist = []
		#counttest = 1
		with open(dirpath + "/newvchangedexistingobject_id_object_2013_03.txt") as newchangedexistingfile:
			for line in newchangedexistingfile:
				toks = line.strip().split("\t")
				objectid = toks[0]
				if objectid not in newchangedexistinglist:
					newchangedexistinglist.append(objectid)
				if objectid.startswith("a") and objectid not in self.newchangedexistingauthorlist:
					self.newchangedexistingauthorlist.append(objectid)
				if objectid.startswith("v") and objectid not in self.newchangedexistingconflist:
					self.newchangedexistingconflist.append(objectid)
				#print "counttest value: ", counttest
				#counttest += 1
		print "#new and changed existing objects", len(newchangedexistinglist)
		print "#new and changed existing authors", len(self.newchangedexistingauthorlist)
		print "#new and changed existing confs", len(self.newchangedexistingconflist)




	def generate_random_aca(self, outfilename, numwalks, walklength, neighbourlistoutfilename):
		for conf in self.conf_paper:
			self.conf_authorlist[conf] = []
			for paper in self.conf_paper[conf]:
				if paper not in self.paper_author: continue
				for author in self.paper_author[paper]:
					self.conf_authorlist[conf].append(author)
					if author not in self.author_conflist:
						self.author_conflist[author] = []
					self.author_conflist[author].append(conf)
		#print "author-conf list done"
		print "number of confs  ", len(self.conf_authorlist)
		print "number of authors  ", len(self.author_conflist)

		print "Starting cac  "
		authorneighbourlist = []
		missingconfnum = 1
		outfile = open(outfilename, 'w')
		#for conf in self.conf_authorlist:
		for conf in self.newchangedexistingconflist:
			conf0 = conf
			if conf0 not in self.conf_authorlist:
				missingconfnum += 1
				continue
			if conf0 not in self.node_neighbourlist:
				self.node_neighbourlist[conf0] = []
			for j in xrange(0, numwalks ): #wnum walks
				outline = self.id_conf[conf0]
				for i in xrange(0, walklength):
					authors = self.conf_authorlist[conf]
					numa = len(authors)
					authorid = random.randrange(numa)
					author = authors[authorid]
					outline += " " + self.id_author[author]
					#if author not in self.node_neighbourlist[conf0]:
						#self.node_neighbourlist[conf0].append(author)
					if author not in authorneighbourlist:
						authorneighbourlist.append(author)
					confs = self.author_conflist[author]
					numc = len(confs)
					confid = random.randrange(numc)
					conf = confs[confid]
					outline += " " + self.id_conf[conf]
				outfile.write(outline + "\n")
			for currentauthorneighbour in authorneighbourlist:
				self.node_neighbourlist[conf0].append(currentauthorneighbour)
			authorneighbourlist = []
		print "Finished cac  "

		print "Starting aca  "
		venueauthorneighbourlist = []
		missingauthornum = 1
		#for theauthor in self.author_conflist:
		for theauthor in self.newchangedexistingauthorlist:
			theauthor0 = theauthor
			if theauthor0 not in self.author_conflist:
				missingauthornum += 1
				continue
			if theauthor0 not in self.node_neighbourlist:
				self.node_neighbourlist[theauthor0] = []
			for m in xrange(0, numwalks ):
				outline0 = self.id_author[theauthor0]
				for n in xrange(0, walklength):
					conferences = self.author_conflist[theauthor0]
					numc0 = len(conferences)
					conferenceid = random.randrange(numc0)
					conference = conferences[conferenceid]
					outline0 += " " + self.id_conf[conference]
					#if conference not in self.node_neighbourlist[theauthor0]:
						#self.node_neighbourlist[theauthor0].append(conference)
					if conference not in venueauthorneighbourlist:
						venueauthorneighbourlist.append(conference)
					theauthors = self.conf_authorlist[conference]
					numa0 = len(theauthors)
					theauthorid = random.randrange(numa0)
					currentauthor = theauthors[theauthorid]
					#if currentauthor not in self.node_neighbourlist[theauthor0]:
						#self.node_neighbourlist[theauthor0].append(currentauthor)
					if currentauthor not in venueauthorneighbourlist:
						venueauthorneighbourlist.append(currentauthor)
					outline0 += " " + self.id_author[currentauthor]
				outfile.write(outline0 + "\n")
			for currentvenueauthorneighbour in venueauthorneighbourlist:
				self.node_neighbourlist[theauthor0].append(currentvenueauthorneighbour)
			venueauthorneighbourlist = []

		outfile.close()
		print "Finished aca  "
		print "Number of missing authors  ", missingauthornum
		print "Number of missing confs  ", missingconfnum

		#write neighbour nodes for venue and author nodes
		print "Starting neighbourlist writing  "
		neighbourlistoutfile = open(neighbourlistoutfilename, 'w')
		#neighbourlistoutfile.write("Neighbour List:" + "\n")
		for node in self.node_neighbourlist:
			neighbourlistoutfile.write(node + "\n")
			allneighbour = ""
			for neighbour in self.node_neighbourlist[node]:
				allneighbour += neighbour + " "
			neighbourlistoutfile.write(allneighbour + "\n")

		neighbourlistoutfile.close()
		print "Finished neighbourlist writing  "
		#print "missingconf:  ", missingconf
		#print "missingauthor:  ", missingauthor


#sample cmd run command:
#python Ada2vecMetapathsGenT1.py 50 20 Ada2vecCodeData/Part1_Dynamic_(Processed_Datasets)/2013 AMiner2013SubsetV1.w50.l20.txt AMiner2013SubsetV1.w50.l20.neighbourlist.txt






numwalks = int(sys.argv[1])
walklength = int(sys.argv[2])

dirpath = sys.argv[3]
outfilename = sys.argv[4]
neighbourlistoutfilename = sys.argv[5]

def main():
	mpg = MetaPathGenerator()
	mpg.read_data(dirpath)
	mpg.generate_random_aca(outfilename, numwalks, walklength, neighbourlistoutfilename)


if __name__ == "__main__":
	main()






























