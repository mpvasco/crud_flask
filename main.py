from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)

# Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'crudflask'



mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(userName, userPassword) VALUES(%s, %s)",(name, password))
        mysql.connection.commit()
        cur.close()
        return redirect('/read')
    return render_template('create.html')

@app.route('/read')
def read():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue:
        userDetails = cur.fetchall()
        return render_template('read.html',userDetails=userDetails)
    else:
      return 'No items'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users where userID = "+ str(id) +";")
    resultValue= cur.fetchall()
    mysql.connection.commit()
    cur.close()
    if request.method=='GET':
      return render_template('update.html', x=resultValue )

    if request.method=='POST':
      userName = request.form['name']
      cur = mysql.connection.cursor()
      query = "UPDATE users SET userName = %s WHERE userID = %s;"
      cur.execute(query, (userName, id))
      resultValue= cur.fetchall()
      mysql.connection.commit()
      cur.close()
    return redirect('/read')


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users where userID = "+ str(id) +";")
    resultValue= cur.fetchall()
    mysql.connection.commit()
    cur.close()
    if request.method=='GET':
      return render_template('delete.html', x=resultValue )

    if request.method=='POST':
      cur = mysql.connection.cursor()
      query = "DELETE FROM users WHERE userID = %s;"
      # cur.execute(query, str(id))
      cur.execute(query, (id,))
      resultValue= cur.fetchall()
      mysql.connection.commit()
      cur.close()
    return redirect('/read')




if __name__ == '__main__':
    app.run(debug=True)