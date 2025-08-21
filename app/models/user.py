
def init_user(db):
    class User(db.Model):
        id = db.Column('student_id', db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        password = db.Column(db.String(100))

        def __init__(self, name, password):
            self.name = name
            self.password = password
