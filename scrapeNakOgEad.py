from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.options import Options



page_limit = 3000
visited_links_limit = 3000


# basic setup
url = 'https://www.dr.dk/mad/program/nak-aed'
linksToRecipes = []

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'./geckodriver')
driver.get(url)
html = driver.page_source.encode('utf-8')
page_num = 0

# accept nice cookies
driver.find_element_by_css_selector('#CybotCookiebotDialogBodyButtonAccept').click()

#  As long as we can click the 'show more' button we do that
while driver.find_elements_by_css_selector('.load-more') and page_num < page_limit: 
    driver.find_element_by_css_selector('.load-more').click()
    page_num += 1
    print("getting page number "+str(page_num))
    time.sleep(1)

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
all_recipe_links = soup.find_all('a', class_='item__heading heading-small')

# creating a list of links to recipes
for link in all_recipe_links:
    linksToRecipes.append('https://www.dr.dk' + link.get('href'))
    
# now we have to access each link and fetch ingredients and and steps
links_visted = 0
for link in linksToRecipes:

    print('reading recipe ' + str(links_visted + 1) + ' of ' + str(len(linksToRecipes)))

    # limiting our requests
    if links_visted >= visited_links_limit:
        break;

    driver.get(link)
    recipe_html = driver.page_source.encode('utf-8')
    recipe_soup = BeautifulSoup(recipe_html, 'html.parser')

    # getting the title
    recipe_string = recipe_soup.find('h1', {'class': 'heading-xxlarge'}).get_text(strip=True) + '\n'

    # getting the ingredients
    recipe_string += 'INGREDIENSER: \n' 
    all_ingredients = recipe_soup.find_all('li', {'itemprop': 'recipeIngredient'})
    for ingredient in all_ingredients:
        # compiling amounts and ingredients
        amount = ingredient.find('span', {'class' : 'recipe-ingredients__unit-amount'}).get_text(strip=True)
        item = ingredient.find('span', {'class' : 'recipe-ingredients__ingredient-instruction'}).get_text(strip=True)
        recipe_string += amount + ' ' + item + '\n'

    recipe_string += '\n'
    
    # getting the steps
    recipe_string += 'FREMGANGSMÅDE: \n'
    steps = recipe_soup.find('div', {'itemprop': 'recipeInstructions'})
    all_steps = steps.find_all('li')
    step_num = 1
    for step in all_steps:
        # compiling step number and actual instruction
        instruction = step.get_text(strip=True)
        recipe_string += str(step_num) + ' ' + instruction + '\n'
        step_num += 1

    recipe_string += '\n'

    # appending the compiled recipes to a file
    with open('KillAndDevourDataSet.txt', 'a') as file:
        file.write(recipe_string)

    links_visted += 1

print ('All done')




