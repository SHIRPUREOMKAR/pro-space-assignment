import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

urls = ["https://www.linkedin.com/in/alisha-barik-4235201a9", "https://www.linkedin.com/in/praveenkishore96", 
        "https://in.linkedin.com/in/praveenkishore96", "https://www.linkedin.com/in/christie-corcoran"]

# ------------------------------------------------------------------------------------------------
def extract_education_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    education_section = soup.find('section', {'data-section': 'educationsDetails'})
    if not education_section:
        return []

    education_list = education_section.find('ul', {'class': 'education__list'})
    if not education_list:
        return []

    education_data = []
    for li in education_list.find_all('li', {'class': 'profile-section-card'}):
        institute_name = li.find('h3').text.strip()
        institute_name = institute_name.replace('\n', ' ')
        degree = li.find('h4').text.strip()
        degree = degree.replace('\n', ' ')
        education_data.append({
            'institute_name': institute_name,
            'degree': degree
        })

    return education_data

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

def extract_current_position_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    current_position_section = soup.find('div', {'data-section': 'currentPositionsDetails'})
    if not current_position_section:
        return 'No current position details found'

    current_position_div = current_position_section.find('div', {'data-test-id': 'top-card-link'})
    current_position_link = current_position_section.find('a', {'data-test-id': 'top-card-link'})

    if current_position_div:
        current_position_text = current_position_div.get_text(separator=' ', strip=True)
    elif current_position_link:
        current_position_text = current_position_link.get_text(separator=' ', strip=True)
    else:
        return 'No current position details found'

    return current_position_text

# ------------------------------------------------------------------------------------------------

for i in range(len(urls)):
    driver = webdriver.Chrome()
    driver.get(urls[i])

    # Wait for the modal to appear
    wait = WebDriverWait(driver, 20)
    modal_close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tracking-control-name="public_profile_contextual-sign-in-modal_modal_dismiss"]')))

    # Click the close button
    modal_close_button.click()

    # Sleep for 20 seconds
    # time.sleep(1)

    # Save the page
    html = driver.page_source
    driver.quit()

    # with open(f"ji{i}.html", "w", encoding='utf-8') as f:
    #     f.write(html)
    #     f.close()
    
    # with open(f"ji{i}.html", "r", encoding='utf-8') as f:
    #     html = f.read()
    #     f.close()
    
    # education_data = extract_education_data(html)
    # print(education_data)
    # about_data = extract_about_data(html)
    # print(about_data)
    # current_position_data = extract_current_position_data(html)
    # print(current_position_data)