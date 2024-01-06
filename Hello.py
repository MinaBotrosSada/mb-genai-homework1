import feedparser
from urllib.request import urlopen
from bs4 import BeautifulSoup
from vertexai.language_models import TextGenerationModel
import vertexai


# Fetch the RSS feeds for the first X articles
def fetchRSS(URL, limit=50):
    RSS = feedparser.parse(URL)
    return RSS.entries[:limit]


# Fetch the HTML content of the article
def fetchBeautifulHTMLContent(URL):
    url = URL
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    html_text = '\n'.join(chunk for chunk in chunks if chunk)

    return html_text    


import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

      
def run():
    import vertexai
    from vertexai.preview.language_models import TextGenerationModel

    st.write("# Welcome to MB's Streamlit GenAI RSS Summarizer! 👋")

    title = st.text_input('RSS Feed URL', 'https://moxie.foxnews.com/google-publisher/latest.xml')
    st.write('The current RSS Feed URL is', title)
    
    if st.button('Summarize', type="primary"):        
        if title is None:
            title='https://moxie.foxnews.com/google-publisher/latest.xml'

        st.write('Summarization in progress...')

        vertexai.init(project="minab-ddf-sandbox", location="us-central1")
        parameters = {
            "max_output_tokens": 1024,
            "temperature": 0.2,
            "top_k": 40, 
            "top_p": 0.8
        }
        model = TextGenerationModel.from_pretrained("text-bison@001")

         # Load the model            
        list_of_articles = fetchRSS(title, 10)

        # Iterate over the list of articles
        for article in list_of_articles:
            st.markdown(f"### {article.title}")
                        
            prompt = fetchBeautifulHTMLContent(article.link)
                        
            response = model.predict(
            f"""Provide a very short summary, no more than four sentences, for the following article:
                        
            input: {prompt}

            output: 
            """,
                **parameters
            )        

            text = ' '.join(response.text.split())
            
            
            st.markdown(f"**Summary:** {text}") 

            st.markdown(f"[Read more on this topic]({article.link})") 


if __name__ == "__main__":
    run()
