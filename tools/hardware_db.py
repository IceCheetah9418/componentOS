HARDWARE_PROFILES = {
    "esp32": {
        "allowed_modules": ["machine", "time", "network", "esp32", "math", "dht"],
        "default_pins": {"sda": 21, "scl": 22, "tx": 1, "rx": 3}
    },
    "esp8266": {
        "allowed_modules": ["machine", "time", "network", "esp8266", "math", "dht"],
        "default_pins": {"sda": 4, "scl": 5, "tx": 1, "rx": 3}
    },
    "pico_w": {
        "allowed_modules": ["machine", "time", "network", "rp2", "math", "dht"],
        "default_pins": {"sda": 4, "scl": 5, "tx": 0, "rx": 1}
    },
    "raspberry_pi": {
        "allowed_modules": ["board", "digitalio", "busio", "time", "math", "os"],
        "default_pins": {"sda": 2, "scl": 3, "tx": 14, "rx": 15}
    },
    "stm32": {
        "allowed_modules": ["machine", "time", "pyb", "math"],
        "default_pins": {"sda": "PB9", "scl": "PB8", "tx": "PA9", "rx": "PA10"}
    },
    "arduino_nano_rp2040": {
        "allowed_modules": ["machine", "time", "network", "rp2", "math", "dht"],
        "default_pins": {"sda": 18, "scl": 19, "tx": 0, "rx": 1}
    }
}

def get_hardware_profile(device_type: str) -> dict:
    return HARDWARE_PROFILES.get(device_type.lower(), {"allowed_modules": ["machine", "time"], "default_pins": {}})
