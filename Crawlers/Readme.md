crawler
---

## 1. description

there are muliple methods to create a web crawler, basically it has two categories

- tools to simulate user interactions, such as selenium
- purt http calls

## 2. selenium

```python
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument('--always-authorize-plugins=true')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-blink-features')
chrome_options.add_argument('--user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"')

chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

webElement = driver.find_element(By.XPATH,"//button[@class='options__load-more' and text()='Load more episodes']")

## get attributes
elementHTML = WebElement.get_attribute('outerHTML')

## get text from webelement
elementText = webElement.text

## convert webelement to to soup
soup = BeautifulSoup(elementHTML, 'html.parser')
## or
soup = BeautifulSoup(webElement.parent.page_source,'html.parser')

## or
soup = BeautifulSoup(driver.page_source,'html.parser')


##get attribute value from soup tag
episode_href=article.find('header',class_='clearfix').find('a')['href']
## get text from soup tag
episode_title=article.find('header',class_='clearfix').find('a').get_text()

```

## 3. load more items

```python
    load_more_element = driver.find_elements(By.XPATH,"//a[@href='#' and text()=' Load more items']")

    while load_more_element:
      try:
          load_more_element = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"//a[@href='#' and text()=' Load more items']")))
          load_more_element.location_once_scrolled_into_view
          driver.execute_script("arguments[0].click();", load_more_element)
      except TimeoutException:
          print(f"Retrieve eposide list of year {year_element.text} finished!")
          load_more_element=''
```

or

```python
for i in range(10):
  load_more_element = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='options__load-more' and text()='Load more episodes']")))
  #load_more_element.location_once_scrolled_into_view
  #https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView
  driver.execute_script("arguments[0].scrollIntoView();", load_more_element)
  driver.execute_script("arguments[0].click();", load_more_element)
  #https://developer.mozilla.org/en-US/docs/Web/API/Document/readyState
  time.sleep(5)
  root_content0= driver.execute_script("return document.getElementsByClassName('podcast-section episode-list')[0]")
  root_content = driver.execute_script("return document.getElementsByClassName('podcast-section episode-list episode-list-infinite')[0]")

```
