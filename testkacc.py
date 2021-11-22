def foo(namaorang):
	print("Halo, " + namaorang + ". Semangat tubesnya!")

while (True) :
    nama = input("Masukkan nama Anda : ")
    if (nama != ""):
        foo(nama)
    else :
        break