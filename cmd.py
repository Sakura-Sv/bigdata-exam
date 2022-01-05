import os

from app import create_app, db

app = create_app(os.getenv("FLASK_CONFIG", "development"))


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, app=app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
