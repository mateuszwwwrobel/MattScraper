import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from . import models
import itertools
from urllib.parse import quote_plus

BASE_EBAY_URL = 'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={}&_sacat=0&LH_BIN=1&_sop=10'
BASE_IMAGE_URL = 'https://i.ebayimg.com/{}/s-l225.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_EBAY_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
   

    post_listings = soup.find_all('li', {"class": "s-item"})
    
    final_postings = []
 

    for post in post_listings:
        try:
            post_title = post.find('img', {'class': 's-item__image-img'})['alt']
            post_image = post.find('img', {'class': 's-item__image-img'})['src']
            post_href = post.find('a', {'class': 's-item__link'})['href']
            post_price = post.find('span',{'class': 's-item__price'}).text
        except:
            continue
        

        final_postings.append((post_title, post_image, post_href, post_price))


    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)
        
