from datetime import datetime

from requests_html import HTMLSession
from pyppeteer.errors import TimeoutError


def get_news(url):
    session = HTMLSession()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    response = session.get(url, headers=headers)

    response = __render_html(response)
    title = __get_title(response)
    content = __get_content(response)
    image = __get_image(response)

    data = {
        "text": content,
        "title": title, 
        "img_url": image,
        "date": '',
        "summary":'',
        "url":url
    }

    return data


def __render_html(response, tries=3):
    try:
        response.html.render(timeout=30)
        return response
    except TimeoutError:
        if tries == 0:
            return ''
        __render_html(response, tries=tries-1)


def __get_title(response):
    try:
        title = response.html.xpath(
            "//*[@id='wrapper']/div[1]/main/article/div/div[2]/div[1]/h1"
        )[0].text
        return title
    except Exception as e:
        print(f"Error: scraper exception {e}")
        return ""


def __get_content(response):
    try:
        raw_text = response.html.xpath(
            "//*[@id='wrapper']/div[1]/main/article/div/div[2]/div[2]"
        )[0].full_text
        text = __get_subtitle(response) + raw_text
        full_text = __sanitize_text(text)
        return full_text
    except Exception as e:
        print(f"Error: scraper exception {e}")
        return ""


def __get_subtitle(response):
    try:
        sub_title = response.html.xpath(
           "//*[@id='wrapper']/div[1]/main/article/div/div[2]/div[1]/div[2]" 
        )[0].text
        return sub_title + "\n"
    except Exception as e:
        print(f"Error: scraper exception {e}")
        return ""


def __get_image(response):
    try:
        image = response.html.xpath(
            "//*[@id='wrapper']/div[1]/main/article/div/div[2]/div[2]/div/figure/img"
        )[0].attrs['data-src']

        return image
    except Exception as e:
        print(f"Error: scraper exception {e}")
        return ""


def __sanitize_text(text):
    # Replace all the \xa0 chars into ''
    text = text.replace('\xa0', '')

    return text
