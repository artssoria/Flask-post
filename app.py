from flask import Flask, request, render_template_string , jsonify
from models.article import db, Article
from models.user import User


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)

with app.app_context():
    db.create_all()

#ruta inicial
@app.route('/')
def home():
    return "hola desde flask"

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first() is not None:
        return jsonify({'error': 'El email ya está registrado'}), 400
    
    new_user = User(username = data['username'], email = data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'success': 'El usuario {new_user.username} fue registrado con éxito'}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'error': 'Credenciales inválidas'})
    
    return jsonify({'success': f'Bienvenido {user.username}'}), 200


#Listado de todos los arcticulos
@app.route('/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify([{
        'id': article.id,
        'title': article.title,
        'content': article.content
    }for article in articles])

#Crear un nuevo articulo
@app.route('/articles', methods=['POST'])
def create_article():
    data = request.get_json()
    new_article = Article(title=data['title'], content=data['content'])
    db.session.add(new_article)
    db.session.commit()
    return jsonify({
        'id': new_article.id,
        'title': new_article.title,
        'content': new_article.content
    }), 201 

#Actualizar un articulo
@app.route('/article/<int:id>', methods=['PUT'])
def update_article(id):
    article = Article.query.get_or_404(id)
    data = request.get_json()
    article.title = data['title']
    article.content = data['content']
    db.session.commit()
    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content
    })

#Eliminar un articulo
@app.route('/article/<int:id>', methods=['DELETE'])
def delete_article(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({'message': f'El articulo {article.title} fue eliminado con éxito'}), 200
#obtener un articulo
@app.route('/article/<int:article_id>', methods=['GET'])
def view_article(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content
    })
 


if __name__ == '__main__':
    app.run(debug=True)