from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .auth import admin
from .models import Article
from . import db
from sqlalchemy import update


views = Blueprint('views', __name__)

@views.route('/')
def Intro():
    return render_template('introduction.html',user=current_user)


@views.route('/admin')
@login_required
def Admin():
    if current_user.username == admin.username and current_user.password == admin.password:
        list_article = db.session.query(Article).all()
        return render_template('admin_section.html', user=current_user,list_article=list_article )
    else:
        return redirect(url_for('views.Intro'))
    

@views.route('/new', methods=["GET", "POST"])
@login_required
def NewArticle():
    if request.method == 'POST':
        if request.form:
            title = request.form.get('title')
            description = request.form.get('description')
            new_article = Article(title=title, description=description)
            db.session.add(new_article)
            db.session.commit()
            flash('Article added' , category='success')
            return redirect(url_for('views.Admin'))
        else:
            flash('Please enter the informations' ,category="error")
    else:
        pass
    return render_template('new_article.html', user=current_user)

@views.route('/delete/<int:id>')
@login_required
def Delete(id):
    d = db.session.get(Article, id)
    db.session.delete(d)
    db.session.commit()
    return redirect(url_for("views.Admin"))

@views.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def Update(id):
    if request.method == 'POST':
        if request.form:
            title = request.form.get('title2')
            description = request.form.get('description2')
            article = db.session.query(Article).filter(Article.id == id)
            update = dict(title=title, description=description)
            article.update(update)
            article.session.commit()
            return redirect(url_for('views.Admin'))       
    return render_template('update_article.html', user=current_user)

@views.route('/article/<int:id>')
@login_required
def ArticleDetail(id):
    d = db.session.get(Article, id)
    return render_template('detail_article.html', user=current_user, d=d)

@views.route('/home')
@login_required
def Home():
    list_article = db.session.query(Article).all()
    return render_template('home.html', user=current_user, list_article=list_article)