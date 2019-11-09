from setuptools import setup, find_packages

setup(
    name='ml_monitor',
    description='Monitoring of deep learning model training process',
    version='0.0.1',
    author=u'Wojciech Pratkowiecki',
    author_email='wpratkowiecki@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pydrive>=1.3.0,<2'
    ],
    python_requires='>=3.6',
)
