from setuptools import setup, find_packages

setup(
    name='Simple Habit Tracker',
    version='0.1',
    author='Eszes Bálint',
    author_email='eszes.balint96@gmail.com',
    url='',
    packages=find_packages(),
    package_dir={'habit': 'habit'},
    install_requires=[
        'flask',
        'flask-wtf',
        'flask-sqlalchemy',
        'email-validator',
        'flask-bcrypt',
        'flask-login',
        'eventlet',
        'flask-socketio'
    ],
)
