import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select('.storylink')
subtext = soup.select('.subtext')

def get_new_page(index):
	res2 = requests.get(f'https://news.ycombinator.com/news?p={index}')
	soup2 = BeautifulSoup(res2.text, 'html.parser')
	links2 = soup2.select('.storylink')
	subtext2 = soup2.select('.subtext')
	return links2, subtext2

def sort_stories_by_votes(hnlist):
	return sorted(hnlist, key=lambda k:k['votes'], reverse=True)

def create_custom_hn(l, s):
	hn = []
	for idx, item in enumerate(l):
		title = l[idx].getText()
		href = l[idx].get('href', None)
		vote = s[idx].select('.score')
		if len(vote):
			points = int(vote[0].getText().replace(' points', ''))
			if points > 99:
				hn.append({'title': title, 'link': href, 'votes': points})
	return sort_stories_by_votes(hn)

for i in range(1, 11):
	print(f'https://news.ycombinator.com/news?p={i}')
	response = get_new_page(i)
	links += response[0]
	subtext += response[1]


new_hackernews = create_custom_hn(links, subtext)

for item in new_hackernews:
	print('\n')
	print('Title: ' + item['title'])
	print('Votes: ' + str(item['votes']))
	print('\n')
	print('---------------------------------------------------------')
	print('\n')
