import datetime
import itertools

import hollow

import PySimpleGUI as sg

SIZE = (12, 1)
charms_details = hollow.Charms()


def display_play_time(play_time: float) -> str:
    """Convert playTime from save state - which is float - to human readably time hh:mm:ssss
    """
    timedelta = datetime.timedelta(seconds=play_time)
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
        [sg.Text("Simple Keys", size=SIZE), sg.Input("", key="-SIMPLE-KEYS")]
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
    window["-SIMPLE-KEYS"].update(inventory_details.simple_keys)

    return None


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
    menu_def = [['&File', ['&Open', '&Save', 'E&xit']],
                ['&Help', '&About...'], ]

    # ------ Tabs ------ # TODO: refactor tabs layout
    inventory_tab = inventory_layout()
    charms_tab = charms_layout()
    tab_group = [
        [sg.TabGroup(
            [
                [sg.Tab("Inventory", inventory_tab, border_width=10, tooltip="Inventory Details",
                        element_justification="left"),
                 sg.Tab("Charms", charms_tab, border_width=10, tooltip="Charms", visible=False,
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
            except FileNotFoundError:  # this error is raised if no file is chosen.
                print("No file chosen.")
        if event.endswith(".PNG"):
            charms_details.has_charm[event.rstrip(".PNG")] = values[event]
        if event == "Save":
            if file_io is None:
                sg.popup("No user data file opened yet.")
                continue
            file_io.update_user_data(charms_details.has_charm)  # TODO: hasCharm_NUMMER muss zu hollow hinzugefuegt werden

    window.close()


if __name__ == '__main__':
    main()
