# QUESTION-ANSWERING BOT

## Deployment
This app can be run by forking and cloning this repo and running below commands:


This app is deployed using Streamlit service at: [QABot](https://question-answer-bot.streamlit.app/)

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

- Using NLP for expanding normazlization techniques
- Need to check if asynchronous results in better performance than multi-threading
- Input validation
- Implementing caching for answers
- Need to experiement with different pipeline models or fine-tune a custom one

## Issues

- The app is not able to answer questions that are not present in the content. This is because the model is trained on SQuAD2.0 dataset which dot not have answer for all the questions. This can be improved by using a model that can generate answers instead of extracting them from the content.
- The app might not work on cross-platforms. This is because for Streamlit Cloud to work, the app must be able to run on Debian. As I am using Selenium, it requires chromium & chromedriver to be installed (mentioned in packages.txt). This may or may not work on Windows. However, I have tested with chrome & chromedriver On Windows along with webdriver-manager library. For more info, take a look at this repo: https://github.com/Franky1/Streamlit-Selenium/tree/main
