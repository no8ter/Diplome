import app, waitress, sys

if __name__ == '__main__':
    print('Server starting...')
    if len(sys.argv) > 1:
        waitress.serve(app.app, host=sys.argv[1], port=80)
    else:
        waitress.serve(app.app, host='localhost', port=80)
    print('Shutdown server')