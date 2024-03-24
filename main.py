import requests

from bs4 import BeautifulSoup

url = "https://cizgivedizi.com/dizi/sb/sungerbob_karepantolon"
r = requests.get(url)
soup = BeautifulSoup(r.content, features="lxml")
div = soup.find("div", {"id": "tumBolumler"})

links = div.find_all("a")

hrefs = [url + link.get('href').replace("\n", "").removeprefix("/dizi/sb/sungerbob_karepantolon") for link in links]
video_links_new = []
video_links_old = []

for i in hrefs:
	r = requests.get(i)
	soup = BeautifulSoup(r.content, features="lxml")
	p = soup.find_all("p")
	x = p[1].find_all("a")

	if len(x) == 3:
		video_links_old.append(x[1]["onclick"].removeprefix("sendVideo('").removesuffix("')"))
		video_links_old.append(x[2]["onclick"].removeprefix("sendVideo('").removesuffix("')"))
		print(f"{i} has original cnbc dub")
	elif len(x) == 2:
		video_links_old.append(x[1]["onclick"].removeprefix("sendVideo('").removesuffix("')"))
		print(f"{i} has original cnbc dub")
	else:
		div = soup.find("div", class_="ratio ratio-16x9")
		if div.find("iframe")["src"]:
			video_links_new.append(div.find("iframe")["src"])
		print(f"{i} doesn't have original cnbc dub")

old = open("old-episodes.txt", "w")
new = open("new-episodes.txt", "w")

for i in video_links_old:
	old.write(i + "\n" if i != video_links_old[-1] else i)
for i in video_links_new:
	new.write(i + "\n" if i != video_links_new[-1] else i)

old.close()
new.close()
