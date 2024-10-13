from flask import Flask, redirect, request, session, url_for
import tweepy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Eine beliebige Geheimnisvariable für Sitzungen

# Twitter API-Schlüssel
consumer_key = "DEIN_CONSUMER_KEY"
consumer_secret = "DEIN_CONSUMER_SECRET"

# Route zum Starten des OAuth-Prozesses
@app.route('/login')
def login():
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, callback='https://steuernkompakt.com/callback')
    try:
        redirect_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token  # Speichere den Token in der Sitzung
        return redirect(redirect_url)
    except tweepy.TweepyException:  # Ändere hier TweepError zu TweepyException
        return "Fehler beim Abrufen der Autorisierungs-URL"

# Callback-Route, nachdem der Benutzer die Authentifizierung abgeschlossen hat
@app.route('/callback')
def callback():
    request_token = session.get('request_token')
    session.pop('request_token', None)  # Entferne den temporären Token

    # OAuth-Verifizierungscode abrufen
    oauth_verifier = request.args.get('oauth_verifier')
    
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, request_token['oauth_token'], request_token['oauth_token_secret'])
    try:
        auth.get_access_token(oauth_verifier)
        
        # Speichere Access Token und Secret in der Sitzung
        session['access_token'] = auth.access_token
        session['access_token_secret'] = auth.access_token_secret
        
        return "Authentifizierung erfolgreich! Du kannst jetzt Tweets löschen."
    except tweepy.TweepyException:  # Ändere hier TweepError zu TweepyException
        return "Fehler beim Abrufen des Access Tokens"
