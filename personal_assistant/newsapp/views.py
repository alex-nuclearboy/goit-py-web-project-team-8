from django.shortcuts import render
import requests
import datetime

from .translations import translations

WEATHER_API_KEY = '681232aad95a86f210ad402860d90308'


def get_language(request):
    """
    Get the language from the request or session.
    - Retrieves the language from the GET parameters or session.
    - Defaults to English if no language is found.
    - Stores the language in the session.
    """
    language = request.GET.get('lang')
    if not language:
        language = request.session.get('language', 'en')
    request.session['language'] = language
    return language


def main(request):
    """
    Main view function to display the weather and exchange rates.
    - Retrieves the language from the session.
    - Loads the translations based on the language.
    - Fetches the weather and exchange rates data.
    - Handles errors and displays appropriate messages.
    """
    language = get_language(request)
    trans = translations.get(language, translations['en'])

    error_message = None
    weather_error_message = None
    default_city = 'Kyiv' if language == 'en' else 'Київ'
    city = request.GET.get('city', default_city)

    try:
        weather_data = fetch_weather(city, trans, language)
    except ValueError as ve:
        weather_error_message = str(ve)
        weather_data = None
    except requests.RequestException as e:
        weather_error_message = (
            trans['error_fetching_weather'] % {'error': str(e)}
        )
        weather_data = None

    exchange_rates = fetch_exchange_rates()

    context = {
        'translations': trans,
        'weather_data': weather_data,
        'exchange_rates': exchange_rates,
        'selected_city': city,
        'error_message': error_message,
        'weather_error_message': weather_error_message
    }
    return render(request, 'newsapp/index.html', context)


def fetch_weather(city, trans, language):
    """
    Fetch weather data from OpenWeatherMap API.
    - Retrieves weather data for the specified city.
    - Uses the language parameter to get the data in the desired language.
    - Raises a ValueError if the city is not found.
    """
    url = (
        f'https://api.openweathermap.org/data/2.5/weather?q={city}'
        f'&APPID={WEATHER_API_KEY}&units=metric&lang={language}'
    )
    response = requests.get(url)
    if response.status_code == 401:
        raise ValueError(
            trans['error_fetching_weather'] % {'error': 'Invalid API key'}
        )
    if response.status_code == 404:
        raise ValueError(trans['city_not_found'] % {'city': city})
    response.raise_for_status()
    data = response.json()
    return data


def fetch_exchange_rates():
    """
    Fetch exchange rates data from PrivatBank API.
    - Retrieves the exchange rates for the required currencies.
    """
    today = datetime.datetime.today().strftime('%d.%m.%Y')
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={today}'
    response = requests.get(url)
    data = response.json()
    required_currencies = ['USD', 'EUR', 'GBP', 'CHF', 'PLN']

    exchange_rates = [
        rate for rate in data['exchangeRate']
        if rate['currency'] in required_currencies
    ]
    exchange_rates.sort(key=lambda x: required_currencies.index(x['currency']))
    return exchange_rates
