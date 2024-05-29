from setuptools import setup

# setup for gradls
setup(
    name="smokesim",
    version="0.0.1",
    packages=["smokesim"],
    install_requires=[
        "numpy",
        "pygame",
    "pygame_gui==0.6.9",
    "mediapipe",
        "black",
    ],
    author="Ramkrishna Acharya(QViper)",
    author_email="qramkrishna@gmail.com",
    description="A package for doing smoke simulation.",
    url="https://github.com/q-viper/SmokeSim",
)