import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from . import models

BASE_CRAIGSLIST_URL = 'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={}&_sacat=0&LH_BIN=1&_sop=10'
BASE_IMAGE_URL = 'https://www.globalinnovationforum.com/wp-content/uploads/2014/03/ebay-logo.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format((search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='lxml')

#    post_listings = soup.find_all('li.lvprice', 'h3.lvtitle',)

    final_postings = []

    for titles in soup.select("h3.lvtitle"):
        post_title = titles.find('a')['title'].split('access ')[1]
        post_url = titles.find('a').get('href')
        post_image_url = BASE_IMAGE_URL

        for prices in soup.select('li.lvprice'):
            post_price = prices.find('span').text



        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)
