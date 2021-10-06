# APIREST Plerk
---
## Instalación y uso 

Procedemos a clonar el proyecto

> git clone https://github.com/Ladivcr/Api_P.git

Una vez clonado, nos movemos al proyecto y creamos nuestro entorno virtual para 
instalar las dependencias

> cd Api_P

>  python3 -m venv .plerkENV

>  source .plerkENV/bin/activate

> cd plerk

>  pip install -r requirements.txt

**NOTA:** en caso de que no puedas instalar por el error de _pkg-resources == 0.0.0_
abre el archivo de _requirements.txt_ y elimina _pkg-resources_ y vuelve a correr el comando de instalación

Sí todo ha salido bien, puedes ejecutar el siguiente comando para correr el proyecto

> python3 manage.py runserver

## Visualización de lo establecido en la prueba

> Datos de las transacciones: http://127.0.0.1:8000/transactions/

> Datos de las compañias: http://127.0.0.1:8000/companies/

> Servicios de resumen: http://127.0.0.1:8000/services/

> Servicio de empresa:  http://127.0.0.1:8000/services/<ID_Empresa>

> > **ejemplo:** http://127.0.0.1:8000/services/4f0270bb-13a6-4b89-a21a-72594f4b85c5

- Además del día en que se realizarón **más** transacciones también se ha determinado el mes en el que se realizarón **más** transacciones

## Collection postman
### GET
- http://127.0.0.1:8000/transactions/
- http://127.0.0.1:8000/companies/
- http://127.0.0.1:8000/services/
- http://127.0.0.1:8000/services/4f0270bb-13a6-4b89-a21a-72594f4b85c5


## Diagrama de la base de datos
Se trata de una relación de uno a muchos, ya que si lo pensamos detenidamente una empresa puede estar asociada a múltiples transacciones pero una transacción esta asociada únicamente a una empresa. De ahí la **relación 1:M**

| Empresa             | 
|---------------------|
| Nombre VARCHAR(50)  |
| Status BOOL         |
| ID VARCHAR(36)      |
| --------------------|
| PRIMARY KEY ID      |


**1:M**


| Transacción                  | 
|------------------------------|
| ID VARCHAR(36)               |
| ID_Empresa VARCHAR(36)       |
| Price FLOAT                  |
| Fecha_Transaction DATETIME   |
| Status_Transaction VARCHAR(8)|
| Status_Approved BOOL         |
| Cobro_Final BOOL             |
| -----------------------------|
| PRIMARY KEY ID               |
| FOREIGN KEY ID_Empresa       |
 
