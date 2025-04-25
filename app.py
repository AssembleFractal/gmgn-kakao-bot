import requests

def format_market_cap(value):
    if value is None:
        return "N/A"
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.1f}K"
    else:
        return f"{value:.1f}"

def get_token_info(contract_address, api_key):
    url = f"https://public-api.birdeye.so/public/token/{contract_address}"

    headers = {
        "x-chain": "solana",
        "X-API-KEY": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json().get("data", {})
        symbol = data.get("symbol")
        market_cap = data.get("market_cap")
        market_cap_formatted = format_market_cap(market_cap)
        return symbol, market_cap_formatted
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, None

# 예시 사용
api_key = "여기에_너의_API_KEY_입력"
contract = "9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E"  # soBTC
symbol, mc = get_token_info(contract, api_key)

print(f"Symbol: {symbol}")
print(f"Market Cap: {mc}")
