import requests

from urllib.parse import urlencode

class Model_Api():

    list_static_parameters = None
    list_result = None
    
    def get(self, host, url_additional_path, secure_url=True):
        static_parameter_string = None
        if host is None:
            return None
        if type(host) is not (str):
            return None
        if url_additional_path:
            if type(url_additional_path) is not (str):
                return None
        url = host.replace('https://', '').replace('http://', '')
        url =  f"https://{url}" if secure_url else f"http://{url}"
        if self.list_static_parameters:
            static_parameter_string = ''
            for param in self.list_static_parameters:
                static_parameter_string += urlencode(param) + "&"
        url += url_additional_path + static_parameter_string
        response = requests.get(url)
        if response:
            if response.status_code == 200:
                return response.json()
        return None

    def url_parameters_add(self, dict_static_parameters):
        if dict_static_parameters is None:
            return None
        elif type(dict_static_parameters) is not dict:
            return None
        try:
            if self.list_static_parameters is None:
                self.list_static_parameters = []
            self.list_static_parameters.append(dict_static_parameters)
        except:
            print('Error while adding a static parameter to the list.')

    def recursively_content_json(self, json_dict, key=None):
        if type(json_dict) is dict and json_dict:
            for key in json_dict:
                self.recursively_content_json(json_dict[key], key)
        elif type(json_dict) is list and json_dict:
            for entity in json_dict:
                self.recursively_content_json(entity)
        else:
            if self.list_result is None:
                        self.list_result = []
            self.list_result.append({f"{key}":f"{json_dict}"})      

