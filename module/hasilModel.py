import streamlit as st
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup

from gensim.models import Word2Vec
from gensim.utils import tokenize
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import MultinomialNB

def parseHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def removeDigits(string):
    for i in range(10):
        string=string.replace(str(i),' ')
        return string

def printResults(y_true, y_predicted):
    hasil = accuracy_score(y_true, y_predicted)

    columns=['true', 'false']
    # ConfusionMatrixDisplay(y_true, y_predicted, columns)
    precision, recall, fscore, support = score(y_true, y_predicted)
    
    hasilModel = {'accuracy': hasil*100, 'precision': precision[0]*100, 'recall':recall[0]*100, 'fscore':fscore[0]*100}
    
    return hasilModel

def hasilModel():
    # Baca CSV
    df = pd.read_csv("src/DataTwitter/dataTraining.csv")
    
    # Hapus Link dan Tanda Baca
    df['Tweet'] = df['Tweet'].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '')
    df['Tweet'] = df['Tweet'].str.replace(r"[\"\'\|\?\!\=\:\/\-\_\.\@\#\*\,]", '')
    
    tweet = df.Tweet.values
    polaritas = df.Polaritas.values

    #hapus html
    tweet=list(map(parseHtml, tweet))

    #hapus digits
    tweet=list(map(removeDigits, tweet))

    tokenizedText=[list(tokenize(item.lower())) for item in tweet]

    trainTweets=tokenizedText[:3000]
    trainPolaritas=polaritas[:3000]
    testTweets=tokenizedText[3216:]
    testPolaritas=polaritas[3216:]
    
    model = Word2Vec.load('src/Vector/train_model_capres.w2v')

    def getVectors(dataset):
        singleDataItemEmbedding=np.zeros(100)
        vectors=[]
        for dataItem in dataset:
            wordCount=0
            for word in dataItem:
                if word in model.wv.index_to_key:
                    singleDataItemEmbedding=singleDataItemEmbedding+model.wv[word]
                    wordCount=wordCount+1
        
            singleDataItemEmbedding=singleDataItemEmbedding/wordCount  
            vectors.append(singleDataItemEmbedding)
        return vectors

    trainTweetVectors=getVectors(trainTweets)
    testTweetVectors=getVectors(testTweets)
    
    clfNB = MultinomialNB()

    scaler = MinMaxScaler()
    scaledTrainX= scaler.fit_transform(trainTweetVectors)
    scaledTestX = scaler.fit_transform(testTweetVectors)
    clfNB.fit(scaledTrainX, trainPolaritas)

    #test naive bayes accuracy
    testLabelsPredicted=list(clfNB.predict(scaledTestX))
    
    return printResults(testLabelsPredicted, testPolaritas)