import re
from bs4 import BeautifulSoup
import requests

# def get_news_titles(news_links):
# 	news_title = []
# 	for i in news_links:
	

		
		
def get_news_link(company_name):
	company_url = f"""https://www.google.com/search?sca_esv=562371431&rlz=1C1ONGR_enIN1001IN1001&sxsrf=
	AB5stBg33JZjPbgGS_TI9kd0Df0ftKePeQ:1693769192639&q={company_name}&tbm=nws&source=
	lnms&sa=X&ved=2ahUKEwiP5Lv4lY-BAxWA3TgGHc_FAHEQ0pQJegQIDBAB&biw=1745&bih=881&dpr=1.1"""

	response = requests.get(company_url)

	soup = BeautifulSoup(response.content, "html.parser")

	all_links = soup.find_all('a')
	https_links = []
	for i, j in enumerate(all_links):
		if re.search(r"https://", j.get('href')):
			if re.search(r"/url\?q=", j.get('href')):
				https_links.append(j.get('href').replace(r"/url?q=", ""))
	# return https_links[:len(https_links)-4]
	return https_links[:len(https_links)-4]

