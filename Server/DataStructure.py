from pyasn1.compat.octets import null

from Firebase import Firebase

fb = Firebase()

structure = {
    "Order": {
        "GREEN001": "TL001",
        "RED001": "TL002",
        "RED002": "TL003"
    },

    "TrafficAmount":{
        "RED001": "fetching......",
        "RED002": "fetching......"
    }
}

fb.update("Server",structure)
