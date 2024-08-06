#!/usr/bin/python

import subprocess, json, sys, time

def get_icon(code):
    icons = {
        "01d": "",
        "01n": "",
        "02d": "",
        "02n": "",
        "03d": "󰖐",
        "03n": "󰖐",
        "04d": "",
        "04n": "",
        "09d": "",
        "09n": "",
        "10d": "",
        "10n": "",
        "11d": "",
        "11n": "",
        "13d": "󰖘",
        "13n": "󰖘",
        "50d": "",
        "50n": "" 
    }
    try:
        return icons[code]
    except KeyError:
        return None

def get_temperature():
    try:
        result = subprocess.run(
            ["curl", "-s", "wttr.in?format=%t"],
            capture_output=True,
            text=True
        )
        temperature = result.stdout.strip().replace('+', '')
        return temperature
    except Exception as e:
        return f"Error: {e}"

def main():
    # Aquí puedes agregar la lógica para obtener el código del ícono si es necesario
    icon_code = "01d"  # Ejemplo de código de ícono
    data = {
        "icon": get_icon(icon_code),
        "temp": get_temperature()
    }
    return data

if __name__ == "__main__":
    try:
        while True:
            try:
                sys.stdout.write(json.dumps(main()) + "\n")
                sys.stdout.flush()
                time.sleep(1800)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(2)

    except KeyboardInterrupt:
        exit(0)
