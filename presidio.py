from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time
from transformers import pipeline

def search_web(topic):
    # Set up Selenium
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without opening a browser window)
    chrome_options.add_argument('--disable-gpu')  # Disables the GPU usage (useful when running on a server without a GPU)
    # disable popup
    chrome_options.add_argument('--disable-popup-blocking')
    # disable notifications
    chrome_options.add_argument('--disable-notifications')
    # disable infobars
    chrome_options.add_argument('--disable-infobars')
    # disable extensions
    chrome_options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Search the web
    topic = topic.replace(' ', '+')
    query = f'{topic}'
    url = f'https://www.google.com/search?q={query}'
    driver.get(url)

    # Extract information from the search results
    time.sleep(2)  # Wait for the page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # get all the links
    search_results = soup.find_all('div', class_='yuRUbf')

    # Extract the URLs from the search results
    info = []
    for i in range(0, 2):
        link = search_results[i].a.get('href')
        driver.get(link)
        time.sleep(5)  # Wait for the page to load due to dynamic content
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        text = soup.get_text().strip().replace('\n', ' ')
        info.append({'link': link, 'snippet': text})

    # Close the Selenium driver
    driver.quit()

    return info


def initialize_question_answering_pipeline():
    return pipeline('question-answering')

def main():
    # Get the topic from the user
    topic = input('Enter a topic: ')

    # Search the web and extract information
    info = search_web(topic)

    # Initialize the question-answering pipeline
    qa_pipeline = initialize_question_answering_pipeline()

    # Process follow-up questions
    while True:
        question = input('Enter a follow-up question (or type "quit" to exit): ')
        if question.lower() == 'quit':
            break

        # Concatenate all the snippets as the context for the question answering model
        context = ' '.join([item['snippet'] for item in info])
        print(context)

        # Answer the question using the question-answering pipeline
        answer = qa_pipeline(question=question, context=context)
        print('Answer:', answer['answer'])
        print('Score:', answer['score'])
        print()

if __name__ == '__main__':
    main()