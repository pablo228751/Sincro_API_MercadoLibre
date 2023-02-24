from __future__ import print_function
import time
import meli
from meli.rest import ApiException
from pprint import pprint


'''
Aclaraciones: 
PASO 1: Aqui se resuelve si el Sku que se recibe como parametro en la Funcion calcular_M es un SKU, en dicho caso lo busca entre los
productos de MeLI, recupera asi el codigo MLA y el Id_producto al que pertenece el SKU recibido.
Paso 2: En el caso de no completarse la secuencia anterior se asume que el codigo SKU es un codigo MLA y se prueba una llamada, si es que
hay respuesta se asume que el producto solo contiene 1 porducto (id_producto) ,,ya que
no hay manera de comparar un Sku. El return a la clase que consulta contendra solo este ID. (Revisar: En el caso que los productos esten mal
cargados en la Base, este proceso va a borrar Atributos_Combinados de otros productos)


'''
####################################################### PASO 1 ##############################################################
class Calcular_M_sku():
	def calcular_M(self,sku2,usr_id,token_m):		
		configuration = meli.Configuration(
			host = "https://api.mercadolibre.com"
		)
		print('1_Recibo este codigo calcular_M:',sku2)
		print('sku2::::',sku2)
		print('usr-id::::',usr_id)
		print('token_m::::',token_m)		
		
		sku_dato=sku2
		sku_dato2=sku2
		user_id=usr_id
		codigo_mla=''
		resource2 = ('users/'+user_id+'/items/search?seller_sku='+sku_dato)
		resource3 = ('users/'+user_id+'/items/search?seller_sku='+sku_dato.lower())
		access_token =token_m
		metodo2=True
		metodo2=False
		
		
		################################ Con SKU busco codigo MLA #####################################
		
		with meli.ApiClient() as api_client:
		
		
			
			api_instance = meli.RestClientApi(api_client)          
			
		
		try:    
			api_response = api_instance.resource_get(resource2, access_token)
			if api_response['results']:
				print('El codigo result es:::',api_response['results'])
			else:
				print('No se encontro result::: Intentando nuevamente...',api_response['results'])
				api_response = api_instance.resource_get(resource3, access_token)
			print('RESULT::::',api_response['results'])

			if api_response['results']:
				
				codigo_mla=str(api_response['results'][0].strip())
				
				################################ PASO 2, Con el codigo MLA listo los productos #####################################
				with meli.ApiClient() as api_client:
					api_instance2 = meli.RestClientApi(api_client)		
				try:
					resource3 = ('items/'+codigo_mla+'?include_attributes=all')
					api_response2 = api_instance2.resource_get(resource3, access_token)    
					#pprint(api_response2)
					variaciones=api_response2['variations']
					for elem in variaciones:
						for k,v in elem.items():
							if(k=='attributes'):
								att=v
								idd=elem['id']
								cant=elem['available_quantity']
								#pprint(att)
								for e in att:
									if (e['id']  == 'SELLER_SKU'):
										sku2=e
										sku=sku2['value_name'].strip()
										if(sku==sku_dato or sku==sku_dato.lower()):
											print('******************************************************************************************************************')
											print('SKU: '+sku)
											print('ID: ',idd)
											print('Cantidad: ',cant)
											print('******************************************************************************************************************')
		
											lista_rta=[codigo_mla,sku,idd,cant,api_response['results']]
		
											return lista_rta
		
				except ApiException as e:
					print("Error2 RestClientApi->resource_get: %s\n" % e)




					####################################################### PASO 2 ##############################################################

			else:
				print('No se encontro concidencia SKU-->MLA...Probando codigo como MLA...')
				codigo_mla=sku_dato
				print('2° Intento, Buscando codigo en MeLi')
				################################ PASO 2, Con el codigo MLA listo los productos #####################################
				with meli.ApiClient() as api_client:
					api_instance2 = meli.RestClientApi(api_client)		
				try:
					resource3 = ('items/'+codigo_mla+'?include_attributes=all')
					api_response2 = api_instance2.resource_get(resource3, access_token)    
					#pprint(api_response2)
					if 'variations' in api_response2:
						
						variaciones=api_response2['variations']
						for elem in variaciones:
							for k,v in elem.items():
								if(k=='attributes'):
									att=v
									idd=elem['id']
									cant=elem['available_quantity']
									#pprint(att)
									for e in att:
										if (e['id']  == 'SELLER_SKU'):
											sku2=e
											sku=sku2['value_name'].strip()
											#if(sku==sku_dato):
											print('******************************************************************************************************************')
											print('SKU: '+sku)
											print('ID: ',idd)
											print('Cantidad: ',cant)
											print('******************************************************************************************************************')
			
											lista_rta=[codigo_mla,sku,idd,cant,api_response['results']]
			
											return lista_rta
		
				except ApiException as e:
					print("No se encontraron Coincidencias... Intentando Metodo Filtro ...")
					if metodo2:
						if '-' in sku_dato:
							cadena=sku_dato2.split('-')
							if len(cadena[1]) >0 and metodo3==False:
								#print(len.cadena[1])
								print('Probando Metodo len(cadena)')
								metodo3=True
							else:
								print('Metodo3 True')
								sku_dato=cadena[0]+cadena[1]
								metodo2=False
								msj=['**',sku_dato]
								return msj
						else:
							print('No se encontro en Metodo Filtro ')
							metodo2=False
					if metodo2 == False:
						#print('pase por aqui')
						lista_rta=['-','-','-','-',[]]
						return lista_rta
				



		except ApiException as ex:
			print("Error1 RestClientApi->resource_get: %s\n" % ex)
			return [99999,99999,99999,[]]


	def calcular_M2(self,sku2,meli_cod,usr_id,token_m):		
		configuration = meli.Configuration(
			host = "https://api.mercadolibre.com"
		)
		print('2_Recibo este codigo calcular_M2:',sku2,' MLA:',meli_cod)		
		
		sku_dato=sku2
		sku_dato2=sku2
		user_id=usr_id
		codigo_mla=''
		resource2 = ('users/'+user_id+'/items/search?seller_sku='+sku_dato)
		access_token =token_m
		metodo2=True
		metodo2=False
		
		
		################################ Con SKU busco codigo MLA #####################################
		
		with meli.ApiClient() as api_client:	
			
			api_instance = meli.RestClientApi(api_client)      
			
		
		try:
			if 1 == 1:
				codigo_mla=meli_cod
				
				################################ PASO 2, Con el codigo MLA listo los productos #####################################
				with meli.ApiClient() as api_client:
					api_instance2 = meli.RestClientApi(api_client)		
				try:
					resource3 = ('items/'+codigo_mla+'?include_attributes=all')
					api_response2 = api_instance2.resource_get(resource3, access_token)    
					#pprint(api_response2)
					variaciones=api_response2['variations']
					for elem in variaciones:
						for k,v in elem.items():
							if(k=='attributes'):
								att=v
								idd=elem['id']
								cant=elem['available_quantity']
								#pprint(att)
								for e in att:
									if (e['id']  == 'SELLER_SKU'):
										sku2=e
										sku=sku2['value_name'].strip()
										if(sku==sku_dato):
											print('******************************************************************************************************************')
											print('SKU: '+sku)
											print('ID: ',idd)
											print('Cantidad: ',cant)
											print('******************************************************************************************************************')
		
											lista_rta=[codigo_mla,sku,idd,cant]
		
											return lista_rta
		
				except ApiException as e:
					print("Error2 RestClientApi->resource_get: %s\n" % e)

		except ApiException as ex:
			print("Error2 RestClientApi->resource_get: %s\n" % ex)
			return [99999,99999,99999,[]]

	


'''

##########MAIN##########
sku_d='82825521-36.5' ##Codigo Dato id_producto: 81211678266
#sku_d='915143335' ##Codigo MLA
ur='358163046'
tk= 'APP_USR-844444444444444444444444444444444444444444444444444446' 
prueba=Calcular_M_sku().calcular_M(sku_d,ur,tk)
print('Prueba:',prueba)
if prueba[0] == '**':
	print('MEtODO AQUI')
	print(prueba[1])
if prueba[0] =='-':

## prueba=[codigoMLA,sku,ID_delProducto,Cantidad,Lista de MLA]
'''

