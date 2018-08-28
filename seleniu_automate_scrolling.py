import sys
sys.path.append('/usr/local/lib/python3.5/dist-packages')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep

MAKE_DIV_XPATH='//*[@id="aj_scr"]'
MODEL_DIV_XPATH='//*[@id="aj_scrr"]'
PAGE_NUMBER_TABLE_XPATH='//*[@id="aj_out_poisk"]/div/table[1]/tbody/tr/td[3]/table'
LOT_TABLE_XPATH='//*[@id="aj_out_poisk"]/div/table[2]'
#r'C:\Python\chromedriver.exe'
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('http://auc.autoworldjapan.com/')



def find_login_container():
	element=driver.find_element_by_xpath('//*[@id="aj_login_but_r"]')
	#element.click()
	return element

def login_the_website(element):
	element.click()
	sleep(1)
	username=driver.find_element_by_xpath('//*[@id="form_auth"]/table/tbody/tr/td[1]/table[1]/tbody/tr[1]/td[2]/input')
	password=driver.find_element_by_xpath('//*[@id="form_auth"]/table/tbody/tr/td[1]/table[2]/tbody/tr[1]/td[2]/input')
	username.send_keys("jay.k")
	password.send_keys("kaveri1981")
	log_in=driver.find_element_by_xpath('//*[@id="form_auth"]/table/tbody/tr/td[2]/input[3]')
	log_in.click()
	sleep(2)
	redirect_element=driver.find_element_by_xpath('//*[@id="aj_out_ALT"]/table/tbody/tr/td/div[1]/div[1]/table/tbody/tr[2]/td/a')
	redirect_element.click()
	driver.get('http://auc.autoworldjapan.com/aj_neo?classic')

def find_make_div(element_xpath):
	make_div_element=driver.find_element_by_xpath(element_xpath)
	return make_div_element

#---Finding table that contains all "lot number" a tag--- 
def find_table_containing_lot_number(element_xpath):
	lot_table_element=driver.find_element_by_xpath(element_xpath)
	a_tag=lot_table_element.find_elements_by_class_name("my_bids")
	count_lot=0
	for a_t in a_tag:
		if a_t.text !="":
			sleep(2)
			print(a_t.text.strip())
			lot_xpath='//*[@id="aj_view'+str(count_lot)+'"]/td[2]/table/tbody/tr[2]/td/a'
			print(lot_xpath)
			a_t=driver.find_element_by_xpath(lot_xpath)
			a_t.click()
			count_lot=count_lot+1
			driver.switch_to_window(driver.window_handles[-1])
			sleep(2)
			driver.close()
			driver.switch_to_window(driver.window_handles[0])

	#pass

#---Finding the table containing all the page number "a" tag---
def find_page_number_table(element_xpath):
	wait = WebDriverWait(driver, 10)
	element=driver.find_element_by_xpath(element_xpath)
	a_tag=element.find_elements_by_tag_name('a')
	count_a=1
	for a_t in a_tag:
		try:
			
			a_xpath='//*[@id="aj_out_poisk"]/div/table[1]/tbody/tr/td[3]/table/tbody/tr/td['+str(count_a)+']/a'
			a_t_new=wait.until(EC.element_to_be_clickable((By.XPATH,a_xpath)))

			print(a_t_new.get_attribute("text"))		
			a_t_new.click()
			find_table_containing_lot_number(LOT_TABLE_XPATH)
		#print(a_t.text)
			count_a=count_a+1
			sleep(2)
						#print(prev_page)
		except Exception as e:
			#print(a_t.get_attribute("text"))
			print(e)
	

def find_model_div(element_xpath):
	wait = WebDriverWait(driver, 10)
	element=driver.find_element_by_xpath(element_xpath)
	model_a_tag=element.find_elements_by_tag_name('a')
	for m_a_t in model_a_tag:
		try:
			m_a_t = wait.until(EC.visibility_of_element_located((By.ID,m_a_t.get_attribute("id"))))
			sleep(1)
			if m_a_t.text !='Any':	
				actions_1 = ActionChains(driver)
				actions_1.move_to_element(m_a_t)
				actions_1.click(m_a_t)
				actions_1.perform()
				print(m_a_t.text)
				find_page_number_table(PAGE_NUMBER_TABLE_XPATH)
		except Exception as e:
			print(e)
			driver.execute_script("arguments[0].scrollIntoView();",m_a_t)
			driver.execute_script("window.scrollTo(0, -150)")
			actions_1 = ActionChains(driver)
			actions_1.move_to_element(m_a_t)
			actions_1.click(m_a_t)
			actions_1.perform()
			print(m_a_t.text)
			find_page_number_table(PAGE_NUMBER_TABLE_XPATH)
	#print(len(model_a_tag))
	#return model_a_tag	

def find_a_tag_in_make_div(element):
	wait = WebDriverWait(driver, 10)
	a_tag=element.find_elements_by_tag_name('a')
	#print(len(a_tag))
	for a_t in a_tag:
		if a_t.text=="Any":
			pass
		else:
			try:
				#driver.execute_script("arguments[0].scrollIntoView();",a_t)
				#a_t_id = wait.until(EC.visibility_of_element_located((By.ID,a_t.get_attribute("id"))))
				
				sleep(1)
				#a_t.click()
				#a_t.scrollIntoView()	
				actions = ActionChains(driver)
				actions.move_to_element(a_t)
				actions.click(a_t)
				actions.perform()
				print(a_t.text)
				find_model_div(MODEL_DIV_XPATH)
				#model_a_tag=find_model_div(MODEL_DIV_XPATH)
				#for m_a_t in model_a_tag:
				#	try:
				#		m_a_t = wait.until(EC.visibility_of_element_located((By.ID,m_a_t.get_attribute("id"))))
				#		sleep(1)	
				#		actions_1 = ActionChains(driver)
				#		actions_1.move_to_element(m_a_t)
				#		#actions_1.click(m_a_t)
				#		actions_1.perform()
				#		print(m_a_t.text)
				#	except Exception as e:
				#		print(e)

			except Exception as e:
				print(e)
				#driver.execute_script("arguments[0].scrollIntoView();",a_t)
				#a_t.click()

def main():
	element=find_login_container()
	login_the_website(element)
	make_div_element=find_make_div(MAKE_DIV_XPATH)
	find_a_tag_in_make_div(make_div_element)
	#print(make_div_element)	


if __name__=="__main__":
	main()

