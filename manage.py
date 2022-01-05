import os

from flask_script import Manager, Shell

from app import create_app, db

config = os.getenv("FLASK_CONFIG", "default")
app = create_app(config)


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    else:
        db.session.commit()
    db.session.remove()


manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context()))


@manager.command
def test():
    """Run the Unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()