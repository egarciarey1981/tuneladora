#!/bin/python

import subprocess

def listar_contextos():
    try:
        output = subprocess.check_output(["kubectl", "config", "get-contexts", "-o", "name"], text=True)
        contextos = output.splitlines()
        return contextos
    except subprocess.CalledProcessError as e:
        print("Error al obtener la lista de contextos de Kubernetes:", e)
        return []

def seleccionar_contexto(contextos):
    print("\nLista de contextos disponibles:")
    for i, contexto in enumerate(contextos):
        print(f"{i + 1}. {contexto}")

    while True:
        seleccion = input("\nSelecciona el número del contexto deseado (1, 2, etc.): ")
        try:
            seleccion = int(seleccion)
            if 1 <= seleccion <= len(contextos):
                return contextos[seleccion - 1]
            else:
                print("Selección no válida. Introduce un número válido.")
        except ValueError:
            print("Selección no válida. Introduce un número válido.")

def seleccionar_namespace(contexto):
    try:
        output = subprocess.check_output(["kubectl", "get", "namespaces", "-o", "name", "--context", contexto], text=True)
        namespaces = output.splitlines()
        print("\nLista de namespaces disponibles:")
        
        my_dict = {}

        for i, namespace in enumerate(namespaces):
            my_dict[i + 1] = namespace.replace("namespace/", "")

        if len(my_dict) > 15:
            middle = len(my_dict) // 2
            for i in range(1, middle + 1):
                print(f"{str(i).rjust(2)}. {my_dict[i]:<30}", end="")
                if i + middle <= len(my_dict):
                    print(f"{str(i+middle).rjust(2)}. {my_dict[i+middle]:<30}")
        else:
            for i, namespace in enumerate(namespaces):
                foo = namespace.replace("namespace/", "")
                print(f"{i + 1:02d}. {foo}")

        while True:
            seleccion = input("\nSelecciona el número del namespace deseado (1, 2, etc.): ")
            try:
                seleccion = int(seleccion)
                if 1 <= seleccion <= len(namespaces):
                    return (namespaces[seleccion - 1]).replace("namespace/", "")
                else:
                    print("Selección no válida. Introduce un número válido.")
            except ValueError:
                print("Selección no válida. Introduce un número válido.")
    except subprocess.CalledProcessError as e:
        print("Error al obtener la lista de namespaces de Kubernetes:", e)
        return []

def seleccionar_servicio(contexto, namespace):
    try:
        output = subprocess.check_output(["kubectl", "get", "svc", "-n", namespace, "-o", "name", "--context", contexto], text=True)
        servicios = output.splitlines()
        print("\nLista de servicios disponibles:")
        for i, servicio in enumerate(servicios):
            foo = servicio.replace("service/", "")
            print(f"{i + 1}. {foo}")

        while True:
            seleccion = input("\nSelecciona el número del servicio deseado (1, 2, etc.): ")
            try:
                seleccion = int(seleccion)
                if 1 <= seleccion <= len(servicios):
                    return servicios[seleccion - 1].replace("service/", "")
                else:
                    print("Selección no válida. Introduce un número válido.")
            except ValueError:
                print("Selección no válida. Introduce un número válido.")
    except subprocess.CalledProcessError as e:
        print("Error al obtener la lista de servicios de Kubernetes:", e)
        return []

def seleccionar_puerto_remoto(contexto, namespace, servicio):
    try:
        output = subprocess.check_output(["kubectl", "get", "svc", servicio, "-n", namespace, "-o", "jsonpath='{.spec.ports[0].port}'", "--context", contexto], text=True)
        return output.replace("'", "")
    except subprocess.CalledProcessError as e:
        print("Error al obtener el puerto del servicio de Kubernetes:", e)
        return []

if __name__ == "__main__":
    contextos = listar_contextos()
    if not contextos:
        print("No se encontraron contextos de Kubernetes.")
    else:
        contexto_seleccionado = seleccionar_contexto(contextos)
        namespace_seleccionado = seleccionar_namespace(contexto_seleccionado)
        servicio_seleccionado = seleccionar_servicio(contexto_seleccionado, namespace_seleccionado)
        puerto_remoto = seleccionar_puerto_remoto(contexto_seleccionado, namespace_seleccionado, servicio_seleccionado)
        sistema_operativo = input(f"\nSistema operativo:\n 1. Linux \n 2. Mac \n\nSelecciona el sistema operativo deseado (1, 2): ")
        puerto_local = input(f"\nIntroduce el puerto local deseado ({puerto_remoto}): ")

        if puerto_local == "":
            puerto_local = puerto_remoto

        ip_local = ""
        if sistema_operativo == "1":
            ip_local = "--address 0.0.0.0"

        print(f"\nPara acceder al servicio, ejecuta el siguiente comando:\n")
        print(f"kubectl port-forward --context {contexto_seleccionado} --namespace {namespace_seleccionado} service/{servicio_seleccionado} {puerto_local}:{puerto_remoto} {ip_local}")
