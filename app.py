from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace the user, password, database, and connection name with your actual Google Cloud SQL information
# Format for PostgreSQL: 'postgresql://user:password@/database?host=/cloudsql/connection_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<USER>:<PASSWORD>@/<DATABASE>?host=/cloudsql/<CONNECTION_NAME>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define models
class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=False)
    posted_at = db.Column(db.DateTime, server_default=db.func.now())

# Create the tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], email=data['email'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({"message": "Customer added successfully"}), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    customers_list = Customer.query.all()
    customers = [{"id": customer.id, "name": customer.name, "email": customer.email} for customer in customers_list]
    return jsonify(customers)

@app.route('/announcements', methods=['POST'])
def post_announcement():
    data = request.json
    new_announcement = Announcement(content=data['content'])
    db.session.add(new_announcement)
    db.session.commit()
    return jsonify({"message": "Announcement posted successfully"}), 201

@app.route('/announcements', methods=['GET'])
def get_announcements():
    announcements_list = Announcement.query.all()
    announcements = [{"id": announcement.id, "content": announcement.content, "posted_at": announcement.posted_at} for announcement in announcements_list]
    return jsonify(announcements)

if __name__ == '__main__':
    app.run(debug=True)
