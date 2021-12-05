from pyasn1.compat.octets import null

from Firebase import Firebase

fb = Firebase()

structure = {
    "Order": {
        "GREEN001": "TL001",
        "RED001": "TL002",
        "RED002": "TL003"
    },

    "TrafficAmount": {
        "RED001": "fetching......",
        "RED002": "fetching......"
    },

    "Event": {
        "Ambulance": {
            "TL001": "FALSE",
            "TL002": "FALSE",
            "TL003": "FALSE"},
        "Switch": {
            "TL001": "SWITCH",
            "TL002": "SWITCH",
            "TL003": "SWITCH"
        },
    },
    "Traffic Light Status": {
        "TL001": "Normal",
        "TL002": "Normal",
        "TL003": "Normal"
    }
}

fb.remove_data("Server","")
fb.update("Server", structure)
