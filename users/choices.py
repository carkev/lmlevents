"""Choices module.
"""
from operator import itemgetter
import pycountry

country_list = sorted(
    [(country.name, country.name) for country in list(pycountry.countries)],
    key=itemgetter(0))

country_list.insert(0, ("*Select Country", "*Select Country"))

COUNTRIES = country_list
