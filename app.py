import os
from flask import Flask, redirect, render_template, request, session
from models import  db, User , Application , Post 
from flask_migrate import Migrate
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = 'sandy_secret_123'




UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sandy4@localhost/job_portals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


db.init_app(app)
migrate = Migrate(app, db)






@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            email_id=request.form['email_id'],
            password=request.form['password']
        )
        db.session.add(user)
        db.session.commit()
        
        return redirect('/login')

    return render_template('register.html')







@app.route('/login', methods = ['GET' , 'POST'])
def login():
    
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user'] = user.id
            return redirect('/post_page')
        else:
            return render_template('logout.html')
        
    return render_template('login.html')




@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')








@app.route('/job_post/' , methods = ['GET' , 'POST'])
def job_post():
    
        # admin check
    if 'user' not in session:
        return redirect('/')
    
    if request.method == 'POST':
            
        job = Application (title=request.form['title'] , company=request.form['company'] ,description = request.form['description'],salary = request.form['salary'])
        db.session.add(job)
        db.session.commit()
        return redirect('/post_page')
        
    return render_template('application.html')





@app.route('/post_page')
def jobs():
    
    search = request.args.get('search')
    min_salary = request.args.get('min_salary')

    query = Application.query

    if search:
        query = query.filter(Application.title.like(f"%{search}%"))

    if min_salary:
        query = query.filter(Application.salary >= min_salary)

    all_jobs = query.all()

    return render_template('job_post.html', jobs=all_jobs)







@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        file = request.files['resume']

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        user = User.query.filter_by(id = session['user']).first()

        new_application = Post(
            user_id=user.id,
            job_id=job_id,
            your_name = request.form['your_name'],
            phone_number = request.form['phone_number'],
            email = request.form['email'],
            address = request.form['address'],
            location = request.form['location'],
            resume=filename
        )

        db.session.add(new_application)
        db.session.commit()

        return redirect ('/admin/applications')
    

    return render_template('apply.html', job_id=job_id)







@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    user = User.query.filter_by(id = session['user']).first()
    applications = Post.query.filter_by(user_id=user.id).all()

    return render_template('dashboard.html', apps=applications)





@app.route('/admin/applications')
def view_applications():
    apps = Post.query.all()
    return render_template('admin.html', apps=apps)






port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)



