import hashlib
import json
from datetime import datetime

import requests

from AssignmentTimeframe import AssignmentTimeframe
from Feed import Feed
import FeedItem
# EKooli Endpointid
API_URL = 'https://postikana.ekool.eu/rest/json'
SERVER_ROOT_URL = 'https://ekool.eu/'
REACTIONS_API_URL = 'https://api.ekool.eu/v1'
MESSAGING_API_URL = 'https://messaging.ekool.eu/'
MESSAGING_WEB_SOCKET = 'wss://messaging.ekool.eu/messaging_websocket:8020/'
SMARTID_URL = "https://login.ekool.eu/smart-id/"
SMARTID_CHECK_URL = "https://login.ekool.eu/smart-id/check-status"
DWR_URL = "https://ekool.eu/dwr/call/plaincall/"

def format_date_for_ekool(date):
    # 05.01.2020

    date_str = str(date.day).zfill(2) + "." + str(date.month).zfill(2) + "." + str(date.year)
    return date_str


def get_absences(access_token, student_id):
    return data_miner_with_cache(pathElements=['absences90Days', student_id], access_token=access_token)


def get_feed_item(event_id, access_token, student_id):
    return data_miner_with_cache(['feeditem', student_id, event_id], access_token=access_token)


def get_feed(student_id):
    return Feed(data_miner_with_cache(['feed', student_id]))

def get_grades(student_id):
    feed = get_feed(student_id)
    for i, FeedItem in enumerate(feed.feed):
        print(FeedItem)

    #return data_miner_with_cache(pathElements=['feed', student_id, 'grades'], access_token=access_token)

def get_assignments_for_timeframe(startingDate, endDate, access_token, student_id):
    starting_str = format_date_for_ekool(startingDate)
    end_str = format_date_for_ekool(endDate)

    raw_data = data_miner_with_cache(
        pathElements=['todolist', str(student_id), starting_str, end_str], apiUrl=API_URL, access_token=access_token)

    return AssignmentTimeframe(raw_data)


def get_person_data(access_token):
    person_info = data_miner_with_cache(pathElements=['person'], apiUrl=API_URL,
                                        access_token=access_token)
    # student_id = str(person_info["roles"][0]["studentId"])
    return person_info


def get_parents(access_token):
    '''
     {'students': [{'name1': 'NAME', 'name2': 'LASTNAME', 'profileImgFn': 'REDACTED'}], 'parents': [{'name1': 'PARENTNAME', 'name2': 'PARENTLASTNAME', 'profileImgFn': None}, {'name1': 'PARENTNAME', 'name2': 'PARENTLASTNAME', 'profileImgFn': None}]}
    :return:
    '''
    parents = data_miner_with_cache(pathElements=['family'], apiUrl=API_URL, access_token=access_token)[
        "parents"]
    return parents


def bot_login(username, password):
    query_base = {'grant_type': 'password', 'client_id': 'mKool', 'username': username, 'password': password}

    headers = {
        'Authorization': 'Basic bUtvb2w6azZoOTdoYWZzcnZvbzNzZDEzZ21kdXE4YjZ0YnM1czE2anFtYTZydThmajN0dWVhdG5lOGE4amxtN2Jt',
        'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.post(SERVER_ROOT_URL + 'auth/oauth/token', data=query_base, headers=headers)
    login_state = r.json()
    if r.status_code is 200:
        return {"logged_in": True, "access_token": login_state["access_token"],
                "refresh_token": login_state["refresh_token"]}
    else:
        return {"logged_in": False}


def data_miner_with_cache(access_token, pathElements, apiUrl=API_URL):
    key = ''
    for element in pathElements:
        key += '/' + str(element)
    query_base = stampTheBase(get_query_base())
    headers = {"Authorization": "Bearer " + access_token, 'Content-Type': 'application/json;charset=UTF-8'}
    r = requests.post(apiUrl + key, data=json.dumps(query_base), headers=headers)
    if r.status_code is 200:
        return r.json()
    else:
        None


def get_query_base():
    return {'langCode': 'ru', 'version': "4.6.6", 'deviceId': "1234567", 'userAgent': "Google Chrome", 'checksum': None,
            'pushType': '1', 'localTime': str(int(datetime.timestamp(datetime.now()))), 'gradePush': True,
            'absencePush': True, 'noticePush': True, 'todoPush': True, 'messagePush': True}


def stampTheBase(query_base):
    str = ''
    str += query_base['langCode'] or ''
    str += query_base['version'][::-1] or ''
    str += query_base['deviceId'] or ''
    str += query_base['userAgent'] or ''
    str += query_base['pushType'] or ''
    str += query_base['version'] or ''
    str += query_base['localTime'] or ''
    query_base["checksum"] = hashlib.md5(str.encode('utf-8')).hexdigest()
    return query_base
