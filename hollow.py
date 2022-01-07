import json
import shutil
import pathlib

from typing import Dict, List, Union

import constants


def filter_non_number_value_from(dictionary: dict):
    result_dict = {}
    for key, value in dictionary.items():
        if str(value).isnumeric():
            result_dict[key] = value

    return result_dict


def map_charm_to_order_number() -> Dict[str, List[Union[str, bool]]]:
    """Map name of charm to key in user.dat and a flag if user has charm.
    E.g.: {"Wayward Compass": ["gotCharm_1": False], ... }
    """
    charms_to_number = {charm: [f"gotCharm_{idx}", False] for idx, charm in
                        enumerate(constants.CHARMS, start=1)}

    return charms_to_number


class FileIO:

    def __init__(self, user_data_path):
        self.user_data_path: str = user_data_path
        self.backup_path: str = user_data_path + ".bak"
        self.save_state = self.read_save_state()

    def create_backup(self):
        shutil.copy(self.user_data_path, self.backup_path)

    def read_save_state(self) -> dict:
        with open(self.user_data_path) as save_state:
            save_state_entries = save_state.read()
            save_state_dict = json.loads(save_state_entries)

        return save_state_dict

    def update_user_data(self, user_changes: dict = None):
        for key, value in user_changes.items():
            self.save_state["playerData"][key] = value

    def write_user_data_changes(self):
        with open(self.user_data_path, "w") as user_data:
            json.dump(self.save_state, user_data)

    @property
    def player_data(self):
        return self.save_state["playerData"]


class CharmsImages:
    image_path: pathlib.Path = pathlib.Path("../images/charms")
    charm_to_image: Dict[str, pathlib.Path]

    def __init__(self):
        self.charm_to_image = self.map_charm_to_image()

    def map_charm_to_image(self) -> Dict[str, pathlib.Path]:
        charms = dict.fromkeys(constants.CHARMS)

        for key in charms.keys():
            for child in self.image_path.iterdir():
                if key.replace(" ", "_").upper() in child.stem.upper():
                    charms[key] = child

        return charms


class Charm:

    def __init__(self, file_handle: FileIO, name: str, ordinal: int):
        self.player_data = file_handle.save_state["playerData"]
        self.name = name
        self.ordinal = ordinal
        self.got_charm = self.player_data.get(f"gotCharm_{self.ordinal}", False)
        self.cost = self.player_data.get(f"charmCost_{self.ordinal}", constants.CHARM_COSTS[self.name])


class CharmFactory:
    charms: Dict[str, Charm]

    def __init__(self, file_handle: FileIO):
        self.charms = {name: Charm(file_handle, name, idx) for name, idx in constants.CHARMS_ORDINALS.items()}


class Inventory:

    def __init__(self, file_handle: FileIO):
        player_data = file_handle.player_data

        self.geo = player_data["geo"]
        self.simple_keys = player_data["simpleKeys"]
        self.ore = player_data["ore"]
        self.dream_orbs = player_data["dreamOrbs"]
        self.play_time = player_data["playTime"]


class HollowKnight:

    def __init__(self, file_handle: FileIO):
        player_data = file_handle.player_data

        self.charm_slots = player_data["charmSlots"]
        self.blue_health = player_data["healthBlue"]
        self.nail_damage = player_data["nailDamage"]
        self.nail_range = player_data["nailRange"]
        self.beam_damage = player_data["beamDamage"]


class Environment:
    has_city_key: bool


if __name__ == '__main__':
    charms_ = CharmsImages()

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
 "charmSlots"
 """
