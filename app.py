from flask import Flask, render_template, request
from flask_session import Session
from project import find_news, scraping, inference, is_paragraph

app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/find', methods=["POST"])
def find():
    if request.method == 'POST':
        topic = request.form.get("topic")
        articles = []
        for title, source, article_url in find_news(topic):
            article = {'title': title, 'source': source, 'url': article_url}
            # print('\n', title, ' | ', source)
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
            article['summary'] = summary
            # print(summary)
            articles.append(article)

            # print("\n", "#" * 50)
    return render_template('articles.html', articles=articles, topic=topic)


@app.route('/summarize')
def summarize():

    return render_template('summarize.html')


@app.route('/summary', methods=["POST"])
def summary():
    url = request.form.get("url")

    article = {'url': url}
    payload, summary = "", ""
    paragraph_counter, max_n_paragraph, sum_every_n = 0, 9, 5
    for i, text in enumerate(scraping(url)):
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
    article['summary'] = summary

    return render_template('summary.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)
    print("hello")
