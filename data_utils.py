import tensorflow as tf
import os, sys
import nltk.data
from nltk.tokenize import wordpunct_tokenize
reload(sys)
sys.setdefaultencoding('utf-8')

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def tokenize_phrase(phrase):
	return wordpunct_tokenize(phrase)

def conv_sentperline(text):
	sent = sent_detector.tokenize(text.strip())
	return sent

def file_to_datapoint_without_tag(filename):
	with open(filename+'.txt', 'rb') as f:
		sentences = conv_sentperline(f.read())
		words = [tokenize_phrase(sentence) for sentence in sentences]
		text = '\n\n'.join(['\n'.join(sent) for sent in words])
        #debug code
        # fo = open(filename+'.col','wb')
        # fo.write(text)
        # fo.close()
        mergewithtag(filename, words)
	

def mergewithtag(filename, words):
    string=""
    in2 = open(filename+'.out',"rb")
    out = open(filename+".final",'wb')
    file2 = in2.read().split()
    j=0
    offset = 0
    for sentence in words:
        string += '\n'.join([sentence[i]+'\t'+file2[offset+i]  for i in xrange(len(sentence))])
        offset += len(sentence)
        string += '\n\n'
    out.write(string)
    out.close()
    in2.close() 

def convert_output(filename):
    tags = ['HAB', 'HABCONT', 'BAC', 'BACCONT', 'GEO', 'GEOCONT']
    # filename = 'BB-cat+ner-6107735'
    # print(filename)
    with tf.gfile.GFile(filename+'.txt', "r") as f:
        with tf.gfile.GFile(filename+'.a2', "r") as f1:
            text = f.read().decode('utf-8')
            init = len(tokenize_phrase(text.strip()))
            a2 = f1.read().splitlines()
            red = 0
            end = 0
            start = 0
            prev_red = 0
            for line in a2:
                if line[0] == 'T':
                    split_line = line.split()
                    if ';' in split_line[3]:
                        split_line.remove(split_line[3]);
                    left = int(split_line[2]) - red
                    if int(split_line[2]) == start:
                        left += prev_red
                    right = int(split_line[3]) - red
                    if int(split_line[3]) <= end:
                        continue
                    end = int(split_line[3])
                    start = int(split_line[2])
                    #debug code
                    # print (text[left:right] + " : " + split_line[1][0:3].upper() + " " + str(len(split_line[5:])))
                    red = red + len(text)
                    prev_red = len(text)
                    # if text[left-1] not in [' ', '\n']:
                    #     left -= 1;
                    # if text[right] not in [' ', '\n']:
                    #     right += 1;
                    text = text[:left] + split_line[1][0:3].upper() + ''.join([' ' + split_line[1][0:3].upper() + 'CONT']*len(tokenize_phrase(text[left:right])[1:])) + text[right:]
                    red = red - len(text)
                    prev_red -= len(text)
    new_text = ['OTH' if word not in tags else word for word in tokenize_phrase(text.strip())]
    #debug code
    # if init != len(tokenize_phrase(text.strip())):
    #     print (filename)
    #     print (init)
    #     print (back)
    #     break
    # words = [tokenize_phrase(sentence) for sentence in conv_sentperline(text)]
    # text = '\n\n'.join(['\n'.join(sent) for sent in words])
    # print(text)
    # print(' '.join(new_text))
    with tf.gfile.GFile(filename+'.out', "w") as f:
        f.write((' '.join(new_text)).encode('utf-8'))
    # return outputs


path = 'data/BioNLP-ST-2016_BB-cat+ner_train/'
filenames = []
for file in os.listdir(path):
    if file.endswith(".txt"):
        filenames.append(file[:-4])
for filename in filenames:
	print(path+filename)
	convert_output(path + filename)
	file_to_datapoint_without_tag(path + filename)
# convert_output('data/BioNLP-ST-2016_BB-cat+ner_train/BB-cat+ner-19622846')
# file_to_datapoint_without_tag('data/BioNLP-ST-2016_BB-cat+ner_train/BB-cat+ner-19622846')