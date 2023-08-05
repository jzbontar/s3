from distutils.core import setup

setup(
    name="s3",
    version="1.0",
    entry_points={
        "console_scripts": ["s3=s3:main"],
    },
    install_requires=["awscli"],
)
