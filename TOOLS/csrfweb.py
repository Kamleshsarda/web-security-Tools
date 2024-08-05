from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users = {'user1': 'password1'}
balances = {'user1': 1000}

@app.route('/')
def home():
    return render_template_string('''
        <h1>Welcome to the Bank</h1>
        <a href="{{ url_for('login') }}">Login</a>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('account', username=username))
        else:
            return 'Invalid credentials'
    return render_template_string('''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/account/<username>', methods=['GET', 'POST'])
def account(username):
    if request.method == 'POST':
        amount = int(request.form['amount'])
        balances[username] -= amount
        return f'Transferred {amount} dollars. New balance: {balances[username]}'
    return render_template_string('''
        <h1>{{ username }}'s Account</h1>
        <p>Balance: {{ balances[username] }}</p>
        <form method="post">
            Transfer amount: <input type="number" name="amount"><br>
            <input type="submit" value="Transfer">
        </form>
    ''', username=username, balances=balances)

if __name__ == '__main__':
    app.run(debug=True)
