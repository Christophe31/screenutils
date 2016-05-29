from distutils.core import setup

setup(
    name='screenutils',
    version='0.0.1.5.5',
    packages=['screenutils',],
    license='GNU Public License >=2 (ask me if you want other)',
    author="Christophe Narbonne",
    author_email="@Christophe31",
    url="http://github.com/Christophe31/screenutils",
    description =
    "lib for gnu-screen: creates/close/list/log sessions, injects commands...",
    classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=open('README.rst').read(),
)

