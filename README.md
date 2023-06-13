# Python Package Pipeline

Esta librería contiene funciones para el manejo de tareas en procesamiento paralelo con multiprocessing asincrónico



## Desarrollo

Crear archivo `requirements.txt`:

```bash
pipenv requirements > requirements.txt
```

Si en el archivo `requirements.txt` hay una dependencia que viene de Github, deberá estar definida de la siguiente manera:
```txt
<name> @ git+https://github.com/lcastiglione/pp-pipeline.git@<id>#egg=pipeline
```



Tests:

```bash
python -m unittest discover -s 'tests' -p 'test_pipeline.py'
```



### Control de versiones:

```bash
git tag -a <tag> -m "<descripcion>" # Crear tag local
git push origin <tag>               # Subir tag a repositorio remoto
git tag -d <tag>                    # Eliminar tag en forma local
git push --delete origin <tag>      # Subir tag a repositorio remoto
```



## Instalación

```bash
pipenv install git+https://github.com/lcastiglione/pp-pipeline#egg=pipeline



## Ejemplo de uso
