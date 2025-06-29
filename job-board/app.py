from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    company = db.Column(db.String(100))

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant = db.Column(db.String(100))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        job = Job(title=title, company=company)
        db.session.add(job)
        db.session.commit()
        return redirect('/jobs')

    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    message = None
    if request.method == 'POST':
        name = request.form['name']
        job_id = request.form['job']
        application = Application(applicant=name, job_id=job_id)
        db.session.add(application)
        db.session.commit()
        message = f"✅ {name}, your application has been submitted!"

    jobs = Job.query.all()
    return render_template('apply.html', jobs=jobs, message=message)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)