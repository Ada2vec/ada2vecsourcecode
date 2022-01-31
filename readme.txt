Part2_Heterogeneity
-------------------------------------------------------------------------------
Examples:
python Ada2vecMetapathsGenT.py 50 20 Ada2vecCodeData/Part1_Dynamic_(Processed_Datasets)/2011 AMiner2011V1.w50.l20.txt AMiner2011V1.w50.l20.neighbourlist.txt


Usage:
python Ada2vecMetapathsGenT.py [paramters]
Parameters for generating metapath-guided random walks:
	-numwalks <int>
		Set number of random walks
	-walklength <int>
		Set length of random walks
	-dirpath
		Use input data from dirpath to generate metapath-guided random walks
	-output
		random walk output file name
	-output
		node heterogeneous neighbour list output file name


Input:
	Nodes and edges in the dynamic heterogeneous graph at the initial time stamp t=1.
	An example can be found in ../Part1_Dynamic_(Processed_Datasets)/2011
	Example input files are:
		1. id_author.txt
		2. id_conf.txt
		3. paper_author.txt
		4. paper_conf.txt


Output:
	The metapath-guided random walks, each of which consists of different types of nodes. An example can be found in ../Part1_Dynamic_(Processed_Datasets)/2013/AMiner2013SubsetV1.w50.l20.txt
	Currently, the code supports two types of nodes: 
		1. one starting from "v", e.g., vMachineLearning
		2. one starting from "a", e.g., aMichaelP.Wellman


	Node heterogeneous neighbour list. An example can be found in ../Part1_Dynamic_(Processed_Datasets)/2013/AMiner2013SubsetV1.w50.l20.neighbourlist.txt


Examples:
python Ada2vecMetapathsGenT1.py 50 20 Ada2vecCodeData/Part1_Dynamic_(Processed_Datasets)/2013 AMiner2013SubsetV1.w50.l20.txt AMiner2013SubsetV1.w50.l20.neighbourlist.txt

Please notice that the Usage, Input and Output of Ada2vecMetapathsGenT1.py is very similar to Ada2vecMetapathsGenT.py.

Main difference is the input, the input of Ada2vecMetapathsGenT1.py are nodes and edges in the dynamic heterogeneous graph from the time stamp t+1 (t=1,2,3,...,i).

In addition, when generating metapath-guided random walks, the Ada2vecMetapathsGenT1.py script maps from new and changed existing nodes instead of all the nodes in the network. Refer to code in line 80 "with open(dirpath + "/newvchangedexistingobject_id_object_2013_03.txt") as newchangedexistingfile:".


-------------------------------------------------------------------------------
Part3_Change
-------------------------------------------------------------------------------
Examples:
python Ada2vecChange.py


Usage:
identify changed existing nodes using the hoeffding bound


Input:
parameters of the Ada2vecChange.py script (line 11-17):
	-datasetdir
		File directory of input files; an example directory is ../Part1_Dynamic_(Processed_Datasets)/2013/Part3_Change_Input_Files
	-neighbourlistdatasetname
		File name of node heterogeneous neighbour list; an example file is	../Part1_Dynamic_(Processed_Datasets)/2013/Part3_Change_Input_Files/AMiner2011V1.w50.l20.neighbourlist.txt
	-connectionTdatasetname
		File name of node heterogeneous connection at time stamp t (t=1,2,3,...,i); an example file is ../Part1_Dynamic_(Processed_Datasets)/2013/Part3_Change_Input_Files/object_connection_2011.txt
	-connectionT1datasetname
		File name of node heterogeneous connection at time stamp t+1 (t=1,2,3,...,i); an example file is ../Part1_Dynamic_(Processed_Datasets)/2013/Part3_Change_Input_Files/object_connection_2013.txt
	-testingfilename
		File name of testing output file; an example file is ../Part1_Dynamic_(Processed_Datasets)/2013/Part3_Change_Input_Files/testingoutputconfidence0.3.txt
	-changedobjectsfilename
		File name of changed existing node output file; an example file is ../Part1_Dynamic_(Processed_Datasets)/2013/Part3_Change_Input_Files/changedobjectsconfidence0.3.txt
	-confidencevalue
		Confidence value set of the the hoeffding bound


Output:
	Changed existing node output file; an example file is ../Part1_Dynamic_(Processed_Datasets)/2013/Part3_Change_Input_Files/changedobjectsconfidence0.3.txt
	
	Testing output file; an example file is ../Part1_Dynamic_(Processed_Datasets)/2013/Part3_Change_Input_Files/testingoutputconfidence0.3.txt
