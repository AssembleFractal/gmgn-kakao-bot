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

def get_token_info(contract_address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{contract_address}"
    response = requests.get(url)

    print("💬 Response Status:", response.status_code)
    if response.status_code != 200:
        print("❌ API 요청 실패:", response.text)
        return None, None

    data = response.json().get("pairs")
    if not data:
        print("❌ 해당 주소에 대한 토큰 정보 없음.")
        return None, None

    # 첫 번째 쌍 기준으로 추출
    token_info = data[0].get("baseToken", {})
    symbol = token_info.get("symbol")
    market_cap = data[0].get("fdv")  # Fully Diluted Valuation ≒ 시가총액

    market_cap_formatted = format_market_cap(market_cap)
    return symbol, market_cap_formatted

# 🔍 테스트 예시: JITO (Solana)
contract = "8BtoThi2ZoXnF7QQK1Wjmh2JuBw9FjVvhnGMVZ2vpump"
symbol, mc = get_token_info(contract)

if symbol:
    print(f"✅ Symbol: {symbol}")
    print(f"💰 Market Cap: {mc}")
else:
    print("❌ 토큰 정보 확인 실패")
