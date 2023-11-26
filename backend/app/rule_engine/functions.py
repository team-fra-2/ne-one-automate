from typing import Optional

import Levenshtein
import requests

import config
from models.one_record import LogisticsObject, ChangeRequest


def dict_to_sorted_string(d):
    return str(sorted(d.items()))


def levenshtein_distance_between_dicts(d1, d2):
    str1 = (
        dict_to_sorted_string(d1)
        .replace("true", "1")
        .replace("True", "1")
        .replace("false", "0")
        .replace("False", "0")
    )
    str2 = (
        dict_to_sorted_string(d2)
        .replace("true", "1")
        .replace("True", "1")
        .replace("false", "0")
        .replace("False", "0")
    )
    return Levenshtein.distance(str1, str2)


def ask_chatgpt(change_request: dict) -> str:
    """
    Send request to ChatGPT asking if the change request should be accepted or rejected.
    """
    return "REJECTED"


airport_to_city = {
    "LCY": "London",
    "ATL": "Atlanta",
    "PEK": "Beijing",
    "LAX": "Los Angeles",
    "DXB": "Dubai",
    "HND": "Tokyo",
    "ORD": "Chicago",
    "LHR": "London",
    "PVG": "Shanghai",
    "CDG": "Paris",
    "DFW": "Dallas/Fort Worth",
    "AMS": "Amsterdam",
    "FRA": "Frankfurt",
    "IST": "Istanbul",
    "CAN": "Guangzhou",
    "JFK": "New York",
    "SIN": "Singapore",
    "ICN": "Seoul",
    "DEN": "Denver",
    "BKK": "Bangkok",
    "DEL": "Delhi",
    "SFO": "San Francisco",
    "KUL": "Kuala Lumpur",
    "MAD": "Madrid",
    "CTU": "Chengdu",
    "LAS": "Las Vegas",
    "MIA": "Miami",
    "MUC": "Munich",
    "SYD": "Sydney",
    "BCN": "Barcelona",
    "YYZ": "Toronto",
    "LGW": "London",
    "MXP": "Milan",
    "LIN": "Milan",
    "BGY": "Milan",
    "MIL": "Milan",  # Representing all Milan airports
    "LON": "London",  # Representing all London airports
    "TYO": "Tokyo",  # Representing all Tokyo airports
    "NYC": "New York",  # Representing all New York airports
    "YTO": "Toronto",  # Representing all Toronto airports
    # Add more airports as needed
}


def get_city_of_airport(code: str) -> Optional[str]:
    """
    Returns the city for a given three letter IATA airport code
    """
    if code in airport_to_city:
        return airport_to_city[code]
    return None


def same_airport_city(code1, code2):
    """
    Check if two airport codes are similar (i.e., belong to the same city or metropolitan area).

    :param code1: First airport code
    :param code2: Second airport code
    :return: True if codes are similar, False otherwise
    """
    city1 = airport_to_city.get(code1.upper())
    city2 = airport_to_city.get(code2.upper())

    return city1 is not None and city1 == city2


def get_gross_weight(logistics_object: LogisticsObject) -> float:
    """
    Get gross weight from logistics object
    """
    if logistics_object.gross_weight is not None:
        return logistics_object.gross_weight.numerical_value
    elif logistics_object.total_gross_weight:
        return logistics_object.total_gross_weight.numerical_value
    return None


def get_goods_description(logistics_object: LogisticsObject) -> Optional[str]:
    """
    Get goods description from logistics object
    """
    if logistics_object is not None and logistics_object.goods_description is not None:
        return logistics_object.goods_description
    return None


def get_original_logistics_object(change_request: ChangeRequest) -> LogisticsObject:
    """
    Get original logistics object from change request
    """
    return change_request.original_logistics_object


def get_updated_logistics_object(change_request: ChangeRequest) -> LogisticsObject:
    """
    Get original logistics object from change request
    """
    return change_request.updated_logistics_object


def is_typo_correction(original_string: str, updated_string: str) -> bool:
    """
    Check if updated string is a typo correction of original string
    """

    api_key = config.bing_api_key

    endpoint = "https://api.bing.microsoft.com/v7.0/SpellCheck"

    data = {"text": original_string}

    params = {"mkt": "en-us", "mode": "proof"}

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Ocp-Apim-Subscription-Key": api_key,
    }
    response = requests.post(endpoint, headers=headers, params=params, data=data)

    corrections = response.json()
    corrected_text = original_string
    for token in corrections["flaggedTokens"]:
        best_suggestion = max(token["suggestions"], key=lambda x: x["score"])[
            "suggestion"
        ]
        updated_value = token["token"]
        corrected_value = best_suggestion
        corrected_text = corrected_text.replace(updated_value, corrected_value)

    # get max value from levenshtein_distances
    if (
        Levenshtein.distance(updated_string, corrected_text)
        / len(corrections["flaggedTokens"])
    ) < 3.0:
        return True
    else:
        return False
