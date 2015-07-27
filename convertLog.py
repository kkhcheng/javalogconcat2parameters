import os
import fnmatch
import re

def convertLog(filename):
	print filename + ":"
	# file is an iterator
	with open(filename) as file:
		tempfilename = filename + "_tmp1234"
		outfile = open(tempfilename, "w")
		for line in file:
			if (re.search("logger.logp", line) != None):
				# tokens = line.split(",")
				if (re.search(";", line) == None):
					#multiline statement, merge into single line
					multiline = line
					for line in file:
						multiline += line.replace('\t',"")
						# print "multi:"+ multiline
						# edge = len(tokens)-1
						# tokens += line.split(",")
						# tokens[edge:edge+1] = [''.join(tokens[edge:edge+1])]
						if (re.search(";", line) != None):
							break;
					templine = multiline.replace('\n', "")

				else:
					templine = line	

				# print "original:"
				# print templine
				tokens = templine.split("+")
				#print "tokens:" 
				#print tokens
				if (len(tokens) >1):
					fixedParams = tokens[0].split(',')
					fixlen = len(fixedParams)
					begining = ','.join(fixedParams[0:fixlen-1])
					#print "begining:" + begining
					paramstr = ""
					end = "new Object[] {"+ fixedParams[fixlen-1] + ',' + ','.join(tokens[1:len(tokens)]).replace(");", "});")
					#print "end:" + end
					for i in range(len(tokens)):
						paramstr += '{' + str(i) + '} '

					# print "new line:" 
					print >>outfile, begining + ',"'+ paramstr.strip() +'",'+ end

				else:
					# print "############no change:"
					print >>outfile, templine
			else:
				outfile.write(line)
		outfile.close()
	file.close()
	os.remove(filename)
	os.rename(tempfilename, filename)
				


for root, dirnames, filenames in os.walk("."):
	for filename in fnmatch.filter(filenames, "*.java"):
		convertLog(os.path.join(root, filename))
		