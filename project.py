from bs4 import BeautifulSoup
import requests
import configparser
import re
# import pdb


def main():
    """
    Generates summaries for news articles related to the given topic.

    Parameters:
    - topic (str): The topic for which news articles should be retrieved and summarized.

    Prints:
    - Summaries for each news article, including the article title, source, and summary text.

    Note:
    This function uses the `find_news` function to discover news articles related to the given topic. For each article, it uses the `scraping` function to extract paragraphs and then sends the paragraphs to the `inference` function for summary generation.Summaries are printed for each article.
    """

    topic = input("Enter topic: ")

    for title, source, article_url in find_news(topic):
        print('\n', title, ' | ', source)
        payload, summary = "", ""
        paragraph_counter, max_n_paragraph, sum_every_n = 0, 9, 5
        for i, text in enumerate(scraping(article_url)):
            if is_paragraph(text):
                paragraph_counter += 1
                # print(i, paragraph_counter)
                payload += text
                if i % sum_every_n == sum_every_n-1:
                    # print(payload)
                    query = {"inputs": payload}
                    summary += inference(query)[0]['summary_text'] + "\n"
                    payload = ""
                if paragraph_counter == max_n_paragraph:
                    break

        if payload:
            query = {"inputs": payload}
            summary += inference(query)[0]['summary_text']

        print(summary)

        print("\n", "#" * 50)


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


def find_news(about):
    """
    Finds news articles related to a specific topic.

    Parameters:
        about (str): The topic to search for in the news articles.

    Returns:
        generator: A generator that yields tuples containing the article title, source name, and URL.

    Raises:
        ValueError: If the API response indicates an error.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config.get('NEWSAPI', 'key')

    url = "https://newsapi.org/v2/everything"
    payload = {'q': about,
               'sortBy': 'popularity',
               'searchIn': 'title',
               'apiKey': api_key,
               'language': 'en',
               'pageSize': '5'
               }

    web_data = requests.get(
        url,
        params=payload,
        timeout=100,
    )

    if web_data.json()['status'] == 'ok':
        for article in web_data.json()['articles']:
            yield (article['title'], article['source']['name'], article['url'])
    else:
        raise ValueError(web_data.json()['message'])


def is_paragraph(text):
    """
    Check if the given text is a paragraph.

    :param text: The text to check.
    :type text: str
    :return: True if the text is a paragraph, False otherwise.
    :rtype: bool
    """

    if len(text.split()) > 15:
        return True
    else:
        matches = re.findall(r"[\.?!](?:[ \w]|$)", text)
        if len(matches) > 3:
            return True
    return False


if __name__ == '__main__':
    main()
