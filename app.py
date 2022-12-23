from flask import Flask,render_template, request, session, redirect
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import os
import string
import random
import datetime
 
app = Flask(__name__)
app.secret_key=os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'stocket'
mysql = MySQL(app)

app.config['UPLOAD_FOLDER'] = './static/uploads/'


def get_user(of_user = '', all=False):
    cursor = mysql.connection.cursor()
    if of_user != '':
        cursor.execute("""select name, user_id, photo, background, bio from users where user_id = '{}'""".format(of_user))
    elif all:
        cursor.execute("""select name, user_id, photo, background, bio, email, pno from users where user_id = '{}'""".format(session['user_id']))
    else:
        cursor.execute("""select name, user_id, photo, background, bio from users where user_id = '{}'""".format(session['user_id']))
    user = cursor.fetchall()
    return user

def get_posts(of_user = ''):
    cursor = mysql.connection.cursor()
    if of_user != '':
        # print("""select name, posts.user_id, raw_post, likes, image, posted_at,photo from posts INNER JOIN users on posts.user_id = users.user_id where posts.user_id = '{}'""".format(of_user))
        cursor.execute("""select name, posts.user_id, raw_post, likes, image, posted_at,photo from posts INNER JOIN users on posts.user_id = users.user_id where posts.user_id = '{}' order by posts.id desc""".format(of_user))
    else:
        # print("""select name, posts.user_id, raw_post, likes, image, posted_at,photo from posts INNER JOIN users on posts.user_id = users.user_id""")
        cursor.execute("""select name, posts.user_id, raw_post, likes, image, posted_at,photo from posts INNER JOIN users on posts.user_id = users.user_id order by posts.id desc""")
    posts = cursor.fetchall()
    return posts

def get_path():
    path = request.root_url.replace('/?','')
    return path

@app.route('/')
def home():
    if 'user_id' in session:
        posts = get_posts()
        path = get_path()
        user = get_user()
        # print(posts)
        return render_template('index.html', posts=posts, user=user, path=path)
    else:
        return redirect('/login')

@app.route('/compose')
def compose():
    if 'user_id' in session:
        path = get_path()
        user = get_user()
        x = datetime.datetime.now()
        date = x.strftime("%B %d, %Y")
        return render_template('compose.html', user=user, date=date, path=path)
    else:
        return redirect('/login')

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect('/')
    else:
        print(request.root_url)
        return render_template('login.html')

@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect('/')
    else:
        return render_template('register.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users = cursor.fetchall()
    if len(users)>0:
        session['user_id'] = users[0][5]
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('name')
    email=request.form.get('email')
    pno=request.form.get('pno')
    password=request.form.get('password')
    user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    cursor = mysql.connection.cursor()
    cursor.execute("""INSERT INTO `users` (`name`, `email`, `pno`, `password`, `user_id`) values ("{}","{}","{}","{}","{}")""".format(name,email,pno,password,user_id))
    print("""INSERT INTO `users` (`name`, `email`, `pno`, `password`, `user_id`) values ("{}","{}","{}","{}","{}")""".format(name,email,pno,password,user_id))
    mysql.connection.commit()
    return redirect('/login')

@app.route('/new_post', methods=['POST'])
def new_post():
    if 'user_id' in session:
        post_data=request.form.get('post_data')

        user_id = session['user_id']
        x = datetime.datetime.now()
        created_at = x.strftime("%B %d, %Y")
        f = request.files['image']
        cursor = mysql.connection.cursor()
        if f.filename is not '':
            filename = os.path.join(app.config['UPLOAD_FOLDER'], session['user_id'] + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))+secure_filename(f.filename))
            f.save(filename)
            print("""INSERT INTO `posts` (`raw_post`, `user_id`, `posted_at`, `image`) values ("{}","{}","{}","{}")""".format(post_data, user_id, created_at, filename))
            cursor.execute("""INSERT INTO `posts` (`raw_post`, `user_id`, `posted_at`, `image`) values ("{}","{}","{}","{}")""".format(post_data, user_id, created_at, filename))
        else:
            print("""INSERT INTO `posts` (`raw_post`, `user_id`, `posted_at`) values ("{}","{}","{}")""".format(post_data, user_id, created_at))
            cursor.execute("""INSERT INTO `posts` (`raw_post`, `user_id`, `posted_at`) values ("{}","{}","{}")""".format(post_data, user_id, created_at))
        mysql.connection.commit()
        return redirect('/')
    else:
        return render_template('login.html')

@app.route('/update-profile', methods=['POST'])
def update_profile():
    if 'user_id' in session:
        name=request.form.get('name')
        email=request.form.get('email')
        pno=request.form.get('pno')
        bio=request.form.get('bio')
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        # print("""INSERT INTO `posts` (`raw_post`, `user_id`, `posted_at`) values ("{}","{}","{}")""".format(post_data, user_id, created_at))
        cursor.execute("""UPDATE `users` SET name = '{}', email = '{}', pno='{}',bio='{}' where user_id = '{}' """.format(name, email, pno, bio, user_id))
        mysql.connection.commit()
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/@<path:user_id>')
def user(user_id):
    if 'user_id' in session:
        path = get_path()
        res = get_user(user_id)
        user = get_user()
        print(res)
        if len(res) > 0:
            posts = get_posts(res[0][1])
            return render_template('profile.html', res = res, user = user, posts = posts, path=path)
        else:
            return f'No User Found'
    else:
        return redirect('/login')

@app.route('/@<path:user_id>/edit-profile')
def edit_profile(user_id):
    if 'user_id' in session:
        if session['user_id'] == user_id:
            path = get_path()
            user = get_user(all=True)
            return render_template('edit-profile.html', user = user, path=path)
        else:
            red = '/@'+user_id
            return redirect(red)
    else:
        return redirect('/login')



@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/login')

@app.route('/test')
def test():
    return render_template('test.html')


app.run(port=5000, debug=True)