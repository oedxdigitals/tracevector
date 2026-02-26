from setuptools import setup, find_packages

setup(
    name="tracevector",
    version="2.5.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "tvx=tvx.main:main"
        ]
    },
)
