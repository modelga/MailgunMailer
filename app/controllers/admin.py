from flask import render_template, request

from app import app
from app.models.Login import login_required


@app.route('/admin')
@login_required
def admin_index():
	from app.models.Settings import get_user_ip
	user_ip = get_user_ip()
	return render_template('admin/index.html', user_ip=user_ip)


@app.route('/admin/pw_show', methods=['POST'])
@login_required
def admin_pw_show():
	from flask_bcrypt import generate_password_hash
	try:
		password = request.form['password']
	except Exception as inst:
		print("Error Type:", type(inst))
		print("Error Arguments:", inst.args)
		password = "Sometext"

	pw_hash = generate_password_hash(password).decode('utf8')
	return pw_hash
