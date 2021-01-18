## Import necessary modules
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import wikipedia

# Collecting data from wikipedia.

def get_article(query):
    title = wikipedia.search(query)[0]
    page = wikipedia.page(title)
    return page.content

# Function to plot the wordcloud.
def show_cloud(word_cloud, interpolation='bilinear'):
    plt.imshow(word_cloud, interpolation=interpolation)
    plt.axis('off')
    plt.show()

# Generating the wordcloud
def create_wc(text):
    wc_mask = np.array(Image.open('path of the pngfile'))
    stop_words = set(STOPWORDS)
    wc = WordCloud(mask = wc_mask,
                 max_words = 250,
                 stopwords = stop_words,
                 background_color = 'white').generate(text)
    show_cloud(wc)
    wc.to_file("masked_wc.png") #(To save your wordcloud locally)


article = get_article('Data Science')
create_wc(article)