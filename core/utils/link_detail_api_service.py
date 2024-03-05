import json
import requests

from core.models import Subscription, PanelConnection


def byte_to_gigabytes(byte_data):
    gigabytes = byte_data / (1024 ** 3)
    megabytes = byte_data / (1024 ** 2)
    kilobytes = byte_data / 1024

    if gigabytes >= 1:
        return f"{gigabytes:.2f} GB"
    elif megabytes >= 1:
        return f"{megabytes:.2f} MB"
    else:
        return f"{kilobytes:.2f} KB"


headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
PATH_API_alireza = "/xui/API/inbounds/"
PATH_API_MHSANAEI = "/panel/api/inbounds/"

PATH_GET_TRAFFIC = 'getClientTraffics/'


def connection_test(username, password, panel_url):
    body = {"username": username, "password": password}
    try:
        response = requests.post(f"{panel_url}/login", data=json.dumps(body), headers=headers)
        if response.status_code == 200 and response.json()['success']:
            return [response.headers['Set-Cookie'], True]

        return [None, False]
    except:
        return [None, False]


def set_new_session(session_data: Subscription):
    session_cookie, is_panel_active = connection_test(session_data.panel_connection.username,
                                                      session_data.panel_connection.password,
                                                      session_data.panel_connection.url)

    if is_panel_active:
        panel_connection = PanelConnection.objects.get(session_data.panel_connection)
        panel_connection.save()


def get_user_info(link: Subscription):
    if link.panel_connection.panel_name == PanelConnection.panel_marzban:
        response = requests.get(link.subscription_link)
        if response.status_code == 200:
            response = response.headers['subscription-userinfo'].split("; ")
            data = {}

            for pair in response:
                key, value = pair.split("=")
                data[key] = int(value) if value.isdigit() else value

            data['download'] = str(byte_to_gigabytes(data.get('download')))
            data['upload'] = str(byte_to_gigabytes(data.get('upload')))
            data['total'] = str(byte_to_gigabytes(data.get('total')))
            return data
        else:
            return None

    headers['Cookie'] = link.panel_connection.session_cookie

    if link.panel_connection.panel_name == PanelConnection.panel_alireza:
        response = requests.get(
            f"{link.panel_connection.url}{PATH_API_alireza}{PATH_GET_TRAFFIC}{link.user_email_in_xui_panel}",
            headers=headers
        )
    elif link.panel_connection.panel_name == PanelConnection.panel_sanaei:
        response = requests.get(
            f"{link.panel_connection.url}{PATH_API_MHSANAEI}{PATH_GET_TRAFFIC}{link.user_email_in_xui_panel}",
            headers=headers
        )
    else:
        return None

    if response.status_code == 200 and response.json()['success']:
        return {
            'upload': byte_to_gigabytes(json.loads(response.text)['obj']['up']),
            'download': byte_to_gigabytes(json.loads(response.text)['obj']['down']),
            'total': byte_to_gigabytes(json.loads(response.text)['obj']['total']),
            'expire': json.loads(response.text)['obj']['expiryTime'],
        }
    else:
        set_new_session(link)
        return None
