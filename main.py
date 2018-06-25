from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

import urllib, subprocess, os

class DAScraper:
    def __init__(self, term):
        # Make sure the search term is URL safe
        self.term = urllib.parse.quote(term)

        # Tell the web driver not to display images to speed up the scraping
        # process
        self.options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        self.options.add_experimental_option("prefs",prefs)

        # Create an empty list to act as our download queue
        self.queue = []

        # Set the download counter to 0
        self.downloaded = 0

    def scrape(self, limit=0):
        # Create a web driver with the previously defined options
        driver = webdriver.Chrome(chrome_options=self.options)

        # Open the DevientArt home page so that the cookies can be loaded
        driver.get('https:deviantart.com')

        # Load the cookies from file and load them to the web driver
        try:
            with open('cookies.pkl', 'rb') as cookies_file:
                cookies = pickle.load(cookies_file)
                for cookie in cookies:
                    driver.add_cookie(cookie)
        except IOError:
            pass

        # Set the search URL and web driver wait time and then load the URL
        # TODO: Implement the various search terms on DevientArt such as
        # Newest and Undiscovered
        url = 'https://www.deviantart.com/?q=' + self.term
        wait = WebDriverWait(driver, 0.5)
        driver.get(url)

        # Gather all search results
        result_urls = []
        while len(result_urls) < limit or limit == 0:
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='torpedo-end-of-results visible']")))
                results = driver.find_elements(By.XPATH, "//a[@class='torpedo-thumb-link']")
                for result in results:
                    try:
                        result_url = result.get_attribute('href')
                    except StaleElementReferenceException:
                        continue
                    if result_url not in result_urls:
                        result_urls.append(result_url)
                break
            except TimeoutException:
                results = driver.find_elements(By.XPATH, "//a[@class='torpedo-thumb-link']")
                for result in results:
                    result_url = result.get_attribute('href')
                    if result_url not in result_urls:
                        result_urls.append(result_url)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        print('Found', len(result_urls), 'results.')

        # Open the page of each result and add the download link to the queue
        for result_url in result_urls:
            try:
                driver.get(result_url)
                image = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dev-view-deviation']/img")))
                download_url = image.get_attribute('src')
                self.queue.append(download_url)
            except TimeoutException:
                continue

        # Close the driver
        driver.close()

    def download(self):
        for url in self.queue:
            subprocess.call(['curl', '-O', '-g', '-s', '--url', url])
            self.downloaded += 1

if __name__ == '__main__':
    term = input('Search Term: ')
    try:
        path = os.path.join('downloads', term)
        os.makedirs(path)
    except IOError:
        pass
    os.chdir(path)
    scraper = DAScraper(term)
    try:
        scraper.scrape()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            scraper.download()
        except KeyboardInterrupt:
            pass
        print(scraper.queue)
