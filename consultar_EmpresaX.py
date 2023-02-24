from __future__ import print_function
import time
import meli
from meli.rest import ApiException
from pprint import pprint
from datetime import datetime
import pymysql
import time
from mercadol import Mercadolibre
from mercadol import recibe_parametros


class Meli_D_():
    configuration = meli.Configuration(host = "https://api.mercadolibre.com")
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
    def errores(self,det,suc,sku):
        try:
            var=open("meli.txt","r")
            var_lineas=var.readlines()
            var.close()
            conexion = pymysql.connect(host=var_lineas[7].rstrip(),
                             user=var_lineas[8].rstrip(),
                             password=var_lineas[9].rstrip(),
                             db=var_lineas[10].rstrip())
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error en Conexion: ", e)
            time.sleep(6)
        try:
            fec_hor = datetime.now()
            with conexion.cursor() as cursor:
                cursor.execute("INSERT INTO err (detalle,sucursal,codigo,fecha_hora) VALUES ('{}','{}','{}','{}')".format(det,suc,sku,fec_hor))
                n=cursor.rowcount
                conexion.commit()
                conexion.close()
                return n
        finally:
            cursor.close()
    def token(self):

        try:    
            api_response = self.api_instance.get_token(grant_type=self.grant_type, client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, code=self.code, refresh_token=self.refresh_token)
            api_response
            self.access_token=api_response['access_token']
            print('EL nuevo token es:',self.access_token.strip())
            var=open("meli.txt","r+")
            self.var_lineas[6]=(self.access_token.strip()+'\n')
            var.seek(0)
            var.writelines(self.var_lineas)
            var.close()
        except ApiException as e:
            print('Error en Token',e)
    def filtrar_MLA(self):
        lista_mla=[]
        cont=0
        offset=0
        limit=100
        continuar=True
        configuration = meli.Configuration(host = "https://api.mercadolibre.com")
        
        while continuar == True:
            try:
                var=open("meli.txt","r")
                var_lineas=var.readlines()
                var.close()
                tk =var_lineas[6].rstrip()
                usr_id=var_lineas[20].rstrip()
                with meli.ApiClient() as api_client:
                    api_instance = meli.RestClientApi(api_client)
                    resource = 'users/'+usr_id+'/items/search?&offset='+str(offset)+'&limit='+str(limit)
                    access_token = tk
                    api_response = api_instance.resource_get(resource, access_token)
                    mla=api_response['results']
                    if mla:
                        for elem in mla:
                            lista_mla.append([cont,elem])
                            cont += 1                            
                    else:
                        continuar=False
                    
            except ApiException as e:
                print("Error al consultar RestClientApi->resource_get: %s\n" % e)
                self.token()
            if lista_mla:
                offset=limit
                print('El nuevo valor de offset es: ',offset)
                limit= limit+99
                print('El nuevo valor de limit es: ',limit)
        if lista_mla:
            self.filtrar_SKU(lista_mla,tk)



    def filtrar_SKU(self,lista_mla,tk):
        print('EN filtrar_SKU')
        continuar=True
        cod_mla=''
        lista_rta=[]
        vueltas=str(lista_mla[-1][0])
        print('Cantidad de Vueltas:',vueltas)
        contador=1
        
        for i in lista_mla:
            #print('CONTADOR:::::::::::::',contador)
            contador += 1
            try:
                cod_mla=str(i[1]).strip()
                #print('Codigo_MLA ES::::',cod_mla)
                with meli.ApiClient() as api_client:
                    api_instance = meli.RestClientApi(api_client)
                resource = ('items/'+cod_mla+'?include_attributes=all')
                api_response = api_instance.resource_get(resource, tk)
                variaciones=api_response['variations']
                for elem in variaciones:
                    for k,v in elem.items():
                        if(k=='attributes'):
                            att=v
                            idd=elem['id']
                            cant=elem['available_quantity']
                            for e in att:
                                if (e['id']  == 'SELLER_SKU'):
                                    sku2=e
                                    sku=sku2['value_name'].strip()
                                    '''
                                    print('**********************************************************************')
                                    print('SKU: '+sku)
                                    print('ID: ',idd)
                                    print('Cantidad: ',cant)
                                    print('******************************************************************')
                                    '''
                                    lista_rta.append([contador,sku,idd,cant])
            except ApiException as e:
                print("Error2 RestClientApi->resource_get: %s\n" % e)
                continue
        if lista_rta:
            #print('Lista_RTA:',lista_rta)
            print('Lista_RTA:',len(lista_rta))
            self.select_sinc(lista_rta)

    def select_sinc(self,lista_rta):
        lista_final=[]
        lista_consulta=[]
        str_consulta=''
        dic_consultas={}
        lista_s=()
        for i in lista_rta:
            dic_consultas[i[1]]=i[3]

        for clave in dic_consultas:
            lista_consulta.append(clave)

        inicio="('"+str(lista_consulta[0])
        fin=str(lista_consulta[-1])+"')"
        print('INICIO::::::',inicio)
        print('FIN:::::::::',fin)
        lista_consulta[0]=inicio
        lista_consulta[-1]=fin        
        var=open("meli.txt","r")
        var_lineas=var.readlines()
        var.close()
        try:
            conexion = pymysql.connect(host=var_lineas[7].rstrip(),
                             user=var_lineas[8].rstrip(),
                             password=var_lineas[9].rstrip(),
                             db=var_lineas[10].rstrip())
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("Ocurrió un error en Conexion: ", e)
            time.sleep(6)
        for i in lista_consulta:
            str_consulta=str_consulta+"'"+str(i)+"',"



        #print('LISTA PARA mYSQLLLLLLLLLL::',lista_consulta)
        str_consulta= str_consulta[1:-2].strip()
        #print('Esto1:: ',str_consulta)

        if str_consulta:
            try:
                consulta="SELECT codigo,cantidad FROM sinc WHERE codigo in "+str_consulta
                with conexion.cursor() as cursor:
                    cursor.execute(consulta)
                    lista_s = cursor.fetchall()
                    conexion.close()
            finally:
                cursor.close()
        #print('Imprimiendo LISTA MYSQL::::::',lista_s)

        for i in lista_rta:
            for j in lista_s:
                if i[1].strip() == j[0].strip() and i[3] != j[1]:
                    #print('El codigo i[1]:',i[1],' es igual a j[0]:',j[0],' Hay diferencia en la cantidad: i[1]:',i[3],' y j[1]:',j[1])
                    lista_final.append([i[1].strip(),j[1]])

        print('Lista para actulizar Stock::::::',lista_final)
        if lista_final:
            self.actualizar(lista_final)



    def actualizar(self,lista_final):
        for i in lista_final:
            sku=i[0].strip()
            cant=i[1]
            print('-------------------***********************MELI_D_*********************************------------------')
            print('Enviar sku: ',sku, ' y cantidad: ',cant)
            obj_D=recibe_parametros(str(sku).strip(),cant)
            metodo2=True
            if(obj_D[0]==400):
                det='Error 400 Bad request en Meli_D_'
                suc='MercadoLibre_D_'
                try:
                    self.errores(det,suc,sku)
                except ApiException as e:
                    print('Error en Conexion_1, Intentando Nuevamente en 10´´...',e)
                    time.sleep(10)
                    continue
                det=''
                suc=''
                ############### Contiene otro codigo Meli ############
            elif(obj_D[0]==44):
                print('Desde Consultar,llego un segundo codigo: ',obj_D[1])
                ################# Si existe mas de un codigo #########################
                lista_mla=[]
                lista_mla= obj_D[1]
                for i in lista_mla:
                    time.sleep(2)
                    mercado_d=Mercadolibre()
                    mercado_d.Implementar2(str(sku).strip(),str(i).strip(),cant)
                    time.sleep(5)
                    ################ Meli ###############################################
            elif(obj_D[0]==43):
                print('Item modificado, Lista MLA vacia, Continuar...: ')
                ########### FIN Contiene otro codifo ##################
            elif(obj_D[0]==404):
                det='Error 404 No se encontro en Meli_D_'
                suc='MercadoLibre_'
                try:
                    self.errores(det,suc,sku)
                except ApiException as e:
                    print('Error en Conexion_2, Intentando Nuevamente en 10´´...',e)
                    time.sleep(10)
                    continue
                det=''
                suc=''
            elif(obj_D[0]==21):
                det='Error 21 No se encontro Codigo en Meli_D_'
                suc='MercadoLibre_D_'
                try:
                    self.errores(det,suc,sku)
                except ApiException as e:
                    print('Error en Conexion_3, Intentando Nuevamente en 10´´...',e)
                    time.sleep(10)
                    continue
                det=''
                suc=''
            elif(obj_D[0]==999999):
                if metodo2:
                    print('RECIBI, Consultar...Aplicando metodo2....')
                    mercado_d=MercadoLibre()
                    cod_mel_sku=str(sku).strip()
                    calculo_codigo=CodigoSKU().calcular(cod_mel_sku)
                    sku_2=calculo_codigo[0]
                    cant_2=int(cant)
                    mercado_d.Implementar(sku_2,cant_2,cod_mel_sku)
                    metodo2=False
            elif(obj_D[0]==7777):
                print('Desde Consultar, se Modifico Item Meli_')
            else:
                det=('Error al Modificar en Meli_D_, codigo desconocido: '+str(obj_D))
                suc='MercadoLibre_D_'
                try:
                    self.errores(det,suc,sku)
                except ApiException as e:
                    print('Error en Conexion_4, Intentando Nuevamente en 10´´...',e)
                    time.sleep(10)
                    continue
                det=''
                suc=''
                    # FIN Meli_
                print('-------------------***********************FIN_MELI_*********************************------------------')
                time.sleep(3)





mla=Meli_D_()
mla.filtrar_MLA()