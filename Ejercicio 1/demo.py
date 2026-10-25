"""Small native Win32 version of the Suma Olimpo demo.

This file intentionally uses only the Python standard library.  The input,
button, and result controls are native Win32 controls so VBA's
EnumChildWindows can find them as Edit, Button, and Static windows.
"""

import ctypes
import sys
from ctypes import wintypes


if sys.platform != "win32":
    raise RuntimeError("This program requires Windows.")


user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

HWND = wintypes.HWND
HINSTANCE = wintypes.HINSTANCE
LRESULT = ctypes.c_ssize_t
HANDLE = wintypes.HANDLE
WNDPROC = ctypes.WINFUNCTYPE(
    LRESULT, HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM
)


class WNDCLASSW(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int),
        ("hInstance", HINSTANCE),
        ("hIcon", HANDLE),
        ("hCursor", HANDLE),
        ("hbrBackground", HANDLE),
        ("lpszMenuName", wintypes.LPCWSTR),
        ("lpszClassName", wintypes.LPCWSTR),
    ]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt_x", ctypes.c_long),
        ("pt_y", ctypes.c_long),
    ]


# Window and control styles.
CS_HREDRAW = 0x0002
CS_VREDRAW = 0x0001
WS_CHILD = 0x40000000
WS_VISIBLE = 0x10000000
WS_BORDER = 0x00800000
WS_CAPTION = 0x00C00000
WS_SYSMENU = 0x00080000
WS_TABSTOP = 0x00010000
WS_EX_LAYERED = 0x00080000
WS_EX_APPWINDOW = 0x00040000
ES_AUTOHSCROLL = 0x0080
BS_DEFPUSHBUTTON = 0x0001
SW_SHOW = 5
WM_CLOSE = 0x0010
WM_DESTROY = 0x0002
WM_COMMAND = 0x0111
WM_SETFONT = 0x0030
BN_CLICKED = 0
LWA_ALPHA = 0x00000002
IDC_ARROW = 32512


user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASSW)]
user32.RegisterClassW.restype = wintypes.ATOM
user32.CreateWindowExW.argtypes = [
    wintypes.DWORD,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.DWORD,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    HWND,
    wintypes.HMENU,
    HINSTANCE,
    wintypes.LPVOID,
]
user32.CreateWindowExW.restype = HWND
user32.DefWindowProcW.argtypes = [
    HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
]
user32.DefWindowProcW.restype = LRESULT
user32.SetLayeredWindowAttributes.argtypes = [
    HWND,
    wintypes.COLORREF,
    wintypes.BYTE,
    wintypes.DWORD,
]
user32.SetLayeredWindowAttributes.restype = wintypes.BOOL
user32.SetWindowTextW.argtypes = [HWND, wintypes.LPCWSTR]
user32.SetWindowTextW.restype = wintypes.BOOL
user32.GetWindowTextW.argtypes = [HWND, wintypes.LPWSTR, ctypes.c_int]
user32.GetWindowTextW.restype = ctypes.c_int
user32.SendMessageW.argtypes = [
    HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
]
user32.SendMessageW.restype = LRESULT
user32.ShowWindow.argtypes = [HWND, ctypes.c_int]
user32.ShowWindow.restype = wintypes.BOOL
user32.UpdateWindow.argtypes = [HWND]
user32.UpdateWindow.restype = wintypes.BOOL
user32.DestroyWindow.argtypes = [HWND]
user32.DestroyWindow.restype = wintypes.BOOL
user32.PostQuitMessage.argtypes = [ctypes.c_int]
user32.PostQuitMessage.restype = None
user32.GetMessageW.argtypes = [ctypes.POINTER(MSG), HWND, wintypes.UINT, wintypes.UINT]
user32.GetMessageW.restype = ctypes.c_int
user32.TranslateMessage.argtypes = [ctypes.POINTER(MSG)]
user32.TranslateMessage.restype = wintypes.BOOL
user32.DispatchMessageW.argtypes = [ctypes.POINTER(MSG)]
user32.DispatchMessageW.restype = LRESULT
user32.MessageBoxW.argtypes = [HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT]
user32.MessageBoxW.restype = ctypes.c_int
user32.LoadCursorW.argtypes = [HINSTANCE, wintypes.LPCWSTR]
user32.LoadCursorW.restype = HANDLE

kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
kernel32.GetModuleHandleW.restype = HINSTANCE


CLASS_NAME = "SumaOlimpoPythonWindow"
WINDOW_TITLE = "Demo Suma Olimpo"
BUTTON_ID = 1001
FONT = None
controls = {}


def control_text(handle):
    buffer = ctypes.create_unicode_buffer(256)
    user32.GetWindowTextW(handle, buffer, len(buffer))
    return buffer.value


def show_sum():
    try:
        a_text = control_text(controls["a"]).strip().replace(",", ".")
        b_text = control_text(controls["b"]).strip().replace(",", ".")
        result = float(a_text) + float(b_text)
        result_text = f"{result:.15g}"
    except ValueError:
        result_text = "ERROR"

    user32.SetWindowTextW(controls["result"], f"Resultado: {result_text}")


@WNDPROC
def window_proc(hwnd, message, w_param, l_param):
    if message == WM_COMMAND:
        command_id = w_param & 0xFFFF
        notification = (w_param >> 16) & 0xFFFF
        if command_id == BUTTON_ID and notification == BN_CLICKED:
            show_sum()
            return 0
    elif message == WM_CLOSE:
        user32.DestroyWindow(hwnd)
        return 0
    elif message == WM_DESTROY:
        user32.PostQuitMessage(0)
        return 0

    return user32.DefWindowProcW(hwnd, message, w_param, l_param)


def create_control(class_name, text, style, x, y, width, height, parent, control_id=0):
    handle = user32.CreateWindowExW(
        0,
        class_name,
        text,
        style,
        x,
        y,
        width,
        height,
        parent,
        control_id,
        kernel32.GetModuleHandleW(None),
        None,
    )
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    if FONT:
        user32.SendMessageW(handle, WM_SETFONT, FONT, 1)
    return handle


def create_window():
    instance = kernel32.GetModuleHandleW(None)
    window_class = WNDCLASSW()
    window_class.style = CS_HREDRAW | CS_VREDRAW
    window_class.lpfnWndProc = window_proc
    window_class.hInstance = instance
    arrow_cursor = ctypes.cast(ctypes.c_void_p(IDC_ARROW), wintypes.LPCWSTR)
    window_class.hCursor = user32.LoadCursorW(None, arrow_cursor)
    window_class.hbrBackground = HANDLE(6)  # COLOR_WINDOW + 1
    window_class.lpszClassName = CLASS_NAME

    if not user32.RegisterClassW(ctypes.byref(window_class)):
        error = ctypes.get_last_error()
        if error != 1410:  # ERROR_CLASS_ALREADY_EXISTS
            raise ctypes.WinError(error)

    hwnd = user32.CreateWindowExW(
        WS_EX_LAYERED | WS_EX_APPWINDOW,
        CLASS_NAME,
        WINDOW_TITLE,
        WS_VISIBLE | WS_CAPTION | WS_SYSMENU,
        0,
        0,
        380,
        220,
        None,
        None,
        instance,
        None,
    )
    if not hwnd:
        raise ctypes.WinError(ctypes.get_last_error())

    common_style = WS_CHILD | WS_VISIBLE
    label_style = common_style
    edit_style = common_style | WS_BORDER | WS_TABSTOP | ES_AUTOHSCROLL

    create_control("STATIC", "A:", label_style, 30, 30, 60, 24, hwnd)
    controls["a"] = create_control("EDIT", "", edit_style, 110, 25, 180, 24, hwnd)
    create_control("STATIC", "B:", label_style, 30, 70, 60, 24, hwnd)
    controls["b"] = create_control("EDIT", "", edit_style, 110, 65, 180, 24, hwnd)
    create_control(
        "BUTTON",
        "Sumar",
        common_style | WS_TABSTOP | BS_DEFPUSHBUTTON,
        110,
        105,
        120,
        32,
        hwnd,
        BUTTON_ID,
    )
    controls["result"] = create_control(
        "STATIC", "Resultado:", label_style, 30, 155, 300, 24, hwnd
    )

    # Keep the controls fully readable while making the top-level window subtly transparent.
    if not user32.SetLayeredWindowAttributes(hwnd, 0, 245, LWA_ALPHA):
        raise ctypes.WinError(ctypes.get_last_error())

    user32.ShowWindow(hwnd, SW_SHOW)
    user32.UpdateWindow(hwnd)
    return hwnd


def main():
    create_window()
    message = MSG()
    while True:
        result = user32.GetMessageW(ctypes.byref(message), None, 0, 0)
        if result == 0:
            break
        if result == -1:
            raise ctypes.WinError(ctypes.get_last_error())
        user32.TranslateMessage(ctypes.byref(message))
        user32.DispatchMessageW(ctypes.byref(message))


if __name__ == "__main__":
    main()
