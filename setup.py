try:
    from setuptools import setup, find_packages
except ImportException:
    from distutils.core import setup

setup(
    name="check-es",
    version="1.1.1",
    license="GPLv3",
    description="Elasticsearch check tool for Nagios and ZenOSS",
    author="Josten Landtroop",
    author_email="j@no-io.net",
    maintainer="Josten Landtroop",
    download_url="https://bitbucket.org/josten/check-es",
    url="https://bitbucket.org/josten/check-es",
    packages= find_packages(),
    scripts = ["check-es"],
    install_requires=["ipaddress"]
    )
