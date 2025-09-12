def externa():
    x =10

    def interna():
        nonlocal x # avisa que x vem de fora
        x= 20 # altera o  x da funcao externa
        print(f"Interna:{x}")
    
    interna()
    print(f"Externa:{x}")


externa()