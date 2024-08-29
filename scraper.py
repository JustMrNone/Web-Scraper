import requests 
from bs4 import BeautifulSoup

page  = requests.get("https://en.wikipedia.org/wiki/Water")

soup = BeautifulSoup(page.content, "html.parser")



list(soup.children)


print("\n\n")

print(soup.find("h4").get_text())
