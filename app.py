from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CYBER-INTEL | أداة البحث</title>
    <style>
        body { font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; padding: 20px; }
        .container { max-width: 600px; width: 100%; text-align: center; margin-top: 40px; }
        h1 { color: #38bdf8; }
        form { display: flex; gap: 10px; margin-bottom: 20px; }
        input { flex: 1; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #1e293b; color: #fff; font-size: 16px; }
        button { padding: 12px 24px; border-radius: 8px; border: none; background: #0284c7; color: white; font-weight: bold; cursor: pointer; }
        button:hover { background: #0369a1; }
        .results { text-align: right; background: #1e293b; padding: 20px; border-radius: 8px; border: 1px solid #334155; margin-top: 20px; }
        .card { padding: 12px; margin-bottom: 10px; background: #0f172a; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #334155; }
        a { color: #38bdf8; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 CYBER-INTEL OSINT</h1>
        <p>ادخلي اسم المستخدم للبحث عنه في المنصات:</p>
        
        <form method="GET" action="/">
            <input type="text" name="q" value="{{ username }}" placeholder="اكتبي اليوزر هنا..." required>
            <button type="submit">بحث</button>
        </form>

        {% if results %}
        <div class="results">
            <h3>نتائج البحث عن: {{ username }}</h3>
            {% for platform, info in results.items() %}
                <div class="card">
                    <span><strong>{{ platform }}</strong>: 
                        {% if "موجود" in info.status %}
                            <span style="color: #4ade80;">{{ info.status }}</span>
                        {% else %}
                            <span style="color: #f87171;">{{ info.status }}</span>
                        {% endif %}
                    </span>
                    <a href="{{ info.url }}" target="_blank">زيارة الرابط 🔗</a>
                </div>
            {% endfor %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    username = request.args.get('q', '').strip()
    results = {}
    
    if username:
        platforms = {
            "GitHub": f"https://github.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "Telegram": f"https://t.me/{username}",
            "X (Twitter)": f"https://x.com/{username}"
        }
        
        for name, url in platforms.items():
            try:
                r = requests.get(url, timeout=3, headers={"User-Agent": "Mozilla/5.0"})
                # ملاحظة: بعض المواقع مثل انستجرام وتويتر تحجب الطلبات البسيطة، لكن جيت هوب وتليجرام يستجيبون بدقة
                results[name] = {
                    "status": "موجود 🟢" if r.status_code == 200 else "غير موجود / محجوب 🔴",
                    "url": url
                }
            except:
                results[name] = {"status": "تعذر التحقق", "url": url}
                
    return render_template_string(HTML_TEMPLATE, results=results, username=username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
