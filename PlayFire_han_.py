from Firebase import Firebase

fb = Firebase()
fb.remove_data("Testing","Color")

while True:
    flag = input("input number [1 - 3] :")
    fb.update("Testing", {"Controller":flag})
