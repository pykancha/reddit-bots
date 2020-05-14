"""
This module combines the article extraction and translation part.
It combines the two library googletrans/translate and newspaper_wrapper
"""

import os
import time

from googletrans import Translator
from newspaper_wrapper import Article
from newspaper_wrapper.article import ArticleException
from translate import Translator as MyMemoryTranslator


def get_news(url):
    article = Article(url, language="hi")
    try:
        article.download()
        article.parse()
        article.nlp()
    except ArticleException:
        print(f"Error: Download timeout {url}")
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
    print(f"Got news: \n{data}")
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
        print("Reusing translated full news")
        summary_en = __cut_text(full_news_en, length=limit)[0]
    else:
        summary_en = translate(summary) if __is_nepali(summary) else ''

    summary = __ensure_paragraphs(summary)
    summary_en = __ensure_paragraphs(summary_en)
    print(f"Got summary and its translation \n{summary} \n{summary_en}")

    return summary, summary_en


def get_full_news(text):
    '''
    We only want to translate if it is in nepali.
    '''
    full_news = text
    full_news_en = ''

    if __is_nepali(full_news):
        full_news_en = translate(full_news, google_only=True)

    full_news = __ensure_paragraphs(full_news)
    full_news_en = __ensure_paragraphs(full_news_en)
    print(f"Got full_news and its translation \n{full_news} \n{full_news_en}")

    return full_news, full_news_en


def translate(text, google_only=False):
    """
    We split the text to valid paragraph < 500 chars to give to translation
    The cuts are not exact 500 but based on last (full stop or purnabiram) 

    We can translte the split cuts at single request from google so we try that
    If it fails we use multi request operation.
    """
    cuts = __cut_text(text, length=500)
    print(f"translate: Got cuts: \n{cuts}")
    translation = __try_single_request_translation(cuts)
    if not translation:
        translation = __try_multi_request_translation(cuts, google_only)
    return translation


def __cut_text(text, length=500):
    cuts = []

    def rec_cut(text, length):
        """Turn arbitary string cut to valid one by looking at last fullstop
        str = ab. cd. ef.
        Suppose input: text=str and length=5
        if lenght >= str just dont cut and return str
        cut = str[:5] --> 'ab. c'
        fullstop car at 2
        final_cut = cut[:3] -> 'ab.'
        pass_remaining_to_recursion, text=cut[3:] and length=5
        """
        print("Cutting text")
        text_length = len(text)
        if length >= text_length:
            cuts.append(text)
            return
        else:
            print(f"length {length} is smaller than text {len(text)}")
            snippet = text[:length]
            print(f"generated snippet \n{snippet}")
            last_purnabiram = snippet.rfind("।") + 1
            last_fullstop = snippet.rfind(".") + 1
            # rfind returns -1 on failure (-1 + 1) == 0
            if last_purnabiram == 0 and last_fullstop == 0:
                raise ValueError("No purnabiram or fullstop found in given length")
            punctuation = last_purnabiram if last_purnabiram else last_fullstop
            print(
                f"Punctuation:{punctuation} fullstop:{last_fullstop} purnabiram:{last_purnabiram}"
            )
            valid_paragraph = snippet[:punctuation]
            print(f"Generated valid paragraph \n{valid_paragraph}")
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
        print("google failed Using mymemory")
        translation = __translate_from_mymemory(cuts)
    return translation


def __translate_from_google(cuts):
    useragent = os.getenv("LINK_GURU_USERAGENT")
    google_translator = Translator(user_agent=useragent)
    translation = ""
    for paragraph in cuts:
        paragraph = f"""{paragraph}"""
        try:
            translated = google_translator.translate(paragraph, src="ne")
            translation += translated.text
            time.sleep(2)  # Pray google wont ban our ip
        except Exception as e:
            print(f"Error during translation: {e}")
            return None

    return translation.strip()


def __translate_from_mymemory(cuts):
    secret = os.getenv("LINK_GURUBOT_MYMEMORY_KEY")
    mymemory_translator = MyMemoryTranslator(
        from_lang="ne", to_lang="en", secret_access_key=secret
    )
    translation = ""
    for paragraph in cuts:
        paragraph = f"""{paragraph}"""
        try:
            translated_snippet = mymemory_translator.translate(paragraph)
            translation += translated_snippet
        except Exception as e:
            print(f"Error during translation: {e}")
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
