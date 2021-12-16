import datetime

import hollow

import PySimpleGUI as sg

SIZE = (10, 1)


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


def inventory():
    layout = [
        [sg.Text("Play Time", size=SIZE), sg.Input("", key="-PLAY-TIME-")]
    ]

    return layout


def main():
    # ------ Menu Definition ------ #
    menu_def = [['&File', ['&Open', '&Save', 'E&xit']],
                ['&Help', '&About...'], ]

    # ------ Tabs ------ #
    inventory_tab = inventory()
    charms_tab = []
    tab_group = [
        [sg.TabGroup(
            [
                [sg.Tab("Inventory", inventory_tab, border_width=10, tooltip="Inventory Details",
                        element_justification="center"),
                 sg.Tab("Charms", charms_tab, border_width=10, tooltip="Inventory Details",
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
            print(save_state_file_path)
            file_io = hollow.FileIO(save_state_file_path)
            inventory_details = hollow.Inventory(file_io)
            print(display_play_time(inventory_details.play_time))
            window["-PLAY-TIME-"].update(display_play_time(inventory_details.play_time))

    window.close()


if __name__ == '__main__':
    main()
