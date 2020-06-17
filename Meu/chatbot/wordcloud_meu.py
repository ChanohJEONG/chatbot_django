import pandas as pd
from collections import Counter
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import nltk
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud


def wordcloud(chatbot_data, member_id):
    okt = Okt()
    # chatbot_data = pd.read_csv('./modified_20000.csv')
    # text = list(chatbot_data.Q)
    text = chatbot_data
    sentences_tag = []
    for sentence in text:
        morph = okt.pos(sentence)
        sentences_tag.append(morph)
    noun_adj_list = []
    for sentence1 in  sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun','Adjective']:
                noun_adj_list.append(word)
    
    ko = nltk.Text(noun_adj_list, name='감성분석')
    dic1=ko.vocab()
    dic2={}
    dic2 = {key: value for key, value in dic1.items() if len(key) >=2}
    count = Counter(dic2)
    # stopwords=["있어", "있는","같아","있어요","있을까","같아요","있는데","같은데","해도"]
    data=count.most_common(100)
    data3=dict(data)
    
    # for word in stopwords:
    #     del data3[word] 
    
    alice_mask = np.array(Image.open("./wordcloud/cat4.png"))

    wordcloud = WordCloud(
        font_path='./wordcloud/malgun.ttf',
        width = 150,
        height = 150,
        # stopwords=stopwords,
        background_color="white",
        mask = alice_mask
    )
    
    wordcloud = wordcloud.generate_from_frequencies(data3)
    fig =plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    
    fig.savefig('./chatbot/static/chatbot/img/wordcloud/diary_'+str(member_id)+'.png')

    return "OK"
