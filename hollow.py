import json
import pathlib

from typing import Dict

import constants


def read_save_state(path: str = "hollow_knight/user3.dat") -> dict:
    with open(path) as save_state:
        save_state_entries = save_state.read()
        save_state_dict = json.loads(save_state_entries)

    return save_state_dict


def filter_non_number_value_from(dictionary: dict):
    result_dict = {}
    for key, value in dictionary.items():
        if str(value).isnumeric():
            result_dict[key] = value

    return result_dict


class Charms:
    image_path: pathlib.Path = pathlib.Path("images/charms")
    # number of available charm notches
    number_of_charm_slots: int
    # define if charm in slot number N is available
    has_charm: Dict[str, bool] = {f"charm#{i}": False for i in range(1, 41)}
    charm_to_image: Dict[str, pathlib.Path]
    # slot usage per charm
    charm_slots: Dict[str, int] = {key: constants.CHARM_COSTS[key] for key in has_charm.keys()}

    def __init__(self):
        self.charm_to_image = self.map_charm_to_image()

    def map_charm_to_image(self) -> Dict[str, pathlib.Path]:
        charms = dict.fromkeys(constants.CHARMS)

        for key in charms.keys():
            for child in self.image_path.iterdir():
                if key.replace(" ", "_").upper() in child.stem.upper():
                    charms[key] = child

        return charms


class Inventory:
    geo: int
    simple_keys: int
    ore: int
    dream_orbs: int


class Environment:
    has_city_key: bool


if __name__ == '__main__':
    charms_ = Charms()

# ["playerData"]["geo"]
# ["playerData"]["charmSlots"]
# ["playerData"]["gotCharm_1-40"]
# ["playerData"]["hasCityKey"]
"""
 'hasCityKey': False,
 'hasCyclone': True,
 'hasDash': True,
 'hasDashSlash': True,
 'hasDoubleJump': True,
 'hasDreamGate': True,
 'hasDreamNail': True,
 'hasGodfinder': False,
 'hasHuntersMark': False,
 'hasJournal': True,
 'hasKingsBrand': True,
 'hasLantern': True,
 'hasLoveKey': False,
 'hasShadowDash': True,
 'simpleKeys': 0,
 'ore': 2,
 'dreamOrbs': 1359,
 'charmCost_1': 1,
 'charmCost_10': 1,
 'charmCost_11': 3,
 'charmCost_12': 1,
 'charmCost_13': 3,
 'charmCost_14': 1,
 'charmCost_15': 2,
 'charmCost_16': 2,
 'charmCost_17': 1,
 'charmCost_18': 2,
 'charmCost_19': 3,
 'charmCost_2': 1,
 'charmCost_20': 2,
 'charmCost_21': 4,
 'charmCost_22': 2,
 'charmCost_23': 2,
 'charmCost_24': 2,
 'charmCost_25': 3,
 'charmCost_26': 1,
 'charmCost_27': 4,
 'charmCost_28': 2,
 'charmCost_29': 4,
 'charmCost_3': 1,
 'charmCost_30': 1,
 'charmCost_31': 2,
 'charmCost_32': 3,
 'charmCost_33': 2,
 'charmCost_34': 4,
 'charmCost_35': 3,
 'charmCost_36': 5,
 'charmCost_37': 1,
 'charmCost_38': 3,
 'charmCost_39': 2,
 'charmCost_4': 2,
 'charmCost_40': 2,
 'charmCost_5': 2,
 'charmCost_6': 2,
 'charmCost_7': 3,
 'charmCost_8': 2,
 'charmCost_9': 3,
 'healthBlue': 0,
 'maxHealth': 8,
 'maxHealthBase': 8,
 'maxHealthCap': 9,
 'maxMP': 99,
 'nailDamage': 17,
 'nailRange': 0,
 """
