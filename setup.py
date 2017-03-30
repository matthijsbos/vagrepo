import setuptools

setuptools.setup(
    name='vagrepo',
    version='0.1',
    packages=['vagrepo'],
    entry_points={
        'console_scripts': [
            'vagrepo=vagrepo:main'
        ]
    }
)