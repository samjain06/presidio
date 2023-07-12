import re
import time
import streamlit as st

from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from transformers import pipeline
from webdriver_manager.chrome import ChromeDriverManager


def initialize_question_answering_pipeline():
    return pipeline('question-answering', model='deepset/roberta-base-squad2')


def normalize_context(context):
    # Reconstruct the normalized context
    normalized = re.sub(r'[\n\s]+', ' ', context)
    return normalized


def setup_selenium():
    # Set up Selenium
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver


def extract_info_from_link(link):
    # Set up Selenium
    driver = setup_selenium()

    # Extract the information from the link
    try:
        driver.get(link)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        text = soup.get_text()
        cleaned_text = re.sub(r'[\n\s]+', ' ', context)
        print('*****CLEANED TEXT IN EXTRACT*****', cleaned_text)
        return cleaned_text

    except Exception as e:
        print(f'[ERROR] encountered while extracting info from link {link}: {str(e)}')
    finally:
        driver.quit()


def search_web(topic):
    # Search the web
    query = f'{topic}'
    search_results = list(search(query, num_results=10, lang='en'))
    print('*****SEARCH RESULTS IN SEARCH_WEB*****', search_results)
    # Extract the URLs from the search results
    info = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(extract_info_from_link, link) for link in search_results]
        for clean_text in futures:
            try:
                snippet = clean_text.result()
                if snippet:
                    info.append(snippet)
            except Exception as e:
                pass
    print('*****INFO IN SEARCH_WEB*****', info)
    return info


def main():
    # Get the topic from the user
    st.title('Question Answering System')
    st.header('Ask a question about a specific topic and Bot will answer it!')
    topic = st.text_input('Type a topic you\'d like to learn more about', key='topic')

    if topic != '' and topic is not None:
        # Search the web and extract information
        info = search_web(topic)
        print('*****INFO IN MAIN*****', info)
        # Initialize the question-answering pipeline
        qa_pipeline = initialize_question_answering_pipeline()

        # Process follow-up questions
        if info is not None:
            question = st.text_input('Ask a follow-up question (or type "quit" to exit): ', key='follow-up-question')
            if question != '' and question is not None:
                if question.lower() == 'quit':
                    st.stop()

                # Concatenate all the snippets as the context for the question answering model
                context = ' '.join(info)

                # Answer the question using the question-answering pipeline
                answer = qa_pipeline(question=question, context=context)
                st.write('Answer:', answer['answer'])
                score = round(answer['score']*100, 2)
                st.write('Score:', score)


if __name__ == '__main__':
    main()
