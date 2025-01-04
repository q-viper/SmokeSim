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
    keywords=["smoke", "simulation"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    download_url="https://github.com/q-viper/SmokeSim/archive/refs/tags/v0.0.1.tar.gz",
)
