from extensions import db

class Reservation(db.Model):
    __tablename__ = 'reservation'
    
    id = db.Column(db.Integer(), primary_key=True)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)
    workspace_id = db.Column(db.Integer(), db.ForeignKey("workspace.id"))
    username = db.Column(db.String(), db.ForeignKey("user.username")) 

    @classmethod
    def get_all_future_reservations(cls, today): # today = datetime.datetime.now() resource methodin JSONiin
        return cls.query.filter_by(start_time=today).all()

    @classmethod
    def get_all_reservations_by_workspace_name(cls, workspace_name, today): # today = datetime.datetime.now() resource methodin JSONiin
        return cls.query.filter_by(id=workspace_name, start_time=today).all()

    @classmethod    # ei toimi vielä
    def get_all_by_user(cls, username):
        return cls.query.filter_by(username=username).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
