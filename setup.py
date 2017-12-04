from setuptools import setup

setup(
    name='envoy_discovery_service',
    packages=['envoy_discovery_service'],
    include_package_data=True,
    install_requires=[
        'flask-marshmallow',
        'flask'
    ],
)
