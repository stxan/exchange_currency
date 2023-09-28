from django.shortcuts import render
from xml.etree import ElementTree
import requests
from .models import CurrencyRate
from django.http import JsonResponse

# Настройки API для получения курсов валют. Данные берутся через API ЦБ РФ
API_URL = 'https://cbr.ru/scripts/XML_daily.asp'


def getCurrencyRates():
    try:
        response = requests.get(f'{API_URL}')
        #print(response.text)
        xml_data = response.text
        root = ElementTree.fromstring(xml_data)
        data = {}
        for elem in root:
            for i in range(2, 5):
                key = elem[1].text
                if key not in data:
                    data[key] = []
                data[elem[1].text].append(elem[i].text)
        root = None
        return data
    except Exception as e:
        print(f"Ошибка при получении данных о курсах валют: {e}")
        return None


def updateDatabase(data):
    for key in data:
        currency_code = str(key)
        rate = float(data[key][2].replace(',', '.')) / float(data[key][0].replace(',', '.'))
        currency_name = data[key][1]
        try:
            currency_rate = CurrencyRate.objects.get(currency_code=str(currency_code))
            currency_rate.rate = rate
            currency_rate.currency_name = currency_name
            currency_rate.save()
        except CurrencyRate.DoesNotExist:
            CurrencyRate.objects.create(currency_code=currency_code, rate=rate, currency_name=currency_name)

#Основная функция, которая возвращает отношение валют
def getExchangeRate(from_currency, to_currency):
    if from_currency == to_currency:
        return 1
    if to_currency == "RUB":
        return float((CurrencyRate.objects.get(currency_code = from_currency)).rate)
    if from_currency == "RUB":
        return 1 / float((CurrencyRate.objects.get(currency_code = to_currency)).rate)
    from_rate = float((CurrencyRate.objects.get(currency_code = from_currency)).rate)
    to_rate = float((CurrencyRate.objects.get(currency_code = to_currency)).rate)
    return from_rate / to_rate


def convertCurrency(request):
# Обновляем нашу базу данных
    data = getCurrencyRates()
    updateDatabase(data)
# Обрабатываем запрос
    from_currency = request.GET.get('from')
    to_currency = request.GET.get('to')
    value = float(request.GET.get('value'))
    exchange_rate = getExchangeRate(from_currency, to_currency)
    converted_value = value * exchange_rate

    final_data = {"rate": round(converted_value, 5)}
    return JsonResponse(final_data)

def viewHomePage(request):
    #Обновляем нашу базу данных с текущими котировками согласно ЦБ РФ
    #data = getCurrencyRates()
    #updateDatabase(data)
    return render(request, 'rates/home.html')
