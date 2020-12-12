from extensions import db

class Workspace(db.Model):
    __tablename__ = 'workspace'
    
    id = db.Column(db.Integer, primary_key=True) # automatic id tietokannasta
    name = db.Column(db.String(100), nullable=False)# tilan nimi
    user_limit = db.Column(db.Integer())# maksimi käyttäjämäärä
    available_from = db.Column(db.Time())# kellonaika josta lähtien varattavissa 16 [datetime]
    available_till = db.Column(db.Time()) # kellonaika johon asti varattavissa 21 [datetime]
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    reservations = db.relationship('Reservation', backref='workspace')


    @classmethod
    def get_all(cls):
        return cls.query.all()    

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    

    