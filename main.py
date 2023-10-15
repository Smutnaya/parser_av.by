import asyncio

from parser import parsing
import time
from selenium import webdriver


async def main():
    driver = webdriver.Firefox()
    time.sleep(2)
    url = 'https://cars.av.by'
    await parsing(url, driver)

    time.sleep(3)
    driver.quit()


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end-start)