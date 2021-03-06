import os
import requests
from datetime import date
import json
from urllib.parse import urljoin


def fetch_data():

    api = {
        'creds': {
            'username': 'rd_dreams',
            'password': 'djT6LasE',
        },
        'url': "https://robot-dreams-de-api.herokuapp.com",
        'headers_auth':
            {
                'content-type': "application/json"
            },
        'headers_get':
            {
                'authorization': "",
                'content-type': "application/json"
            },
    }
    loading_dates = {
        'date': "2021-12-14"
    }

    url_auth = urljoin(api['url'], "/auth")

    api_jwt = requests.post(
                        url_auth,
                        headers=api["headers_auth"],
                        data=json.dumps(api["creds"]
                    )
                ).json().get("access_token")

    # print(f"API jwt: {api_jwt}")
    api["headers_get"]["authorization"] = "JWT {}".format(api_jwt)

    url_get = api['url'] + "/out_of_stock"

    _headers = {
        'authorization': 'JWT {}'.format(api_jwt),
        'content-type': "application/json"
    }

    response = requests.get(
                    url_get,
                    headers=_headers,
                    data=json.dumps(loading_dates),
                    timeout=5
                )

    response.raise_for_status()

    result = response.json()

    dir_name = os.path.join('/home/user/data_' + str(date.today()))
    # '/Users/imac/Projects/data_engineering/fetch_airflow/data_'
    # /home/user/data
    os.makedirs(dir_name, exist_ok=True)


    file_name = os.path.join(dir_name, loading_dates['date']+'.txt')

    with open(file_name, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(result))
        print(f"Wrote data to file {file_name}")


if __name__ == '__main__':
    fetch_data()
