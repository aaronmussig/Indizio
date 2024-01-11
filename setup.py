import sys

# Check setuptools is installed
try:
    from setuptools import setup, find_packages
except ImportError:
    sys.exit('Please install setuptools before installing this package.')

setup(name='indizio-dev',
      version='0.0.1',
      # description=meta['description'],
      # long_description=readme(),
      # long_description_content_type='text/markdown',
      # author=meta['author'],
      # author_email=meta['author_email'],
      # url=meta['url'],
      # license=meta['license'],
      # project_urls={
      #     'Bug Tracker': meta['bug_url'],
      #     'Documentation': meta['doc_url'],
      #     'Source Code': meta['src_url'],
      # },
      entry_points={
          'console_scripts': [
              'indizio = indizio.__main__:main'
          ]
      },
      # classifiers=[
      #     "Development Status :: 4 - Beta",
      #     "Intended Audience :: Science/Research",
      #     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
      #     'Natural Language :: English',
      #     "Operating System :: OS Independent",
      #     "Programming Language :: Python :: 3",
      #     "Programming Language :: Python :: 3.8",
      #     "Programming Language :: Python :: 3.9",
      #     "Programming Language :: Python :: 3.10",
      #     "Topic :: Scientific/Engineering :: Bio-Informatics",
      #     "Topic :: Software Development :: Libraries :: Python Modules",
      # ],
      packages=find_packages(),
      include_package_data=True,
      install_requires=['dash', 'dash_bootstrap_components', 'dash_cytoscape', 'diskcache',
                        'dash[diskcache]', 'dash_bio', 'pydantic', 'networkx', 'orjson', 'dendropy',
                        'frozendict', 'pillow', 'pandas', 'numpy', 'tqdm', 'scipy', 'phylodm'],
      setup_requires=['setuptools'],
      python_requires='>=3.8',
      zip_safe=False,
      )
