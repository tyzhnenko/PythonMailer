from setuptools import setup, Command

version = __import__('PythonMailer').__version__

setup(
    name = "PythonMailer",
    version = version,
    url = 'https://github.com/tyzhnenko/PythonMailer/',
    author = 'Tyzhnenko Dmitry',
    author_email = 't.dmitry@gmail.com',
    maintainer = 'Tyzhnenko Dmitry',
    maintainer_email = 't.dmitry@gmail.com',
    description = 'Mail creator and sender for Python like PHPMailer',
    license = "GPLv3",
    packages = ['PythonMailer'],
)
