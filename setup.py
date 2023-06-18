from setuptools import setup

VERSION = "1.0"


with open("README.md") as f:
    ldesc = f.read()


setup(
        name='shellbind',
        version=VERSION,
        license='GPL-3.0',
        author="Hydr0nium/Sol",
        scripts=["shellbind.py"],
        description="Shellbinding to Webshell",
        long_description=ldesc,
        long_description_content_type="text/markdown",
        install_requires=['nclib>=1.0.2', 'Requests>=2.28.2'],
        url="https://github.com/hydr0nium/shellbind"
)
