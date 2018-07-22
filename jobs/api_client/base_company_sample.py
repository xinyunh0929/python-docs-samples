#!/usr/bin/env python

# Copyright 2018 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import string

# [START jobs_instantiate]
from googleapiclient.errors import Error

import pprint
import json
import httplib2

from apiclient.discovery import build_from_document
from apiclient.http import build_http
from oauth2client.service_account import ServiceAccountCredentials
import os

scopes = ['https://www.googleapis.com/auth/jobs']
credential_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    credential_path, scopes)

http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
http = credentials.authorize(http=build_http())
content = open("/usr/local/google/home/xinyunh/discovery/talent_public_discovery_v3_distrib.json",'r').read()
discovery = json.loads(content)

client_service = build_from_document(discovery, 'talent', 'v3', http=http)
parent = 'projects/' + os.environ['GOOGLE_CLOUD_PROJECT']

# [END jobs_instantiate]


# [START jobs_basic_company]
def generate_company():
    # external id should be a unique Id in your system.
    external_id = 'company:' + ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(16))

    display_name = 'Google'
    headquarters_address = '1600 Amphitheatre Parkway Mountain View, CA 94043'

    company = {
        'display_name': display_name,
        'external_id': external_id,
        'headquarters_address': headquarters_address
    }
    print('Company generated: %s' % company)
    return company
# [END jobs_basic_company]


# [START jobs_create_company]
def create_company(client_service, company_to_be_created):
    try:
        request = {'company' : company_to_be_created}
        company_created = client_service.projects().companies().create(
            parent=parent, body=request).execute()
        print('Company created: %s' % company_created)
        return company_created
    except Error as e:
        print('Got exception while creating company')
        raise e
# [END jobs_create_company]


# [START jobs_get_company]
def get_company(client_service, company_name):
    try:
        company_existed = client_service.projects().companies().get(
            name=company_name).execute()
        print('Company existed: %s' % company_existed)
        return company_existed
    except Error as e:
        print('Got exception while getting company')
        raise e
# [END jobs_get_company]


# [START jobs_update_company]
def update_company(client_service, company_name, company_to_be_updated):
    try:
        request = {'company' : company_to_be_updated}
        company_updated = client_service.projects().companies().patch(
            name=company_name, body=request).execute()
        print('Company updated: %s' % company_updated)
        return company_updated
    except Error as e:
        print('Got exception while updating company')
        raise e
# [END jobs_update_company]


# [START jobs_update_company_with_field_mask]
def update_company_with_field_mask(client_service, company_name,
                                   company_to_be_updated, field_mask):
    try:
        request = {
        'company' : company_to_be_updated,
        'update_mask' : field_mask
        }
        company_updated = client_service.projects().companies().patch(
            name=company_name,
            body=request).execute()
        print('Company updated: %s' % company_updated)
        return company_updated
    except Error as e:
        print('Got exception while updating company with field mask')
        raise e
# [END jobs_update_company_with_field_mask]


# [START jobs_delete_company]
def delete_company(client_service, company_name):
    try:
        client_service.projects().companies().delete(name=company_name).execute()
        print('Company deleted')
    except Error as e:
        print('Got exception while deleting company')
        raise e
# [END jobs_delete_company]


def run_sample():
    # Construct a company
    company_to_be_created = generate_company()

    # Create a company
    company_created = create_company(client_service, company_to_be_created)

    # Get a company
    company_name = company_created.get('name')
    get_company(client_service, company_name)

    # Update a company
    company_to_be_updated = company_created
    company_to_be_updated.update({'website_uri': 'https://elgoog.im/'})
    update_company(client_service, company_name, company_to_be_updated)

    # Update a company with field mask
    update_company_with_field_mask(
        client_service, company_name, {
            'displayName': 'changedTitle',
            'externalId': company_created.get('externalId')
        }, 'displayName')

    # Delete a company
    delete_company(client_service, company_name)


if __name__ == '__main__':
    run_sample()
