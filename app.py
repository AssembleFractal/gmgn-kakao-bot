from flask import Flask, request, jsonify
import requests

app = Flask(__name__)  # ✅ Gunicorn이 찾는 Flask 인스턴스

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

    if response.status_code != 200:
        return None, None, None

    data = response.json().get("pairs")
    if not data:
        return None, None, None

    token_info = data[0].get("baseToken", {})
    symbol = token_info.get("symbol")
    market_cap = format_market_cap(data[0].get("fdv"))
    chart_url = data[0].get("url")
    return symbol, market_cap, chart_url

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    print("🔥 Webhook Body:", body)

    # JSON 구조 방어적 접근
    user_msg = body.get("userRequest", {}).get("utterance", "").strip()

    if user_msg.startswith("ca "):
        contract = user_msg[3:].strip()
        symbol, mc, url = get_token_info(contract)

        if symbol:
            reply = f"💎 {symbol}\n💰 Market Cap: {mc}\n📊 {url}"
        else:
            reply = "❌ 해당 컨트랙트 주소의 정보를 찾을 수 없습니다."
    else:
        reply = "📌 'ca <contract_address>' 형식으로 입력해주세요."

    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": reply
                    }
                }
            ]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Render에서 필요함
