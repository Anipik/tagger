import nltk.data
from nltk.tokenize import wordpunct_tokeniz


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
		string = string + '\n'

	return string[:-1]


        









conv_sentperline("big.txt")
