# Flask-Firebase
Starter template for a flask hosted website with firebase authentication. 

Works with provider oAuth2 authentication. 

Sign in with Google, Email, Phone/SMS, MFA

Bootstrap 5

Includes Alerting and Toast Notifications

Alerting is triggered by passing the alert variable through Jinja

Toast notifications are triggered with a JS function call


Windows

`python -m venv venv --upgrade-deps`

`venv\Scripts\Activate.ps1`

`python -m pip install -r requirements.txt`


Requires Firebase Environment Variables

`FIREBASE_API_KEY`

`AUTH_DOMAIN`

Flask Secret Key Environment Variable

`SECRET_KEY`
