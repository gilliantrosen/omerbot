from setuptools import setup, find_packages

setup(
    name='omerbot',
    version="0.0.0",
    description='Discord bot that reminds you to count the omer.',
    long_description='Discord bot that reminds you to count the omer.',
    long_description_content_type='text/markdown',
    url='https://github.com/gilliantrosen/omerbot',
    author_email='gilliantrosen@gmail.com',
    author='G Rosen',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords='omer jewish discord bot',
    install_requires=['discord.py'],
)
