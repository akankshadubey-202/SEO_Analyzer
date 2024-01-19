import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import streamlit as st
nltk.download('stopwords')
nltk.download('punkt')

st.title("SEO ANALYZER")
url= st.text_input("ENTER URL: ") # takes input from users

def seo_analysis(url): #Save the good and the warnings in lists from
    good=[]
    bad=[]
    
    if not url:
        st.warning("Enter The URL.")
        return

    # Check if the URL has a valid scheme (http or https)
    if not (url.startswith('http://') or url.startswith('https://')):
        # If no scheme is provided, default to 'https://'
        url = 'https://' + url


    response = requests.get(url)
    #Check the response status code
    if response.status_code!=200:
        print("Error: Unable to access the website. Please Enter the URL")
        return 
    
    #Parse the HTML content
    soup=BeautifulSoup(response.content,'html.parser')

    #Extract the title and description
    title = soup.find('title').get_text()
    description=soup.find('meta',attrs={'name':'description'})['content']
   

   #check if the title and description exist
    if title:
        good.append("Title Exists! Great!")

    else:
        bad.append("Title does not exist! Add a Title")


    if description:
        good.append("Description Exists! Great!")
    else:
        bad.append("Description does not exist! Add Meta Description")


#Grab the Heading
        
    hs=['h1','h2','h3','h4','h5','h6']
    h_tags=[]

    for h in soup.find_all(hs):
        good.append(f"{h.name}----> {h.text.strip()}")
        h_tags.append(h.name)

    if 'h1' not in h_tags:
        bad.append("No H1 tag found")

        #Extract the images without Alt
    for i in soup.find_all('img',alt=''):
        bad.append(f"No Alt: {i}")

    #  Extract keywords
    #Grab the text from the body of html
    bod=soup.find('body').text

    #extract all the words in the body and lowercase them in a list
    words=[i.lower() for i in word_tokenize(bod)]

      # Extract the bigram from the tokens  
    bi_grams=ngrams(words,2)
    freq_bigrams=nltk.FreqDist(bi_grams)
    bi_grams_freq=freq_bigrams.most_common(10)

    # Grab a list of English Stopwords
    sw=nltk.corpus.stopwords.words('english)
    new_words=[]

    #Put the tokens that are not stopwords and are actual words(no punctuation)
    for i in words:
        if i not in sw and i.isalpha():
            new_words.append(i)
        

    # Extract the frequency of the words and get the 0 most common ones
    freq = nltk.FreqDist(new_words)
    keywords=freq.most_common(10)



    #Print The Output
    tab1, tab2, tab3, tab4 = st.tabs(['Keywords','BiGrams','Good','Bad'])
    with tab1:
        for i in keywords:
            st.text(i)
    with tab2:
        for i in bi_grams_freq:
            st.text(i)
    with tab3:
        for i in good:
            st.success(i)
    with tab4:
        for i in bad:
            st.text(i)


seo_analysis(url)
        
      



