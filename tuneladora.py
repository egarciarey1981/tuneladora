#!/bin/python

if __name__ == "__main__":
    tunnel_type = input("\nTipos de túneles:\n 1. Servicio \n 2. Base de datos \n\nSelecciona el tipo de túnel deseado (1, 2): ")
    
    
    if tunnel_type == "1":
        exec(open("/home/egr/repositorios/tuneladora/servicio.py").read())
    elif tunnel_type == "2":
        exec(open("/home/egr/repositorios/tuneladora/database.py").read())
    else:
        print(f"\n¿DÓNDE HAS VISTO TÚ EL TÚNEL {tunnel_type}?")
