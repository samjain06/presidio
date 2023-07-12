# QUESTION-ANSWERING BOT

## Deployment

This app is deployed using Streamlit service at: [QABot](https://)

## Introduction

This streamlit version of web app accepts a string input from the user, searches the internet for the information about it, and answers any questions regarding the topic
It provides the answer along with its accuracy score (out of 100%).

This is app uses following libraries and technologies:

- Built using Python
- Hosted by Streamlit for web app interface
- Uses Selenium library to get content from dynamic website (like websites using Jinja templates)
- BeautifulSoup4 library is used to parse the html contents
- Regex expressions to normalize the content (with possibility to include further normalization)
- ChromeDriverManager from WebDriver-MAnager package to get the host Chrome version and install driver accordingly for Selenium
- Google Search package to get the search results for the topic
- Transformers pipeline using pretrained model 'roberta-base' fine-tuned using the SQuAD2.0 dataset
- Multithreading for parsing multiple links simultaneously

## Improvements

Some of the improvements worth working towards are:

1. Using NLP for expanding normazlization techniques
2. Need to check if asynchronous results in better performance than multi-threading
3. Input validation
4. Implementing caching for answers
5. Need to experiement with different pipeline models or fine-tune a custom one