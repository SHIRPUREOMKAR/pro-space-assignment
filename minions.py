from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time
import random
import csv

# Gathering data from Google search results using Selenium
# The goal is to get the names, roles, URLs of the LinkedIn profiles of Software Developers

# The search query is: "Software Developers" -intitle:"profiles" -inurl:"dir /" site:linkedin.com/in/ OR site:linkedin.com/pub/
# ------------------------------------------------------------------------------------------------------------------

def write_data_to_csv(name, url, role, education_data, about_data, current_workplace_data):
    with open('./data/data.csv', 'a', encoding='utf-8') as file:
        file.write(f'"{name}", "{url}", "{role}", "{current_workplace_data}", "{education_data}", "{about_data}"\n')

# ------------------------------------------------------------------------------------------------

def extract_education_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    education_section = soup.find('section', {'data-section': 'educationsDetails'})
    if not education_section:
        return ''

    education_list = education_section.find('ul', {'class': 'education__list'})
    if not education_list:
        return ''

    education_data = []
    for li in education_list.find_all('li', {'class': 'profile-section-card'}):
        institute_name = li.find('h3').text.strip()
        institute_name = institute_name.replace('\n', ' ')
        degree = li.find('h4').text.strip()
        degree = degree.replace('\n', ' ')
        education_data.append(f'institute_name: {institute_name} - degree: {degree}')

    return '; '.join(education_data)

# ------------------------------------------------------------------------------------------------

def extract_about_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    about_section = soup.find('section', {'data-section': 'summary'})
    if not about_section:
        return ''

    about_content = about_section.find('div', {'class': 'core-section-container__content'})
    if not about_content:
        return ''

    about_text = about_content.get_text(separator=' ', strip=True)
    return about_text

# ------------------------------------------------------------------------------------------------

def extract_current_workplace_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    current_workplace_section = soup.find('div', {'data-section': 'currentPositionsDetails'})
    if not current_workplace_section:
        return 'No current position details found'

    current_workplace_div = current_workplace_section.find('div', {'data-test-id': 'top-card-link'})
    current_workplace_link = current_workplace_section.find('a', {'data-test-id': 'top-card-link'})

    if current_workplace_div:
        current_workplace_text = current_workplace_div.get_text(separator=' ', strip=True)
    elif current_workplace_link:
        current_workplace_text = current_workplace_link.get_text(separator=' ', strip=True)
    else:
        return 'No current position details found'

    return current_workplace_text

# ------------------------------------------------------------------------------------------------

def get_profile_pages(name, url, role):
    driver = webdriver.Chrome()
    driver.get(url)

    # A modal appears when opened the website. Wait for it to appear and then close it
    wait = WebDriverWait(driver, 20)
    modal_close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tracking-control-name="public_profile_contextual-sign-in-modal_modal_dismiss"]')))
    
    time.sleep(random.randint(1, 3))
    modal_close_button.click()

    # Sleep for 20 seconds
    time.sleep(random.randint(1, 3))

    # Save the page
    html = driver.page_source
    driver.quit()

    time.sleep(3)

    # --------for debug purposes--------
    # with open(f"ji{i}.html", "w", encoding='utf-8') as f:
    #     f.write(html)
    #     f.close()
    
    # --------for debug purposes--------
    # with open(f"ji{i}.html", "r", encoding='utf-8') as f:
    #     html = f.read()
    #     f.close()
    
    education_data = extract_education_data(html)
    # print(education_data)
    about_data = extract_about_data(html)
    # print(about_data)
    current_workplace_data = extract_current_workplace_data(html)
    # print(current_workplace_data)
    write_data_to_csv(name, url, role, education_data, about_data, current_workplace_data)


# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Processing the HTML to extract the data
# Some patterns were observed in the HTML that can be used to extract the data which are described in functions


def main():
    with open('./data/data-small.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    start = int(input('Enter the starting index: '))
    end = int(input('Enter the ending index: '))
    lines = lines[start:end]

    for line in lines:
        name, url, role = line.strip().split(',')
        url = url.strip()  # Strip leading/trailing white spaces
        print(url)
        get_profile_pages(name, url, role)

    print(f'Data extraction complete for index {start} to {end}. Check data.csv for the results.')

if __name__ == "__main__":
    main()