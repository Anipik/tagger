import nltk.data


def conv_sentperline(filename):
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	fo = open(filename, "r+")
	string = fo.read()
	string =' '.join(string.split())
	sent = sent_detector.tokenize(string.strip())
	sent = '\n'.join(sent)
	fo.seek(0)
	fo.write(sent)
	fo.close


conv_sentperline("big.txt")
