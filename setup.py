import setuptools
setuptools.setup(
    name='desmos-sync',
    version='0.1',
    author='Ryan Marina',
    description='synchronize Desmos expressions between the local filesystem and the web calculator',
    packages=["desmossync"],
    entry_points = {
        "console-scripts": [ "desmos-sync=desmossync.cli.entry" ]
    },
    install_requires=[
        'setuptools',
        'websockets',
        'watchdog'
    ]
)