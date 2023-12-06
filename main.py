# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup
import pandas as pd

import time
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"
]


def print_hi():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # URL of the website to be scraped
    url = "https://certificateland.com/google-ads-search-exam-answers/"

    # Session ile istek yapma
    with requests.Session() as s:
        s.headers.update(headers)
        response = s.get(url)

    # Parsing the webpage using BeautifulSoup
    soup = BeautifulSoup(response.content, 'lxml')

    # Finding all question and answer sections in the webpage
    qa_sections = soup.find("div", class_="entry-content")
    qa_sectionx = qa_sections.find_all('p')
    # Extracting questions and answers
    questions_deep_link = []
    for section in qa_sectionx:
        # Each section is split by <strong> tags, the first one usually contains the question
        first_a_tag = section.find('a')
        page_link = first_a_tag['href'] if first_a_tag else 'no href'
        if 'https://certificateland.com' in page_link and '/contact-us/' not in page_link:
            questions_deep_link.append(page_link)
    all_answers = []
    all_questions = []
    for deep_link in questions_deep_link[0:5]:
        random_user_agent = random.choice(user_agents)
        time.sleep(random.uniform(1, 10))  # 1 ile 5 saniye arasında rastgele bir süre bekler

        if len(deep_link) > 20 and deep_link != 'no href':
            print(deep_link)
            with requests.Session() as a:
                a.headers.update({'User-Agent': random_user_agent})
                detail_response = s.get(deep_link)

            # Parsing the webpage using BeautifulSoup
            soup = BeautifulSoup(detail_response.content, 'lxml')
            main_title = soup.find('h1', class_='entry-title').text

            # 'entry-content clearfix' sınıfına sahip div'i bul
            entry_content_div = soup.find('div', class_='entry-content clearfix')

            # Bu div içindeki tüm ul etiketlerini bul
            ul_tags = entry_content_div.find_all('ul') if entry_content_div else []

            # İkinci ul etiketini seç (Liste indexi 0'dan başlar, bu yüzden ikinci eleman için [1] kullanılır)
            second_ul = ul_tags[1] if len(ul_tags) > 1 else None

            # İkinci ul içindeki tüm li etiketlerinin metnini al
            li_texts = [li.get_text(strip=True) for li in second_ul.find_all('li')] if second_ul else []
            if len(li_texts) > 0 and len(main_title) > 0:
                joined_string = ','.join(li_texts)
                all_answers.append(joined_string)
                all_questions.append(main_title)
    data = {'Column1': all_questions, 'Column2': all_answers}
    df = pd.DataFrame(data)
    df.to_excel("output.xlsx", index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
