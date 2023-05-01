import numpy as np
import pandas as pd
import pickle

from bs4 import BeautifulSoup
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from tqdm.auto import tqdm
from gensim.utils import tokenize
from gensim.models import Word2Vec

# List Side Function #
def parseHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def removeDigits(string):
    for i in range(10):
        string=string.replace(str(i),' ')
    return string
# Akhir Side Function #
 
# Main Function #
def prosesSentimen(namaCalon, bulan):
    hasilAkhir = []
    minggu = ["Minggu1","Minggu2","Minggu3","Minggu4"]
    for i in range(4):
        hasilTemp = [i+1]
        for nama in range(len(namaCalon)):
            namaFile = "".join(["data", namaCalon[nama], bulan, minggu[i], ".csv"])
            namaVector = "".join(["vector", namaCalon[nama], bulan, minggu[i], ".w2v"])
            directoryFile = "".join(["src/DataTwitter/", bulan, "/" , namaFile])
            directoryVector = "".join(["src/Vector/", bulan, "/" , namaVector])
            
            df = pd.read_csv(directoryFile)

            df['Tweet'] = df['Tweet'].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '')
            df['Tweet'] = df['Tweet'].str.replace(r"[\"\'\|\?\!\=\:\/\-\_\.\@\#\*\,]", '')

            df.drop(index=df.index[0], axis=0, inplace=True)

            tweet = df.Tweet.values

            #hapus html
            tweet=list(map(parseHtml, tweet))

            #hapus digits
            tweet=list(map(removeDigits, tweet))
            
            #hapus Stopwords
            factory = StopWordRemoverFactory()
            stopword = factory.create_stop_word_remover()

            for x, kalimat in tqdm(enumerate (df['Tweet'])):
                df.loc[x, 'Tweet'] = stopword.remove(kalimat)

            tokenizedText=[list(tokenize(item.lower())) for item in tweet]
            
            model = []
            
            if(namaCalon[nama] == 'Puan' and bulan == 'Februari'):
                model = Word2Vec(tokenizedText, vector_size=128, window=5, min_count=1, workers=1, epochs=300)
            else:
                model = Word2Vec.load(directoryVector)
            
            def getVectors(dataset):
                singleDataItemEmbedding=np.zeros(128)
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
            
            testTweetVectors=getVectors(tokenizedText)
            
            print(testTweetVectors[999])
            
            loadedModel = pickle.load(open("src/modelTrainedNB.pkl", "rb"))

            result = loadedModel.predict(testTweetVectors)

            output = pd.DataFrame(data={"sentiment":result})
            
            hasilTemp.append(output.sentiment.value_counts()['Positif'])
        hasilAkhir.append(hasilTemp)
    return hasilAkhir

def tampilSentimen(namaInput, bulanInput):
    namaCalon = []
    listCalon = {'Agus Harimurti Yudhono': 'AHY', 'Anies Baswedan':'Anies', 'Ganjar Pranowo':'Ganjar', 
                'Prabowo Subianto':'Prabowo', 'Puan Maharani':'Puan', 'Ridwan Kamil':'Ridwan'}
    listBulan = {'Desember 2022':'Desember', 'Januari 2023':'Januari', 'Februari 2023':'Februari'}
    for i in range(len(namaInput)):
        namaCalon.append(listCalon[namaInput[i]])
    bulan = listBulan[bulanInput]
    
    hasil = prosesSentimen(namaCalon, bulan)
    
    return hasil
    
# Akhir Main Function #