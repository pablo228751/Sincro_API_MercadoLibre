from __future__ import print_function
import time
import meli
from meli.rest import ApiException
from pprint import pprint
import pymysql
import time
from calculo_cod import CodigoSKU
from calculo_meli import Calcular_M_sku


class Mercadolibre():
    configuration = meli.Configuration(
    host = "https://api.mercadolibre.com"
)


    var=open("meli.txt","r")
    var_lineas=var.readlines()
    var.close()
    #print(var_lineas)
    with meli.ApiClient() as api_client:        
        api_instance = meli.OAuth20Api(api_client)
        api_instance_modif = meli.RestClientApi(api_client)
        grant_type =var_lineas[0].rstrip()
        client_id =var_lineas[1].rstrip()
        client_secret =var_lineas[2].rstrip()
        redirect_uri =var_lineas[3].rstrip()   
        code =var_lineas[4].rstrip()
        refresh_token =var_lineas[5].rstrip()
        access_token =var_lineas[6].rstrip()
        #PARA MODIFICAR        
        producto=''
        id_producto=''
        sku_producto=''
        cant_producto=''
        usr_id=var_lineas[20].rstrip()
        #resource = ('items/MLA')
        resource = ('items/')  
        var1=False
        #estado=''
        precio=''
        cantidad=None
        nombre=''
        valor_id=''
        valor_nom=''        
        cantidad_vend=''
        img_ids=None
        variaciones=None
        atributos=None
        atributos_comb=None ##Revisar esta variable
        imagenes=[]
        lista_body=[]
        metodo1=True
        lista_MLA=[]
        




                     

    
#### PARA RECUPERAR TOKEN

    def token(self):


        try:    
            api_response = self.api_instance.get_token(grant_type=self.grant_type, client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, code=self.code, refresh_token=self.refresh_token)
            api_response
            '''
            ###Leer diccionario (api_response)
            diccion=api_response
            
            for k,v in diccion.items():
                print ("%s -> %s" %(k,v))
            '''
            self.access_token=api_response['access_token']
            print('EL nuevo token es:',self.access_token.strip())
            var=open("meli.txt","r+")
            self.var_lineas[6]=(self.access_token.strip()+'\n')
            var.seek(0)
            var.writelines(self.var_lineas)
            var.close()
        except ApiException as e:
            print(e)

####METODO GET
    def obtener(self):
        try:            
            resource2 = ('items/'+self.producto+'?include_attributes=all')
            tk=self.actualizar_tk()
            api_response = self.api_instance_modif.resource_get(resource2, tk)
            #pprint(api_response)
            self.variaciones=api_response['variations']
            #pprint(self.variaciones)
            # Utilizo esta condicion para productos que no contienen la proiedad attribute_combinations
            if (self.variaciones==[]):
                self.nombre='Vacio'
                self.valor_id='Vacio'
                self.valor_nom='Vacio'
            else:
                for elem in self.variaciones:
                    for k,v in elem.items():
                        if(k=='id'):
                        ###### ABAJO modifico la cantidad de id_producto y agrego el dict a la lista para Body                            
                            if v == int(self.id_producto):                                
                                self.atributos_comb=v
                                elem['available_quantity']=self.cantidad
                                dic={'id':elem['id'],'price':elem['price'],'attribute_combinations':elem['attribute_combinations'],'available_quantity':elem['available_quantity'],'sold_quantity':elem['sold_quantity'],'picture_ids':elem['picture_ids']}
                                self.lista_body.append(dic)
                                print('Se modifico Cantidad en body:')
                                print(dic)
                        ######### ABAJO agrego a la lista para body el reto de los productos
                            else:
                                dic={'id':elem['id'],'price':elem['price'],'attribute_combinations':elem['attribute_combinations'],'available_quantity':elem['available_quantity'],'sold_quantity':elem['sold_quantity'],'picture_ids':elem['picture_ids']}
                                self.lista_body.append(dic)

                #print(self.lista_body)
                print('*******************************************************************************************************************')
                #print(self.diccionario)
                #print(self.lista_body)            
            
        except ApiException as e:
            print("Error al obtener: %s\n" % e)
            #return 337

#### PARA MODIFICAR

    def modificar(self):
        self.obtener()
        body = {"variations": self.lista_body }
    
        try:
            tk=self.actualizar_tk()
            api_response = self.api_instance_modif.resource_put((self.resource+self.producto), tk, body, async_req=True)
            api_response.get()
            print('Desde Modificar se envio solicitud')
    

            return [7777,0]       
    
        except ApiException as e:
            #Nota: Revisar Modificaciones en ApiException
            print('Error:',e)
            return [337,0]
        



    def hilo1(self):
        resultado=self.modificar()
        if (str(resultado[0])=='400'): 
            print("Dentro de Exception 400") # Bad request, error en la sintaxis de la consulta
            print(self.producto)
            print(self.cantidad)
            print('Revisar PRODUCTO: ',self.producto, ' CANTIDAD: ',self.cantidad)
            if self.metodo1:
            	print('mercadol.py METODO1...........................................')
            	return [999999,0]
            else:
            	print('Error 400 en hilo1 ')
            	return [404,0]
        elif (str(resultado[0])=='7777'):
            ################ Si lista_MLA contiene otro codigo reinicio el ciclo            
            print("Item MERCADO LIBRE Modificado...") #Return True (api_response.get())
            self.var1=False
            ##self.lista_MLA.pop(0)
            if len(self.lista_MLA) > 0:
                #### SI esxiste mas de un codigo retorno
                return [44,0]
            else:
                return [43,0]

        elif (str(resultado[0])=='401'):
            print("Dentro de Exception 401") #Unauthorized, Error en acces_token procede refresh
            self.token()
            print('token en 401')
            self.var1=True
        elif (str(resultado[0])=='9999998'):
            print("Error en Metodo Obtener")
        elif (str(resultado[0])=='404'):
            print("NO se encontro Producto") 
        else:
            print("N° de Exception desconocido: ",resultado)
        return [0,0]

    def Implementar(self,prod,cant,cod_mel_sku):
        print('IMPLEMENTAR SINCRO: PRODUCTO:',prod,' CANT:',cant,' COD_MELI_SKU:',cod_mel_sku)
        self.img_ids=None
        self.producto=''
        self.id_producto=''
        self.var1=False
        self.cantidad=None
        self.lista_body.clear()
        self.valor_id=''
        self.valor_nom=''
        self.nombre=''
        self.atributos_comb=None
        self.variaciones=None  ##Reseteo Variables
        self.atributos=None
        self.cantidad=cant ##Esta es la cantidad a modificar
        self.mel_sku=cod_mel_sku
        buscar_cod2=None
        try:
            tk=self.actualizar_tk()
            buscar_cod=Calcular_M_sku().calcular_M(prod,self.usr_id,tk)
            if buscar_cod:
                #### cargar lista MLA si existe
                try:
                    if len(buscar_cod[4]) >1:
                        print('Lista MLA es mayor a UNO...Agregando a Lista_MLA ',len(buscar_cod[4]),' codigos')
                        self.lista_MLA=buscar_cod[4]
                        print('LISTA_MLA_Antes:',self.lista_MLA)
                        self.lista_MLA.pop(0)
                        print('LISTA_MLA_Despues:',self.lista_MLA)
                except:
                    print ('Error al consultar lista mla_DANTE')
                ################ Fin cargar lista
                if buscar_cod[0] == '**':
                    tk=self.actualizar_tk()
                    buscar_cod2=Calcular_M_sku().calcular_M(buscar_cod[1],self.usr_id,tk)
                    self.producto=buscar_cod2[0]
                    self.sku_producto=buscar_cod2[1]
                    self.id_producto=buscar_cod2[2]
                    self.cant_producto=buscar_cod2[3]
                elif buscar_cod[0] == '-':
                    return [21,0]
                elif buscar_cod[0] == 99999:
                    print('Expiró Token....1')
                    self.token()                    
                    #self.var1=True
                    tk=self.actualizar_tk()
                    buscar_cod=Calcular_M_sku().calcular_M(prod,self.usr_id,tk)
                    if buscar_cod:
                        try:
                            if len(buscar_cod[4]) >1:
                                print('Lista MLA es mayor a UNO...Agregando a Lista_MLA ',len(buscar_cod[4]),' codigos')
                                self.lista_MLA=buscar_cod[4]
                                print('LISTA_MLA2_Antes-2:',self.lista_MLA)
                                self.lista_MLA.pop(0)
                                print('LISTA_MLA2_Despues2:',self.lista_MLA)
                        
                            self.producto=buscar_cod[0]
                            self.sku_producto=buscar_cod[1]
                            self.id_producto=buscar_cod[2]
                            self.cant_producto=buscar_cod[3]
                        except:
                            print ('Error2 al consultar lista mla_DANTE2')

                else:
                    if buscar_cod: 
                        self.producto=buscar_cod[0]
                        self.sku_producto=buscar_cod[1]
                        self.id_producto=buscar_cod[2]
                        self.cant_producto=buscar_cod[3]
                    else:
                        self.token()
                        print('Activar token.....')
                        try:
                            tk=self.actualizar_tk()
                            buscar_cod=Calcular_M_sku().calcular_M(prod,self.usr_id,tk)
                            self.producto=buscar_cod[0]
                            self.sku_producto=buscar_cod[1]
                            self.id_producto=buscar_cod[2]
                            self.cant_producto=buscar_cod[3]
                            print('token en buscar_cod2')
                            self.var1=True
                        except:
                            print('Error__*')
            else:
                print('Buscar_cod llega Vacio')
        except ApiException as e:
            print('Error en Calcular_M_sku en mercadol.py...llamando a refresh_token...')
            self.token()
            print('token en ApiException')
            self.var1=True
        ### Aqui cortar el flujo de Script si el return de producto o id_producto es = '-'(return de clase Calcular_M_sku)
        print('Hilo_1')        
        obj_h=self.hilo1()
        if obj_h == None:
            obj_h = [0,0]
        if str(obj_h[0]) == '999999':
            print('999999 sale de aqui')
            return [999999,0]
        elif str(obj_h[0]) == '337':
            print('Err_ 337 en modificar')
        elif str(obj_h[0]) == '44':
            return [44,self.lista_MLA]
        if (self.var1==True):
            print('2° Intento, ejecutando hilo1...')
            try:
                if len(buscar_cod[4]) >1:
                    print('Lista MLA Reintentando...Agregando a Lista_MLA2 ',len(buscar_cod[4]),' codigos')
                    self.lista_MLA=buscar_cod[4]
                    self.lista_MLA.pop(0)
                    print('LISTA_MLA2:',self.lista_MLA)
            except:
                print ('Error al consultar lista mla_DANTE')
            try:
                tk=self.actualizar_tk()
                buscar_cod=Calcular_M_sku().calcular_M(prod,self.usr_id,tk)
                try:
                    
                    if '**' in buscar_cod[0]:
                        tk=self.actualizar_tk()
                        buscar_cod2=Calcular_M_sku().calcular_M(buscar_cod[1],self.usr_id,tk)
                        self.producto=buscar_cod2[0]
                        self.sku_producto=buscar_cod2[1]
                        self.id_producto=buscar_cod2[2]
                        self.cant_producto=buscar_cod2[3]
                    #elif buscar_cod[0] == '-':
                    elif '-' in buscar_cod[0]:
                        return [21,0]
                    elif buscar_cod[0] == 99999:
                        print('Expiró Token....2')
                        self.token()
                        self.var1=True
                    else:
                        self.producto=buscar_cod[0]
                        self.sku_producto=buscar_cod[1]
                        self.id_producto=buscar_cod[2]
                        self.cant_producto=buscar_cod[3]
                except:
                    return [477,0]
            except ApiException as e:
                print('2° Intento...Error en Calcular_M_sku en mercadol.py...')
            print('Hilo_2')
            obj_h=self.hilo1()
            if obj_h == None:
                obj_h = [0,0]
            if str(obj_h[0])=='999999':                
                return [999999,0]
            elif str(obj_h[0]) == '337':
                print('Err_ 337 en modificar')
            elif str(obj_h[0]) == '44':
                return [44,self.lista_MLA]
            elif str(obj_h[0]) == '43':
                return [43,0]





    def Implementar2(self,prod,meli_cod,cant2):
        self.img_ids=None
        self.producto=''
        self.id_producto=''
        self.var1=False
        self.cantidad=None
        self.lista_body.clear()
        self.valor_id=''
        self.valor_nom=''
        self.nombre=''
        self.atributos_comb=None
        self.variaciones=None
        self.atributos=None
        self.cantidad=cant2
        self.mel_sku=meli_cod
        try:
            var=open("meli.txt","r")
            var_lineas=var.readlines()
            var.close()
            tk =var_lineas[6].rstrip()
            self.access_token=tk
            buscar_cod=Calcular_M_sku().calcular_M2(prod,meli_cod,self.usr_id,tk)
            if buscar_cod:
                if buscar_cod[0] == 99999:
                    ### REVISAR si var 1 aplica en este nivel
                    print('Expiró Token....3')
                    self.token()                    
                    self.var1=True
                else:
                    self.producto=buscar_cod[0]
                    self.sku_producto=buscar_cod[1]
                    self.id_producto=buscar_cod[2]
                    self.cant_producto=buscar_cod[3]
            else:
                print('No se encontro el segundo codigo')
                return [4347,0]
            print('Hilo_3')
            obj_h=self.hilo1()
            if obj_h == None:
                obj_h = [0,0]
            if str(obj_h[0]) == '999999':
                print('999999 sale de aqui')
                return [999999,0]
            elif str(obj_h[0]) == '337':
                print('Err_ 337 en modificar')
            elif str(obj_h[0]) == '44':
                return [44,self.lista_MLA[1]]
            elif str(obj_h[0])=='7777':
                return [7777,0]
            elif str(obj_h[0]) == '43':
                print('Lista_MLA Vacia...retornando...')
                return [43,0]
            else:
                return [obj_h,0]
        except ApiException as e:
            print('Error_F99')
            return [41,0]
    def actualizar_tk(self):
        try:
            var=open("meli.txt","r")
            var_lineas=var.readlines()
            var.close()
            tk =var_lineas[6].rstrip()
            self.access_token=tk
            return tk
        except:
            print('No se pudo recuperar token')




def recibe_parametros(pro,cant2):
    mercado2=Mercadolibre()
    cod_mel_sku=pro
    calculo_codigo=CodigoSKU().calcular(cod_mel_sku)
    code=calculo_codigo[1]
    sku=calculo_codigo[0]
    color=calculo_codigo[2]
    talle=calculo_codigo[3]
    cant=cant2
    print('recibe_parametros sku recibido: ',pro, 'cantidad: ',cant2)
    obj=mercado2.Implementar(sku,cant,cod_mel_sku)
    if obj == None:
        obj = [0,0]
    if str(obj[0])== '999999':
        print('Retorno 4 Objeto: ', obj)
        return [999999,0]
    elif str(obj[0])=='7777':
        return [7777,0]
    elif str(obj[0]) == '44':
        print('Lista MLA llena, siguiente codigo: ',obj[1])
        return [44,obj[1]]
    elif str(obj[0]) == '43':
        print('Lista_MLA Vacia...retornando...')
        return [43,0]
    else:
        return [obj,0]






'''
mercado=Mercadolibre()
cod_mel_sku='82825521-36.5'
calculo_codigo=CodigoSKU().calcular(cod_mel_sku)
code=calculo_codigo[1]
sku=calculo_codigo[0]
color=calculo_codigo[2]
talle=calculo_codigo[3]
cant=0


llamar=mercado.Implementar(sku,cant,cod_mel_sku)
if llamar[0] == 44:
elif llamar[0] == 43:
    print('Lista MLA esta Vacia')
'''





