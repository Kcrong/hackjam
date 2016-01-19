import app.prob.models
from app import db

if db.session.query(app.prob.models.Prob).filter_by(title='signup').first() is None:
    p = app.prob.models.Prob()
    p.title = "signup"
    p.score = "0"
    p.key = ""
    db.session.add(p)
    db.session.commit()
