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
            "IS PASS":"AMBULANCE NOT PASS",
            "TL001": "NO AMBULANCE",
            "TL002": "NO AMBULANCE",
            "TL003": "NO AMBULANCE"
        },
        "Switch": {
            "TL001": "SWITCH",
            "TL002": "SWITCH",
            "TL003": "SWITCH"
        },
        "Capture":{
            "CM001":"IDLE",
            "CM002":"IDLE",
            "CM003":"IDLE"
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
