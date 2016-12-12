from flask import render_template, request

from app import app
from app.models.Login import login_required


@app.route('/admin')
@login_required
def admin_index():
    return render_template('admin/index.html')


@app.route('/admin/pw_show', methods=['POST'])
@login_required
def admin_pw_show():
    from flask_bcrypt import generate_password_hash
    try:
        password = request.form['password']
    except:
        password = "Sometext"

    pw_hash = generate_password_hash(password).decode('utf8')
    return pw_hash
