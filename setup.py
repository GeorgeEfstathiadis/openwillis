# author:    Vijay Yadav
# website:   http://www.bklynhlth.com

import setuptools

with open('requirements.txt') as fp:
    install_requires = fp.read()

#Long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='openwillis',
                 version='0.3',
                 description='digital health measurement',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='https://github.com/bklynhlth/openwillis',
                 author='bklynhlth',
                 python_requires='>=3.6.*',
                 install_requires=install_requires,
                 author_email='admin@bklynhlth.com',
                 packages=setuptools.find_packages(),
                 zip_safe=False,
                 license='Apache',
                 project_urls={
                     "Documentation": "",
                     "Source Code": "https://github.com/bklynhlth/openwillis",
                     "Bug Tracker": "https://github.com/bklynhlth/openwillis/issues",
                 }
                )