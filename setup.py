import setuptools

setuptools.setup(
    name="smokesim",
    packages=setuptools.find_packages(),
    use_scm_version=True,
    setup_requires=["setuptools>=42", "setuptools_scm"],
    install_requires=[
        "numpy<2",
        "pygame==2.6.1",
        "pygame_gui==0.6.9",
        "black==24.4.2",
        "pydantic==2.7.1",
        "opencv-python<4.10.0",
        "pillow",
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
    homepage="https://q-viper.github.io/SmokeSim/",
)
