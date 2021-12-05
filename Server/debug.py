from pyasn1.compat.octets import null

from Firebase import Firebase

fb = Firebase()

a = fb.access_by_path("Server/Event/Switch/TL001")
print(a)