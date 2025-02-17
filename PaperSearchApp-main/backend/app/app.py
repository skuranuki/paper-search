import sqlite3
from flask import Flask,render_template,request,redirect,g

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        # データベースをオープンしてFlaskのグローバル変数に保存
        g.db = sqlite3.connect('DB.db')
    return g.db

@app.route('/', methods=["GET","POST"])
def index():
    if request.method=="POST":
        # 選択されたカンファレンス
        conference_name = request.form["conference_name"]
        
        return render_template('result.html', conference_name=conference_name)

    else:
            return render_template('index.html')   


if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)  