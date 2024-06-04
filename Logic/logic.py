import Logic.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class Running(webdriver.Chrome):
    def __init__(self, teardown=False):
        self.teardown = teardown
        super(Running, self).__init__()
        self.implicitly_wait(10)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def SignIn(self):
         try:
             cross_button = self.find_element(By.XPATH, '//button[@data-testid="xMigrationBottomBar"]')
             print("Clicked on the cross button")
             cross_button.click()

             button = self.find_element(By.XPATH, '//a[@data-testid="loginButton"]')
             print("Clicked on the button")
             button.click()

             input_field = self.find_element(By.XPATH, '//input[@autocomplete="username"]')

             input_field.send_keys(const.USERNAME)
             print("Username entered")

             next_button = self.find_element(By.XPATH, '//button[.//span[text()="Next"]]')

             next_button.click()

             password_field = self.find_element(By.XPATH, '//input[@autocomplete="current-password"]')

             password_field.send_keys(const.PASSWORD)
             print("Password Entered")

             logIn_button = self.find_element( By.XPATH, '//button[.//span[text()="Log in"]]')

             logIn_button.click()
             print("Logged In")
         except Exception as e:
            print(f"Error during sign-in: {e}")

    def extract_trending_topics(self):
        try:
            wait = WebDriverWait(self, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Timeline: Trending now']")))

            html_content = self.page_source
            soup = BeautifulSoup(html_content, "html.parser")
            trending_container = soup.find("div", {"aria-label": "Timeline: Trending now"})
            trend_elements = trending_container.find_all("div", {"class": "css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1bymd8e"})

            trending_topics = [element.find("span").get_text().strip() for element in trend_elements if element.find("span")]
            return trending_topics
        except Exception as e:
            print(f"Error extracting trending topics: {e}")
            return []