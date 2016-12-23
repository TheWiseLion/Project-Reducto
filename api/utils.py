# coding=utf-8
import re
import struct
import urllib2
import html2text
import io
from BeautifulSoup import BeautifulSoup
common_replacement = ["There was an error emailing this page.","Your message has been sent."]


def getImageInfo(data):
    data = data
    size = len(data)
    # print(size)
    height = -1
    width = -1
    content_type = ''

    # handle GIFs
    if (size >= 10) and data[:6] in (b'GIF87a', b'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'image/gif'
        w, h = struct.unpack(b"<HH", data[6:10])
        width = int(w)
        height = int(h)

    # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and data.startswith(b'\211PNG\r\n\032\n')
          and (data[12:16] == b'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(b">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and data.startswith(b'\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(b">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and data.startswith(b'\377\330'):
        content_type = 'image/jpeg'
        jpeg = io.BytesIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = jpeg.read(1)
                while (ord(b) == 0xFF): b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(b">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(b">H", jpeg.read(2))[0]) - 2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass

    return content_type, width, height


def obtain_title(source, domain = None):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_tables = True
    h.body_width = 0
    parsed_text = h.handle(source.decode('utf8'))
    title_expression = re.compile('\n#\s(.{6,})\n') # title should be at least 6 chars
    return title_expression.search(parsed_text).group(1)

# Strip down to hard content for extractive summery
def obtain_text(source, domain = None):
    """

    :param source:
    :param domain: domain of source for additional logic
    :return:
    """
    # # TODO: only get content after the title
    # # TODO: optional quotes
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_tables = True
    h.body_width = 0
    parsed_text = h.handle(source.decode('utf8')).replace("_","\"")
    title_expression = re.compile('\n#\s(.{6,})\n')
    title = title_expression.search(parsed_text).group(1)

    # Heuristic: find the title then go from there
    title = parsed_text.find(title)
    if title is not -1:
        parsed_text = parsed_text[title:]
    # Heuristic: Find the first "by", if it's less than 20% into the text then split there
    first_by = parsed_text.find(r'By')
    if first_by is not -1:
        parsed_text = parsed_text[first_by:]


    # Only Content That Starts with letters and has proper sentence structure (Capital, period)
    text_expression = re.compile('\n("?[A-Z].{25,}\."?)', re.IGNORECASE)
    for b in common_replacement:
        parsed_text = parsed_text.replace(b, "",1000)

    return text_expression.findall(parsed_text)

# Summarize Text
def obtain_images(source, minX=600, minY=500):
    """
    Get image url's from page
    :param source: string - html source
    :param minX: min image width
    :param minY: min image height
    :return:
    """
    images = []
    page = BeautifulSoup(source)
    for img in page.findAll('img'):
        try:
            print img
            tmp = img.get('src')
            if tmp is None:
                tmp = img.get('data-lazy')
                if tmp is None:
                    tmp = img.get('data-src')
            else:
                tmp = tmp.split('?', 1)[0]

            if tmp is not None and not (tmp.startswith("http") or tmp.startswith('https')):
                tmp = "http:" + tmp

        except Exception as src_err:
            print src_err.message, " of ", img

        print tmp
        try:

            req = urllib2.Request(tmp, headers={"Range": "5000"})
            r = urllib2.urlopen(req)
            ctype, w, h = getImageInfo(r.read(1024))

        except Exception as e:
            try:
                req = urllib2.Request(tmp, headers={"Range": "5000"})
                r = urllib2.urlopen(req)
                ctype, w, h = getImageInfo(r.read(50 * 1024))
            except Exception as e2:
                print e2.message
                continue
        print w,h
        if w >= minX or h >= minY:
            images.append(str(tmp.encode('ascii','ignore')))
    # images.reverse()  # seems to load images in reverse order...
    return images



# def summarize_text(document_text, sentances=3):
#     LANGUAGE = "english"
#     stemmer = Stemmer(LANGUAGE)
#     stopper = get_stop_words(LANGUAGE)
#
#     # summarizer = LsaSummarizer(stemmer)
#     # summarizer.stop_words = stopper
#     parser = PlaintextParser.from_string(document_text, Tokenizer("english"))
#     summarizer = LexRankSummarizer()
#     r = summarizer(parser.document, sentances)
#     return [str(s) for s in r]

# from cookielib import CookieJar
# cj = CookieJar()
# url = "http://www.cio.com/article/3149511/leadership-management/jetblue-cio-drives-innovation-through-it-s-toolkit.html"
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
# opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')]
# data = opener.open(url).read()
# text = " ".join(obtain_text(data)[:10])
# print text
# print obtain_title(data)
# print obtain_images(data)
# print summarize_text(text)
