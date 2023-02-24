

class CodigoSKU():
	
	def calcular(self,cod):
	
		codigo_2=cod
		lista_cod=['1','1.5','2.5','2','2.5','3','3.5','4','4.5','5','5.5','6','6.5','7','7.5','8','8.5','9','9.5','10','11','11.5','10.5','20','21','22','23','24','25','26','27','28','29','30','31','32','32.5','33','33.5','34','34.5','35','35.5','36','36.5','37','37.5','38','38.5','39','39.5','40','40.5','41','41.5','42','42.5','43','43.5','44','44.6','46','46.5','47','47.5','48','48.5','XL','X','S','M']
		txt2=''
		codigo=''
		sku=''
		talle=''
		color=''
		txt3=''
		cadena3=''
		cadena4=''
		cadena5=''
		txt_talle=''
		txt_color=''
		lista_cod2=None ## Se usa en el filtro de 3 caracteres o mas
		
		if '-' in codigo_2:
			#print('La cadena tiene guion')
			cadena3=codigo_2.split('-')
			cadena4=cadena3[0]
			cadena5=cadena3[1]
			can_n=len(cadena5)
			#print('La cantidad de caracteres es de',can_n)
			if(can_n==1):
				codigo=codigo_2
				sku=codigo_2
				color='C_Vacio'
				talle='T_Vacio'
				rta=[codigo,sku,color,talle]
				print('Enviado desde calculo_cod 1/-', rta)
				return(rta)
				txt_color=can_n
				#print('Color: ',txt_color)
			elif(can_n==2):
				print('En 2')
				list_num = []
				for n in cadena5:
					#n = int(n)
					if type(n) ==int:
						n = int(n)
					list_num.append(n)
				#print(list_num)
				seg_num=str(list_num[1])
				if seg_num in lista_cod:
					txt_talle=seg_num
					txt_c=list_num[0]
					txt_color=str(txt_c).strip()
					#print('El numero SI esta en la LISTA el Color es: '+txt_color+ ' el Talle: '+txt_talle)
		
				else:
					txt_color="".join(cadena5).strip()
					#txt_color.split(' ')
					#print('El numero no esta en lista de codgo, perentece a un Color, el color es: '+txt_color)
			elif(can_n ==3 or can_n ==4):
				print('En 3/4')
				txt_talle=cadena5[1:]
				txt_color=cadena5[:2]
				
				if txt_color[1].isdigit() and txt_color[0].isdigit():
					if int(txt_color[1]) <=3 or int(txt_color[0]) > 1 :
						txt_color=txt_color[0]
						#print('Se calcula  Color s: '+txt_color+ ' y el Talle: '+txt_talle)
					else:
						if '.' in cadena5:
							txt_color=str(txt_color[0])
							print('Se calcula  Color : '+str(txt_color)+ ' y el Talle: '+str(txt_talle))

						else:
							txt_talle=txt_talle[-2:]
							#txt_talle=txt_talle[-1] #Configurado anteriormente
							print('Se calcula  Color : '+txt_color+ ' y el Talle: '+txt_talle)
		
			elif can_n >=5:
				print('En 5')
				# Al contener 4 o mas caracteres
				
				if '.' in cadena5:
					txt2=cadena5[1:len(cadena5)]
					lista_cod2=lista_cod	
					for x in lista_cod2:
						if '.' not in x:
							lista_cod2.remove(x)
					#print('Lista_cod2 es: ',lista_cod2)
					#can_n2=len(txt2)
					txt_talle=cadena5[-4:]
		
					## Abajo si el codigo restante tiene 4 o mas caracteres voy a deducir que los primeros 2 hacen referencia al Color
				else:
					txt_color=cadena5[:2]
					txt_talle=cadena5[2:len(cadena5)]
					print('Con 4 caracteres o mas el Color es: '+txt_color+' y el Talle: ',txt_talle)
		
		
		
				if txt_talle in cadena5:			
					txt_c=cadena5.split(txt_talle)
					del txt_c[1]
					txt_color="".join(txt_c).strip()
					print('En la secuencia con (.) el Color es: '+txt_color+ ' el Talle: '+txt_talle)
		
				#REVISAR
				#if lista_cod2 is not None and int(txt_color)<15:
				#	for i in lista_cod2:
				#		a=i
				#		if(a in txt_talle):
				#			txt_talle=i
							#print('En la secuencia con (.) el Talle es ',txt_talle)

					
		
		
			
			try:
				codigo=codigo_2
				sku=cadena4+'-'+txt_color
				color=txt_color
				talle=txt_talle
			except:
				print('error en el codigo')
				codigo=codigo_2
				sku=codigo_2
				color='C_Vacio'
				talle='T_Vacio'
				rta=[codigo,sku,color,talle]
				print('Enviado desde Excepcion1')
				return(rta)
						
		
		
		
		else:
			print('Cadena sin (-)')
			codigo=codigo_2
			sku=codigo_2
			color='C_Vacio'
			talle='T_Vacio'
		
		
		
		#print('El Codigo es: '+codigo)
		#print('El SKU es: '+sku)
		#print('El Color: '+color)
		#print('El Talle: '+talle)
		#rta= {'Codigo':codigo,'SKU':sku,'Color':color,'Talle':talle}
		rta=[codigo,sku,color,talle]
		#print('Desde calculo...',rta)
		return(rta)


 
#cal=print(CodigoSKU().calcular('81825543-211'))
#cal=print(CodigoSKU().calcular('81835565-410'))





