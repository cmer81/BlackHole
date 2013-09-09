from distutils.core import setup

setup(
    name='BlackHole',
    version='4.5',
    packages=['blackhole', 'blackhole.black_hole', 'blackhole.black_hole_db', 'blackhole.black_hole_db.management',
              'blackhole.black_hole_db.management.commands', 'blackhole.black_hole_engine'],
    url='https://github.com/aenima-x/BlackHole',
    license='',
    author='Nicolas, Rebagliati',
    author_email='nicolas.rebagliati@aenima-x.com.ar',
    description='Curses ssh client made in python'
)
