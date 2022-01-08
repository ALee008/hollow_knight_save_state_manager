from client_ui.main_ui import main

# command line for pyinstaller, : instead of ; for unix
# pyinstaller cli.py --onefile --name hollow_knight --add-data "./images/charms/*.png;./images/charms/"

if __name__ == '__main__':
    main()
