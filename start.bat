

IF NOT EXIST "venv\Scripts\pip.exe" (
	python -m venv venv 
	"venv\Scripts\pip" install -r requirements.txt
) ELSE (
	echo venv exists already.
)

"venv\Scripts\python.exe" wsgi.py 0.0.0.0
exit
