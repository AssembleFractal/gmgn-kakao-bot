from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def kakao_webhook():
    try:
        req = request.get_json()
        user_input = req['userRequest']['utterance'].strip()

        # GMGN API 호출
        gmgn_api = "https://gmgn.network/api/pairs"
        response = requests.get(gmgn_api)
        data = response.json()

        # 입력값이 address랑 매칭되는 토큰 찾기
        matched = next((d for d in data if d.get("ca", "").lower() == user_input.lower()), None)

        if matched:
            text = f"{matched['ticker']} - {matched['mc']}"
        else:
            text = f"해당 CA에 해당하는 토큰을 찾을 수 없습니다.\n입력값: {user_input}"

        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {"text": text}
                }]
            }
        })

    except Exception as e:
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": f"[오류] 서버 처리 중 문제가 발생했습니다.\n{str(e)}"
                    }
                }]
            }
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
