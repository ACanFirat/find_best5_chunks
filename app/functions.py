import os
import requests
import fitz

path = os.getcwd() + "/documents"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 YaBrowser/19.6.1.153 Yowser/2.5 Safari/537.36'}

if not os.path.exists(path):
    os.mkdir(path)
    print("Directory ", path, " Created ")


def download_file(download_url):

    response = requests.get(download_url, headers=headers)
    file = open("documents/downloaded.pdf", "wb")
    file.write(response.content)
    file.close()


def check_url_is_same(url, index_content):
    if index_content == url:
        return True
    else:
        return False


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        page_text = page.get_text()
        page_text = page_text.replace('-\n', '')
        page_text = page_text.replace('\n', ' ')
        text += page_text
    return text
