import app, waitress

if __name__ == '__main__':
    print('Server starting...')
    waitress.serve(app.app, host='0.0.0.0', port=80)
    print('Shutdown server')