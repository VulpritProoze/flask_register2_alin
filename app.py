'''
	Flask program
'''

from flask import Flask, render_template, redirect, request, flash
from dbhelper import *
import os

app = Flask(__name__)
uploadfolder = 'static/img/'
app.config['SECRET_KEY'] = '!@#$%^'
app.config['UPLOAD_FOLDER'] = uploadfolder

def get_users() -> object:
	return getall_records('users')

def get_user(idno:str) -> object:
	return getone_record('users', idno=idno)

def substringer(s, phrase):
    i = s.find(phrase)
    return s[i + len(phrase):] if i != -1 else ''

@app.route('/register', methods=['POST'])
def register():
	idno:str = request.form['idno']
	lastname:str = request.form['lastname']
	firstname:str = request.form['firstname']
	course:str = request.form['course']
	level:str = request.form['level']
	flag:str = request.form['flag']
	file:object = request.files['uploadimage']
	print(f"Filename of image to upload: {file}")
	filename, extension = os.path.splitext(file.filename)
	imagename = os.path.join(uploadfolder, f'{filename}{idno}{extension}')
	files = [os.path.join(uploadfolder, f) for f in os.listdir(uploadfolder) if os.path.isfile(os.path.join(uploadfolder, f))]
	print(f"Directory + Filename of image to upload: {imagename}")
	try:
		ok:bool = False
		print(files)
		if flag == '0':
			if file.filename != '':
				ok = add_record('users', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
			else:
				ok = add_record('users', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level)
			msg:str = "New User Registered!" if ok else "Error Registering User!"			
		else:
			if file.filename != '':
				ok = update_record('users', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
			else:
				ok = update_record('users', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level)
			msg:str = "User Updated successfully!" if ok else "Error Updating User!"
		file.save(imagename)
		flash(f"Registration.db: {msg}")
	except Exception as e:
		flash(f"File Saving Error: {e}")
		print(e)
	return redirect('/')

@app.route('/delete_user', methods=['POST'])
def delete_user():
	idno:str = request.form['idno']
	imagename:str = get_user(idno)[0]['image']
	# print(imagename)
	ok:bool = delete_record('users', idno=idno)
	message:str = "User Delete: User deleted successfully!" if ok else "Error Deleting User: Something went wrong"
	try:
		if os.path.exists(imagename):
			os.remove(imagename)
	except Exception as e:
		flash(f"Error within '/delete_user': File path error")
	flash(message)
	return redirect('/')

@app.route('/')
def index():
	return render_template('index.html', pagetitle='Registration', users=get_users())

if __name__ == '__main__':
	app.run(debug=True)
	