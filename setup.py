from setuptools import setup, find_packages

setup(
    name='ml_monitor',
    description='Monitoring of deep learning model training process',
    version='0.0.1',
    author=u'Wojciech Pratkowiecki',
    author_email='wpratkowiecki@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pydrive>=1.3.0,<2',
        'prometheus_client>=0.7.1,<1',
        'pyyaml>=5.1.2,<6',
    ],
    python_requires='>=3.6',
)
