

import bs4, requests

#the following

dan_selector_1 = '#stream-item-tweet-952606539432505344 > div.tweet.js-stream-tweet.js-actionable-tweet.js-profile-popup-actionable.dismissible-content.original-tweet.js-original-tweet > div.content > div.js-tweet-text-container > p'
dan_selector_2 = '#stream-item-tweet-952304907582918657 > div.tweet.js-stream-tweet.js-actionable-tweet.js-profile-popup-actionable.dismissible-content.original-tweet.js-original-tweet > div.content > div.js-tweet-text-container > p'
dan_url = 'https://twitter.com/delers447'

brandon_url = 'https://twitter.com/brandonsavage'
brandon_selector_1 = '#stream-item-tweet-952672415179358208 > div.tweet.js-stream-tweet.js-actionable-tweet.js-profile-popup-actionable.dismissible-content.original-tweet.js-original-tweet > div.content > div.js-tweet-text-container > p'
brandon_selector_2 = '#stream-item-tweet-952614847652466689 > div.tweet.js-stream-tweet.js-actionable-tweet.js-profile-popup-actionable.dismissible-content.original-tweet.js-original-tweet > div.content > div.js-tweet-text-container > p'

hundred_days_url = 'https://twitter.com/hashtag/100daysofcode?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Ehashtag'

def scrap_something(url, selector):
    res = requests.get(url)
    res.raise_for_status()
    soup_item = bs4.BeautifulSoup(res.text, 'html.parser')
    elements = soup_item.select(selector)
    print(elements[0].text)

#scrap_something(dan_url, dan_selector_1)
#scrap_something(dan_url, dan_selector_2)
#scrap_something(brandon_url, brandon_selector_1)
#scrap_something(brandon_url, brandon_selector_2)

def print_tweets_from_url(url):
    res = requests.get(url)
    res.raise_for_status()
    soup_item = bs4.BeautifulSoup(res.text, 'html.parser')
    elements = soup_item.find_all(class_='js-tweet-text-container')
    #elements = soup_item.find_all('div', class_='js-tweet-text-container')
    print(len(elements))
    for tweet in elements:
        print(tweet.text)

print_tweets_from_url(dan_url)
print_tweets_from_url(hundred_days_url)
