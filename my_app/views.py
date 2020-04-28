import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from . import models
import itertools

BASE_CRAIGSLIST_URL = 'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={}&_sacat=0&LH_BIN=1&_sop=10'
BASE_IMAGE_URL = 'https://i.ebayimg.com/{}/s-l225.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format((search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    post_listings = soup.find_all('li', {"class": "sresult"})
    #print(post_listings)
    final_postings = []

    for post in post_listings:
        post_title = post.find(('h3', {'class': 'lvtitle'})).text
        post_url = post.find(('a', {'class': 'vip'})).get('href')
        post_price = post.find('li', {'class': 'lvprice'}).text

        img_items = post.find('img').get('imgurl')

        image_list = []

        if img_items is not None:
            image_list.append(img_items)
        else:
            continue
        

        post_image_link = str(image_list)
        post_image_id = post_image_link.split('com/')[1].split('/s')[0]
        post_image_url = BASE_IMAGE_URL.format(post_image_id)



        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)
        
