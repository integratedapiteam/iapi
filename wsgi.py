#from app import app

#if __name__ == '__main__':
#    app.run(port=5000, host="0.0.0.0", debug=False,
#            ssl_context=('/etc/letsencrypt/live/i-api.co.kr/fullchain.pem',
#                         '/etc/letsencrypt/live/i-api.co.kr/privkey.pem'))

from app import app 

if __name__ == "__main__": 
    app.run()
