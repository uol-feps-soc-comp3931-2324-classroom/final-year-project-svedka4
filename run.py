from app import app, db

def create_database():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_database()
    app.run(debug=True)