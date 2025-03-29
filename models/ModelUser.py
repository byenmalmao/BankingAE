from .entitties.User import User

class ModelUser:
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            
            # Consulta usando los nombres exactos de tus columnas
            sql = """SELECT IdUsuario, username, password FROM usuario 
                     WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            
            if row:
                # Verificar contraseña
                password_ok = User.check_password(row[2], user.password)
                
                # Buscar cliente relacionado (usando IdUsuario)
                cursor.execute("""SELECT * FROM cliente 
                               WHERE IdUsuario = {}""".format(row[0]))
                cliente_row = cursor.fetchone()
                
                # Convertir a diccionario si existe cliente
                cliente_data = None
                if cliente_row:
                    # Asumiendo que sabes el orden de las columnas en cliente
                    cliente_data = {
                        'IdCliente': cliente_row[0],
                        'Nombre': cliente_row[1],
                        # ... otras columnas que necesites
                    }
                
                return User(
                    id=row[0],  # IdUsuario
                    username=row[1],
                    password=password_ok,
                    cliente=cliente_data
                )
            return None
            
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            
            # Obtener usuario
            sql = "SELECT IdUsuario, username FROM usuario WHERE IdUsuario = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            
            if row:
                # Buscar cliente relacionado
                cursor.execute("""SELECT * FROM cliente 
                               WHERE IdUsuario = {}""".format(row[0]))
                cliente_row = cursor.fetchone()
                
                cliente_data = None
                if cliente_row:
                    cliente_data = {
                        'IdCliente': cliente_row[0],
                        'Nombre': cliente_row[1],
                        # ... otras columnas
                    }
                
                return User(
                    id=row[0],  # IdUsuario
                    username=row[1],
                    password=None,
                    cliente=cliente_data
                )
            return None
            
        except Exception as ex:
            raise Exception(ex)