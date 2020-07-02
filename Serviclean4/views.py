"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, url_for, request, session, redirect, flash
from flask_login import login_required, current_user, UserMixin, login_user, logout_user
from bson.objectid import ObjectId
#imports from init.py the initialized app
from Serviclean4 import app
#imports required extensions
from .extensions import mongo 
from .extensions import login_manager
from .util.security import ts
from .util.email import send_email

#from project.token import generate_confirmation_token, confirm_token

#Defines the collection of users
users = mongo.db.users
user_login = None

#FINISH DEFINING THIS
class User(UserMixin):
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def __init__(self, email, password, confirmed,
                 paid=False, admin=False, confirmed_on=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.perfil = perfil
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
    pass

name' : request.form['username'], 
                              'password' : request.form['password'], 
                              'email' : request.form['user_email'], 
                              'keyword': request.form['keyword'],
                              'perfil': request.form['perfil'],
                              'confirmed' : False,
                              'registered_on': datetime.now(),
                              'confirmed_on': None}

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
@login_required
def home():
    """Renders the home page after succesful login."""
    return render_template(
        'home/home.html',
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
        message='Application description page.'
    )

@login_manager.user_loader
def user_loader(user_login):   
    user = User()
    user.id = user_login

    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    #retrieve from the database user info":
    user_login_temp = users.find_one({'name' : username})
    if user_login_temp:
        user = User()
        user.id = username
        user.is_authenticated = request.form['password'] == users[user_login]['password']

        return user
    return ('Invalido ', None)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return (login.html)

    user_login = request.form['username']
    if user_login:
        #Verifying user is in database and retrieving info
        db_login = users.find_one({'name' : user_login})

        #AQUI FALTA AGREGAR CONDICIONAL QUE USUARIO EXISTE O NO

        #change removing encode('utf-8') because of debugging issue: 'bytes' object has no attribute 'encode'
        #pending implementing bcrypt:
        #if bcrypt.hashpw(request.form['password'].encode(encoding='UTF-8'), login_user['password'].encode(encoding='UTF-8')) == login_user['password'].encode(encoding='UTF-8'):
        if request.form['password'] == db_login['password']:
            session['username'] = request.form['username']
            # Login and validate the user.
            user = User()
            user.id = user_login
            login_user(user)
            perfil = db_login['perfil']
            #Pending optimizing redirect_url with profile variable
            if perfil == 'Colaborador':
                return render_template(
                    'home/home_colab.html',
                    title='Inicio',
                    year=datetime.now().year,
                    message='Has ingresado con exito ' + session['username']
                )
            elif perfil == 'Supervisor':
                return render_template(
                    'home/home_sup.html',
                    title='Inicio',
                    year=datetime.now().year,
                    message='Has ingresado con exito ' + session['username']
                )
            elif perfil == 'Cliente':
                    return render_template(
                    'home/home_cliente.html',
                    title='Inicio',
                    year=datetime.now().year,
                    message='Has ingresado con exito ' + session['username']
                )
            else:
                    return render_template(
                    'home/home_admin.html',
                    title='Inicio',
                    year=datetime.now().year,
                    message='Has ingresado con exito ' + session['username']
                )

                #sacado de register route, redundante?:
                #session['username'] = request.form['username']
                #perfil = request.form['perfil']
                ##return redirect(url_for('login'))
                ##change for render template
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
                #     return render_template(
                #        'home_cliente.html',
                #        title='Inicio',
                #        year=datetime.now().year,
                #        message='Has ingresado con exito ' + session['username']
                #    )
                #else:
                #     return render_template(
                #        'home_admin.html',
                #        title='Inicio',
                #        year=datetime.now().year,
                #        message='Has ingresado con exito ' + session['username']
                #    )

    return 'Nombre de usuario o password invalida, intente de nuevo!'
                
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
                'user/register.html',
                title='Registro',
                year=datetime.now().year,
                message='Por favor ingrese el resto de datos solicitados',
                perfil=perfil,
            )
        elif existing_profile['Perfil'] == 'Supervisor':
            return render_template(
                'user/register.html',
                title='Registro',
                year=datetime.now().year,
                perfil=existing_profile['Perfil'],
                message='Por favor ingrese el resto de datos solicitados'
            )
        elif existing_profile['Perfil'] == 'Cliente':
             return render_template(
                'user/register.html',
                title='Registro',
                year=datetime.now().year,
                perfil=existing_profile['Perfil'],
                message='Por favor ingrese el resto de datos solicitados'
            )
        else:
             return render_template(
                'user/register.html',
                title='Registro',
                year=datetime.now().year,
                perfil=existing_profile['Perfil'],
                message='Por favor ingrese el resto de datos solicitados'
            )
    return render_template(
        "user/register_home.html",
        title='Selección de usuario',
        year=datetime.now().year,
        message='Favor de ingresar el perfil que corresponde'
    )

@app.route('/register', methods=['POST', 'GET'])
def register():
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
                              'perfil': request.form['perfil'],
                              'confirmed' : False,
                              'registered_on': datetime.now(),
                              'confirmed_on': None}
                             )
                #<input type="email" class="form-control" id="user_email" placeholder="nombre@ejemplo.com">

                # Send email confirmation link
                subject = "Confirm your email"
                #token = ts.dumps(self.email, salt='email-confirm-key')
                token = ts.dumps(self.email, salt='email-confirm-key')
                
                confirm_url = url_for(
                    'confirm_email',
                    token=token,
                    _external=True)

                html = render_template(
                    'user/activate.html',
                    confirm_url=confirm_url)

                # send_email needs to be defined in /util.py
                send_email(user.email, subject, html)

                #code line from realpy after sending email, CHECK:
                #login_user(user)

                #CHECAR ESTE CODIGO ALTERNO / COMPLEMENTARIO PARA MANDAR TOKEN COMO FUNCION
                #def confirm_token(token, expiration=3600):
                    #serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
                    #try:
                    #    email = serializer.loads(
                    #        token,
                    #        salt=app.config['SECURITY_PASSWORD_SALT'],
                    #        max_age=expiration
                    #    )
                    #except:
                    #    return False
                    #return email
                #Be sure to add the SECURITY_PASSWORD_SALT to your app’s config (BaseConfig()):

                #@user_blueprint.route('/register', methods=['GET', 'POST'])
                #def register():
                #    form = RegisterForm(request.form)
                #    if form.validate_on_submit():
                #        user = User(
                #            email=form.email.data,
                #            password=form.password.data,
                #            confirmed=False
                #        )
                #        db.session.add(user)
                #        db.session.commit()

                #        token = generate_confirmation_token(user.email)


                #SECURITY_PASSWORD_SALT = 'my_precious_two'


                return redirect(url_for("index"), message = 'Correo de confirmación enviado, revise su correo para continuar')

            return render_template(
                'user/register.html',
                title='Registro',
                year=datetime.now().year,
                message='Las contraseñas no coinciden, favor de verificar!'
                )
        return render_template(
            'user/register.html',
            title='Registro',
            year=datetime.now().year,
            message='Nombre de usario existente / ya registrado!'
            )

    return render_template('user/register.html') #render_template("accounts/create.html", form=form

#needs to be adapted to mongo instead of sql
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = users.find_one({'email' : email}).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
    #user = User.query.filter_by(email=email).first_or_404()
        user.insert_one({'confirmed': True},
                        {'confirmed_on' : datetime.now()})
        flash('You have confirmed your account. Thanks! Please login now', 'success')  
    #db.session.add(user)
    #db.session.commit()

    return redirect(url_for('login'))