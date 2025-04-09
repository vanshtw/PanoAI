import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.techtarget.com/whatis/definition/ChatGPT"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

# Extract title
title = soup.find("title").text
#print("Title:", title)

# Extract all links
links = [a["href"] for a in soup.find_all("a", href=True)]
#print("Links:", links)

print(soup.text)


#data = {"Title": [title], "Links": [links]}
#df = pd.DataFrame(data)
#df.to_csv("output.csv", index=False)