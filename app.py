from flask import Flask, render_template, request
import requests
import time

app = Flask(__name__)

def get_user_info(sid):
    """Fetch user information from StarMaker API using the provided SID."""
    if not sid.isdigit():
        return {'error': 'Invalid SID', 'message': 'SID must be numeric'}

    url = "https://pay.starmakerstudios.com/rapid/user"
    ts = str(int(time.time()))
    params = {
        'category': '6',
        'id': sid,
        'ts': ts
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://m.starmakerstudios.com',
        'Referer': 'https://m.starmakerstudios.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=0',
        'Te': 'trailers'
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.status_code, 'message': response.text}

@app.route('/', methods=['GET', 'POST'])
def index():
    """Render the main page and handle SID submissions."""
    user_info = None
    error_message = None

    if request.method == 'POST':
        sid = request.form['sid']
        user_info = get_user_info(sid)

        if 'error' in user_info:
            error_message = f"Error {user_info['error']}: {user_info['message']}"
            user_info = None  # Reset user info if there's an error

    return render_template('index.html', user_info=user_info, error_message=error_message)

@app.route('/about')
def about():
    """Render the About page."""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Render the Contact page."""
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
