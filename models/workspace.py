from extensions import db

class Workspace(db.Model):
    __tablename__ = 'workspace'
    
    id = db.Column(db.Integer, primary_key=True) # automatic id from the database
    name = db.Column(db.String(100), nullable=False)# name of the workspace
    user_limit = db.Column(db.Integer())# capacity of workspace
    available_from = db.Column(db.Time())# time from when it's available to start booking the workspace (16 [datetime])
    available_till = db.Column(db.Time()) # the workspace is available for booking up until this time (21 [datetime])
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

    

    