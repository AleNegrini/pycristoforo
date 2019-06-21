import src.pycristoforo.utils.utils as utils_py
import src.pycristoforo.geo.key_value_pair as keyvaluepair_py


class EUCountryList:

    def __init__(self, full_path):
        """
        Inizializer method that builds the country dictionary with 'key','value' pair
        :param full_path: path where the geojson is stored
        """
        self.__country_dict = {}
        countries = utils_py.read_json(full_path)
        for elem in countries['features']:
            country = keyvaluepair_py.KeyValuePair(elem['properties']['FIPS'], elem['properties']['UN'])
            self.__country_dict[country.key] = country.value
            country = keyvaluepair_py.KeyValuePair(elem['properties']['ISO2'], elem['properties']['UN'])
            self.__country_dict[country.key] = country.value
            country = keyvaluepair_py.KeyValuePair(elem['properties']['ISO3'], elem['properties']['UN'])
            self.__country_dict[country.key] = country.value
            country = keyvaluepair_py.KeyValuePair(elem['properties']['NAME'], elem['properties']['UN'])
            self.__country_dict[country.key] = country.value
            country = keyvaluepair_py.KeyValuePair(elem['properties']['UN'], elem['geometry'])
            self.__country_dict[country.key] = country.value

    def get_by_key(self, key: str) -> int:
        try:
            return self.__country_dict[key]
        except KeyError as ex:
            print(f'No key {ex} in country dictionary')
            return None

    def get_country_dict(self):
        return self.__country_dict
