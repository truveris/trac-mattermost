from setuptools import find_packages, setup

setup(
    name="TracMattermost", version="0.1",
    author="Truveris Inc.",
    author_email="engineering@truveris.com",
    url="http://github.com/truveris/trac-mattermost",
    packages=find_packages(exclude=["*.tests*"]),
    license='ISC License',
    install_requires=[
        "requests",
    ],
    entry_points = {
        "trac.plugins": [
            "trac_mattermost = trac_mattermost",
        ],
    },
)
