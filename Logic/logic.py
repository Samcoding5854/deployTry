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

    def extract_trending_topics(self):

        # Wait until the content is loaded
        wait = WebDriverWait(self, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Timeline: Trending now']")))

        # Get the HTML content after it's loaded
        html_content = self.page_source

        # Close the browse

        # Parse the HTML content with BeautifulSoup

        soup = BeautifulSoup(html_content, "html.parser")
        # Find the container containing trending topics
        trending_container = soup.find("div", {"aria-label": "Timeline: Trending now"})

        # Find all elements with role "link" inside the container
            # Find all elements with the specified CSS class
        trend_elements = trending_container.find_all("div", {"class": "css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1bymd8e"})

        # Extract trending topics from the elements
        trending_topics = []
        for element in trend_elements:
            try:
                # Extract topic text
                
                topic_text = element.find("span").get_text().strip()
                trending_topics.append(topic_text)
            except:
                pass


        return trending_topics