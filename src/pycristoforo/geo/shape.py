import numpy.random as numpy_random
import shapely.geometry as geom_shapely
import src.pycristoforo.geo.eucountries as eucountries_py
import src.pycristoforo.utils.constants as constants_py
import json


def generate_random(shape, points: int, country: str) -> list:
    """
    It generates 'points' (ex. 1, 5, 10, 1000) random latitude-longitude pairs
    :param shape: shape in which you want to fit your geolocations . Polygon and MultiPolygon are the only shapes accepted
    :param points: how many random latitude-longitude pairs do you want to generate
    :param country: country name
    :return: list of features (geojson) containing the random points generated by the method
    """

    # getting min, max lat/lng
    min_lng = get_min_lng(shape)
    min_lat = get_min_lat(shape)
    max_lng = get_max_lng(shape)
    max_lat = get_max_lat(shape)

    # supporting variables
    counter = 0
    tot = 0

    list_of_points = []

    # random point generation
    while counter != points:
        tot += 1
        # generate random float between [min_lng, max_lng)
        val1 = numpy_random.uniform(min_lng, max_lng)
        # generate random float between [min_lat, max_lat)
        val2 = numpy_random.uniform(min_lat, max_lat)

        # Point var created
        random_point = geom_shapely.Point(val1, val2)

        # checking if the generated point is withing the shape passed as input
        if random_point.within(shape):
            ran_point = '{"type": "Feature",' \
                '"geometry": '\
                '{"type": "Point",'\
                '"coordinates": ['+str(val1)+','+str(val2)+\
                ']},"properties": {"point": "'\
                + str(counter+1)+'","country": "'+country+'"}}'
            list_of_points.append(json.loads(ran_point))
            counter += 1

    #print(f"Tentative {tot}, fair {counter}. Rate {round((counter/tot)*100,2)}")

    return list_of_points


def setup_shape(key: str):
    """
    This method returns the shape (or shapes) as 'Polygon' or 'MultyPoligon' type
    :param key: country ISO2 code/ISO3 code/name/FIPS code
    :return: the shape as Polygon or Multipolygon
    """

    # importing geojson file
    country_ids = eucountries_py.EUCountryList(constants_py.Constants.EU_PATH)
    uid = country_ids.get_by_key(key)
    shape_dict = country_ids.get_by_key(uid)

    # list of poligons (only used for MultiPolygon)
    poligons = []
    if shape_dict['type'] == "MultiPolygon":
        for polygon in shape_dict['coordinates']:
            for sub_polygon in polygon:
                pol = geom_shapely.Polygon(sub_polygon)
                poligons.append(pol)
        shape = geom_shapely.MultiPolygon(poligons)
    else:
        if shape_dict['type'] == "Polygon":
            shape = geom_shapely.Polygon(shape_dict['coordinates'][0])
        else:
            raise Exception('Error occurred during setting up the shape')

    return shape


def get_min_lat(shape):
    """
    It returns the minimum latitude given a shape
    :param shape: country shape
    :return: the min latitude
    """
    return shape.bounds[1]


def get_min_lng(shape):
    """
    It returns the minimum longitude given a shape
    :param shape: country shape
    :return: the min longitude
    """
    return shape.bounds[0]


def get_max_lat(shape):
    """
    It returns the maximum latitude given a shape
    :param shape: country shape
    :return: the max latitude
    """
    return shape.bounds[3]


def get_max_lng(shape):
    """
    It returns the maximum longitude given a shape
    :param shape: country shape
    :return: the max longitude
    """
    return shape.bounds[2]
