from bs4 import BeautifulSoup
from requests import get
from re import search
from google import generativeai as genai
import argparse


def ask_gemini(query, count):
    parser = argparse.ArgumentParser(description="News Summarizer using Gemini AI")
    parser.add_argument("-api", "--api_key", help="Gemini-ai api key", required=True)
    parser.add_argument("-o", "--filename", help="filename to save", required=True)
    args = parser.parse_args()
    file = args.filename

    genai.configure(api_key=args.api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Simply this cyber security news for children aged 8-12, and words must be simpler, if I am using the same query again and again use a cache or gimme the same response: {query}")
    print(response.text)
    with open(file, 'a') as f:
        f.writelines(f"News {count}: \n\n"+''.join(response.text))


def extract_ptags(links):
    count = 0
    for link in links:
        page = get(f"{link}")
        soup = BeautifulSoup(page.content, "html.parser")
        div = soup.find(id="articlebody")
        p_tags = div.find_all("p")
        text_contents = []
        count += 1 
        for p_tag in p_tags:
            text_contents.append(p_tag.get_text(strip=True))
        text = ''.join(text_contents)
        ask_gemini(text, count)
        print("WHy would i do it")


def main():
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
    url = "https://thehackernews.com/"
    page = get(url, headers=header)
    soup = BeautifulSoup(page.content, "html.parser")
    tags = soup.find_all(class_="story-link")
    links = []
    for tag in tags:
        link = tag.attrs['href']
        
        if search(r"^https://thehackernews.com/2025/01/.*html$", link):
            links.append(link)  
    extract_ptags(links)


if __name__ == "__main__":
    main()