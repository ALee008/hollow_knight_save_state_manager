import datetime
import itertools

import hollow

import PySimpleGUI as sg

SIZE = (12, 1)


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

    return iter(lambda: tuple(itertools.islice(iterable, size)), ())


def charms_layout():
    charms_details = hollow.Charms()
    charms_names = chunk(charms_details.charm_to_image.keys(), 10)
    charms_images = chunk(charms_details.charm_to_image.values(), 10)

    layout = []

    for names in charms_names:
        layout.append([sg.Text(name) for name in names])

    for images in charms_images:
        # image path in .values is of type pathlib.Path -> use str() to convert to string
        layout.append([sg.Image(str(image_path)) for image_path in images])

    return layout


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
                        element_justification="center"),
                 sg.Tab("Charms", charms_tab, border_width=10, tooltip="Charms",
                        element_justification="center"),
                 ]
            ]
        )]
    ]

    layout = [
        [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],

    ]

    # define window
    window = sg.Window("Hollow Knight Save State Editor", layout + tab_group)

    while True:
        event, values = window.read()
        if event in ("Exit", sg.WIN_CLOSED):
            break
        if event == "Open":
            save_state_file_path = sg.popup_get_file("Save State", no_window=True, file_types=(("User Data", "*.dat"),))
            file_io = hollow.FileIO(save_state_file_path)
            update_inventory_ui(window, file_io)


    window.close()


if __name__ == '__main__':
    main()