from parser import parsing
import time
from selenium import webdriver


def main():
    driver = webdriver.Firefox()
    time.sleep(2)
    url = 'https://cars.av.by'
    parsing(url, driver)

    time.sleep(3)
    driver.quit()


if __name__ == '__main__':
    main()
