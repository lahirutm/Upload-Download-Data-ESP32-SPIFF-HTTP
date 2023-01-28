import os
import sys
import json
import string

GOOD_CHARS = ''.join(
    [i for i in string.printable if i not in "*\t\n\r\x0b\x0c"])


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def dump_json(path, data):
    with open(path, 'w') as f:
        f.write(json.dumps(data, indent=4))


def load_json(path):
    with open(path, 'r') as f:
        return json.loads(f.read())


def write_text(ser,  addr, size, text):
    size -= 1
    text = [ord(i) for i in text if i in GOOD_CHARS]
    if len(text) < size:
        text += [0] * (size - len(text))  # Add Padding to text
    if len(text) > size:
        text = text[:size].copy()
    text += [0]
    for i in range(size):
        ser.update(addr + i, text[i])


def read_text(ser,  addr, size):
    size -= 1
    text = []
    for i in range(size):
        c = ser.get(addr + i)
        text.append(chr(c))
    text = [i for i in text if i in GOOD_CHARS]
    if len(text) > size:
        text = text[:size].copy()
    return ''.join(text)


if __name__ == '__main__':
    print(get_ports())
