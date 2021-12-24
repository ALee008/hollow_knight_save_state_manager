import datetime
import itertools
from typing import Any

import hollow

import PySimpleGUI as sg

SIZE = (12, 1)
charms_details = hollow.Charms()


class UserChanges:
    def __init__(self):
        self.user_changes_dict = dict()

    def add_change(self, key: str, value: Any):
        self.user_changes_dict[key] = value


def display_play_time(play_time: float) -> str:
    """Convert playTime from save state - which is float - to human readably time hh:mm:ssss
    """
    timedelta = datetime.timedelta(seconds=round(play_time))
    # return its string representation, which is the desired format.
    return str(timedelta)


def play_time_from_time(play_time: str) -> float:
    """Convert string from UI to float for subsequent update to save state.
    """
    hh, mm, ss = play_time.split(":")

    return int(hh) * 3600 + int(mm) * 60 + float(ss)


def inventory_layout():
    layout = [
        [sg.Text("Play Time", size=SIZE), sg.Input("", key="-PLAY-TIME-")],
        [sg.Text("Geo", size=SIZE), sg.Input("", key="-GEO-")],
        [sg.Text("Pale Ore", size=SIZE), sg.Input("", key="-PALE-ORE-")],
        [sg.Text("Dream Orbs", size=SIZE), sg.Input("", key="-DREAM-ORBS-")],
        [sg.Text("Simple Keys", size=SIZE), sg.Input("", key="-SIMPLE-KEYS-")]
    ]

    return layout


def update_inventory_ui(window: sg.Window, file_io: hollow.FileIO) -> None:
    """ Update sg.Input in Inventory tab.
    TODO: add validation when user interacts.
    """
    inventory_details = hollow.Inventory(file_io)
    window["-PLAY-TIME-"].update(display_play_time(inventory_details.play_time))
    window["-GEO-"].update(inventory_details.geo)
    window["-PALE-ORE-"].update(inventory_details.ore)
    window["-DREAM-ORBS-"].update(inventory_details.dream_orbs)
    window["-SIMPLE-KEYS-"].update(inventory_details.simple_keys)

    return None


def register_user_changes(values: dict) -> dict:
    """collect all user changes and return dictionary containing changes.
    TODO: check for valid bounds!
    :param values: dictionary from GUI containing values of window fields.
    :return:
    """
    user_changes = UserChanges()
    play_time = play_time_from_time(values["-PLAY-TIME-"])
    user_changes.add_change("playTime", play_time)
    user_changes.add_change("geo", abs(int(values["-GEO-"])))
    user_changes.add_change("ore", abs(int(values["-PALE-ORE-"])))
    user_changes.add_change("simpleKeys", abs(int(values["-SIMPLE-KEYS-"])))
    user_changes.add_change("dreamOrbs", abs(int(values["-DREAM-ORBS-"])))

    return user_changes.user_changes_dict


def chunk(iterable, size):
    """https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    see answer from senderle
    """
    iterable = iter(iterable)

    return iter(lambda: list(itertools.islice(iterable, size)), [])


def charms_layout():

    charms_names = charms_details.charm_to_image.keys()
    charms_text_fields = [sg.Text(name) for name in charms_names]
    charms_images = charms_details.charm_to_image.values()
    charms_image_fields = [sg.Image(str(image_path)) for image_path in charms_images]
    # add .PNG to identify if charm checkbox event fired
    charms_checkboxes = [sg.Checkbox('', enable_events=True, key=charm_name+".PNG") for charm_name in charms_names]

    names_images_checkboxes = [
        list(map(lambda x: [x], elements)) for elements in zip(charms_text_fields, charms_image_fields, charms_checkboxes)
    ]

    frames_layout = []

    for frame_layout in names_images_checkboxes:
        frames_layout.append(sg.Frame(layout=frame_layout, title="", element_justification="center"))

    final_layout = list(chunk(frames_layout, 10))

    return final_layout


def main():
    # ------ Menu Definition ------ #
    menu_def = [['&File', ['&Open', 'Create &Backup', '&Save', 'E&xit']],
                ['&Help', '&About...'], ]

    # ------ Tabs ------ # TODO: refactor tabs layout
    inventory_tab = inventory_layout()
    charms_tab = charms_layout()
    tab_group = [
        [sg.TabGroup(
            [
                [sg.Tab("Inventory", inventory_tab, border_width=10, tooltip="Inventory Details",
                        element_justification="left"),
                 sg.Tab("Charms", charms_tab, border_width=10, tooltip="Charms", disabled=True,
                        element_justification="left"),
                 ]
            ]
        )]
    ]

    layout = [
        [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],

    ]

    # define window
    window = sg.Window("Hollow Knight Save State Editor", layout + tab_group)

    file_io = None

    while True:
        event, values = window.read()
        if event in ("Exit", sg.WIN_CLOSED):
            break
        if event == "Open":
            try:
                save_state_file_path = sg.popup_get_file("Save State", no_window=True, file_types=(("User Data", "*.dat"),))
                file_io = hollow.FileIO(save_state_file_path)
                update_inventory_ui(window, file_io)
                window["Charms"].update(disabled=False)
            except FileNotFoundError:  # this error is raised if no file is chosen.
                print("No file chosen.")
        if event.endswith(".PNG"):
            charms_details.has_charm[event.rstrip(".PNG")] = values[event]
        if event == "Create Backup":
            if file_io is None:
                sg.popup("No user data file opened yet.")
                continue
            file_io.create_backup()
            sg.popup(f"Backup created at {file_io.backup_path}!")
        if event == "Save":
            if file_io is None:
                sg.popup("No user data file opened yet.")
                continue
            # update internal dictionary
            user_changes = register_user_changes(values)

            #file_io.update_user_data(charms_details.has_charm)  # TODO: hasCharm_NUMMER muss zu hollow hinzugefuegt werden
            file_io.update_user_data(user_changes)
            file_io.write_user_data_changes()  # dump changes
            sg.popup("Saved")

    window.close()


if __name__ == '__main__':
    main()
