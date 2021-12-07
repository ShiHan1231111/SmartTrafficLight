from pyasn1.compat.octets import null

from Firebase import Firebase

fb = Firebase()

structure = {
    "Time":5,
    "Order": {
        "GREEN001": "TL001",
        "RED001": "TL002",
        "RED002": "TL003"
    },

    "TrafficAmount": {
        "RED001": "WAITING",
        "RED002": "WAITING"
    },

    "Event": {
        "Ambulance": {
            "TL001": "FALSE",
            "TL002": "FALSE",
            "TL003": "FALSE"
        },
        "Switch": {
            "TL001": "SWITCH",
            "TL002": "SWITCH",
            "TL003": "SWITCH"
        },
        "Capture":{
            "CM001":"CAP",
            "CM002":"CAP",
            "CM003":"CAP"
        }
    },

    "TrafficLights": {
        "TL001": {
            "Red_Light": {
                "status":"Normal",
                "malf_timestamp": "timestamp"},
            "Yellow_Light": {
                "status":"Normal",
                "malf_timestamp": "timestamp"},
            "Green_Light": {
                "status":"Normal",
                "malf_timestamp": "timestamp"},
            "status": "Normal",
            "malf_timestamp": {
                "timestamp": "timestamp"}
        },

        "TL002": {
            "Red_Light": {
                "status":"Normal",
                "malf_timestamp": "timestamp"},
            "Yellow_Light": {
                "status":"Normal",
                "malf_timestamp": "timestamp"},
            "Green_Light": {
                "status":"Normal",
                "malf_timestamp": "timestamp"},
            "status": "Normal",
            "malf_timestamp": {
                "timestamp": "timestamp"}
        },

        "TL003": {
            "Red_Light": {
                "status":"Normal",
                "malf_timestamp": "timestamp"},
            "Yellow_Light": {
                "status":"Normal",
                "malf_timestamp": "timestamp"},
            "Green_Light": {
                "status":"Normal",
                "malf_timestamp": "timestamp"},
            "status": "Normal",
            "malf_timestamp": {
                "timestamp": "timestamp"}
        }
    }
}

fb.remove_data("Server","")
fb.update("Server", structure)
