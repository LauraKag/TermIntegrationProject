
# import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
# from flask_cors import CORS
from werkzeug.utils import secure_filename


app = Flask("Login",template_folder='templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route("/", methods=['GET', 'POST'])
def login():

    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
           
            return redirect('https://termintegrationproject.herokuapp.com/')
   
        else:
            error = 'Insert valid credentials to continue'
    return render_template('register.html', error=error)


if __name__ == '__main__':
    app.run()