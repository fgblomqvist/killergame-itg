from setuptools import setup

setup(
    name='Killergame-ITG',
    version='1.1.1',
    author='Fredrik Blomqvist',
    author_email='fredrik.blomqvist.95@gmail.com',
    packages=['killergame_itg'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
    ],
)