from distutils.core import setup

setup(
    name='screenutils',
    version='0.0.1.3.2',
    packages=['screenutils',],
    license='GNU Public License >=2 (ask me if you want other)',
    author="Christophe Narbonne",
    author_email="@Christophe31",
    url="http://github.com/Christophe31/screenutils",
    description =
    "Handle gnu-screen: creates/close/list/log sessions, injects commands...",
    long_description=open('README.rst').read(),
)

