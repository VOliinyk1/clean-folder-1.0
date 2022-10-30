from setuptools import setup, find_namespace_packages

setup(name='clean-folder-1.0',
      version='1',
      description='Sort all files in folder to relative categories',
      author='Volodymyr Oliinyk',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean_folder = clean_folder.sort:main']})
