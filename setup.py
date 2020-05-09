from setuptools import setup, find_packages

setup(
    name="brainz",
    version="1.0.0",
    description="Project for advanced system design course.",
    author="Keren Solodkin",
    packages=find_packages(),
    install_requires=[
        "click",
        "construct",
        "Flask",
        "Flask-Cors",
        "Flask-RESTful",
        "furl",
        "matplotlib",
        "numpy",
        "pika",
        "Pillow",
        "protobuf",
        "pymongo",
        "requests",
    ],
    tests_require=["pytest", "pytest-mongodb", "requests-mock", "pytest-cov", "codecov"],
)
