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
        .search-box { display: flex; gap: 10px; margin-bottom: 20px; }
        input { flex: 1; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #1e293b; color: #fff; font-size: 16px; }
        button { padding: 12px 24px; border-radius: 8px; border: none; background: #0284c7; color: white; font-weight: bold; cursor: pointer; }
        button:hover { background: #0369a1; }
        .results { text-align: right; background: #1e293b; padding: 20px; border-radius: 8px; border: 1px solid #334155; }
        .card { padding: 10px; margin-bottom: 10px; background: #0f172a; border-radius: 6px; display: flex; justify-content: space-between; }
        a { color: #38bdf8; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 CYBER-INTEL OSINT</h1>
        <p>ادخلي اسم المستخدم للبحث عنه في المنصات:</p>
        <div class="search-box">
            <input type="text" id="username" placeholder="اكتبي اليوزر هنا...">
            <button onclick="searchUser()">بحث</button>
        </div>
        <div id="results" class="results" style="display:none;"></div>
    </div>

    <script>
        async function searchUser() {
            const username = document.getElementById('username').value;
            const resultsDiv = document.getElementById('results');
            if (!username) return;
            
            resultsDiv.style.display = 'block';
            resultsDiv.innerHTML = '<p>جاري البحث...</p>';
            
            try {
                const res = await fetch(/api/osint/username?q=${username});
                const data = await res.json();
                
                let html = <h3>نتائج البحث عن: ${username}</h3>;
                for (const [platform, info] of Object.entries(data.results)) {
                    html += 
                        <div class="card">
                            <span><strong>${platform}</strong>: ${info.status}</span>
                            <a href="${info.url}" target="_blank">زيارة الرابط 🔗</a>
                        </div>
                    ;
                }
                resultsDiv.innerHTML = html;
            } catch (err) {
                resultsDiv.innerHTML = '<p style="color:#ef4444;">حدث خطأ أثناء البحث</p>';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/osint/username', methods=['GET'])
def check_username():
    username = request.args.get('q', '')
    if not username:
        return jsonify({"error": "يرجى تزويد اسم مستخدم"}), 400
        
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Telegram": f"https://t.me/{username}",
        "X (Twitter)": f"https://x.com/{username}"
    }
    
    results = {}
    for name, url in platforms.items():
        try:
            r = requests.get(url, timeout=3)
            results[name] = {
                "status": "موجود" if r.status_code == 200 else "غير موجود / تعذر التحقق",
                "url": url
            }
        except:
            results[name] = {"status": "خطأ بالفحص", "url": url}
            
    return jsonify({"username": username, "results": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
