from datetime import datetime

from custom_scrapers.common import get_soup


def get_news(url):
    soup = get_soup(url)
    title = __get_title(soup)
    content = __get_content(soup)
    date = __get_date(soup)
    image = __get_image(soup)

    data = {"text": content, "title": title, "date": date, "image": image,
            "summary":''}
    return data


def __get_title(soup):
    try:
        title = soup.select(
            "#mainContent > main > div > div:nth-child(2) > div.col-sm-8 > h1"
        )[0].text
        return title
    except Exception as e:
        print(f"Error: scraper exception {e}")
        return ""


def __get_content(soup):
    try:
        raw_text = soup.select(
            "#mainContent > main > div > div:nth-child(2) >"
            "div.col-sm-8 > div:nth-child(8) > div > div"
            ".subscribe--wrapperx > section"
        )[0].get_text()
        text = __get_subtitle(soup) + raw_text
        text = __sanitize_text(text)
        return text
    except Exception as e:
        print(f"Error: scraper exception {e}")
        return ""


def __get_date(soup):
    try:
        raw_date = soup.select(
            "#mainContent > main > div > div:nth-child(2) >"
            "div.col-sm-8 > div:nth-child(8) > div > div"
            ":nth-child(5)"
        )[0].text
        date = __parse_date(raw_date)
        return date
    except Exception as e:
        print(f"Error: scraper exception {e}")
        return ""


def __get_subtitle(soup):
    try:
        sub_title = soup.select(
            "#mainContent > main > div > div:nth-child(2) > div.col-sm-8 > span"
        )[0].text
        return sub_title + "\n"
    except Exception as e:
        print(f"Error: scraper exception {e}")
        return ""


def __get_image(soup):
    try:
        image = soup.select(
            "#mainContent > main > div > div:nth-child(2) >" "div.col-sm-8 > img"
        )[0]["data-src"]

        return image
    except Exception as e:
        print(f"Error: scraper exception {e}")
        return ""


def __parse_date(text):
    """ We receive a string like this "Published at : May 7, 2020 ". """
    date_part = text.split(":")[1].strip()
    date = datetime.strptime(date_part, "%B %d, %Y")
    return datetime


def __sanitize_text(text):
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text


get_news(
    "https://kathmandupost.com/national/2020/05/07/for-nepali-women-rampant-objectification-and-sexualisation-on-the-internet"
)
