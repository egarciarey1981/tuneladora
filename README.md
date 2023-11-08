# tuneladora

Harto de tener que entrar en Kubernetes para consultar el namespace, el nombre del servicio y el puerto para crear un túnel a un servicio, he creado este script en Python acelerar la creación de túneles.

Lo dejo aquí por si a alguien le puede ser útil.

```python
python tuneladora.py

Lista de contextos disponibles:
1. contexto-a
2. contexto-b
3. contexto-c
4. contexto-d

Selecciona el número del contexto deseado (1, 2, etc.): 1

Lista de namespaces disponibles:
 1. namespace-a                   2. namespace-b
 3. namespace-c                   4. namespace-d
 5. namespace-e                   6. namespace-f
 7. namespace-g                   8. namespace-h

Selecciona el número del namespace deseado (1, 2, etc.): 1

Lista de servicios disponibles:
1. servicio-a
2. servicio-b
3. servicio-c
4. servicio-d

Selecciona el número del servicio deseado (1, 2, etc.): 1

Para acceder al servicio, ejecuta el siguiente comando:

kubectl port-forward --context contexto-a --namespace namespace-a service/servicio-a 9306:9306 --address 0.0.0.0
```

