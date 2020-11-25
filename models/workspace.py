from extension import db

class Workspace(db.Model):
    __tablename__ = 'workspace'
    id = db.Column(db.Integer, primary_key=True) # automatic id tietokannasta
    name = db.Column(db.Str(100), nullable=False)# tilan nimi
    user_limit = db.Column(db.Integer())# maksimi käyttäjämäärä
    available_from = db.Column(db.Time(16))# kellonaika josta lähtien varattavissa 16 [datetime]
    available_till = db.Column(db.Time(21)) # kellonaika johon asti varattavissa 21 [datetime]

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

    

    