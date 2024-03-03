
class Helpers():

    def list_json_exists_by_key(list, key, value):
            if list is None or key is None or value is None:
                return None
            for item in list:
                if key in item:
                    if item[key] == value:
                        return True
            return None