from os import error
from flask import Flask, render_template, request, redirect, url_for
from flask.globals import session
import sqlite3
import datetime
import pytils
import random
import string


app = Flask(__name__)
app.debug = True

# database
# db = sqlite3.connect('database.db')
# cur = db.cursor()
# /database

# utilities

def _c(f):
    r = []
    for i in f:
        r.append(i)
    return r

def auth_request():
    '''
    Проверка авторизованности пользователя в текущей сессии
    '''
    if 'userID' in session:
        sql = f"SELECT COUNT(1) FROM `users` WHERE `rowid` = '{session.get('userID')}';"
        db = sqlite3.connect('database.db')
        cur = db.cursor()
        temp = _c(cur.execute(sql))
        if temp[0][0] == 1:
            return True
        else:
            return False
    else:
        return False

def _genRandomString(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def _unicLoginCheck(login):
    db=sqlite3.connect('database.db')
    c = db.cursor()
    req = _c(c.execute(f"select count(1) from `users` where `login` like '{login}'; "))[0][0]
    if req != 0:
        return False
    else:
        return True

def genNewUserLoginPass(secondname):
    login = pytils.translit.translify(secondname)
    password = _genRandomString(8)
    if _unicLoginCheck(login):
        return {'login':login, 'password':password}
    else:
        last = secondname[len(secondname)-1:len(secondname)]
        if last != '1':
            return genNewUserLoginPass(secondname+'1')
        else:
            num = int( secondname[len(secondname)-1:len(secondname)] )+1
            return(genNewUserLoginPass(secondname[:-1]+str(num)))

def _prepared(s):
    return s.strip().replace("'", '').replace("`", '').replace(" ", '')

def saveFormData(form):
    lp = genNewUserLoginPass(form.get('secondname'))
    abLogin = lp['login']
    abPass = lp['password']
    sqlAbiturient = f"""
        INSERT INTO `users`
        VALUES(
            '{abLogin}',
            '{abPass}',
            '{form.get('firstname')}',
            '{form.get('secondname')}',
            '{form.get('tridname')}',
            '{form.get('birthday')}',
            '{form.get('birthplace')}',
            '{form.get('country')}',
            '{_prepared(form.get('passID'))}',
            '{form.get('passDate')}',
            '{form.get('passCountry')}',
            '{form.get('schoolName')}',
            '{form.get('schoolDate')}',
            '{form.get('schoolAttestate')}',
            '{form.get('passLivePlace')}',
            '{form.get('currentLivePlace')}',
            '{form.get('phoneNumber')}',
            '{form.get('сommissariat')}',
            '{form.get('secondLanguage')}',
            '{form.get('medicalGroup')}',
            '{form.get('needHostelSelect')}',
            '{form.get('motherName')}',
            '{form.get('motherPhone')}',
            '{form.get('fatherName')}',
            '{form.get('fatherPhone')}',
            'Абитуриент',
            ''
        );
    """
    sqlClaim = f"""
        INSERT INTO `claims`
        VALUES(
            (SELECT MAX(rowid) FROM `users`),
            {form.get('specialitySelect')},
            True, True, True, True
        );
    """
    try:
        db = sqlite3.connect('database.db')
        c = db.cursor()
        sql = f'''
            select count(1) from `users` where `passID` like '{form.get('passID')}';
        '''
        temp = _c(c.execute(sql))[0][0]
        if temp != 0:
            raise ValueError('Абитуриент с такими данными уже существует')

        c.execute(sqlAbiturient)
        c.execute(sqlClaim)
        db.commit()
    except Exception as e:
        return e, abLogin, abPass
    else:
        return 0, abLogin, abPass

def loginPassCheck(l, p):
    username = l
    password = p
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    sql = f'''select rowid, firstName, statement, info from `users` where login = '{username}' and password = '{password}';'''
    temp = _c(cur.execute(sql))
    return temp

# /utilities


# renders
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        temp = loginPassCheck(username, password)
        
        
        if len(temp) > 0:
            session['userID'] = temp[0][0]
            session['userName'] = temp[0][1]
            session['userState'] = temp[0][2]
            session['userInfo'] = temp[0][3]
            if temp[0][2] == 'administrator':
                return redirect(url_for('cabinet'))
            else:
                return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Wrong login or password')
            
    else:
        return render_template('login.html')

@app.route('/cabinet')
def cabinet():
    if auth_request():
        return render_template('cabinet.html', username=session.get('userName'), state=session.get('userState'))
    else:
        return redirect(url_for('login'))
    
@app.route('/claim', methods=['post', 'get'])
def claim():
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    species = _c(cur.execute("SELECT rowid, `name` FROM `profs` ORDER BY `spec_id`;"))
    if request.method == 'POST':
        check, log, pas = saveFormData(request.form)
        if check == 0:
            temp = loginPassCheck(log, pas)
            session['userID'] = temp[0][0]
            session['userName'] = temp[0][1]
            session['userState'] = temp[0][2]
            session['userInfo'] = temp[0][3]
            return redirect(url_for('claim_success'))
        else:
            return render_template('claim.html', error=check, species=species)
    else:
        return render_template('claim.html', species=species)

@app.route('/claim_success')
def claim_success():
    if auth_request():
        return render_template('claim_success.html')
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if auth_request():
        un = session.get('userName')
        st = session.get('userState')
        
        return render_template('profile.html', username=un, state=st)
    else:
        return redirect(url_for('login'))

@app.route('/ratings')
def ratings():
    return render_template('ratings.html')

@app.route('/professions')
def professions():
    return render_template('professions.html')

@app.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
# /renders


# settings
app.permanent_session_lifetime = datetime.timedelta(hours=1)
app.secret_key = '807607a394f4a04c54db47745d738a3821c5431118346077b904642a58bc9031512bcb40b183657a2b91f84e5083aa69c0061f502f1aad24c6da8972dca338c1'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
    
