from bs4 import BeautifulSoup
import requests
import configparser
import pdb


def main():
    url = "https://edition.cnn.com/2023/11/28/middleeast/thomas-hand-emily-hostage-intl"

    payload, summary = "", ""
    for i, text in enumerate(scraping(url)):
        print(i, text)
        payload += text
        if i % 5 == 4:
            query = {"inputs": payload}
            summary += inference(query)[0]['summary_text'] + "\n"
            payload = ""

    if payload:
        query = {"inputs": payload}
        summary += inference(query)[0]['summary_text']

    print(summary)


def inference(payload):
    """
    Sends a POST request to the Hugging Face inference API to perform inference using the BART-Large-CNN model.

    Args:
        payload (dict): The payload to be sent in the request body as JSON.

    Returns:
        dict: The JSON response from the API containing the inference results.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config.get('API', 'key')

    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def scraping(url):
    """
    Scrape the text of each news item found on the given URL.

    :param url: The URL to scrape.
    :type url: str
    :return: A generator that yields the text of each news item found.
    :rtype: generator
    """

    web_data = requests.get(
        url,
        timeout=100
    )
    soup = BeautifulSoup(web_data.content, features="html.parser")
    news_info = soup.findAll("p")
    for news in news_info:
        yield news.text


if __name__ == '__main__':
    main()
