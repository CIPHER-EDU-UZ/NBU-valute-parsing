import requests

def fetch_exchange_rates():
    url = 'https://nbu.uz/uz/exchange-rates/json/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return None

def display_currency_names(data):
    if data:
        currency_names = [currency['title'] for currency in data]
        print("Available currencies:")
        for idx, name in enumerate(currency_names, 1):
            print(f"{idx}. {name}")
        return currency_names
    return []

def check_null_data(data):
    print("Null data entries:")
    for currency in data:
        null_fields = [key for key, value in currency.items() if value is None]
        if null_fields:
            print(f"{currency['title']} - Null fields: {', '.join(null_fields)}")

def convert_to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def compare_currencies(data, currency_names, from_currency_idx, to_currency_idx):
    if data and from_currency_idx <= len(currency_names) and to_currency_idx <= len(currency_names):
        from_currency = data[from_currency_idx - 1]
        to_currency = data[to_currency_idx - 1]

        buy_exchange_rate = None
        sell_exchange_rate = None

        from_buy = convert_to_float(from_currency.get('nbu_buy_price'))
        to_buy = convert_to_float(to_currency.get('nbu_buy_price'))
        if from_buy and to_buy:
            buy_exchange_rate = to_buy / from_buy
            print(f"1 {from_currency['code']} = {buy_exchange_rate} {to_currency['code']} (NBU Buy Price)")
        else:
            print(f"Xarid kursini hisoblab bo'lmadi, chunki ma'lumotlar etishmayotgani aniq yoki raqamli bo'lmagan ichi bo'sh{from_currency['title']} or {to_currency['title']}")

        from_sell = convert_to_float(from_currency.get('nbu_sell_price'))
        to_sell = convert_to_float(to_currency.get('nbu_sell_price'))
        if from_sell and to_sell:
            sell_exchange_rate = to_sell / from_sell
            print(f"1 {from_currency['code']} = {sell_exchange_rate} {to_currency['code']} (NBU Sell Price)")
        else:
            print(f"Sotish kursini hisoblab bo'lmadi, chunki ma'lumotlar etishmayotgani aniq yoki raqamli bo'lmagan ichi bo'sh {from_currency['title']} or {to_currency['title']}")
    else:
        print("Yaroqsiz valyuta indekslari")

def main():
    exchange_data = fetch_exchange_rates()
    if exchange_data:
        currency_names = display_currency_names(exchange_data)
        if currency_names:
            check_null_data(exchange_data)
            from_currency_idx = int(input("kerakli valyuta indeksini kiriting: "))
            to_currency_idx = int(input("Keyingi valyutasi indeksini kiriting: "))
            compare_currencies(exchange_data, currency_names, from_currency_idx, to_currency_idx)

if __name__ == "__main__":
    main()
