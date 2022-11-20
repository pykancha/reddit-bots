"""
This module combines the article extraction and translation part.
It combines the two library googletrans/translate and newspaper_wrapper
"""

import os
import time
import json

import requests
from googletrans import Translator
from translate import Translator as MyMemoryTranslator
from newspaper_wrapper import Article
from newspaper_wrapper.article import ArticleException

from logger_file import Logger, prettify

logger = Logger().get_logger()


def get_news(url):
    article = Article(url, language="hi")
    try:
        article.download()
        article.parse()
        article.nlp()
    except ArticleException:
        logger.exception(f"Error: Download timeout: {url}")
        return

    data = {
        "date": article.publish_date,
        "title": article.title,
        "keywords": article.keywords,
        "summary": article.summary,
        "text": article.text,
        "img_url": article.top_image,
        "video": article.movies,
        "url": url,
    }
    logger.info(f"Got news:{prettify(data)}")
    return data


def get_summary(full_news, full_news_en=None, limit=3000):
    """
    Returns summary with translation
    param: full_news 
    optional: full_news_en (translation of full news)
    it is optional because incase of full news we dont use the fallback
    translation service as translation are limited to 1000 words per day
    
    optional: limit -> charecter limit on how much to extract  
    It slices the full news based on limit char. Gets the last punctuation
    marks and only return upto that. 
    So return string WILL NOT be same charectar as limit.
    """

    summary = __cut_text(full_news, length=limit)[0]
    if full_news_en:
        logger.info("Reusing translated full news")
        summary_en = __cut_text(full_news_en, length=limit)[0]
    else:
        summary_en = translate(summary) if __is_nepali(summary) else ""

    if not __is_nepali(summary):
        summary_en = summary

    summary = __ensure_paragraphs(summary)
    summary_en = __ensure_paragraphs(summary_en)
    logger.info(
        "Got summary and its translation:" f"{prettify(summary)} {prettify(summary_en)}"
    )

    return summary, summary_en


def get_full_news(text):
    """
    We only want to translate if it is in nepali.
    """
    full_news = text
    full_news_en = ""

    if __is_nepali(full_news):
        full_news_en = translate(full_news, google_only=True)
    else:
        full_news_en = full_news

    full_news = __ensure_paragraphs(full_news)
    full_news_en = __ensure_paragraphs(full_news_en)
    logger.info(
        "Got full_news and its translation:"
        f"{prettify(full_news)} {prettify(full_news_en)}"
    )
    return full_news, full_news_en


def translate(text, google_only=False):
    """
    We split the text to valid paragraph < 500 chars to give to translation
    The cuts are not exact 500 but based on last (full stop or purnabiram) 

    We can translte the split cuts at single request from google so we try that
    If it fails we use multi request operation.
    """
    cuts = __cut_text(text, length=500)
    logger.info(f"translate: Got cuts:{prettify(cuts)}")
    translation = __try_single_request_translation(cuts)
    if not translation:
        translation = __try_multi_request_translation(cuts, google_only)
    return translation


def summarize_to_tldr(text):
    SMMRY_KEY = os.getenv("SAMACHARTLDR_SMMRY_KEY")
    SMMRY_URL = "https://api.smmry.com/"
    url = SMMRY_URL + "&SM_API_KEY=" + SMMRY_KEY
    headers = {"Expect": ""}
    response = requests.post(url, data={"sm_api_input": text}, headers=headers)
    summary = json.loads(response.content.decode("utf-8"))
    logger.info(f"Got tldr summary info:{prettify(summary)}")
    time.sleep(10)
    return summary.get("sm_api_content")


def __cut_text(text, length=500):
    cuts = []

    def rec_cut(text, length):
        """Turn arbitary string cut to valid one by looking at last fullstop
        str = ab. cd. ef.
        Suppose input: text=str and length=5
        if length >= str don't cut and just return str
        cut = str[:5] --> 'ab. c'
        fullstop char at 2
        final_cut = cut[:3] -> 'ab.'
        pass_remaining_to_recursion, text=cut[3:] and length=5
        """
        logger.info("Cutting text")
        text_length = len(text)
        if length >= text_length:
            cuts.append(text)
            return
        else:
            logger.info(f"length {length} is smaller than text {len(text)}")
            snippet = text[:length]
            logger.info(f"generated snippet:{prettify(snippet)}")
            last_purnabiram = snippet.rfind("।") + 1
            last_fullstop = snippet.rfind(".") + 1
            # rfind returns -1 on failure (-1 + 1) == 0
            if last_purnabiram == 0 and last_fullstop == 0:
                raise ValueError("No purnabiram or fullstop found in given length")
            punctuation = last_purnabiram if last_purnabiram else last_fullstop
            logger.info(
                f"Punctuation:{punctuation} fullstop:{last_fullstop} purnabiram:{last_purnabiram}"
            )
            valid_paragraph = snippet[:punctuation]
            logger.info(f"Generated valid paragraph:{prettify(valid_paragraph)}")
            cuts.append(valid_paragraph)
            rec_cut(text[punctuation:], length)

    rec_cut(text, length)
    return cuts


def __try_single_request_translation(cuts):
    google_translator = Translator()
    translations = google_translator.translate(cuts)
    result = ""
    for translation in translations:
        result += translation.text
    return result.strip()


def __try_multi_request_translation(cuts, google_only):
    """ 
    Of course since its unlimited we prefer google translation
    """
    translation = __translate_from_google(cuts)
    if not translation and not google_only:
        logger.info("google failed Using mymemory")
        translation = __translate_from_mymemory(cuts)
    return translation


def __translate_from_google(cuts):
    useragent = os.getenv("SAMACHARTLDR_USERAGENT")
    google_translator = Translator(user_agent=useragent)
    translation = ""
    for paragraph in cuts:
        paragraph = f"""{paragraph}"""
        try:
            translated = google_translator.translate(paragraph, src="ne")
            translation += translated.text
            time.sleep(5)  # Pray google wont ban our ip
        except Exception:
            logger.exception("Error during translation:")
            return None

    return translation.strip()


def __translate_from_mymemory(cuts):
    secret = os.getenv("SAMACHARTLDR_MYMEMORY_KEY")
    mymemory_translator = MyMemoryTranslator(
        from_lang="ne", to_lang="en", secret_access_key=secret
    )
    translation = ""
    for paragraph in cuts:
        paragraph = f"""{paragraph}"""
        try:
            translated_snippet = mymemory_translator.translate(paragraph)
            translation += translated_snippet
        except Exception:
            logger.exception("Error during translation:")
            return None

    return translation.strip()


def __is_nepali(snippet):
    """ check for purnabiram if more than 3 we are on the no 3 is arbitrary
    could be improved """

    last_purnabiram = snippet.rfind("।")
    last_fullstop = snippet.rfind(".")
    # rfind returns -1 on failure
    if last_purnabiram == -1 and last_fullstop != -1:
        return False
    elif not snippet.count("।") > 3:
        return False
    else:
        return True


def __ensure_paragraphs(text):
    """ Checks if paragraph break in text else adds it and returns """
    if "\n\n" in text:
        # Paragraph break detected just return it
        return text

    # If not detected add it ourselves
    new_text = "\n\n".join(__cut_text(text, length=500))
    return new_text
