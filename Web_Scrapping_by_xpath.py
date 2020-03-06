"""
Web Scrapping using x_path from dell website to extract queries and their status
"""

# Importing Libraries:
import pandas as pd
import selenium
from selenium import webdriver
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

# Saving it in a csv file from dictionary to data frame:
DF = pd.DataFrame(sdata, index=[0])
DF.to_csv("Laptops_Posts.csv", encoding='utf-8', index=False)

# Another way of writing into csv is also shown below:
with open("Laptops_Posts_1.csv", "w", newline='', encoding="utf-8") as toWrite:
    write = csv.writer(toWrite, delimiter=",")
    write.writerow(["Laptops", "Posts"])
    for a in sdata.keys():
        write.writerow([a.encode("utf-8"), sdata[a]])


"""
Part 2
"""

# Please change the executable path while running this part of the code:
driver = webdriver.Chrome(executable_path=r"C:\\Users\\shahv\\Downloads\\chromedriver.exe")

# Creating empty lists to store relevant data:
Title = []
Authors = []
Date_Posted = []
Time_Posted = []
Views = []
Replies = []
Kudos = []
Latest_Author = []
Latest_Date = []
Latest_Time = []
Query_Resolved = []

# Looping through pages 1 to 5:
for k in range(1, 6):
    driver.get('https://www.dell.com/community/Inspiron/bd-p/Inspiron/page/%s' % str(k))

    # Getting count of number of rows in a page:
    row = driver.find_elements_by_xpath('//*[@id="grid"]/table/tbody/tr')
    rows_count = len(row)

    # Looping through rows 1 to number of rows in a page:
    for i in range(1, rows_count):

        # Finding all elements by xpath and appending to the empty lists created above:
        TR = driver.find_elements_by_xpath('//*[@id="grid"]/table/tbody/tr' + str([i]) + str('/td[2]/div/div[1]/div'))

        Title.append(TR[0].text)

        Auth = driver.find_elements_by_xpath("//*[@id='grid']/table/tbody/tr" + str([i]) +
                                             str("/td[2]/div/div[2]/span[1]/span[1]"))

        Authors.append(Auth[0].text)

        D_P = driver.find_elements_by_xpath("// *[ @ id = 'grid'] / table / tbody / tr" + str([i]) +
                                            str("/ td[2] / div / div[2] / span / span[2] / span[1]"))
        Date_Posted.append(D_P[0].text)

        T_P = driver.find_elements_by_xpath("// *[ @ id = 'grid'] / table / tbody / tr" + str([i]) +
                                            str("/ td[2] / div / div[2] / span / span[2] / span[2]"))
        Time_Posted.append(T_P[0].text)

        Kudo = driver.find_elements_by_xpath("// *[ @ id = 'grid'] / table / tbody / tr" + str([i]) +
                                             str("/ td[3] / div / span"))
        Kudos.append(Kudo[0].text)

        Vw = driver.find_elements_by_xpath("// *[ @ id = 'grid'] / table / tbody / tr" + str([i]) +
                                           str("/ td[5] / div / span"))
        Views.append(Vw[0].text)

        Reps = driver.find_elements_by_xpath("// *[ @ id = 'grid'] / table / tbody / tr" + str([i]) +
                                             str("/ td[4] / div / span"))
        Rep = [x.text for x in Reps]
        Replies.extend(Reps[0].text)

        # This condition is because the latest post will exist only if the number of replies are greater than 0:
        if Rep[0] == '0':
            continue

        Latest_Auth = driver.find_elements_by_xpath("//*[@id='grid']/table/tbody/tr" + str([i]) +
                                                    str("/td[2]/div/div[2]/span[3]/span[2]"))
        Latest_Author.append(Latest_Auth[0].text)

        Latest_D = driver.find_elements_by_xpath("// *[ @ id = 'grid'] / table / tbody / tr" + str([i]) +
                                                 str("/ td[2] / div / div[2] / span[3] / span[1] / span[1]"))
        Latest_Date.append(Latest_D[0].text)

        Latest_T = driver.find_elements_by_xpath("// *[ @ id = 'grid'] / table / tbody / tr" + str([i]) +
                                                 str("/ td[2] / div / div[2] / span[3] / span[1] / span[2]"))
        Latest_Time.append(Latest_T[0].text)

        Solve = driver.find_elements_by_xpath("// *[aria-label='This thread is solved']/ table / tbody / tr" + str([i]))
        Resolve = [x.text for x in Solve]
        Query_Resolved.append(Resolve)

# Storing into zip list:
Final_List = list(zip(Title, Authors, Date_Posted, Time_Posted, Views, Kudos, Replies, Query_Resolved,
                      Latest_Author, Latest_Date, Latest_Time))

# Creating a Data frame:
Details = pd.DataFrame(Final_List,columns=["Title", "Authors", "Date_Posted", "Time_Posted", "Views", "Kudos",
                                           "Replies",  "Query_Resolved", "Latest_Author", "Latest_Date", "Latest_Time"])

# Transferring output to a CSV file:
Details.to_csv("Details_of_Queries.csv", encoding='utf-8', index=False)
