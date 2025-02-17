from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Click(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    link = db.Column(db.String(200), nullable=False)
    count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Click {self.id}: {self.count}>'