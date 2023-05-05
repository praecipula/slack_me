from setuptools import setup

setup(
    name='slack_me',
    version='0.1.1',    
    description='Utility to conveniently send Slack messages from python and the cli',
    url='https://github.com/praecipula/slack_me',
    author='Matt Bramlage',
    license='MIT',
    packages=['slack_me'],
    install_requires=['pyyaml'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Utility/Personal',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
    ],
)
