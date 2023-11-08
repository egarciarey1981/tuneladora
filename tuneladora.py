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
            foo = namespace.replace("namespace/", "")
            my_dict[i + 1] = foo

        if len(my_dict) > 15:
            for i in range(1, len(my_dict) + 1, 2):
                print(f"{str(i).rjust(2)}. {my_dict[i]:<30}", end="")
                print(f"{str(i+1).rjust(2)}. {my_dict[i+1]:<30}")
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


def seleccionar_puerto(namespace, servicio):
    try:
        output = subprocess.check_output(["kubectl", "get", "svc", servicio, "-n", namespace, "-o", "jsonpath='{.spec.ports[0].port}'"], text=True)
        return output.replace("'", "")
    except subprocess.CalledProcessError as e:
        print("Error al obtener el puerto del servicio de Kubernetes:", e)
        return []

def seleccionar_servicio(namespace):
    try:
        output = subprocess.check_output(["kubectl", "get", "services", "-o", "name", "--namespace", namespace], text=True)
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

if __name__ == "__main__":
    contextos = listar_contextos()
    if not contextos:
        print("No se encontraron contextos de Kubernetes.")
    else:
        contexto_seleccionado = seleccionar_contexto(contextos)
        namespace_seleccionado = seleccionar_namespace(contexto_seleccionado)
        servicio_seleccionado = seleccionar_servicio(namespace_seleccionado)
        puerto = seleccionar_puerto(namespace_seleccionado, servicio_seleccionado)

        print(f"\nPara acceder al servicio, ejecuta el siguiente comando:\n")
        print(f"kubectl port-forward --context {contexto_seleccionado} --namespace {namespace_seleccionado} service/{servicio_seleccionado} {puerto}:{puerto} --address 0.0.0.0\n")
