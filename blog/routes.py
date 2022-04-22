# blog/routes.py

from flask import render_template, request, make_response ,session, flash, redirect, url_for 
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm
import functools

def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
      if session.get('logged_in'):
         return view_func(*args, **kwargs)
      return redirect(url_for('login', next=request.path))
   return check_permissions

def delete_entry(entry_id):
    delete_draft = Entry.query.get(entry_id)
    db.session.delete(delete_draft)
    db.session.commit()

@app.route("/")
def index():
   all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
   return render_template("homepage.html", all_posts=all_posts)


@app.route("/drafts/", methods=['GET', 'POST'])
@login_required
def list_drafts():
   drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
   if request.method == 'POST':
      data = request.form
      entry_id = data.get('button_entry_id')
      delete_entry(entry_id)
      return redirect(url_for("index"))
    
   return render_template("drafts.html", drafts=drafts)


@app.route("/edit-entry/<int:entry_id>", methods=["GET", "POST"])
@app.route("/edit-entry/", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id=None):
   errors = None
   if entry_id:
      entry = Entry.query.filter_by(id=entry_id).first_or_404()
      form = EntryForm(obj=entry)
      if request.method == 'POST':
         if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.commit()
         else:
            rrors = form.errors
         return redirect(url_for("index"))
   else:
      form = EntryForm()
      if request.method == 'POST':
         if form.validate_on_submit():
            entry = Entry(
            title=form.title.data,
            body=form.body.data,
            is_published=form.is_published.data
            )
            db.session.add(entry)
            db.session.commit()
         else:
            errors = form.errors
         return redirect(url_for("index"))

      return render_template("entry_form.html", form=form, errors=errors)
# Do tad wszystko pracuje

@app.route("/login/", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   errors = None
   next_url = request.args.get('next')
   if request.method == 'POST':
       if form.validate_on_submit():
           session['logged_in'] = True
           session.permanent = True  # Use cookie to store session.
           flash('You are now logged in.', 'success')
           return redirect(next_url or url_for('index'))
       else:
           errors = form.errors
   return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
   if request.method == 'POST':
       session.clear()
       flash('You are now logged out.', 'success')

   return render_template("login_form.html", form=form, errors=errors)

@app.route('/cookie/')
def cookie():
    res = make_response("Setting a cookie")
    res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
    return res