import pyphen
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords, brown
from nltk.tokenize import word_tokenize
import math
from collections import Counter 

#generate corpus word_cloud
df = pd.read_csv('song_database')
stop_words = set(stopwords.words('english'))
genius_stop = ['im', 'intro', 'chorus', 'verse', 'refrain', 'hook', 'outro']
stop_words |=set(genius_stop)

syllable_dict = pyphen.Pyphen(lang='en')
def generate_wordcloud(df,stop_words):
    d={}
    massive_string = ""
    for index, row in df.iterrows():
        if type(row['Lyrics']) is str:
            word_tokens = word_tokenize(row['Lyrics'])
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            massive_string += ' '.join(x for x in filtered_sentence)
    word_cloud = WordCloud().generate(massive_string)
    plt.imshow(word_cloud, interpolation = 'bilinear')
    plt.axis("off")
    #plt.show()
    return 0

def word_analysis(df, stop_words):
    d={}
    for index, row in df.iterrows():
        massive_string = ''
        if type(row['Lyrics']) is str:
            row['Lyrics'] = row['Lyrics'].lower()
            row['Lyrics'] = re.sub('\'', '', row['Lyrics'])
            row['Lyrics'] = re.sub('[^a-zA-Z]', ' ', row['Lyrics'])
            word_tokens = word_tokenize(row['Lyrics'])
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            for key in filtered_sentence:
                d[key] = d.get(key,0)+1
            massive_string += ' '.join(x for x in filtered_sentence)
    wcount = sorted(d.items(),key = lambda x: x[1], reverse = True)
    return wcount

if __name__ == "__main__":
    generate_wordcloud(df, stop_words)
    kanye_df = df[df['Artist'] == 'Kanye-west']
    eminem_df = df[df['Artist'] == 'Run-the-jewels']
    nas_df = df[df['Artist'] == 'Nas'] 
    dumbass_df = df[df['Artist'] == '6ix9ine'] 

    corpus_words = word_analysis(df, stop_words)
    kanye_words = word_analysis(kanye_df, stop_words)
    runjewels_df = word_analysis(eminem_df, stop_words)
    nas_words = word_analysis(nas_df, stop_words)
    dumbass_words = word_analysis(dumbass_df, stop_words)
    
    #print([x for x in kanye_words if x[1] > 5])
    print([x for x in runjewels_df if x[1] > 5])
    #print([x for x in nas_words if x[1] > 5])
    print([x for x in dumbass_words if x[1] > 5])
    #print([x for x in corpus_words if x[1] > 5])

