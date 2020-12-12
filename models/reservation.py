from extensions import db

class Reservation(db.Model):
    __tablename__ = 'reservation'
    
    id = db.Column(db.Integer(), primary_key=True)
    start_time = db.Column(db.DateTime(), nullable=False)
    end_time = db.Column(db.DateTime(), nullable=False)
    workspace_id = db.Column(db.Integer(), db.ForeignKey("workspace.id"), nullable=False)
    username = db.Column(db.String(), db.ForeignKey("user.username"))
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_all_reservations(cls): 
        return cls.query.filter_by().all()

    @classmethod
    def get_all_reservations_by_workspace_id(cls, workspace_id):  # poistin today parametrin tästä, koska varmistukset siitä että varaus on tulevaisuudessa on parempi tehdä resurssien metodeissa
        return cls.query.filter_by(workspace_id=workspace_id).all()

    @classmethod   
    def get_all_by_user(cls, username):
        return cls.query.filter_by(username=username).all()

    @classmethod
    def get_by_id(cls, reservation_id):
        return cls.query.filter_by(id=reservation_id).first()

    #def __setitem__(self, index, value):
    
                                                    # nämä tarvitaan ehkä iterointiin?
    #def __getitem__(self,index):  

    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
