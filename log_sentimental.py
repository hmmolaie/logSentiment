import torch
import pandas as pd  
from transformers import pipeline


df = pd.DataFrame()
df[['ip', 'score']] = None

sentiment_analyzer = pipeline('sentiment-analysis')

logFile = open('security.txt', 'r')
Lines = logFile.readlines()[1:]
for line in Lines:

    statement = line.strip()
    sentiment = sentiment_analyzer(statement)[0]

    if sentiment['label']!="POSITIVE":
        sentiment['score']=sentiment['score']*-1
    
    txtsplit=statement.split(";")
    df.loc[len(df)] = [txtsplit[2],sentiment['score']] # cut ip addresse & score in dataframe
       
df1=df.groupby(['ip'])['score'].mean().reset_index(name='score')    
df2=df1.sort_values(by=['score'], ascending=True)
df3=df2[df2['score']<0]
print(df3)
logFile.close()