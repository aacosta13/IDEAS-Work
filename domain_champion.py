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


def retrieve_file_info(uname, pwd):
    commitfile = open('commit_info.txt', 'w')
    commitfile.write('Repository Name/Top Committer/Commit Files Affected')
    print(file=commitfile)

    data = {'Repository': [],
            'Committer': [],
            'Commit Files Touched': []}

    for project in project_dict:
        print(' ', file=commitfile)
        commit_url = 'https://api.github.com/repos/%s/commits' % project_dict[project]
        contributor_url = 'https://api.github.com/repos/%s/contributors' % project_dict[project]

        commit_response = requests.get(commit_url, auth=(uname, pwd))
        commit_json_response = commit_response.json()
        contributor_response = requests.get(contributor_url, auth=(uname, pwd))
        contributor_json_response = contributor_response.json()

        item_count = 0
        page_no = 1
        max_page = False
        # Parse through JSON response of API for author
        while not max_page:
            for item in commit_json_response:
                if item['author'] is None:
                    item_count += 1
                    continue

                # If commit belongs to top dev, analyze the files here
                if item['author']['login'] == contributor_json_response[0]['login']:
                    individual_commit_url = 'https://api.github.com/repos/%s/commits' % project_dict[project] \
                                            + '/' + str(item['sha'])
                    individual_commit_response = requests.get(individual_commit_url, auth=(uname, pwd))
                    individual_json_response = individual_commit_response.json()

                    print('-----------------------------------')
                    print('Developer: ', contributor_json_response[0]['login'])
                    print('')
                    print("Files modified by commit:")

                    for file in individual_json_response['files']:
                        print(file['filename'])
                item_count += 1

            if item_count == 30:
                page_no += 1
                commit_url += '?&page=%s' % str(page_no)
                commit_response = requests.get(commit_url, auth=(uname, pwd))
                commit_json_response = commit_response.json()
                item_count = 0

            else:
                max_page = True


if __name__ == '__main__':
    username = input('GitHub Authentication Username: ')
    password = input('Password: ')
    retrieve_repo_info(username, password)
    retrieve_file_info(username, password)
