from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # لسماح للواجهة بالاتصال بالسيرفر بدون مشاكل

@app.route('/api/osint/username', methods=['GET'])
def check_username():
    username = request.args.get('q')
    if not username:
        return jsonify({"error": "يرجى تحديد اسم المستخدم"}), 400

    # المنصات المستهدفة للفحص الفعلي
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "X (Twitter)": f"https://x.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Telegram": f"https://t.me/{username}"
    }

    results = {}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5, headers=headers)
            # إذا كان الرمز 200 يعني الحساب موجود، 404 غير موجود
            if response.status_code == 200:
                results[platform] = {"status": "موجود", "url": url}
            else:
                results[platform] = {"status": "غير موجود أو متاح", "url": url}
        except Exception as e:
            results[platform] = {"status": "تعذر الاتصال", "url": url}

    return jsonify({"username": username, "results": results})

if __name__ == ' __main__ ' :
    app.run(host='0.0.0.0', port=5000)
