import re

import responses

from quickbuild import QBClient

USERS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.User>
    <id>1</id>
    <favoriteDashboardIds>
      <long>1</long>
    </favoriteDashboardIds>
    <name>admin</name>
    <password secret="hash">0DPiKuNIrrVmD8IUCuw1hQxNqZc=</password>
    <pluginSettingDOMs/>
  </com.pmease.quickbuild.model.User>
</list>
"""

USER_INFO_XML = """<?xml version="1.0" encoding="UTF-8"?>

<com.pmease.quickbuild.model.User>
  <id>1</id>
  <favoriteDashboardIds>
    <long>1</long>
  </favoriteDashboardIds>
  <name>admin</name>
  <password secret="hash">0DPiKuNIrrVmD8IUCuw1hQxNqZc=</password>
  <pluginSettingDOMs/>
</com.pmease.quickbuild.model.User>
"""


@responses.activate
def test_get():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users'),
        content_type='application/xml',
        body=USERS_XML,
    )

    response = QBClient('http://server').users.get()
    assert len(response) == 1
    assert response[0]['id'] == '1'


@responses.activate
def test_get_info():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users/1'),
        content_type='application/xml',
        body=USER_INFO_XML,
    )

    response = QBClient('http://server').users.get_info(1)
    assert response['id'] == '1'
    assert response['name'] == 'admin'


@responses.activate
def test_get_display_name():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users/1/display_name'),
        content_type='application/xml',
        body='admin',
    )

    response = QBClient('http://server').users.get_display_name(1)
    assert response == 'admin'