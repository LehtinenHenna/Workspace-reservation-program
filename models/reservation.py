from extensions import db

class Reservation(db.Model):
    __tablename__ = 'reservation'
    
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)
    workspace_id = db.Column(db.Integer(), db.ForeignKey("workspace.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    @classmethod
    def get_all_future_reservations(cls, today): # today = datetime.datetime.now() resource methodin JSONiin
        return cls.query.filter_by(start_time>=today).all()

    @classmethod
    def get_all_reservations_by_workspace_id(cls, workspace_id, today): # today = datetime.datetime.now() resource methodin JSONiin
        return cls.query.filter_by(id=workspace_id, start_time>=today).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()