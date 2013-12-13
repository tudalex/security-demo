from flask import Flask
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
mysql.init_app(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'placinta'
app.config['MYSQL_DATABASE_PASSWORD'] = 'placinta'

@app.route('/')
def hello_world():

    return 'Hello World!'

if __name__ == '__main__':
    app.run()
