from setuptools import setup

setup(
    name='envoy_listener_discovery',
    packages=['envoy_listener_discovery'],
    include_package_data=True,
    install_requires=[
        'flask-marshmallow',
        'flask'
    ],
)
