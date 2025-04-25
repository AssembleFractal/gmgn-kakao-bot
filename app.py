from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def kakao_webhook():
    req = request.get_json()
    user_msg = req['userRequest']['utterance'].strip().lower()

    if user_msg == "ca":
        gmgn_api = "https://gmgn.network/api/pairs"
        response = requests.get(gmgn_api)
        data = response.json()
        formatted = "\n".join([f"{d['ticker']} - {d['mc']}" for d in data[:5]])

        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {"text": f"🔥 GMGN Ticker & MC\n\n{formatted}"}
                }]
            }
        })

    else:
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {"text": "명령어를 인식하지 못했어요. 'ca'를 입력해보세요."}
                }]
            }
        })

if __name__ == "__main__":
    app.run(debug=True)
