from bs4 import BeautifulSoup
import requests

with open('simple.html') as html_file:
    soup = BeautifulSoup(html_file, features="html.parser")

# 1
print(soup)
print(soup.prettify())

print(soup.title)
print(soup.title.text)

print(soup.find('div', class_='footer'))

# 2
article = soup.find('div', class_='article')
headline = article.h2.a.text

print(article)
print(headline)

# 3
for article in soup.find_all('div', class_='article'):
    headline = article.h2.a.text
    print(headline)

    summary = article.p.text
    print(summary)

# 4
wikipedia_source = requests.get('http://www.wikipedia.org').text
wikipedia_soup = BeautifulSoup(wikipedia_source, features="html.parser")

pt = wikipedia_soup.find('div', lang='pt')
print(pt.a.small.span.text)
