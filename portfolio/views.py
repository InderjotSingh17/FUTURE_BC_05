from django.shortcuts import render
from .models import CoinHolding
import requests

def portfolio_view(request):
    holdings = CoinHolding.objects.all()
    enriched_holdings = []
    total_value = 0

    if holdings:
        ids = ','.join([coin.name.lower() for coin in holdings])
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd'

        try:
            response = requests.get(url)
            price_data = response.json()

            for coin in holdings:
                coin_id = coin.name.lower()
                price = price_data.get(coin_id, {}).get('usd', 0)
                value = price * coin.amount
                total_value += value

                enriched_holdings.append({
                    'name': coin.name,
                    'amount': coin.amount,
                    'price': price,
                    'value': value
                })

        except Exception as e:
            print("Error fetching data:", e)

    return render(request, 'portfolio.html', {
        'holdings': enriched_holdings,
        'total_value': total_value
    })
