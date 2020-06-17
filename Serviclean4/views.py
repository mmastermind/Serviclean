"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, url_for, request, session, redirect
#imports from init.py the initialized app
from Serviclean4 import app
#imports pymongo from extensions
from .extensions import mongo 


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def home():
    """Renders the home/index page to login."""
    return render_template(
        'home.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'home.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/login', methods=['POST'])
def login():
    #creates a collection of users
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        #change removing encode('utf-8') because of debugging issue: 'bytes' object has no attribute 'encode'
        #original line:
        #if bcrypt.hashpw(request.form['password'].encode(encoding='UTF-8'), login_user['password'].encode(encoding='UTF-8')) == login_user['password'].encode(encoding='UTF-8'):
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            #return redirect(url_for('home'))
            #Change of return by returning a template of home insted of redirect
            print('Llegue hasta aqui')
            return render_template(
                "home.html",
                title='Inicio',
                year=datetime.now().year,
                message='Has ingresado con exito como'+session['username']
            )

    return 'Combinación usuario / password invalida, intente de nuevo!'
                
@app.route('/register_home', methods=['POST', 'GET'])
def register_home():
    profiles = mongo.db.profiles
#    profiles.insert({'Perfil' : 'Supervisor'})
    if request.method == 'POST':
        profiles = mongo.db.profiles
        existing_profile = profiles.find_one({'Perfil' : request.form['perfil']})
        print(existing_profile)
        if existing_profile['Perfil'] == 'Colaborador':
            print('llegue al colaborador')
            return render_template(
                'register.html',
                title='Registro pagina 2',
                year=datetime.now().year,
                message='Por favor ingrese el resto de datos solicitados'
            )
        elif existing_profile['Perfil'] == 'Supervisor' or existing_profile['Perfil'] == 'Cliente':
            print('llegue al supervisor / cliente')
            return render_template(
                'register.html',
                title='Registro Avanzado',
                year=datetime.now().year,
                message='Por favor ingrese el resto de datos solicitados'
            )
    return render_template(
        "register_home.html",
        title='Selección de usuario',
        year=datetime.now().year,
        message='Favor de ingresar su elección'
    )

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            #change removing encode('utf-8') because of debugging issue: 'bytes' object has no attribute 'encode'
            #hashpass = bcrypt.hashpw(request.form['pass'], bcrypt.gensalt())
            #original line
            #hashpass = bcrypt.hashpw(request.form['password'].encode(encoding='UTF-8'), bcrypt.gensalt())
            #users.insert({'name' : request.form['username'], 'password' : hashpass})
            users.insert({'name' : request.form['username'], 
                          'password' : request.form['password'], 
                          'email' : request.form['user_email'], 
                          'keyword': request.form['keyword']})
            #<input type="email" class="form-control" id="user_email" placeholder="nombre@ejemplo.com">
            session['username'] = request.form['username']
            #return redirect(url_for('login'))
            #change for render template
            return render_template(
                'home.html',
                title='Home',
                year=datetime.now().year,
                message='Has ingresado con exito' + session['username']
            )
        return 'Nombre de usario existente / ya registrado!'

    return render_template('register.html')