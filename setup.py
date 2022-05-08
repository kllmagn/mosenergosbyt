from distutils.core import setup
import mosenergosbyt

setup(
    name='mosenergosbyt',
    packages=['mosenergosbyt'],
    version=mosenergosbyt.__version__,
    license='MIT',
    description='API для работы с порталом Мосэнергосбыта',
    author='@kkuryshev',
    author_email='kkurishev@gmail.com',
    maintainer='Alex Bratchik',
    maintainer_email='abratchik@gmail.com',
    url='https://gitflic.ru/project/alexbratchik/mosenergosbyt.git',
    keywords=['mosenergosbyt', 'MEANINGFULL', 'KEYWORDS'],
    classifiers=[
        'Development Status :: 3 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
