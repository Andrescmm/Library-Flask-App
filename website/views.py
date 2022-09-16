from crypt import methods
from difflib import get_close_matches
from email.mime import image
from pdb import post_mortem
from turtle import title
from flask import Blueprint, render_template, request, flash, jsonify
from flask import request, Response
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from .models import Book
from flask_bootstrap import Bootstrap
from . import db
import json
from datetime import datetime, date
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
import keyword

views = Blueprint('views', __name__)

@views.route('/screen', methods=['GET', 'POST'])
@login_required
def screen():
    return render_template('screen.html',user=current_user)



@views.route('/', methods=['GET'], defaults={"page": 1}) 
@views.route('/<int:page>', methods=['GET'])
@login_required
def view(page):
    page = page
    per_page = 5
    threads = Book.query.paginate(page,per_page,error_out=False)


    list_of_authors = []
    authors = Book.query.all()
    for i in authors:
       if i.author not in list_of_authors:
          list_of_authors.append(i.author)

    school = Book.query.filter_by(author='3').all()
    print("gaa",school)      

    return render_template("home.html", threads=threads,user=current_user ,list_of_authors=list_of_authors)


@views.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    if request.method == 'POST':

        book = request.form.get('title')
        author= request.form.get('author')
        year = request.form.get('year')
        edition = request.form.get('edition')
        amount= request.form.get('amount')
        image = request.form.get('image')
        

        new_book = Book(title=book,author=author,year=year,edition=edition,image=image,amount=amount)
        db.session.add(new_book)
        db.session.commit()
        flash('Book Added', category='success')

    return render_template("books.html",user=current_user )



@views.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update(id):
    name_to_update = Book.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.title = request.form.get('title')
        name_to_update.author= request.form.get('author')
        name_to_update.year = request.form.get('year')
        name_to_update.edition = request.form.get('edition')
        name_to_update.amount= request.form.get('amount')
        name_to_update.image = request.form.get('image')

        db.session.commit()
        flash('Book Edited', category='success')

    return render_template("update.html",id=id,name_to_update=name_to_update,user=current_user)    

	
	
@views.route('/delete/<int:id>')
@login_required
def delete(id):
    user_to_delete = Book.query.get_or_404(id)

    db.session.delete(user_to_delete)
    db.session.commit()
    flash('Book deleted Successfully', category='success')

    our_users = Book.query.order_by(Book.title)
    return render_template("screen.html",id=id,our_users=our_users,user_to_delete=user_to_delete,user=current_user)    




@views.route('/search',methods=["POST"])
@login_required
def search():
    title=request.form.get("title").lower()

    list1=[]
    list2 =[]
    list3 =[]
    list4 =[]
    list5 =[]
    list6 =[]
    #a = get_close_matches(title,['principito','principe','apple','leah'])
    #print(a)
    results = Book.query.all()
    #print (results)
    for i in results:
        if ((title in i.title.lower() )or (title in i.author.lower())) is True:
            print("entrando if ")
            list1.append(i.title)
            list2.append(i.author)
            list3.append(i.year)
            list4.append(i.edition)
            list5.append(i.image)
            list6.append(i.amount)

    return render_template("search.html",count=len(list1), result1 =list1, result2=list2,result3=list3,result4 =list4,result5 =list5,result6 =list6,user=current_user) 
    db.session.commit()

