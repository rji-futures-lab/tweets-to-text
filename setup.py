import io
from setuptools import find_packages, setup


with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()


setup(
    name='tweets2text',
    version='0.1.0',
    url='https://github.com/rji-futures-lab/tweets-to-text',
    license='MIT',
    maintainer='RJI Futures Lab',
    maintainer_email='gordonj@rjionline.org',
    description='TweetsToText is a bot that collects your live tweets into '
                'plain textfiles.',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'python-dotenv',
        'twitterapi',
        'zappa',
    ],
)
