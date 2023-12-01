# News Summarizer
#### Video Demo: https://youtu.be/-mo-vtymL4Y

#### Description:

The News Summarizer application seamlessly combines command line and web-based interfaces to offer users a convenient and versatile tool for summarizing news articles. Users can interact with the application through both the command line and a user-friendly web app, providing flexibility and accessibility. Whether users prefer a traditional terminal approach or a graphical interface, the application accommodates their preferences.

The application empowers users to explore news on any topic of interest effortlessly. By providing a search functionality, users can input a topic, and the app fetches the five most popular news items related to that subject. This feature ensures users stay informed about the latest developments in areas they care about. Additionally, the application allows users to input a specific URL, offering the capability to summarize the content of any web page. This feature is particularly useful for those who want concise insights into lengthy articles or reports.

Under the hood, the News Summarizer leverages the NewsAPI to fetch real-time news data, ensuring that the information presented is up-to-date and relevant. This integration enhances the app's ability to deliver timely and accurate news summaries. Moreover, the application harnesses the power of AI through an advanced model hosted on Hugging Face. This AI model excels at generating concise and coherent summaries, enhancing the overall user experience by providing high-quality, automated content summaries.

In summary, the News Summarizer not only offers a dual interface for user interaction but also delivers a robust set of features. From fetching popular news on user-specified topics to summarizing specific URLs, the app seamlessly integrates API calls to NewsAPI and deploys advanced AI models from Hugging Face, ensuring users receive accurate, timely, and succinct news summaries tailored to their preferences.

#### How to run:
Run the command line app:
`python project.py`

Run the web app:
`python app.py`

#### Functionality :

##### 1. project.py main():
This function takes no parameters and does not have a return type. The function prompts the user to enter a topic and assigns the input to the variable 'topic'. It then iterates over the results returned by the 'find_news' function, which takes the 'topic' as an argument. For each result, it prints the 'title' and 'source' of the news article.

Inside the loop, the function initializes the variables 'payload' and 'summary' as empty strings. It also initializes the variables 'paragraph_counter','max_n_paragraph', and 'sum_every_n' to 0, 9, and 5 respectively. The function then iterates over the text returned by the 'scraping' function, which takes 'article_url' as an argument.

For each text, it checks if it is a paragraph using the 'is_paragraph' function. If it is a paragraph, the function increments the 'paragraph_counter' by 1 and appends the text to the 'payload' string. If the index of the text is a multiple of 'sum_every_n' minus 1, the function sends the 'payload' as input to the 'inference' function. It appends the 'summary_text' from the inference result to the 'summary' string and resets the 'payload' to an empty string. If the 'paragraph_counter' is equal to 'max_n_paragraph', the function breaks out of the loop.

After the loop, if there is any remaining text in the 'payload', the function sends it as input to the 'inference' function. It appends the 'summary_text' from the inference result to the 'summary' string.

Finally, the function prints the 'summary' and a line of '#' characters.

##### 2. project.py inference():
Uses Python's configparser module to read a configuration file named 'config.ini'. The configuration file likely contains sensitive information, such as API keys. Specifically, it retrieves the API key from the 'API' section in the 'config.ini' file.

The URL for the Hugging Face model is defined (API_URL). The headers dictionary is set up with an "Authorization" field containing the API key. This key is essential for authenticating and authorizing the API request.

The requests.post method sends a POST request to the specified Hugging Face API URL (API_URL). The request includes the previously set headers and a JSON payload (payload). The response from the API is stored in the response variable. Finally, the function returns the JSON content of the response.

To use this function pass a payload containing the input data to be processed by the Hugging Face model. The API key stored in the 'config.ini' file is crucial for authentication and ensuring that the request is authorized to access the Hugging Face model.

##### 3. project.py scraping():
This code uses the requests.get method to send an HTTP GET request to the specified url. The timeout parameter is set to 100 seconds, meaning the request will timeout if it doesn't receive a response within that timeframe. The response from the web server is stored in the web_data variable.

The BeautifulSoup object is created to parse the HTML content of the web page. The web_data.content contains the HTML content fetched from the web page. The parser specified is the HTML parser provided by the html.parser module.

The findAll method of BeautifulSoup locates all paragraphs (<p>) in the parsed HTML content. The result is a collection of Tag objects representing the paragraphs.

This is a generator function that iterates over the collection of paragraph tags (news_info). For each paragraph, it yields the text content using news.text. Using yield instead of return makes this function a generator, allowing the caller to iterate over the paragraphs one at a time rather than retrieving all of them at once.

In summary, this function, when provided with a URL, fetches the web page content, extracts the text from all paragraphs using BeautifulSoup, and yields each paragraph's text one at a time. It's a convenient way to process and extract information from the textual content of web pages.

##### 4. project.py find_news():
The function starts by reading a configuration file ('config.ini') using the configparser module. It retrieves the NewsAPI key from the 'NEWSAPI' section in the configuration file.

The function then constructs the URL for the NewsAPI endpoint ('https://newsapi.org/v2/everything') and defines a payload containing parameters for the API request. These parameters include the search query (about), sorting by popularity, searching within the article titles, the API key, language, and specifying a page size of 5 articles. The requests.get method is used to send an HTTP GET request to the NewsAPI with the constructed URL and parameters.

The function checks if the response from NewsAPI indicates a successful request (status 'ok'). If successful, it iterates over the articles in the response and yields a tuple containing the article title, source name, and URL. If the request is not successful, it raises a ValueError with the error message obtained from the NewsAPI response.

In summary, this function fetches news articles from NewsAPI based on a specified query, extracts relevant information from the API response, and yields details about the top articles. It also includes error handling to raise an exception if the NewsAPI request is unsuccessful.

##### 5. project.py is_paragraph():
If the number of words in the text (obtained by splitting the text using whitespaces) is greater than 15, the function immediately returns True, indicating that the text is considered long.

If the word count condition is not met, the function proceeds to check the number of sentence-ending punctuation marks (., !, ?). It uses a regular expression ([\.?!]) to find occurrences of these punctuation marks. The pattern (?:[ \w]|$) is a non-capturing group that matches either a space followed by a word character or the end of the string. The result is a list of matches representing potential sentence endings.

If the number of such matches is greater than 3, the function returns True, indicating that the text is considered long.

In summary, the function uses a combination of word count and sentence structure checks to determine whether a given text is considered "long" based on certain criteria. The specific criteria used here are a word count greater than 15 or having more than 3 potential sentence endings.

##### 6. app.py find():
This Flask route handles the logic for finding news articles related to a given topic. First, it retrieves the value of the "topic" field from the form submitted in the POST request. This assumes that there is an HTML form with an input field named "topic." 

It then iterates over news articles related to the specified topic obtained from the find_news function. The details of this function are not provided, but it is assumed to return a list of tuples containing article information (title, source, URL).

Next, it iterates over paragraphs of text obtained by scraping the content of the article's URL. The scraping function is assumed to provide this functionality.

After accumulating paragraphs into a payload for summarization, If a certain number of paragraphs (determined by sum_every_n) have been accumulated, a summarization query is made using the inference function, and the result is appended to the overall summary.

In summary, this route takes a user-submitted topic, finds related news articles, scrapes and summarizes the content of those articles, and then renders a template to display the articles along with their summaries.

##### 7. app.py summary():
This Flask route handles the summarization of the content from a given URL. It first retrieves the URL from the form submitted in the request. This assumes that there is an HTML form with an input field named "url.".

This function then iterates over paragraphs of text obtained by scraping the content of the provided URL. The scraping function is assumed to provide this functionality.

After filtering out non-paragraph text, it accumulates paragraphs into a payload for summarization. If a certain number of paragraphs (determined by sum_every_n) have been accumulated, a summarization query is made using the inference function, and the result is appended to the overall summary. The loop breaks if the maximum number of paragraphs (max_n_paragraph) is reached.

In summary, this route takes a user-submitted URL, scrapes and summarizes the content of the provided URL, and then renders a template to display the original URL and its summary.