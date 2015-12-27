import os.path
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, "README.md")).read()
    CHANGES = open(os.path.join(here, "CHANGES.md")).read()
except IOError:
    README = CHANGES = ""

setup(
    name="trac-mattermost", version="0.1",
    description="Trac notifications in Mattermost",
    long_description=README + "\n\n" + CHANGES,
    author="Truveris Inc.",
    author_email="engineering@truveris.com",
    url="http://github.com/truveris/trac-mattermost",
    packages=find_packages(exclude=["*.tests*"]),
    license="ISC License",
    install_requires=[
        "requests",
    ],
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Framework :: Trac",
        "Topic :: Software Development :: Bug Tracking",
    ],
    entry_points = {
        "trac.plugins": [
            "trac_mattermost = trac_mattermost",
        ],
    },
)
