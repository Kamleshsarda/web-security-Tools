from flask import Flask, request, render_template_string, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'your_secret_key'
csrf = CSRFProtect(app)

users = {'user1': 'password1'}
balances = {'user1': 1000}

class TransferForm(FlaskForm):
    amount = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Transfer')

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
            return redirect(url_for('account'))
        else:
            return 'Invalid credentials'
    return render_template_string('''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/account', methods=['GET', 'POST'])
def account():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    
    form = TransferForm()
    if form.validate_on_submit():
        amount = form.amount.data
        balances[username] -= amount
        return f'Transferred {amount} dollars. New balance: {balances[username]}'
    return render_template_string('''
        <h1>{{ username }}'s Account</h1>
        <p>Balance: {{ balances[username] }}</p>
        <form method="post">
            {{ form.hidden_tag() }}
            Transfer amount: {{ form.amount }}<br>
            {{ form.submit }}
        </form>
    ''', username=username, balances=balances, form=form)

if __name__ == '__main__':
    app.run(debug=True)
