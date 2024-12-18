import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

def get_currency_rates_for_week():
    url = 'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20241209&end=20241215&valcode=usd&sort=exchangedate&order=asc'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.content)
            dates, rates = [], []

            for currency in root.findall('currency'):
                date = currency.find('exchangedate').text
                rate = float(currency.find('rate').text)
                dates.append(datetime.strptime(date, '%d.%m.%Y'))
                rates.append(rate)

            return dates, rates
        except ET.ParseError:
            print("Не вдалося розібрати XML-відповідь.")
            return None, None
    else:
        print(f"Помилка. Код статусу {response.status_code}.")
        return None, None

def print_currency_rates():
    dates, rates = get_currency_rates_for_week()

    if dates and rates:
        print("Курс долара США в період з 09.12.2024 по 15.12.2024:")
        for date, rate in zip(dates, rates):
            print(f"Дата: {date.strftime('%d.%m.%Y')}, Курс: {rate:.4f}")

def plot_currency_rate():
    dates, rates = get_currency_rates_for_week()

    if dates and rates:
        plt.figure(figsize=(10, 6))
        plt.plot(dates, rates, marker='o', label='Курс USD')

        for i, rate in enumerate(rates):
            plt.annotate(f'{rate:.4f}', (dates[i], rates[i]), textcoords="offset points", xytext=(0, 5), ha='center')

        plt.title('Курс долара США в період з 09.12.2024 по 15.12.2024')
        plt.xlabel('Дата')
        plt.ylabel('Курс (UAH)')
        plt.grid(True, alpha=1)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

print_currency_rates()
plot_currency_rate()