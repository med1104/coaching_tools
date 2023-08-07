# Comandos

```bash
shiny create myapp
```

```bash
shinylive export app_FE_en docs --subdir FEen
shinylive export app_FE_es docs --subdir FEes
```
* cada vez que se actualice la app correr este comando.

## Testear 

```bash
python3 -m http.server --directory docs 8008
```
Y luego abrir en el explorador `http://localhost:8008/`

http://localhost:8008/