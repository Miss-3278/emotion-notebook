#！urs/bin/env python3
# coding=utf-8

from  flask import render_template, Blueprint, redirect, url_for, flash
from run import login_manger
from form import Login_Form, Register_Form
from model import  Users
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required
from run import db


eNote=Blueprint('eNote', __name__, template_folder='templates')  #蓝图

@eNote.route('/')
@eNote.route('/index')
def index():
    form=Login_Form()
    return render_template('login.html', form=form)


@eNote.route('/login',methods=['GET','POST'])
def login():
        form=Login_Form()
        if form.validate_on_submit():
            user=Users.query.filter_by(username=form.name.data).first()
            if user is not  None and user.password==form.pwd.data:
                login_user(user)
                flash('登录成功')
                return  render_template('hello.html', name=form.name.data)
            else:
                flash('用户或密码错误')
                return render_template('login.html', form=form)

#用户登出
@eNote.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出登录')
    return redirect(url_for('eNote.index'))


@eNote.route('/register', methods=['GET','POST'])
def register():
    form=Register_Form()
    if form.validate_on_submit():
        user=Users(username=form.name.data, password=form.pwd.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('eNote.index'))
    return render_template('register.html', form=form)
