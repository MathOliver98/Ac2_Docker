import os
from flask import Flask, render_template, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# Configurações para o MySQL
# define o nome do user
app.config['MYSQL_DATABASE_USER'] = 'root'
# define a senha
app.config['MYSQL_DATABASE_PASSWORD'] = 'mudar123'
# define o nome do DB
app.config['MYSQL_DATABASE_DB'] = 'Products'
# caso usando o docker, o ip precisar ser o da imagem do MySQL
# docker network inspect bridge
app.config['MYSQL_DATABASE_HOST'] = 'db'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/gravarProduto', methods=['POST','GET'])
def gravarAluno():
  nome = request.form['nome']
  preco = request.form['preco']
  categoria = request.form['categoria']
  if nome and preco and categoria:
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('insert into tbl_products (product_name, product_price, product_category) VALUES (%s, %s, %s)', (nome, preco, categoria))
    conn.commit()
  return render_template('index.html')


@app.route('/listar', methods=['POST','GET'])
def listar():
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute('select product_name, product_price, product_category from tbl_products')
  data = cursor.fetchall()
  conn.commit()
  return render_template('lista.html', datas=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5008))
    app.run(host='0.0.0.0', port=port)
