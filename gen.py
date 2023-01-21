import pickle
from fastai import *
from fastai.text.all import * 

import pandas as pd

import numpy as np

id = 44196397

def loadTweets(id):
    with open(str(id), 'rb') as file:
        return pickle.load(file)

#df = pd.DataFrame(loadTweets(id), columns=['text'])

df = pd.read_csv('data/'+str(id), sep='########')
valid_pct = 0.2 #validation percent
print(df)
data_lm = TextDataLoaders.from_df(df=df, text_col='text', is_lm=True, label_col=None, tok_text_col='text')
data_lm.show_batch()
learn = language_model_learner(data_lm, AWD_LSTM, drop_mult=0.5, pretrained=True)
learn.fit_one_cycle(1, 1e-3)
learn.unfreeze()
learn.fit_one_cycle(1, 1e-3)
wd=1e-7
lr=1e-4
lrs = lr

learn.fit(15,lrs, wd)

number_of_ideas = 100
ideas_counter = 0
all_ideas = []

for i in range(100):
    print(i)
    idea = learn.predict("xxbos xxfld a", n_words=40, temperature=0.8)
    print(idea)
    ideas = idea.split("xxbos xxfld a")
    ideas = ideas[1:-1]
    
    for idea in ideas:
        idea = idea.replace("xxbos xxfld 1 ","").strip()
        if(idea):
            all_ideas.append(idea)
            ideas_counter = ideas_counter+1
            
    if ideas_counter > number_of_ideas:
        break

print(all_ideas)
learn.save_encoder('ml_ft_enc')

train_df.to_pickle('data/ml_train_df.pkl')

valid_df.to_pickle('data/ml_valid_df.pkl')

