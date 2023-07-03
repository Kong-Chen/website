from flask import Flask, render_template, request
from flask import redirect, url_for
import psycopg2

app = Flask(__name__)

# 建立資料庫連線
conn = psycopg2.connect(
    host="dpg-ci01rn33cv20nhqqkd50-a.oregon-postgres.render.com",
    port="5432",
    database="linebot_trm4",
    user="kong",
        password="kmJreG7MV3OY8NYcVn9tNYHK3HhzCWBh"
)
cursor = conn.cursor()

# 建立使用者資訊表格
#cursor.execute(" CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY,username VARCHAR(255) NOT NULL,password VARCHAR(255) NOT NULL)")
#conn.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        # 檢查帳號是否重複
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return render_template('register.html', error_message='帳號已被使用')

        # 檢查密碼長度
        if len(password) < 6:
            return render_template('register.html', error_message='密碼長度需至少為6個字元')

        # 將使用者資訊插入資料庫
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()

        # 假設註冊成功，顯示成功訊息
        return render_template('success.html', username=username)

    # 如果是 GET 請求，則顯示註冊表單
    return render_template('register.html')


@app.route('/users', methods=['GET'])
def users():
    # 取得所有使用者
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    return render_template('users.html', users=users)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
