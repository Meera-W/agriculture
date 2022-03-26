from flask import render_template, url_for, flash, redirect, request
from agritech import app, db, bcrypt,storage
from agritech.forms import RegistrationForm, LoginForm
from agritech.models import Equipment, User
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail,Message
from newsapi import NewsApiClient

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hermione1332@gmail.com'
app.config['MAIL_PASSWORD'] = 'Harrypotter@1'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)  


@app.route('/')
def home():
    newsapi = NewsApiClient(api_key="cfdf4dc189f04b9caf6dfaf8e1c32107")
    #topheadlines = newsapi.get_top_headlines(sources="India.com")
    all_articles = newsapi.get_everything(q='farming, agriculture',
                                      sources='the-times-of-india',
                                      domains='https://timesofindia.indiatimes.com/topic/agriculture/news',
                                      language='en',
                                      sort_by='relevancy',
                                      page_size= 5,
                                      page=1)


    articles = all_articles['articles']

    desc = []
    news = []
    url  = []
    img  = []

    for i in range(len(articles)):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        url.append(myarticles['url'])
        img.append(myarticles['urlToImage'])



    #mylist = zip(news, desc, img)
    mylist = zip(news, desc,url,img)

    return render_template('news.html', context = mylist)


@app.route('/weather')
@login_required
def weather():
    return render_template('weather.html')

@app.route('/qgis')
@login_required
def qgis():
    return render_template('qgis.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html',form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/add_equipment',methods=['GET','POST'])
@login_required
def add():
    if (request.method=='POST'):
        eqname = request.form['eqname']
        location = request.form['location']
        price = request.form['price']
        contact = request.form['contact']
        qty = request.form['qty']
        upload = request.files['upload']
        filename = upload.filename
        storage.child("equipments/"+upload.filename).put(upload)
        equip = Equipment( eqname=eqname, location=location, price=price, contact=contact, filename=filename, user_id=current_user.id, qty=qty)        
        db.session.add(equip)
        db.session.commit()
        # db.child("equipments").push(data)
        return redirect('/equipments')
    return render_template('addForm.html')

@app.route('/equipments')
def equipments():
    # print(current_user)
    equipments = Equipment.query.all()
    return render_template('equipments.html',equipments=equipments,storage=storage,User=User)

@app.route('/rent/<id>',methods=['GET','POST'])
@login_required
def rent(id):
    if request.method == 'POST':
        item = Equipment.query.get_or_404(id)
        eqname = item.eqname
        rentee = request.form['rentee']
        location = request.form['location']
        qty = request.form['qty']
        contact = request.form['contact']
        item.qty -= int(qty)
        db.session.commit()
        receiver_email = User.query.filter_by(username=rentee).first().email
        receivers = []
        receivers.append(receiver_email)
        msg = Message('Rent Equipment Request', sender = 'hermione1332@gmail.com', recipients=receivers)
        msg.body = "Hello, I would like to rent " + qty + " "+ eqname +" equipments. I live in " + location + " and this is my contact " + contact
        mail.send(msg)
        return redirect(url_for('equipments'))
    return render_template('rent.html',id=id)