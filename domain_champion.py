#!/usr/bin/env python3

'''
Small script to retrieve domain champ info from different repos. Prints to file and creates a pandas dataframe

By: Armando Acosta
'''

import requests
import pandas as pd

project_dict = {
    'Moose': 'idaholab/moose',
    'Spack': 'spack/spack',
    'yt': 'yt-project/yt',
    'petsc': 'petsc/petsc',
    'E3SM': 'E3SM-Project/E3SM',
    'lammps': 'lammps/lammps',
    'gromacs': 'gromacs/gromacs',
    'OSGConnect': 'OSGConnect/TOREVIEW-tutorial-namd',
    'QMCPACK': 'QMCPACK/qmcpack',
    'Nek5000': 'Nek5000/Nek5000',
    'nwchemgit': 'nwchemgit/nwchem',
    # 'ECP-astro': '???',
    'lanl': 'lanl/LATTE',
    'CRL': 'gridaphobe/CRL',
    'enzo-project': 'enzo-project/enzo-dev'
}


def retrieve_repo_info(uname, pword):
    devfile = open('dev_info.txt', 'w')
    devfile.write('Repository Name/Top Contributor/Number of Contributions')
    print(file=devfile)

    data = {'Repository Name': [],
            'Top Contributor': [],
            'Number of Contributions': []}

    for project in project_dict:
        # Following block for writing data to file
        print(' ', file=devfile)
        url = 'https://api.github.com/repos/%s/contributors' % project_dict[project]

        response = requests.get(url, auth=(uname, pword))
        json_response = response.json()

        print(project, file=devfile)
        print('Top Contributor:', json_response[0]['login'], file=devfile)
        print('Contributions:', json_response[0]['contributions'], file=devfile)
        print('-----------------------------------', file=devfile)

        # Following block for creating dataframe
        data['Repository Name'].append(project)
        data['Top Contributor'].append(json_response[0]['login'])
        data['Number of Contributions'].append(json_response[0]['contributions'])

    df = pd.DataFrame(data)
    print(df)


if __name__ == '__main__':
    username = input('GitHub Authentication Username: ')
    password = input('Password: ')
    retrieve_repo_info(username, password)
