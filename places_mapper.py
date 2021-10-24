"""
A script to generate an interactve overlay of data from the places.xyz project in a local browser.

Find more information at https://places.xyz
"""
__author__ = "https://github.com/hmprt"


import os
import sys
import folium
from web3 import Web3
from tqdm import tqdm


def places_mapper():
    """
    Generates a static map of the coverage of the places.xyz project
    """

    HTTP_PROVIDER = os.environ["HTTP_PROVIDER"]
    CONTRACT_ADDRESS = os.environ["PLACES_CONTRACT_ADDRESS"]
    CONTRACT_ABI = open("contract_abi", "r").read()

    # check an appropriate theme has been set
    try:
        theme = os.environ.get("THEME", "")
        all_themes = [
            theme.rstrip("\n") for theme in open("./data/themes.txt").readlines()
        ]
        assert theme in all_themes
    except AssertionError:
        print(f"Invalid theme. Please select one of:\n {os.linesep.join(all_themes)}")
        sys.exit(0)

    # web3 init
    w3 = Web3(Web3.HTTPProvider(HTTP_PROVIDER))
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

    # contract calls
    NUM_PLACES = contract.functions.getPlaceSupply().call()
    print(f"Grabbing {NUM_PLACES} places...")

    places = []
    pbar = tqdm(range(NUM_PLACES))
    for i in pbar:
        place = contract.functions.getPlace(i).call()
        places.append(
            {
                "name": place[0],
                "address": "\n".join(place[:9]),
                "lat": place[9][-3],
                "long": place[9][-2],
                "elevation": place[9][-1],
                "tags": "\n".join(place[-1]),
            }
        )
        pbar.set_description(f"Place {i+1}: {place[0]}")
    print(f"Done!")

    # populate map
    MAX_LAT = max(place["lat"] for place in places)
    MIN_LAT = min(place["lat"] for place in places)
    AVG_LAT = sum(float(place["lat"]) for place in places) / len(places)

    MAX_LONG = max(place["long"] for place in places)
    MIN_LONG = min(place["long"] for place in places)
    AVG_LONG = sum(float(place["long"]) for place in places) / len(places)

    map = folium.Map(location=[AVG_LAT, AVG_LONG], zoom_start=13, tiles=theme)

    for place in places:
        folium.Marker([place["lat"], place["long"]], tooltip=place["name"]).add_to(map)

    map.save("/tmp/map.html")
    print("Map html saved to /tmp/map.html")


if __name__ == "__main__":
    places_mapper()
