import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select  # to deal with dropdown menues
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd

#driver = webdriver.Chrome('/Users/ik/Codes/soccerway-scraping/chromedriver')
#driver = webdriver.PhantomJS()

list_dates = []

list_player1 = []
list_player2 = []

list_player1_set1 = []
list_player1_set2 = []
list_player1_set3 = []
list_player1_set4 = []
list_player1_set5 = []

list_player2_set1 = []
list_player2_set2 = []
list_player2_set3 = []
list_player2_set4 = []
list_player2_set5 = []

list_courts = []

driver = webdriver.Chrome('/Users/ik/Codes/aopen-scraping/chromedriver')

start_page  = "http://www.ausopen.com/en_AU/scores/completed_matches"

driver.get(start_page)

dropdown_menu = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#eventSelector")))

dropdown_menu.click()

menu_item = Select(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cmatch"))))
menu_item.select_by_value("MS")

time.sleep(3)

# now go to the list of days: it's <div> with id=tournDays

playday_list = driver.find_element_by_xpath("//div[@id='tournDays']/ul")

#print("playday_list=",playday_list.text)
# collect all <a> with href

as_in_playday_list = playday_list.find_elements_by_xpath("li/a[@href]")
total_days = len(as_in_playday_list)
match_dates = [a.get_attribute("title").strip() for a in as_in_playday_list]

a = as_in_playday_list[0]


# suppose there are 14 days in total, but we are asready on day 1, so the total number of clicks will be
# one less than the total umber of days

a.click()
time.sleep(3)  # go to page 1

for i in range(total_days): 

	if i > 0 and i < (total_days - 1):
		driver.find_element_by_xpath("//div[@id='tournDays']/ul").find_elements_by_xpath("li/a[@href]")[i].click()

	print("scraping day", i, "...", end="")

	time.sleep(3)

	score_tables = driver.find_elements_by_xpath("//div[@class='scoringtable' and @data-event='MS']")  # list of tables

	for t in score_tables:
		
		list_dates.append(match_dates[i])  # same match date for tables on the page

		list_courts.append(t.find_element_by_xpath("div/div[@class='courtname']").text)

		player1_set1 = t.find_elements_by_css_selector("span.set1")[0].text
		player2_set1 = t.find_elements_by_css_selector("span.set1")[1].text
		player1_set2 = t.find_elements_by_css_selector("span.set2")[0].text
		player2_set2 = t.find_elements_by_css_selector("span.set2")[1].text
		player1_set3 = t.find_elements_by_css_selector("span.set3")[0].text
		player2_set3 = t.find_elements_by_css_selector("span.set3")[1].text
		player1_set4 = t.find_elements_by_css_selector("span.set4")[0].text
		player2_set4 = t.find_elements_by_css_selector("span.set4")[1].text
		player1_set5 = t.find_elements_by_css_selector("span.set5")[0].text
		player2_set5 = t.find_elements_by_css_selector("span.set5")[1].text

			
		list_player1.append(t.find_elements_by_css_selector(".name.singles")[0].find_element_by_xpath("a").text)
		list_player2.append(t.find_elements_by_css_selector(".name.singles")[1].find_element_by_xpath("a").text)

	print("ok")

	# combine matches in one list of tuples, something like matches of the day
	
data = zip(list_dates, list_courts, list_player1, player1_set1, player1_set2, player1_set3, player1_set4, player1_set5,
				 list_player2, player2_set1, player2_set2, player2_set3, player2_set4, player2_set5)
for z in data:
	print(z)
print("created a zip...")
	

driver.quit()
