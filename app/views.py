from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user

from app import app
from app import login_manager
from forms import LoginForm

@app.route("/")
def homepage():
	return render_template("homepage.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		form = LoginForm(request.form)
		if form.validate():
			login_user(form.user, remember=form.remember_me.data)
			flash("Successfully logged in as %s." % form.user.email, "success")
			return redirect(request.args.get("next") or url_for("homepage"))
	else:
		form = LoginForm()
	return render_template("login.html", form=form)