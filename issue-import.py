#!/usr/bin/env python

"""
	GitHub issue importer.

    See README.md
"""

import json
import requests
import time
from glob import iglob
from os import path
from pprint import pprint

with file('config.json') as config_file:
    config = json.load(config_file)

url_base = 'https://api.github.com'
urls = {
    'issue_create': url_base + '/repos/{0}/issues'.format(config['repository-path']),
    'issue_modify': url_base + '/repos/{0}/issues'.format(config['repository-path']) + '/{num}', # {num} will be substituted with issue number before call
}
common_headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': 'token {0}'.format(config['token']),
    'User-Agent': '{0} issue-importer UA'.format(config['repository-path']),
}

for num in range(1, config['max-issue-id'] + 1): # iterate through required issue IDs
    issue_body_filename = path.join(path.dirname(__file__), 'data', '{0}.txt'.format(num))
    issue_labels_filename = path.join(path.dirname(__file__), 'data', '{0}.labels'.format(num))
    params = {
        'open': True,
        'labels': [],
    }
    if path.isfile(issue_body_filename):
        print('Info: issue #{0} found, trying to upload it'.format(num))
        params['title'] = config['issue-title'].format(num=num)
        with file(issue_labels_filename) as labels_file:
            for label in labels_file:
                label = label.strip()
                if label == 'closed':
                    params['open'] = False
                elif label != '':
                    params['labels'].append(label)
        with file(issue_body_filename) as body_file:
            params['body'] = body_file.read()
    elif not config['preserve-issue-numbers']:
        continue
    else:
        print('Info: issue #{0} not found, trying to generate placeholder'.format(num))
        params['title'] = config['placeholder-issue-title'].format(num=num)
        params['body'] = config['placeholder-issue-body']
        params['labels'] = config['placeholder-issue-labels']
        params['open'] = False
    #pprint(params)
    headers = common_headers.copy()
    try:
        p = requests.post(urls['issue_create'], headers=headers, data=json.dumps(params))
        resp = p.json()
        if p.status_code == 201:
            print('Response status for #{0} was HTTP {1}'.format(num, p.status_code))
        else:
            print('Response status for #{0} was HTTP {1} with message: {2}'.format(num, p.status_code, resp.get('message')))
            #pprint(p.json())
        c_num = resp['number']
        if c_num != num and config['preserve-issue-numbers']:
            raise Exceprion('We were to create issue #{0}, but #{1} was created instead. Giving up.')
        elif not params['open']:
            c = requests.patch(urls['issue_modify'].format(num=c_num), headers=headers, data=json.dumps({'state': 'closed'}))
    except IOError:
        pass
    time.sleep(config['sleep-seconds'])
