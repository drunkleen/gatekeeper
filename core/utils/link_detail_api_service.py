import json
import requests

from core.models import Subscription, PanelConnection


def byte_to_gigabytes(byte):
    gigabytes = byte / (1024 ** 3)
    return gigabytes


headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
PATH_API_alireza = "/xui/API/inbounds/"
PATH_API_MHSANAEI = "/panel/api/inbounds"

PATH_GET_TRAFFIC = 'getClientTraffics/'


# def get_user_info(panel_url: str, email: str, panel_name: str, panel_username: str, panel_password: str):
def get_user_info(link: Subscription):
    session = requests.Session()

    if link.panel_connection.panel_name == PanelConnection.panel_marzban:
        response = requests.get(link.subscription_link)
        if response.status_code == 200:
            response = response.headers['subscription-userinfo'].split("; ")
            data = {}

            for pair in response:
                key, value = pair.split("=")
                data[key] = int(value) if value.isdigit() else value

            data['download'] = str(byte_to_gigabytes(data.get('download'))) + " GB"
            data['upload'] = str(byte_to_gigabytes(data.get('upload'))) + " GB"
            data['total'] = str(byte_to_gigabytes(data.get('total'))) + " GB"
            return data
        else:
            return None

    body = {"username": link.panel_connection.panel_user, "password": link.panel_connection.panel_password}
    session.post(f"{link.panel_connection.panel_url}/login", data=json.dumps(body), headers=headers)

    if link.panel_connection.panel_name == PanelConnection.panel_alireza:
        response = session.get(
            f"{link.panel_connection.panel_url}{PATH_API_alireza}{PATH_GET_TRAFFIC}{link.assigned_to.email}",
            headers=headers
        )
    elif link.panel_connection.panel_name == PanelConnection.panel_sanaei:
        response = session.get(
            f"{link.panel_connection.panel_url}{PATH_API_MHSANAEI}{PATH_GET_TRAFFIC}{link.assigned_to.email}",
            headers=headers
        )
    else:
        return None

    if response.status_code == 200:
        return {
            'upload': json.loads(response.text)['obj']['up'],
            'download': json.loads(response.text)['obj']['down'],
            'total': json.loads(response.text)['obj']['total'],
            'expire': json.loads(response.text)['obj']['expiryTime'],
        }
    else:
        return None
