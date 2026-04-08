from setuptools import setup

setup(
    name = 'otp',
    version = '0.1.0',
    packages = ['otp'],
    entry_points = {
        'console_scripts': [
            'otp = otp.__main__:main'
        ]
    })