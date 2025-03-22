
from .entitties.User import User
class ModelUser():
    
    @classmethod
    def login(self,db, username):
        try:
            cursor=db.connect.cursor()
            sql="SELECT idusuario, username, password, idcliente from usuario where username='{}'".format(username)
            cursor.execute(sql)
            row=cursor.fetchone()
            
            if row != None:
              user=User(row[0], row[1], User.check_password(row[2], user.password), row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)