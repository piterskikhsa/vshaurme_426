from vshaurme import create_app
from vshaurme.extensions import db

app = create_app()
db.create_all(app=app)
app.run(port='5000', host='0.0.0.0')
