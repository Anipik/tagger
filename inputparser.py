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



def file_to_datapoint(filename):
	string=""
	tag = "O"
	sentences = conv_sentperline(filename)
	for sent in sentences:
		words = wordpunct_tokenize(sent)
		for word in words:
			string = string + word +'\t' + tag+'\n'
			#print(string)
		string = string + '\n'

	string = string[:-1]
	fo = open(filename,'w')
	fo.seek(0)
	fo.write(string)
	fo.close
	return string


        









file_to_datapoint("big.txt")
