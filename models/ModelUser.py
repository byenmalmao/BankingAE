# In models/ModelUser.py
from .entitties.User import User

class ModelUser:
    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            
            sql = """SELECT IdUsuario, username, password FROM usuario 
                     WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            
            if row:
                password_ok = User.check_password(row[2], user.password)
                
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
                
                # Buscar cuentas del cliente
                cuenta = []
                if cliente_data:
                    cursor.execute("""SELECT * FROM cuenta 
                                   WHERE IdCliente = {}""".format(cliente_data['IdCliente']))
                    cuenta_rows = cursor.fetchall()
                    
                    for cuenta_row in cuenta_rows:
                        cuenta.append({
                            'id': cuenta_row[0],
                            'tipo': cuenta_row[3],
                            'saldo': cuenta_row[4],
                            'fecha_apertura': cuenta_row[5],
                            'estado': cuenta_row[6],
                            'numero': cuenta_row[7]
                        })
                
                return User(
                    id=row[0],
                    username=row[1],
                    password=password_ok,
                    cliente=cliente_data,
                    cuenta=cuenta
                )
            return None
            
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            
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
                
                # Buscar cuentas del cliente
                cuenta = []
                if cliente_data:
                    cursor.execute("""SELECT * FROM cuenta 
                                   WHERE IdCliente = {}""".format(cliente_data['IdCliente']))
                    cuenta_rows = cursor.fetchall()
                    
                    for cuenta_row in cuenta_rows:
                        cuenta.append({
                            'id': cuenta_row[0],
                            'tipo': cuenta_row[3],
                            'saldo': cuenta_row[4],
                            'fecha_apertura': cuenta_row[5],
                            'estado': cuenta_row[6],
                            'numero': cuenta_row[7]
                        })
                
                return User(
                    id=row[0],
                    username=row[1],
                    password=None,
                    cliente=cliente_data,
                    cuenta=cuenta
                )
            return None
            
        except Exception as ex:
            raise Exception(ex)