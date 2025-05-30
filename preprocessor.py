from keybert._model import KeyBERT
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sympy import evaluate
import tensorflow as tf
import tensorflow_hub as hub
import nltk
import re
import string
import math
import torch
import requests
from dotenv import load_dotenv
import os
load_dotenv()

# rake = Rake()
# tensroflow hub module for Universal sentence Encoder 
#module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" 
#@param ["https://tfhub.dev/google/universal-sentence-encoder/2", "https://tfhub.dev/google/universal-sentence-encoder-large/3"]

#embed = hub.load(module_url)
embed = tf.saved_model.load('model')
def get_features(texts):
    if type(texts) is str:
        texts = [texts]
    #tf.run([tf.global_variables_initializer(), tf.tables_initializer()])
    return embed(tf.constant(texts))

#read the question and answer data from the file
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return data

def getMarks(question):
    s = question[(question.rindex('[')+1):(question.rindex(']'))]
    return float(s)

def listToString(list):
    str=" "
    return(str.join(list))

#def preprocess(text):
   ####### return listToString(words)

def keywordsExtract(text):
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(text)
    keywords = [k[0] for k in keywords]
    return keywords

# def cosine_similarity(model, answer):
#     rvector = set(model).union(set(answer))
#     l1=[]
#     l2=[]
#     for w in rvector: 
#         if w in set(model): l1.append(1) 
#         else: l1.append(0) 
#         if w in set(answer): l2.append(1) 
#         else: l2.append(0)

#     c = 0
#     for i in range(len(rvector)): 
#         c+= l1[i]*l2[i]

#     cosine = c / float((sum(l1)*sum(l2))**0.5)
#     return cosine 

def cosine_similarity(v1, v2):
    # a = np.array(v1)
    # b = np.array(v2)
    # mag1 = np.linalg.norm(a)
    # mag2 = np.linalg.norm(b)
    # if (not mag1) or (not mag2):
    #     return 0
    #return np.dot(a, b) / (mag1 * mag2)
    #cosi = torch.nn.CosineSimilarity(dim=0)
    #return cosi(v1, v2)
    #return tf.keras.losses.cosine_similarity(v1,v2 )
    # tf.convert_to_tensor(v1)
    # tf.convert_to_tensor(v2)
    # print(type(v1))
    # cos = tf.nn.CosineSimilarity(dim=1)
    # return cos(v1,v2)
    t1 = tf.nn.l2_normalize(v1, axis=1)
    t2 = tf.nn.l2_normalize(v2, axis=1)
    cosine = tf.reduce_sum(tf.multiply(t1, t2), axis=1)
    clip_cosine = tf.clip_by_value(cosine, -1.0, 1.0)
    scores = 1.0 - tf.acos(clip_cosine) / np.pi
    return scores

def test_similarity(text1, text2):
    vec1 = get_features(text1)
    vec2 = get_features(text2)
    #print(vec1.shape)
    # tens_1 = torch.tensor(vec1)
    # tens_2 = torch.tensor(vec2)
    return cosine_similarity(vec1, vec2)

def keyword_Matching(model, answer):
    score = 0
    numKeywords = len(model)
    for item in model:
        if item in answer:
            score += 1
    score = score / numKeywords
    return score

def grammar_check(sentence):
    # base_url = "https://api.textgears.com/grammar?key="+os.environ['GRAMMAR_API_KEY']+"&language=en-GB&ai=true"
    base_url = "https://api.textgears.com/grammar?key="+"b4m3d4AWJoBc3qTc"+"&language=en-GB&ai=true"
    sentence = sentence.replace(" ","+")
    r = requests.get(base_url+"&text="+sentence)
    return len(r.json()['response']['errors'])

def grammar_score(model,answer):
    model_score = grammar_check(model)
    answer_score = grammar_check(answer)
    score = 1 - (abs(model_score - answer_score) / model_score)
    return score
def remove_commas(text):
    return text.replace(","," ")

def evaluate(length):
    question = read_data('Data\\question.txt')[0]
    marks = getMarks(question)
    question = question[:(question.rindex('['))]
    model = read_data('Data\\model.txt')[0].lower()
    model_keywords = keywordsExtract(model)
    #print(model_keywords)
    #model = preprocess(model)
    file = open("Data\\dataset.csv","w")
    file.write("Question,Marks,Keyword Score,Grammer Score,Question Score,Total Score")
    question = remove_commas(question)
    for i in range(1,length+1):
        answer = read_data('Data\\answer'+str(i)+'.txt')[0].lower()
        ans = remove_commas(answer)
        file.write("\n" + question + "," + str(marks) + ",")
        answer_keywords = keywordsExtract(answer)
        #answer = preprocess(answer)
        keyword_score = keyword_Matching(model_keywords, answer_keywords) * 0.2 * marks
        qst_score = math.ceil(test_similarity(model, answer) * 0.6 * marks)
        gram_score = grammar_score(model,answer) * 0.2 * marks
        #print("Keyword Score : {keyword:.2f} Question Score : {qst:.2f} Grammer Score : {gst:.2f}".format(keyword=keyword_score, qst=qst_score,gst=gram_score))
        file.write("{keyword:.2f},{gst:.2f},{qst:.2f},".format(keyword=keyword_score, qst=qst_score,gst=gram_score))
        file.write(str(keyword_score + qst_score + gram_score))
    print("Data Preprocessed and saved")
    file.close()