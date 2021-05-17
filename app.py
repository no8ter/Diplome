import datetime
import random
import sqlite3
import string
import os
from flask.helpers import send_from_directory

import pytils
from flask import Flask, redirect, render_template, request, url_for
from flask.globals import session
from flask_bcrypt import Bcrypt

from config import *

app = Flask(__name__)
bcrypt = Bcrypt(app)

# settings
app.debug = True
app.permanent_session_lifetime = datetime.timedelta(hours=1)
app.secret_key = SECURE_KEY

# legacy

# import pdfkit


# def HTMLtoPDF(way: str = "<html><head></head><body><b>Hello, world!</b></body></html>", endname: str = "out.pdf", path_wkhtmltopdf: str = r'\static\wkhtmltopdf\bin\wkhtmltopdf.exe'):
#     '''
#     Преобразование HTML-строки в PDF
#     '''
#     config = pdfkit.configuration(wkhtmltopdf=os.getcwd()+path_wkhtmltopdf)
#     pdfkit.from_string(way, endname, configuration=config)

# /legacy

# utilities


def _c(f) -> list:
    '''
    Конвертация результата запроса в массив
    '''
    r = []
    for i in f:
        r.append(i)
    return r

def req(sql: str, needCommit: bool = True) -> list:
    '''
    Обработка SQL запроса с возвращением результата и автокоммитом
    '''
    db = sqlite3.connect(DATABASE_WAY)
    c = db.cursor()
    if ';' in sql:
        temp = c.executescript(sql)
    else:
        temp = c.execute(sql)
    if needCommit:
        db.commit()
    return _c(temp)


def auth_request() -> bool:
    '''
    Проверка авторизованности пользователя в текущей сессии
    '''
    if 'userID' in session:
        sql = f"SELECT COUNT(1) FROM `users` WHERE `rowid` = '{session.get('userID')}'"
        temp = req(sql)
        if temp[0][0] == 1:
            return True
        else:
            return False
    else:
        return False


def renderDocxTemplate(userLogin:str):
    '''
    Заполнение шаблонного заявление о конкретном пользователе
    '''
    from docxtpl import DocxTemplate
    from docx2pdf import convert
    def _check(a):
        return '' if a == None else a
    def _cHealth(a):
        if a == 'main':
            return 'основная'
        elif a == 'prepare':
            return 'подготовительная'
        elif a == 'specA':
            return 'специальная А'
        elif a == 'specB':
            return 'специальная Б'
        else:
            return ''
    def _cLang(a):
        if a == 'english':
            return 'английский'
        elif a == 'german':
            return 'немецкий'
        elif a == 'french':
            return 'французкий'
        else:
            return ''
        ...
    uID = getUserData(userLogin, 'users.id')[0]
    data = getUserData(userLogin, 'claims.marksAverage','abiturients.fname', 'abiturients.sname', 'abiturients.tname',
                                'abiturients.birthday', 'abiturients.birthplace', 'abiturients.country',
                                'passports.serial', 'passports.number', 'passports.creator', 'passports.date',
                                'claims.spec_id', 'claims.endDate', 'claims.schoolName', 'claims.attestate',
                                'claims.passPlace', 'claims.livePlace', 'claims.phone', 'users.email', 'claims.army',
                                'claims.lang', 'claims.healthGroup', 'claims.needHostel', 'claims.motherName',
                                'claims.motherPhone', 'claims.fatherName', 'claims.fatherPhone')

    doc = DocxTemplate("static\\Заявление-шаблон.docx")
    specName = req(f'select name from profs where rowid = {data[11]}')[0][0]
    context = { 'avg': data[0], 'fname': data[1], 'sname': data[2], 'tname': data[3], 
                'birthday': data[4], 'birthplace': data[5], 'country': data[6],
                'serial': data[7], 'number': data[8], 'creator': data[9], 'date': data[10],
                'profName': specName, 'schoolDate': data[12], 'schoolName': data[13],
                'attestate': data[14], 'passPlace': data[15], 'livePlace': data[16],
                'phone': data[17], 'email': _check(data[18]), 'army': _check(data[19]),
                'lang': _cLang(data[20]), 'healthGroup': _cHealth(data[21]), 
                'needHostel': 'нуждаюсь' if data[22] else 'не нуждаюсь',
                'momName': data[23], 'momPhone': data[24], 'dadName': data[25], 'dadPhone': data[26]}
    doc.render(context)
    s = 'static\\'
    name = f"Заявление-{userLogin}-{uID}"
    doc.save(s+name+".docx")
    convert(s+name+'.docx', s+name+'.pdf')
    os.remove(os.getcwd()+'\\'+s+name+'.docx')
    return name+'.pdf'


def loginPassCheck(un, pw):
    '''
    Проверка логина и пароля пользователя
    '''
    pwHash = req(f"select password from `users` where login = '{un}' ")[0][0]
    pwHash = pwHash[2:-1].encode('utf-8')
    if bcrypt.check_password_hash(pwHash, pw):
        return True
    else:
        False


def getUserData(user: str, *args):
    '''
    Получить информацию о пользователе по переданным аргументам
    '''
    sql = f'''select '''
    for i in args:
        sql += i + ', '
    sql = sql[:-2]
    sql += f''' from `users` join `abiturients` ON users.id = abiturients.userID join `passports` ON passports.abitID=abiturients.id join `claims` ON claims.abitID=abiturients.id where users.login='{user}' '''
    return req(sql, False)[0]


def saveBaseCookies(l):
    '''
    Сохранить базовые Cookie о пользователе
    '''
    temp = getUserData(l, 'users.id', 'abiturients.fname',
                       'users.rules', 'users.email', 'users.login')
    print(temp)
    session['userID'] = temp[0]
    session['userName'] = temp[1]
    session['userState'] = temp[2]
    session['userInfo'] = temp[3]
    session['userLogin'] = temp[4]


def genNewUserLogin(sn: str) -> str:
    '''
    Генерация нового логина по фамилии
    '''
    login = pytils.translit.translify(sn)
    if req(f"select count(1) from `users` where `login` like '{login}'")[0][0] == 0:
        return login
    else:
        try:
            num = int(sn[len(sn)-1])
        except ValueError:
            return genNewUserLogin(sn+'1')
        else:
            return genNewUserLogin(sn[:-1] + str(num+1))


def genNewUserPass() -> dict:
    '''
    Генерация нового пароля
    '''
    cp = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    ph = bcrypt.generate_password_hash(cp)
    return {'password': cp, 'hash': ph}


def saveFormData(form):
    '''
    Сохранение данных из главной формы
    '''
    login = genNewUserLogin(form.get('secondname'))
    temp = genNewUserPass()
    pswrd = temp['password']
    print('new user detected', login, pswrd)
    hash = temp['hash']
    sqlNewUser = f'''

        insert into `passports`(`abitID`, `serial`, `number`, `date`, `creator`) values(
            99999999,
            {form.get('passID')[:4]},
            {form.get('passID')[4:]},
            '{form.get('passDate')}',
            '{form.get('passCountry')}'
        );

        delete from `passports` where `abitID` = 99999999;

        insert into `users`(`login`, `password`) values(
            '{login}',"{hash}"
        );

        insert into `abiturients`(`userID`,`fname`, `sname`, `tname`, `birthday`, `birthplace`, `country`) values(
            (SELECT MAX(id) FROM `users`),
            '{form.get('firstname')}',
            '{form.get('secondname')}',
            '{form.get('tridname')}',
            '{form.get('birthday')}',
            '{form.get('birthplace')}',
            '{form.get('country')}'
        );

        insert into `passports`(`abitID`, `serial`, `number`, `date`, `creator`) values(
            (SELECT MAX(id) FROM `abiturients`),
            {form.get('passID')[:4]},
            {form.get('passID')[4:]},
            '{form.get('passDate')}',
            '{form.get('passCountry')}'
        );

        insert into `claims`(
            `abitID`, `spec_id`, `schoolName`, `endDate`, `attestate`,
            `passPlace`, `livePlace`, `phone`, `army`, `lang`,
            `healthGroup`, `needHostel`, `motherName`, `motherPhone`,
            `fatherName`, `fatherPhone`, `consents`, `marksAverage`
        ) values(
            (SELECT MAX(id) FROM `abiturients`),
            '{form.get('specialitySelect')}',
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
            True,
            {form.get('attestateAverage')}
        );
    '''
    try:
        req(sqlNewUser)
    except Exception as e:
        if 'UNIQUE' in str(e):
            return 'Абитуриент с такими данными уже существует', login, pswrd
        else:
            return e, login, pswrd
    else:
        return 0, login, pswrd


def sendLoginPass(log, paw):
    print(log, paw)


# routing

@app.route('/new_password/<int:uid>')
def new_password(uid):
    data = genNewUserPass()
    sql = f"""UPDATE `users` SET `password` = "{data['hash']}" where `id` = {uid} """
    req(sql)
    return f" {data['password']} - {data['hash']}"


@app.route('/render_claim_pdf')
def render_claim_pdf():
    '''
    Маршрутизация страницы печати заявления
    '''
    if auth_request():

        import pythoncom
        pythoncom.CoInitializeEx(0)
    
        name = renderDocxTemplate(session.get('userLogin'))
        waybase = os.getcwd()+'\\static'
        temp = send_from_directory(waybase, name)
        return temp
    else:
        return redirect(url_for('login'))
     

@app.route('/login', methods=['post', 'get'])
def login():
    '''
    Маршрутизация страницы авторизации
    '''
    if request.method == 'POST':
        un = request.form.get('username')
        pw = request.form.get('password')
        if loginPassCheck(un, pw):
            saveBaseCookies(un)
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Wrong login or password')

    else:
        if session.get('userID') != None:
            return redirect(url_for('profile'))
        return render_template('login.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('layout.html'), 404


@app.route('/cabinet')
def cabinet():
    return redirect(url_for('profile'))


@app.route('/claim', methods=['post', 'get'])
def claim():
    '''
    Маршрутизация формы подачи заявления
    '''
    species = req("SELECT rowid, name FROM `profs` ORDER BY `spec_id`")
    if request.method == 'POST':
        check, log, pas = saveFormData(request.form)
        if check == 0:
            saveBaseCookies(log)
            sendLoginPass(log, pas)
            session['currentSpec'] = req(
                f"select `name` from `profs` where rowid = '{request.form.get('specialitySelect')}' ", False)[0][0]
            session['userLogin'] = log
            session['password'] = pas
            return redirect(url_for('claim_success'))
        else:
            return render_template('claim.html', species=species)
    else:
        return render_template('claim.html', species=species)


@app.route('/claim_success')
def claim_success(p=None, l=None, ps=None):
    '''
    Маршрутизация окна успешной регистрации
    '''
    if auth_request():
        # if True:
        p = session['currentSpec']
        l = session['userLogin']
        ps = session['password']
        session['password'] = None
        return render_template('claim_success.html', prof=p, login=l, pas=ps)
    else:
        return redirect(url_for('login'))


@app.route('/profile', methods=['post', 'get'])
def profile():
    if auth_request():
        if request.method == 'POST':
            print(request.form)
            fm = request.form

            pw = fm.get('password')
            if pw == '':
                return redirect(url_for('profile'))
            elif "'" in pw or '"' in pw or '`' in pw or ';' in pw:
                return redirect(url_for('profile', error='Wrong symbols in new password'))
            elif len(pw) < 6:
                return redirect(url_for('profile', error='The new password must be longer than 6 characters'))
            else:
                new_pw = bcrypt.generate_password_hash(pw)
                req(f"""
                    update `abiturients` set fname = "{fm.get('firstname')}", sname = "{fm.get('secondname')}", tname = "{fm.get('tridname')}", birthday = "{fm.get('birthday')}" where userID = (select id from `users` where login = "{session['userLogin']}");
                    update `users` set login = '{fm.get('login')}', password = "{new_pw}" where login = "{session['userLogin']}";
                """)
                session['userLogin'] = fm.get('login')
                return redirect(url_for('profile'))

        else:
            un = session.get('userLogin')
            st = session.get('userState')
            print(un, st, session.get('userID'))
            data = getUserData(un, 'abiturients.fname', 'abiturients.sname', 'abiturients.tname', 'abiturients.birthday',
                               'passports.serial', 'passports.number', 'claims.phone', 'users.login', 'users.password')
            return render_template('profile.html', username=un, state=st,
                                   userFN=data[1], userSN=data[0], userTN=data[2], userAge=data[3], userPass=data[4]+data[5], userPhone=data[6],
                                   userLogin=data[7], userPassword=data[8])
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('index'))
    except Exception as e:
        print(e)


@app.route('/ratings')
def ratings():
    rating = ENABLE_RATINGS
    if rating:
        temp = req("select profs.spec_id, profs.name, abiturients.fname, abiturients.sname, claims.marksAverage, claims.abitID from profs join claims on claims.spec_id=profs.rowid join abiturients on claims.abitID=abiturients.id order by profs.spec_id, claims.marksAverage desc ", False)
        specs = {}
        for i in temp:
            name = i[0]+' '+i[1]
            abname = i[3]+' '+i[2]
            if name in specs.keys():
                specs[name].append({'name': abname, 'avg': i[4], 'id': i[5]})
            else:
                specs[name] = [{'name': abname, 'avg': i[4], 'id':i[5]}]
        return render_template('ratings.html', ratings=rating, species=specs)
    else:
        return render_template('ratings.html', ratings=rating)


@app.route('/professions/')
def professions():
    data = req(
        "Select rowid, `spec_id`, `name`, `spec_data`, `legend`, `photoWay` From `profs` order by `spec_id`", False)
    return render_template('professions.html', profs=data)


@app.route('/professions/<int:id>')
def showProf(id):
    data = req(
        f" Select rowid, `spec_id`, `name`, `spec_data`, `legend`, `photoWay` From `profs` Where rowid = '{id}'", False)[0]
    return render_template('profPage.html', info=data, profID=id)


@app.route('/')
def index():
    if auth_request():
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('claim'))


if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0', port=80)
