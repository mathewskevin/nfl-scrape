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

def wait_elem(browser, elem_string, type='css'):
	elem_found = False
	while elem_found is False:
	
		try:
			if type=='tag':
				browser.find_element_by_tag_name(elem_string)
			elif type == 'link':
				browser.fine_element_by_link_text(elem_string)
			else:
				browser.fine_element_by_css_selector(elem_string)
		except:
			pass

		elem_found = True

	return browser

def verbose_wait(wait):
	wait_count = int(wait)
	for i in range(0, int(wait)):
		print(wait_count)
		time.sleep(1)
		wait_count -= 1

def load_nfl_data(browser):
	
	css_string = 'select[class="d3-o-dropdown"]'
	elems = browser.find_elements_by_css_selector(css_string)
	
	assert len(elems) == 2
	year_dropdown = elems[0]
	#week_dropdown = elems[1]
	
	year_list = year_dropdown.text.split('\n')
	year_list.reverse()
	
	for year_string in year_list:
	
		# https://stackoverflow.com/questions/7867537/how-to-select-a-drop-down-menu-value-with-selenium-using-python
		browser.find_element_by_xpath("//select[@class='d3-o-dropdown']/option[text()='" + year_string + "']").click()

		time.sleep(2)
		try:
			css_string = 'select[class="d3-o-dropdown"]'
			elems = browser.find_elements_by_css_selector(css_string)
			assert len(elems) == 2
			week_dropdown = elems[1]
			week_list = week_dropdown.text.split('\n')
		except:
			print('ERROR.')
			browser.close()
			exit()
		
		for week_string in week_list:
			browser.find_element_by_xpath("//select[@class='d3-o-dropdown']/option[text()='" + week_string + "']").click()
			time.sleep(3)
			
			# https://stackoverflow.com/questions/55492695/javascript-error-arguments0-scrollintoview-is-not-a-function-using-selenium-o
			img_css = 'img[data-src="https://static.www.nfl.com/image/upload/v1554321393/league/nvfr7ogywskqrfaiu38m.svg"]'
			img_elem = browser.find_elements_by_css_selector(img_css)
			browser.execute_script("arguments[0].scrollIntoView();", img_elem[~0])
			time.sleep(3)
			
			# get tiles
			css_string = 'a[class="nfl-c-matchup-strip__left-area"]'
			elems = browser.find_elements_by_css_selector(css_string)
			
			print(year_string, week_string)
			
			data_list = []
			for elem in elems:
				data = elem.text.split('\n')
				data.append(elem.get_attribute('href'))
				data_list.append(data)
			
			# cycle through elems
			for i in range(0, len(data_list)):
				css_string = 'a[class="nfl-c-matchup-strip__left-area"]'
				elems = browser.find_elements_by_css_selector(css_string)

				try:
					assert len(elems) == len(data_list)
				except:
					pdb.set_trace()
				
				# enter game to get score
				browser.execute_script("arguments[0].scrollIntoView();", elems[i])
				elems[i].click()
				time.sleep(5)
				css_string = 'div[class="nfl-c-strip"]'
				elems = browser.find_elements_by_css_selector(css_string)
				assert len(elems) == 2
				
				game_list = elems[1].text.split('\n')
				
				team_1_rate = game_list[0]
				team_1_score = game_list[3]

				team_2_rate = game_list[~1]
				team_2_score = game_list[5]
				
				data_list = data_list[i] + [team_1_rate, team_1_score, team_2_rate, team_2_score]
				
				browser.back()
				time.sleep(5)
				pdb.set_trace()

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

site_name = 'https://www.nfl.com/schedules/2010/PRE0/'
#site_name = 'https://www.google.com/search?q=NFL+2021&client=firefox-b-1-d&ei=qr59YdO-M7OrwbkPr7-8sA0&oq=NFL+2021&gs_lcp=Cgdnd3Mtd2l6EAMyBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjoHCAAQRxCwA0oECEEYAFD2JljcN2CUOmgFcAJ4AIAB5AGIAaMDkgEFMS4xLjGYAQCgAQHIAQjAAQE&sclient=gws-wiz&ved=0ahUKEwjTu-m0j_PzAhWzVTABHa8fD9YQ4dUDCA0&uact=5#sie=lg;/g/11nym9rnk6;6;/m/059yj;mt;fp;1;;'

browser = webdriver.Firefox() #profile_loc
print('loading page...')
browser.get(site_name)
#verbose_wait(rand_time(10,15))		
#browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
#input('please scroll to top, then hit ENTER')
browser, df = load_nfl_data(browser)

browser.close()

df.to_csv('scraped_games.csv', index=None)