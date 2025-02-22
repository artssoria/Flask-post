from models import db

# Modelo de bbdd
class Article(db.Model):
    __tablename__ = 'article' 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text , nullable= False)

    def __repr__(self):
        return f'<Article {self.title}>'