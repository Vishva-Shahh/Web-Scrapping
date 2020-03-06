"""
Web Scrapping using Beautiful Soup from dell website to extract queries and their status
"""

from urllib.request import urlopen

from bs4 import BeautifulSoup

import csv

"""
Part 1
"""

page_1 = urlopen("https://www.dell.com/community/Laptops/ct-p/Laptops")

soup_1 = BeautifulSoup(page_1, 'html.parser')

Laptops = soup_1.find_all('div', attrs={'class': 'cat-card-title'})

Posts = soup_1.find_all('div', attrs={'class': 'cat-card-stats'})

# Saving data in the dict:

sdata = {}

for i in range(5):
    a = Laptops[i].text.strip()
    if a in ['Inspiron', 'Latitude', 'XPS']:
        sdata[a] = Posts[i].text.split('\n')[2].strip()

for k, v in sdata.items():
    print(k, ":", v)

# Saving it in a csv file:

with open("Laptops_Posts.csv", "w") as toWrite:
    write = csv.writer(toWrite, delimiter=",")
    write.writerow(["Laptops", "Posts"])
    for a in sdata.keys():
        write.writerow([a.encode("utf-8"), sdata[a]])


"""
Part 2
"""

pages = []
list = []

for i in range(1, 6):
    if i == 1:
        url = 'https://www.dell.com/community/Inspiron/bd-p/Inspiron'
    else:
        url = 'https://www.dell.com/community/Inspiron/bd-p/Inspiron/page/' + str(i)
        pages.append(url)

    for item in pages:
        page = urlopen(item)
        soup = BeautifulSoup(page, 'html.parser')
        with open("Details.csv", "w", newline='', encoding="utf-8") as toWrite:
            writer = csv.writer(toWrite, delimiter=",")
            writer.writerow(["Solved", "Title", "Authors", "Date_Posted", "Time_Posted", "Views", "Replies", "Kudos",
                             "Latest_Author"])
            Title = soup.find_all("a", {"class": "page-link lia-link-navigation lia-custom-event"})
            Author = soup.find_all('a', {'class': "lia-link-navigation lia-page-link lia-user-name-link"})
            Date_Posted = soup.find_all("span", {"class": "local-date"})
            Time_Posted = soup.find_all("span", {"class": "local-time"})
            Views = soup.find_all("div", {"class": "lia-component-messages-column-topic-views-count"})
            Replies = soup.find_all('div', {'class': 'lia-component-messages-column-message-replies-count'})
            Kudos = soup.find_all("div", {"class": "lia-component-messages-column-message-kudos-count"})
            Author_Latest = soup.find_all('span',
                                          {'class': "UserName lia-user-name lia-user-rank-1-Copper "
                                                    "lia-component-common-widget-user-name"})
            Time_Latest = soup.find_all("span", {"cssclass": "lia-info-area-item"}, {"class": "local-time"})
            Solved = soup.find_all("td", {"aria-label": "This thread is solved"},
                                   {"class": "triangletop lia-data-cell-secondary lia-data-cell-icon"})
            for p in range(len(Solved)):
                list.append(Solved[p].text.strip())
                for i in range(0, 20):
                    lists = [Title[i].text.strip(), Author[i].text.strip(), Date_Posted[i].text.strip(),
                             Time_Posted[i].text.strip(),
                             Views[i].text.strip(), Replies[i].text.strip(), Kudos[i].text.strip(),
                             Author_Latest[i].text.strip()]
                    list.append(lists)
                    for j in list:
                        writer.writerow(j)
