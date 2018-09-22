from setuptools import setup, find_packages


setup(
    name='mkdocs-awesome-pages-plugin',
    version='2.0.0',
    description='An MkDocs plugin that simplifies configuring page titles and their order',
    long_description='The awesome-pages plugin allows you to customize how your pages show up the navigation of your '
                     'MkDocs without having to configure the full structure in your ``mkdocs.yml``. It gives you '
                     'detailed control using a small configuration file directly placed in the relevant directory of '
                     'your documentation. See `Github <https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin>`_ '
                     'or the README.md for more details.',
    keywords='mkdocs python markdown wiki',
    url='https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/',
    author='Lukas Geiter',
    author_email='info@lukasgeiter.com',
    license='MIT',
    python_requires='>=3.5',
    install_requires=[
        'mkdocs>=1'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(exclude=['*.tests', '*.tests.*']),
    entry_points={
        'mkdocs.plugins': [
            'awesome-pages = mkdocs_awesome_pages_plugin.plugin:AwesomePagesPlugin'
        ]
    }
)
