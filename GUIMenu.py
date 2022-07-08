import PySimpleGUI as sg
from infoTracker import *
import sys, os


def override_where():
    """ overrides certifi.core.where to return actual location of cacert.pem"""
    # change this to match the location of cacert.pem
    return os.path.abspath("cacert.pem")


# is the program compiled?
if hasattr(sys, "frozen"):
    import certifi.core

    os.environ["REQUESTS_CA_BUNDLE"] = override_where()
    certifi.core.where = override_where

    # delay importing until after where() has been replaced
    import requests.utils
    import requests.adapters
    # replace these variables in case these modules were
    # imported before we replaced certifi.core.where
    requests.utils.DEFAULT_CA_BUNDLE_PATH = override_where()
    requests.adapters.DEFAULT_CA_BUNDLE_PATH = override_where()

#Everything above ^ just makes sure that the cacert.pem path is overriden so that the .exe can run when created

sg.set_options(font=('Roboto', 12))

frame_1 = [[sg.Text('NJ Info Tracker', font = 'Roboto 45 bold')], 
           [sg.Image(r'njgreen.png', background_color='#67A2B7')],
           [sg.Button('Gas', size = (6,2), button_color= ('white', '#9E416E'), mouseover_colors= '#67A2B7'), sg.Button('Weather', size = (8,2), button_color= ('white', '#9E416E'), mouseover_colors= '#67A2B7'), sg.Button('Traffic', size = (8,2), button_color= ('white', '#9E416E'), mouseover_colors= '#67A2B7')],
           [sg.Button('About', button_color= ('white', '#9E416E'))]
           ]
           
frame_2 = [[sg.Output(background_color='#67A2B7', size=(100, 40), key = '-DESTINATION-')],]

layout = [
    [sg.Frame('', frame_1, element_justification='c', border_width= 0), 
     sg.Frame('', frame_2, key='Hide', border_width= 0)]
]

window = sg.Window('NJ Info Tracker', layout, finalize=True)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Gas':
        window['-DESTINATION-'].update(' ')
        window['-DESTINATION-'].update(gasAlerts())

    elif event == 'Weather':
        window['-DESTINATION-'].update(' ')
        window['-DESTINATION-'].update(weatherAlerts())

    elif event == 'Traffic':
        window['-DESTINATION-'].update(' ')
        window['-DESTINATION-'].update(trafficAlerts())

    elif event == 'About':
        sg.popup("This application gives you real time updates on the following information for Central New Jersey:\n\nMajor highway taffic and accidents\n3 day weather forecast\nCheapest gas locations\n\n\nCreated by Michael Skolnick")

window.close()