from setuptools import setup

# setup for gradls
setup(
    name="smokesim",
    version="0.0.1",
    packages=["smokesim"],
    install_requires=[
        "numpy",
        "pygame==2.5.2",
        "pygame_gui==0.6.9",
        # "mediapipe==0.10.14",
        "black==24.4.2",
        "pydantic==2.7.1",
        "opencv-python<4.10.0",
    ],
    author="Ramkrishna Acharya(QViper)",
    author_email="qramkrishna@gmail.com",
    description="A package for doing smoke simulation.",
    url="https://github.com/q-viper/SmokeSim",
)
