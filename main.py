import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

class PrivatBankAPI:
    API_URL = "https://api.privatbank.ua/p24api/exchange_rates"

    async def get_exchange_rates(self, date: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.API_URL}?json&date={date}") as response:
                if response.status != 200:
                    raise Exception(f"Error fetching data: {response.status}")
                data = await response.json()
                return data

class CurrencyConverter:
    @staticmethod
    def convert_to_usd(rate: float, amount: float):
        return amount / rate

    @staticmethod
    def convert_to_eur(rate: float, amount: float):
        return amount * rate

async def fetch_currency_rates(days: int):
    try:
        if days < 1 or days > 10:
            print("Кількість днів повинна бути від 1 до 10.")
            return

        api = PrivatBankAPI()
        rates_data = []
        today = datetime.now()
        for i in range(days):
            date = (today - timedelta(days=i)).strftime("%d.%m.%Y")
            data = await api.get_exchange_rates(date)
            exchange_rates = data.get('exchangeRate')
            usd_rate = next((rate for rate in exchange_rates if rate['currency'] == 'USD'), None)
            eur_rate = next((rate for rate in exchange_rates if rate['currency'] == 'EUR'), None)
            rates = {
                date: {
                    'EUR': {
                        'sale': eur_rate['saleRateNB'],
                        'purchase': eur_rate['purchaseRateNB']
                    },
                    'USD': {
                        'sale': usd_rate['saleRateNB'],
                        'purchase': usd_rate['purchaseRateNB']
                    }
                }
            }
            rates_data.append(rates)

        print(rates_data)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <days>")
        sys.exit(1)

    try:
        days = int(sys.argv[1])
        asyncio.run(fetch_currency_rates(days))
    except ValueError:
        print("Days must be an integer.")
        sys.exit(1)