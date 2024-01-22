#!/bin/python

import subprocess
import json

def listar_proyectos():
    try:
        output = subprocess.check_output(["gcloud", "projects", "list", "--format", "value(projectId)"], text=True)
        proyectos = output.splitlines()
        proyectos = list(filter(lambda x: 'fc-db' in x, proyectos))
        return proyectos
    except subprocess.CalledProcessError as e:
        print("Error al obtener la lista de contextos de Kubernetes:", e)
        return []

def seleccionar_proyecto(proyectos):
    print("\nLista de proyectos disponibles:")
    for i, proyecto in enumerate(proyectos):
        print(f"{i + 1}. {proyecto}")

    while True:
        seleccion = input("\nSelecciona el número del proyecto deseado (1, 2, etc.): ")
        try:
            seleccion = int(seleccion)
            if 1 <= seleccion <= len(proyectos):
                return proyectos[seleccion - 1]
            else:
                print("Selección no válida. Introduce un número válido.")
        except ValueError:
            print("Selección no válida. Introduce un número válido.")

def seleccionar_instancia(proyecto):
    try:
        output = subprocess.check_output(["gcloud", "compute", "instances", "list", "--project", proyecto, "--format", "value(NAME)"], text=True)
        instancias = output.splitlines()
        print("\nLista de instancias disponibles:")
        
        my_dict = {}

        for i, instancia in enumerate(instancias):
            my_dict[i + 1] = instancia

        if len(my_dict) > 15:
            middle = len(my_dict) // 2
            for i in range(1, middle + 1):
                print(f"{str(i).rjust(2)}. {my_dict[i]:<40}", end="")
                if i + middle <= len(my_dict):
                    print(f"{str(i+middle).rjust(2)}. {my_dict[i+middle]:<40}")
        else:
            for i, instancia in enumerate(instancias):
                print(f"{i + 1:02d}. {instancia}")

        while True:
            seleccion = input("\nSelecciona el número de la instancia deseada (1, 2, etc.): ")
            try:
                seleccion = int(seleccion)
                if 1 <= seleccion <= len(instancias):
                    return instancias[seleccion - 1]
                else:
                    print("Selección no válida. Introduce un número válido.")
            except ValueError:
                print("Selección no válida. Introduce un número válido.")
    except subprocess.CalledProcessError as e:
        print("Error al obtener la lista de contextos de Kubernetes:", e)
        return []

def seleccionar_puerto(proyecto, instancia):
    try:
        comando = [
            "gcloud",
            "compute",
            "instances",
            "describe",
            instancia,
            "--project",
            proyecto,
            "--format=json"
        ]
        output = subprocess.check_output(comando, text=True)
        instancia = json.loads(output)
        return instancia["labels"]["db-port"]
    except subprocess.CalledProcessError as e:
        print("Error al obtener el puerto de la instancia:", e)
        return []


if __name__ == "__main__":
    proyectos = listar_proyectos()
    if not proyectos:
        print("No hay proyectos disponibles.")
    else:
        proyecto_seleccionado = seleccionar_proyecto(proyectos)
        instancia_seleccionada = seleccionar_instancia(proyecto_seleccionado)
        puerto = seleccionar_puerto(proyecto_seleccionado, instancia_seleccionada)

        print(f"\nPara conectar con la base de datos, ejecuta el siguiente comando:\n")
        print(f"gcloud compute start-iap-tunnel \"{instancia_seleccionada}\" {puerto} --project {proyecto_seleccionado} --local-host-port=0.0.0.0:{puerto}\n")
