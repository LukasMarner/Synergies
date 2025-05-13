import time

import requests
import json


class Pipeline:
    def __init__(self, token: str, upload_url: str = None, monitor_url: str = None, retrieval_url: str = None):
        self.upload_url = upload_url
        self.monitor_url = monitor_url
        self.retrieval_url = retrieval_url
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-TOKEN': token
        }

    """
    :param
    payload: The actual data to be uploaded
    wait_for_confirmation: Waits until the uploaded data execution is completed
    confirmation_sleep: seconds to sleep between checking the upload status
    confirmation_attempts: number of attempts to check the upload status before giving up
    retry_on_fail: resends payload on status code 429: Too Many Requests
    :return
    On success: execution ID
    On failure: None 
    """
    def upload(self, payload: list, wait_for_confirmation: bool = False, confirmation_sleep: int = 1, confirmation_attempts: int = 5, retry_on_fail: bool = False):
        if self.upload_url is None:
            raise Exception('upload_url is None')
        try:
            response = requests.post(self.upload_url,
                                     headers=self.headers,
                                     data=json.dumps(payload))
            if response.status_code == 201:
                execution_id = response.json().get('executionId')
                if wait_for_confirmation:
                    confirmed = False
                    counter = 0
                    while not confirmed:
                        time.sleep(confirmation_sleep)
                        if counter >= confirmation_attempts:
                            return execution_id
                        status = self.check_status(execution_id)
                        if status is not None:
                            if status['status'] == 'completed':
                                confirmed = True
                            else:
                                print('Waiting for confirmation')
                        else:
                            print(f"Status check failed for executionId: {execution_id}")
                        counter += 1
                return execution_id
            elif response.status_code == 429 and retry_on_fail:
                time.sleep(15)
                result = self.upload(payload, wait_for_confirmation, confirmation_sleep, False)
                if result is not None:
                    return result
                return None
            else:
                print(f"Upload failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception during upload: {str(e)}")
            return None


    """
    :param
    execution_id: The execution ID when new upload is created
    :return
    On success: execution data
    On failure: None
    """
    def check_status(self, execution_id: str):
        if self.monitor_url is None:
            raise Exception('monitor_url is None')
        status_url = f'{self.monitor_url}{execution_id}/status'
        response = requests.get(url=status_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f'Status check failed for executionId: {execution_id}. Status code: {response.status_code}')
            return None


    """
    :param
    params: query parameters
    :return:
    On success: query data
    On failure: None
    """
    def retrieve(self, params: dict):
        try:
            response = requests.get(self.retrieval_url, params=params, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print('Exception during retrieval, status code:', response.status_code)
                return None
        except Exception as e:
            print(f"Exception during retrieval: {str(e)}")
            return None
