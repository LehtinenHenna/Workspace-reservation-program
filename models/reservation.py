from extensions import db

class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)
    workspace_id = db.Column(db.Integer(), db.ForeignKey("workspace.id"))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    @classmethod
    def get_all_future_reservations(cls):
        return cls.query.filter_by(start_time=today).all()

    @classmethod
    def get_reservations_by_workspace_id(cls, workspace_id):
        return cls.query.filter_by(id=recipe_id).first()
