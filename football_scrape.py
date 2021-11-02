import webbrowser
from selenium import webdriver
import pdb, time, sys, os
import random, datetime
from datetime import date, timedelta
import pandas as pd
import bs4

from selenium.webdriver.common.keys import Keys

# calculate random time to simulate human input
def rand_time(lower, upper):
	return random.uniform(lower, upper)

def verbose_wait(wait):
	wait_count = int(wait)
	for i in range(0, int(wait)):
		print(wait_count)
		time.sleep(1)
		wait_count -= 1

def load_data(browser):
	print('loading data...')

	div_elems = browser.find_elements_by_css_selector('div[class=\"OcbAbf\"]')
	
	score_list = []
	for cur_div in div_elems:
	
		try:
			week = cur_div.find_element_by_css_selector('div[role=\"heading\"]').text
			print(week)
		except:
			pass
	
		#tile_elems = cur_div.find_elements_by_css_selector('td[class=\"liveresults-sports-immersive__match-tile imso-hov liveresults-sports-immersive__match-grid-bottom-border liveresults-sports-immersive__match-grid-right-border\"]')
		tile_elems = cur_div.find_elements_by_css_selector('div[class=\"imso-loa imso-ani\"]')

		for cur_tile in tile_elems:
			
			tile_list = cur_tile.find_elements_by_css_selector('tr[class=\"L5Kkcd\"]')
			
			assert len(tile_list) == 2
			
			#tile_string = cur_tile.text
			#tile_list = tile_string.split('\n')[~3:]

			try:
				team_1 = tile_list[0].text.split('\n')[1]
				score_1 = tile_list[0].text.split('\n')[0]
				
				team_2 = tile_list[1].text.split('\n')[1]
				score_2 = tile_list[1].text.split('\n')[0]

				score_list.append([week, team_1, team_2, int(score_1), int(score_2)])
				
			except:
				pass
	
	data_out = pd.DataFrame(score_list, columns = ['Week','Team 1','Team 2','Score 1','Score 2'])
	return browser, data_out 

site_name = 'https://www.google.com/search?q=NFL+2021&client=firefox-b-1-d&ei=qr59YdO-M7OrwbkPr7-8sA0&oq=NFL+2021&gs_lcp=Cgdnd3Mtd2l6EAMyBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjoHCAAQRxCwA0oECEEYAFD2JljcN2CUOmgFcAJ4AIAB5AGIAaMDkgEFMS4xLjGYAQCgAQHIAQjAAQE&sclient=gws-wiz&ved=0ahUKEwjTu-m0j_PzAhWzVTABHa8fD9YQ4dUDCA0&uact=5#sie=lg;/g/11nym9rnk6;6;/m/059yj;mt;fp;1;;'

browser = webdriver.Firefox() #profile_loc
print('loading page...')
browser.get(site_name)
#verbose_wait(rand_time(10,15))		
	
#browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
input('please scroll to top, then hit ENTER')
browser, df = load_data(browser)

browser.close()

df.to_csv('scraped_games.csv', index=None)