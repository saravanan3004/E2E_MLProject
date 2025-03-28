from setuptools import find_packages,setup
from typing import List
Hypen_e_dot = '-e .'

def get_requirement(file_path:str)->List[str]:
    '''
    This function will return the list of requirement
    '''
    requirement=[]
    with open(file_path) as file_obj:
        requirement=file_obj.readlines()
        requirement = [req.replace('\n'," ") for req in requirement]

        if (Hypen_e_dot) in requirement:
            requirement.remove(Hypen_e_dot)
    return requirement

setup(
    name = 'E2E ML Project',
    version = '0.0.1',
    author='Saravanan',
    author_email='sarausa045@gmail.com',
    packages=find_packages(),
    requires=get_requirement('requirement.txt')
)