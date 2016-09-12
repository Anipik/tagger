import nltk.data
from nltk.tokenize import wordpunct_tokenize
#from nltk.tokenize import word_tokenize

def conv_sentperline(filename):
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	fo = open(filename, "r+")
	string = fo.read()
	string =' '.join(string.split())
	sent = sent_detector.tokenize(string.strip())
	sent_join = '\n'.join(sent)
	fo.seek(0)
	fo.write(sent_join)
	fo.close
	return sent

def file_to_datapoint_without_tag(filename):
	string=""
	sentences = conv_sentperline(filename)
	for sent in sentences:
		words = wordpunct_tokenize(sent)
		for word in words:
			string = string + word+'\n'
			#print(string)
		string = string + '\n'

	string = string[:-1]
	fo = open(filename[:-4]+'_col.txt','w')
	fo.seek(0)
	fo.write(string)
	fo.close
	return string

def mergewithtag(input_file,tag):
	string=""
	in1 = open(input_file,"r+")
	in2 = open(tag,"r+")
	out = open(input_file[:-4]+"_final.txt",'w')
	for line,line1 in zip(in1,in2):
		if line == "\n":
			string=string+line
		else:
			string = string + line[:-1] +"\t" +line1
	out.seek(0)
	out.write(string)
	out.close()
	in1.close()
	in2.close() 

#file_to_datapoint_without_tag("big.txt")

mergewithtag("big_col.txt","big_col.txt")
