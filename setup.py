from distutils.core import setup

setup(
    name='linguistic-helper-functions',
    version='0.1.22',
    author='Michael McAuliffe',
    author_email='michael.e.mcauliffe@gmail.com',
    packages=['linghelper','linghelper.media'],
    url='http://pypi.python.org/pypi/linguistic-helper-functions/',
    license='LICENSE.txt',
    description='',
    long_description=open('README.md').read(),
    install_requires=['numpy'],
)
