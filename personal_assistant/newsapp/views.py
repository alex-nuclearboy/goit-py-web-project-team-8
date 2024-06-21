from django.shortcuts import render
import requests
import datetime


WEATHER_API_KEY = '7cfac1a5811143f492c163316241906'


def main(request):
    error_message = None
    weather_error_message = None
    city = request.GET.get('city', 'Kyiv')

    try:
        weather_data = fetch_weather(city)
    except ValueError as ve:
        weather_error_message = str(ve)
        weather_data = None
    except requests.RequestException as e:
        weather_error_message = (
            f"An error occurred while fetching weather data: {str(e)}"
        )
        weather_data = None

    exchange_rates = fetch_exchange_rates()

    context = {
        'weather_data': weather_data,
        'exchange_rates': exchange_rates,
        'selected_city': city,
        'error_message': error_message,
        'weather_error_message': weather_error_message
    }
    return render(request, 'newsapp/index.html', context)


def fetch_weather(city):
    url = (
        f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}'
        f'&q={city}'
    )
    response = requests.get(url)
    if response.status_code == 400:
        raise ValueError(f"City '{city}' not found.")
    response.raise_for_status()
    data = response.json()
    return data


def fetch_exchange_rates():
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
