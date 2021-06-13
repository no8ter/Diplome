How to start server
=
To run the flask web server, you need to:
 * Create a python virtual environment with the command: <b> python -m venv venv </b>
 * At the command prompt start the virtual environment: <b> venv\Scripts\activate </b>
 * Install the necessary dependencies from the file requirements.txt: <b> pip install -r requirements.txt </b>
 * If you want to run a local server, just run wsgi.py: <b> python wsgi.py </b>
 * If you want the server to be visible globally, then specify the address 0.0.0.0 at startup: <b> python wsgi.py 0.0.0.0 </b>
 <i> When you start a server with global visibility, you need to open port 80 in your router for the machine that is running Flask </i>
