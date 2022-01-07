import datetime
import itertools
from typing import Any, Dict

import hollow

import PySimpleGUI as sg

SIZE = (12, 1)
charms_image_details = hollow.CharmsImages()


class UserChanges:
    def __init__(self):
        self.user_changes_dict = dict()

    def add_change(self, key: str, value: Any):
        self.user_changes_dict[key] = value


def display_play_time(play_time: float) -> str:
    """Convert playTime from save state - which is float - to human readably time hh:mm:ssss
    """
    seconds = round(play_time)
    # return its string representation, which is the desired format.
    return f"{seconds // 3600}:{seconds // 60 % 60}:{seconds % 60}"


def play_time_from_time(play_time: str) -> float:
    """Convert string from UI to float for subsequent update to save state.
    """
    hh, mm, ss = play_time.split(":")

    return int(hh) * 3600 + int(mm) * 60 + float(ss)


def check_int(window, event, value, key):
    if event == key and value[key] and value[key][-1] not in '0123456789':
        window[key].update(value[key][:-1])


def inventory_layout():
    layout = [
        [sg.Text("Play Time", size=SIZE), sg.Input("", key="_PLAY-TIME_")],
        [sg.Text("Geo", size=SIZE), sg.Input("", key="-GEO-", enable_events=True)],
        [sg.Text("Pale Ore", size=SIZE), sg.Input("", key="-PALE-ORE-", enable_events=True)],
        [sg.Text("Dream Orbs", size=SIZE), sg.Input("", key="-DREAM-ORBS-", enable_events=True)],
        [sg.Text("Simple Keys", size=SIZE), sg.Input("", key="-SIMPLE-KEYS-", enable_events=True)]
    ]

    return layout


def knight_layout():
    layout = [
        [sg.Text("Charm Slots", size=SIZE), sg.Input("", key="-CHARM-SLOTS-", enable_events=True)],
        [sg.Text("Blue Health", size=SIZE), sg.Input("", key="-BLUE-HEALTH-", enable_events=True)],
        [sg.Text("Nail Damage", size=SIZE), sg.Input("", key="-NAIL-DAMAGE-", enable_events=True)],
        [sg.Text("Nail Range", size=SIZE), sg.Input("", key="-NAIL-RANGE-", enable_events=True)],
        [sg.Text("Beam Damage", size=SIZE), sg.Input("", key="-BEAM-DAMAGE-", enable_events=True)],
    ]

    return layout


def update_inventory_ui(window: sg.Window, file_io: hollow.FileIO) -> None:
    """Update sg.Input in Inventory tab.
    """
    inventory_details = hollow.Inventory(file_io)
    window["_PLAY-TIME_"].update(display_play_time(inventory_details.play_time))
    window["-GEO-"].update(inventory_details.geo)
    window["-PALE-ORE-"].update(inventory_details.ore)
    window["-DREAM-ORBS-"].update(inventory_details.dream_orbs)
    window["-SIMPLE-KEYS-"].update(inventory_details.simple_keys)

    return None


def update_knight_ui(window: sg.Window, file_io: hollow.FileIO) -> None:
    """Update sg.Input in Knight tab.
    """
    knight_details = hollow.HollowKnight(file_io)
    window["-CHARM-SLOTS-"].update(knight_details.charm_slots)
    window["-BLUE-HEALTH-"].update(knight_details.blue_health)
    window["-NAIL-DAMAGE-"].update(knight_details.nail_damage)
    window["-NAIL-RANGE-"].update(knight_details.nail_range)
    window["-BEAM-DAMAGE-"].update(knight_details.beam_damage)

    return None


def update_charms_ui(window: sg.Window, file_io: hollow.FileIO) -> dict:
    """ Update Charms Tab. Activate Charms from user data that have already been collected."""
    all_charms = hollow.CharmFactory(file_io).charms
    for name, charm in all_charms.items():
        window[name + ".PNG"].update(charm.got_charm)
        window[name + ".SLOTS"].update(charm.cost)

    return all_charms


def validate(values: dict, key: str) -> int:
    try:
        return int(values[key])
    except ValueError:  # in case a field is left empty
        return 0


def register_user_changes(charms_factory: dict, values: Dict[str, Any]) -> dict:
    """collect all user changes and return dictionary containing changes.
    TODO: check for valid bounds!
    :param values: dictionary from GUI containing values of window fields.
    :param charms_factory: factory containing all changes made to charms
    :return:
    """
    user_changes = UserChanges()
    play_time = play_time_from_time(values["_PLAY-TIME_"])
    user_changes.add_change("playTime", play_time)
    user_changes.add_change("geo", validate(values, "-GEO-"))
    user_changes.add_change("ore", validate(values, "-PALE-ORE-"))
    user_changes.add_change("simpleKeys", validate(values, "-SIMPLE-KEYS-"))
    user_changes.add_change("dreamOrbs", validate(values, "-DREAM-ORBS-"))

    user_changes.add_change("charmSlots", validate(values, "-CHARM-SLOTS-"))
    user_changes.add_change("healthBlue", validate(values, "-BLUE-HEALTH-"))
    user_changes.add_change("nailDamage", validate(values, "-NAIL-DAMAGE-"))
    user_changes.add_change("nailRange", validate(values, "-NAIL-RANGE-"))
    user_changes.add_change("beamDamage", validate(values, "-BEAM-DAMAGE-"))

    register_charms_changes(user_changes, charms_factory)

    return user_changes.user_changes_dict


def register_charms_changes(user_changes: UserChanges, charms_factory: dict) -> None:
    # update gotCharms_i with value from dictionary `values`
    for charm in charms_factory.values():
        user_changes.add_change(f"gotCharm_{charm.ordinal}", charm.got_charm)
        user_changes.add_change(f"charmCost_{charm.ordinal}", charm.cost)

    return None


def chunk(iterable, size):
    """https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    see answer from senderle
    """
    iterable = iter(iterable)

    return iter(lambda: list(itertools.islice(iterable, size)), [])


def charms_layout():
    charms_names = charms_image_details.charm_to_image.keys()
    charms_text_fields = [sg.Text(name) for name in charms_names]
    charms_images = charms_image_details.charm_to_image.values()
    charms_image_fields = [sg.Image(str(image_path)) for image_path in charms_images]
    # add .PNG to identify if charm checkbox event fired
    charms_checkboxes = [sg.Checkbox('', enable_events=True, key=charm_name + ".PNG") for charm_name in charms_names]

    charms_slots_inputs = [sg.Input("", enable_events=True, key=charm_name + ".SLOTS", size=(2, 1),
                                    tooltip="Slots used") for charm_name in charms_names]

    names_images_checkboxes = [list(map(lambda x: [x], elements)) for elements in
                               zip(charms_text_fields, charms_image_fields, charms_checkboxes, charms_slots_inputs)]

    frames_layout = []

    for frame_layout in names_images_checkboxes:
        frames_layout.append(sg.Frame(layout=frame_layout, title="", element_justification="center"))

    final_layout = list(chunk(frames_layout, 10))

    return final_layout


def main():
    # ------ Menu Definition ------ #
    menu_def = [
        ['&File', ['&Open', 'Create &Backup', '&Save', 'E&xit']]
    ]

    # ------ Tabs ------ # TODO: refactor tabs layout
    tab_group = [
        [sg.TabGroup(
            [
                [sg.Tab("Inventory", inventory_layout(), border_width=10, tooltip="Inventory Details",
                        element_justification="left"),
                 sg.Tab("Knight", knight_layout(), border_width=10, tooltip="Character Properties",
                        element_justification="left"),
                 sg.Tab("Charms", charms_layout(), border_width=10, tooltip="Charms", disabled=True,
                        element_justification="left"),
                 ]
            ]
        )]
    ]

    layout = [
        [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
    ]

    status_bar = [
        [sg.StatusBar("", size=(150, 1), key="_STATUS-BAR_")]
    ]

    # define window
    window = sg.Window("Hollow Knight Save State Editor", layout + tab_group + status_bar)

    file_io = None

    while True:
        event, values = window.read()
        if event in ("Exit", sg.WIN_CLOSED):
            break
        if event == "Open":
            try:
                save_state_file_path = sg.popup_get_file("Save State", no_window=True,
                                                         file_types=(("User Data", "*.dat"),))
                file_io = hollow.FileIO(save_state_file_path)
                update_inventory_ui(window, file_io)
                update_knight_ui(window, file_io)
                window["Charms"].update(disabled=False)
                window["_STATUS-BAR_"].update(value=f"Save state: {save_state_file_path}")
                # charms_factory will be used to update save state.
                charms_factory = update_charms_ui(window, file_io)
            except FileNotFoundError:  # this error is raised if no file is chosen.
                print("No file chosen.")
        if event == "Create Backup":
            if file_io is None:
                sg.popup("No user data file opened yet.", title="Warning!")
                continue
            file_io.create_backup()
            sg.popup(f"Backup created at {file_io.backup_path}!", title="Backup successful.")
        if ".PNG" in event:
            # get changed charm and update its property; object will later be used to save changes
            charm: hollow.Charm = charms_factory[event.rstrip(".PNG")]
            charm.got_charm = values[event]
        if ".SLOTS" in event:
            check_int(window, event, values, event)
            charm: hollow.Charm = charms_factory[event.rstrip(".SLOTS")]
            charm.cost = validate(values, event)
        if event == "Save":
            if file_io is None:
                sg.popup("No user data file opened yet.", title="Warning!")
                continue
            # update internal dictionary
            user_changes = register_user_changes(charms_factory, values)
            file_io.update_user_data(user_changes)
            file_io.write_user_data_changes()  # dump changes
            sg.popup("Changes saved successfully.\nEmpty fields will be set to 0.", title="Saved")

        # check if entered values are integer
        integer_fields = [key for key in values if isinstance(key, str) and key.startswith("-") and key.endswith("-")]
        for key in integer_fields:
            check_int(window, event, values, key)

    window.close()


if __name__ == '__main__':
    main()
