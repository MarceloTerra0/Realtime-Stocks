import PySimpleGUI as sg
from psgtray import SystemTray
from funcs.soup import getStockPrice as gsp
from threading import Thread

sg.theme('DarkTeal6')

def main():
    stocks = ['GOOG', 'TSLA', 'AAPL']
    stocksPrice = ['Loading...'] * len(stocks)
    running = True
    #using lambda to get the updated value of "running"
    p1 = Thread(target = gsp, args = (stocks, stocksPrice, lambda: running ))
    p1.start()
    font = ("Arial", 20)

    #26x26 icon converted to BASE64 using https://base64.guru/converter/encode/image/ico
    #Icon source: https://www.flaticon.com/premium-icon/bar-graph_404672?term=graph&page=1&position=5&page=1&position=5&related_id=404672&origin=tag
    icon = b'iVBORw0KGgoAAAANSUhEUgAAABoAAAAaCAYAAACpSkzOAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADdYAAA3WAZBveZwAAAOKSURBVEhLtVZbSBRRGP5nZtddd7xPXnYjd23VNEywMkuCSjKKjIigekgQlIroJaIL3Sgq6KF6CnqoCKIIgoKoHky7WxFRFIr6kOXm/RqZ1u66M9t3ZiZdt91qzT745vznO+f8//n/M2d2OZpiOO2OZJGnOpj8iEKLW1ytPUzn2WOKkbfQQtnFFsqEna9J/yeQcH+Y3tYM00HYDzSJaEpLh7KJaJ6Ba1EylyrqiDgjOCsBl+ndYBwDzwcHYYgoEAIUerLEWvA+7Pm6rAL9hWjmgudUIQgRlY5l4ks1PfATeY09nteQDmH3LKgEuxo8DlaBcSDDV3Av5jRMCIQFxWhkDLzUlHFgjNW/FjwFsvEY8AhY4JRGs1sGjDdhD+2KkivWWAUyCBw1uIm2dfqvwF/5WOngqNAsxtWZxdjnsMdeSwb02YYugRex6AbYDjaDm6B1lM8fYtOSQHMyPMYhSCxam5HJZGaPwDNyK4rsU2QZlaHTcD5Hk1UcBjvh+ILWnYCtR6qlo2i3aN1foFYtuHTskimgFTwB+hSzmMe7Rz7BZmVlOisZwzACt+m2Cqy/dtIsb1phM5CAFNpGicpc/uuYtzEwI4LwHvwAPgOXQorv3XAgFS2qTZWeGWbXSGFC40hRYqPHKbrgOFwWKqajdDsk7hazJwQKgZ1pl/dfRbsPLOlbn8L1b3cQ40BVOqtGCZsUDu3I6OyAfx2zxwJhd8mgXec0piGrOnAz+BxdLsRlWJ47094022lvBpvQL9VkDeywAXWVGgiOKw2m6G5LvNQqJkitJktMD7RyNvY7LLJ6pFdVHTn1e1yz6ne7cpY4v7P7FBI/M1oVk5rB2zLzyJY5h1Izcpm+UhsKj5gohXjer26ZwyPWxN6j0Bg/o4Cy6GYxsroN3mEt+gs0eXIYDxQEd0a+o+/o7TLvmUervWcelilZBXZ9aFIIG8gXn0KKZCW/ShtRYpo+MjmEDfRHBJT6bzD5QBHi3wPpl+VPmPKM/AGBA6sr4NVll6zCGC06DPgSyl4ved3f6IuskD8lnUzDA8QNdhP/7jF5Lf3YGU+GwVEydnloRsMgpSf6qM/DU9eQgR63RJNpSCAhiqNemaNWfILwJ6U3KSHhLpeXk/uxqKjQYY7SfjwiPONfEcLBk6cvXFz2TOc9qzWt1CAIuhyIkAcQUsxw2D9Mk6TPr16/macKmPVzYntHZ80P90kjJzywU38AAAAASUVORK5CYII='
    menu = ['', ['Show Window', 'Hide Window', '---', 'Exit']]
    tooltip = 'Simple Stocks'
    stockExample = 'COMP'
    last_selected = ''
    layout = [[sg.T('Insert stock name:'), sg.Input(stockExample, key='-IN-', s=(20,1)), sg.B('Add Stock')],
              [sg.Button('Remove Stock'), sg.B('Hide Window'), sg.Button('Exit')],
              [sg.Multiline(size=(10,2), key='-STOCK-', font=font, justification="center", disabled=True), sg.Listbox(values = stocks, enable_events=True, size=(30, 3), key="-LIST-")]]

    window = sg.Window('Realtime Stocks', layout, finalize=True, enable_close_attempted_event=True)

    tray = SystemTray(menu, single_click_events=True, window=window, tooltip=tooltip, icon=icon)

    while True:
        event, values = window.read(timeout=500)

        if last_selected:
            window['-STOCK-'].update(stocksPrice[stocks.index(last_selected)])

        # IMPORTANT step. It's not required, but convenient. Set event to value from tray
        # if it's a tray event, change the event variable to be whatever the tray sent
        if event == tray.key:
            event = values[event]       # use the System Tray's event as if was from the window
            
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_ACTIVATED):
            window.un_hide()
            window.bring_to_front()
        elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_icon()
        elif event == 'Hide Icon':
            tray.hide_icon()
        elif event == 'Show Icon':
            tray.show_icon()
        elif event == 'Add Stock':
            if values['-IN-'] not in stocks:
                stocksPrice.append('Loading...')
                stocks.append(values['-IN-'])
                window.Element('-LIST-').update(values=stocks)
        elif event == 'Remove Stock':
            stocksPrice.pop(stocks.index(last_selected))
            stocks.pop(stocks.index(last_selected))
            window.Element('-LIST-').update(values=stocks)
            last_selected = ''
            window['-STOCK-'].update('')
        elif event == '-LIST-':
            if values['-LIST-'][0] != last_selected:
                window['-STOCK-'].update(stocksPrice[stocks.index(values['-LIST-'][0])])
                last_selected = values['-LIST-'][0]

    tray.close()            # optional but without a close, the icon may "linger" until moused over
    window.close()
    running = False
    p1.join()

if __name__ == '__main__':
    main()