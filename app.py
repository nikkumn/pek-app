from flask import Flask, render_template, request
from colorthief import ColorThief
import openai
import os

app = Flask(__name__)

# ✅ 画像から主な色を取得（背景色用）
def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color  # (R, G, B)

# ✅ ChatGPTでキャラの紹介文を生成（モデル切り替え対応！）
def generate_character_intro(filename):
    prompt = f"このキャラクター画像のファイル名「{filename}」から想像して、性格・雰囲気・世界観を200文字以内で紹介してください。"
    openai.api_key = os.environ.get("OPENAI_API_KEY")  # Renderの環境変数から取得
    model_name = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")  # ← モデル切り替え対応！

    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=200
    )
    return response.choices[0].message["content"]

# ✅ トップページ（フォーム）
@app.route('/')
def index():
    return render_template('index.html')

# ✅ アップロード＆生成処理
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "ファイルが送信されていません", 400

    file = request.files['file']
    if file.filename == '':
        return "ファイル名が空です", 400

    filepath = os.path.join('static/uploads', file.filename)
    file.save(filepath)

    # 背景色取得
    bg_color = get_dominant_color(filepath)

    # ChatGPTで紹介文生成
    intro_text = generate_character_intro(file.filename)

    return render_template(
        'result.html',
        filename=file.filename,
        bg_color=bg_color,
        intro_text=intro_text  # 紹介文をテンプレートに渡す！
    )

# ✅ Render対応：ポート指定
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
