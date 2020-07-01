"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, url_for, request, session, redirect, flash
from flask_login import login_required, current_user, UserMixin, login_user, logout_user
#imports from init.py the initialized app
from Serviclean4 import app
#imports required extensions
from .extensions import mongo 
from .extensions import login_manager
from bson.objectid import ObjectId

users = mongo.db.users
#users = {'foo@bar.tld': {'password': 'secret'}}
user_login = None

#print(users)
class User(UserMixin):
    pass

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def home():
    """Renders the home page after succesful login."""
    return render_template(
        'home.html',
        title='Inicio',
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
@login_required
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@login_manager.user_loader
def user_loader(user_login):
    
    print('inicio user_loader ' + user_login)
    #user_login = users.find_one({'name' : request.form['username']})
    user_login_temp = users.find_one({'name' : user_login})
    print(user_login_temp)
    #if user_login_temp not in users:
    if user_login_temp:
        user = User()
        user.id = user_login
        print('fin uso user_loader ' + user.id)
        
        return user
    return None

@login_manager.request_loader
def request_loader(request):

    print('inicio_request_loader')
    username = request.form.get('username')
    #Linea agregada para evitar "collection not iterable":
    user_login_temp = users.find_one({'name' : ObjectId(username)})
    print(user_login_temp)
    if user_login_temp:
        user = User()
        user.id = username
        user.is_authenticated = request.form['password'] == users[user_login]['password']
        print('fin_request_loader' + user.id)
        
        return (user)
    return ('No ingreso ', None)

@app.route('/login', methods=['GET','POST'])
def login():
 
    #user_login = None
    if request.method == 'GET':
        return (login.html)

    #Defines the collection of users
    #users = mongo.db.users
 
    
    user_login = request.form['username']
    print('login route: ' + user_login)
    if user_login:
        db_login = users.find_one({'name' : user_login})
        #change removing encode('utf-8') because of debugging issue: 'bytes' object has no attribute 'encode'
        #original line:
        #if bcrypt.hashpw(request.form['password'].encode(encoding='UTF-8'), login_user['password'].encode(encoding='UTF-8')) == login_user['password'].encode(encoding='UTF-8'):
        print('login: ')
        print(db_login)
       # debugging purposes    if request.form['password'] == user_login['password']:
        if request.form['password'] == db_login['password']:
            session['username'] = request.form['username']
             # Login and validate the user.
            user = User()
            user.id = user_login
            login_user(user)
            print(user.id)
            print('se ha ingresado a: ' + user.id)

            flash('Ingreso exitoso.', category = 'message')  

            return redirect(url_for('about'))
            
            #perfil = user_login['perfil']
            ##Change of return by returning a template of home insted of redirect
            #if perfil == 'Colaborador':
            #    return render_template(
            #        'home_colab.html',
            #        title='Inicio',
            #        year=datetime.now().year,
            #        message='Has ingresado con exito ' + session['username']
            #    )
            #elif perfil == 'Supervisor':
            #    return render_template(
            #        'home_sup.html',
            #        title='Inicio',
            #        year=datetime.now().year,
            #        message='Has ingresado con exito ' + session['username']
            #    )
            #elif perfil == 'Cliente':
            #        return render_template(
            #        'home_cliente.html',
            #        title='Inicio',
            #        year=datetime.now().year,
            #        message='Has ingresado con exito ' + session['username']
            #    )
            #else:
            #        return render_template(
            #        'home_admin.html',
            #        title='Inicio',
            #        year=datetime.now().year,
            #        message='Has ingresado con exito ' + session['username']
            #    )

    return 'Combinación usuario / password invalida, intente de nuevo!'
                
@app.route('/register_home', methods=['POST', 'GET'])
def register_home():
    profiles = mongo.db.profiles
#    Code line to input directly a new profile in the database:
#    profiles.insert({'Perfil' : 'Supervisor'})
    if request.method == 'POST':
        profiles = mongo.db.profiles
        existing_profile = profiles.find_one({'Perfil' : request.form['perfil']})
        perfil = existing_profile['Perfil']
        print(perfil)
        if existing_profile['Perfil'] == 'Colaborador':
            return render_template(
                'register.html',
                title='Registro',
                year=datetime.now().year,
                message='Por favor ingrese el resto de datos solicitados',
                perfil=perfil,
            )
        elif existing_profile['Perfil'] == 'Supervisor':
            return render_template(
                'register.html',
                title='Registro',
                year=datetime.now().year,
                perfil=existing_profile['Perfil'],
                message='Por favor ingrese el resto de datos solicitados'
            )
        elif existing_profile['Perfil'] == 'Cliente':
             return render_template(
                'register.html',
                title='Registro',
                year=datetime.now().year,
                perfil=existing_profile['Perfil'],
                message='Por favor ingrese el resto de datos solicitados'
            )
        else:
             return render_template(
                'register.html',
                title='Registro',
                year=datetime.now().year,
                perfil=existing_profile['Perfil'],
                message='Por favor ingrese el resto de datos solicitados'
            )
    return render_template(
        "register_home.html",
        title='Selección de usuario',
        year=datetime.now().year,
        message='Favor de ingresar el perfil que corresponde'
    )

@app.route('/register', methods=['POST', 'GET'])
def register():
    print('segunda funcion')
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None: 
            if request.form['password'] == request.form['password_rep']:
                #original line
                #hashpass = bcrypt.hashpw(request.form['password'].encode(encoding='UTF-8'), bcrypt.gensalt())
                #users.insert({'name' : request.form['username'], 'password' : hashpass})
                users.insert({'name' : request.form['username'], 
                              'password' : request.form['password'], 
                              'email' : request.form['user_email'], 
                              'keyword': request.form['keyword'],
                              'perfil': request.form['perfil']}
                             )
                #<input type="email" class="form-control" id="user_email" placeholder="nombre@ejemplo.com">
                session['username'] = request.form['username']
                perfil = request.form['perfil']
                #return redirect(url_for('login'))
                #change for render template
                if perfil == 'Colaborador':
                    return render_template(
                        'home_colab.html',
                        title='Inicio',
                        year=datetime.now().year,
                        message='Has ingresado con exito ' + session['username']
                    )
                elif perfil == 'Supervisor':
                    return render_template(
                        'home_sup.html',
                        title='Inicio',
                        year=datetime.now().year,
                        message='Has ingresado con exito ' + session['username']
                    )
                elif perfil == 'Cliente':
                     return render_template(
                        'home_cliente.html',
                        title='Inicio',
                        year=datetime.now().year,
                        message='Has ingresado con exito ' + session['username']
                    )
                else:
                     return render_template(
                        'home_admin.html',
                        title='Inicio',
                        year=datetime.now().year,
                        message='Has ingresado con exito ' + session['username']
                    )
            return render_template(
                'register.html',
                title='Registro',
                year=datetime.now().year,
                message='Las contraseñas no coinciden, favor de verificar!'
                )
        return render_template(
            'register.html',
            title='Registro',
            year=datetime.now().year,
            message='Nombre de usario existente / ya registrado!'
            )

    return render_template('register.html')