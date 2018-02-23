from distutils.core import setup

setup(
    name='draft_kings_db',
    version='0.1.1',
    packages=['draft_kings_db'],
    url='',
    license='MIT',
    author='Ben Brostoff',
    author_email='ben.brostoff@gmail.com',
    description='A tool for retrieving DraftKings data.',
    install_requires=[
        'SQLAlchemy',
        'requests',
    ],
)
