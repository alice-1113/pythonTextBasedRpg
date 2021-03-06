import PySimpleGUI as sg


layout = [
    [sg.T("Attack(A):"), sg.I(key="-A-")],  # 攻撃力
    [sg.T("Defence(D):"), sg.I(key="-D-")],  # 防御力
    [sg.T("EXPR:"), sg.I(key="-E-")],  # 計算式
    [sg.T("RESULT:"), sg.T(size=(55, 1), key="-out-")],
    [sg.B("Calc"), sg.B("Exit")]
]

window = sg.Window("Calc", layout)
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    A = int(values["-A-"])
    D = int(values["-D-"])
    try:
        expr = int(eval(values["-E-"]))
        window["-out-"].update(str(expr))
    except ZeroDivisionError:
        D += 1
        expr = int(eval(values["-E-"]))
        window["-out-"].update(str(expr))

window.close()