# DevOps Credentials API
API encargada de obtener credencial de psafe de la cuenta que pertenece al grupo implementador


## Endpoints

### GET /api/v1.0/"systemname"
Devuelve la credencial de la cuenta implementadora de AD.

### GET /api/v1.0/dbora/"dbinstance"/"schema"
Devuelve la credencial de la cuenta implementadora del schema en la instancia de base de datos oracle. El usuario al cual pertenece esta credencial es el nombre del schema.

### GET /healthcheck
Devuelve el status de la api.