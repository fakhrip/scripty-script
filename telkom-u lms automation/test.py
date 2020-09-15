from bs4 import BeautifulSoup
import re
a = open('test', 'r').read()
soup = BeautifulSoup(a, 'html.parser')
topics = soup.find_all(attrs={"class": "topics"})[0]
sections = topics.find_all('li', recursive=False)
summary = sections[0].find_all(attrs={'class': 'summary'})[0]
summ_text = str(summary.text)
result = ''
temp = ''
found = False
for pos, char in enumerate(summ_text):
    temp += char
    if summary.find(text=temp) != None:
        found = True
        if pos == len(summ_text)-1:
            result += temp + '\n'
            print('------\n' + str(summary.find(text=temp)))
    else :
        if found :
            result += temp[:-1] + '\n'
            print('------\n' + str(summary.find(text=temp[:-1])))
            temp = temp[len(temp)-1:]
            found=False