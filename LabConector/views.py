from utils import *
import uuid
import MySQLdb
import os
import urllib

from datetime import datetime
from django.utils import simplejson

def start_auth(request):
    """
    begin the oAuth protocol with the server
    
    expects either a record_id or carenet_id parameter,
    now that we are carenet-aware
    """

    # create the client to Indivo
    client = get_indivo_client(request, with_session_token=False)
    
    # do we have a record_id?
    record_id = request.GET.get('record_id', None)
    carenet_id = request.GET.get('carenet_id', None)
    
    # prepare request token parameters
    params = {'oauth_callback':'oob'}
    if record_id:
        params['indivo_record_id'] = record_id
    if carenet_id:
        params['indivo_carenet_id'] = carenet_id

    # request a request token
    req_token = client.fetch_request_token(params)

    # store the request token in the session for when we return from auth
    request.session['request_token'] = req_token
    
    # redirect to the UI server
    return HttpResponseRedirect(client.auth_redirect_url)

def after_auth(request):
    """
    after Indivo authorization, exchange the request token for an access token and store it in the web session.
    """
    # get the token and verifier from the URL parameters
    oauth_token, oauth_verifier = request.GET['oauth_token'], request.GET['oauth_verifier']
    
    # retrieve request token stored in the session
    token_in_session = request.session['request_token']
    
    # is this the right token?
    if token_in_session['oauth_token'] != oauth_token:
        return HttpResponse("oh oh bad token")
    
    # get the indivo client and use the request token as the token for the exchange
    client = get_indivo_client(request, with_session_token=False)
    client.update_token(token_in_session)
    access_token = client.exchange_token(oauth_verifier)
    
    # store stuff in the session
    request.session['access_token'] = access_token
    
    if access_token.has_key('xoauth_indivo_record_id'):
        request.session['record_id'] = access_token['xoauth_indivo_record_id']
        if request.session.has_key('carenet_id'):
            del request.session['carenet_id']
    else:
        if request.session.has_key('record_id'):
            del request.session['record_id']
        request.session['carenet_id'] = access_token['xoauth_indivo_carenet_id']
    
    # luego de autenticarse se llama a def index
    
    return HttpResponseRedirect(reverse(index))

def index(request):
	
	# para el metodo get, se hace la verificacion de si el usuario es nuevo o no

	if request.method == "GET":

		# Se hace la busqueda del numero de identificacion segun el record_id

		record_id = request.session['record_id']
	
		db=MySQLdb.connect(host='localhost',user='indivo',passwd='indivo',db='indivo')
		cursor2=db.cursor()
		sql2='SELECT id_patient FROM indivo_patient WHERE id_record ='+'"'+record_id+'"'+';'
		cursor2.execute(sql2)
		resultado2 = cursor2.fetchone()
		cursor2.close
		db.close()

		# obtener los datos demograficos del paciente. NO REGRESA EN FORMATO XML
		
		#client = get_indivo_client(request)
		#resp, content = client.read_demographics(record_id=record_id, response_format='application/xml')
		#demographics = parse_xml(content)

		# el resultado de la busqueda se guarda en la variable "resultado2"

    		
		if resultado2:

			# si "resultado2" tiene algun valor se obtiene el "id_patient" como un string y se guarda tambien en una variable
			# de sesion
			id_patient = str(resultado2[0])
			request.session['patient_document'] = id_patient
		
			# se consultan todos los CDA asociados al id_patient

			db3=MySQLdb.connect(host='localhost',user='indivo',passwd='indivo',db='health')
			cursor3=db3.cursor()
			sql3='SELECT c_sb_c_s_c_section_entry_observation_code_AdisplayName, code_Acode, effectiveTime_Avalue, 				c_sb_c_s_c_section_entry_observation_rr_or_value_high_Avalue, c_sb_c_s_c_section_entry_observation_rr_or_value_high_Aunit, 	c_sb_c_s_c_section_entry_observation_rr_or_value_low_Avalue, c_sb_c_s_c_section_entry_observation_rr_or_value_low_Aunit, 	c_sb_c_s_c_section_entry_observation_value_Avalue, c_sb_c_s_c_section_entry_observation_value_Aunit, rt_pr_patient_name_given0, rt_pr_patient_name_given1, rt_pr_patient_name_family0, rt_pr_patient_name_family1, la_ae_ap_name_given0, la_ae_ap_name_given1, la_ae_ap_name_family0, la_ae_ap_name_family1, rt_pr_po_addr_streetAddressLine, rt_pr_po_addr_city FROM cdaresultado WHERE rt_pr_id_Aextension='+id_patient+';'
			cursor3.execute(sql3)
			resultadocdas = cursor3.fetchall()
			cursor3.close
			db3.close()

			# todos los resultados se guardan el la matriz "resultadocdas", 
			# y esta se guarda en una variable de sesion llamada "resultados"		

			request.session['resultados'] = resultadocdas			

		else:
		
			# si "resultado2" esta vacio, se guarda "id_patient" igual a cero como una bandera para permitir el registro
			id_patient = 0
			# se muestra la pagina index.html que recibe como parametro "id_patient"
			# si "id_patient = 0" se muestra la opcion de registro de un nuevo paciente, de lo contrario se da la 
			# bienvenida a un usuario ya registrado

		return render_template('index', {"id_patient" : id_patient})

	else:
		
		# Se reciben las varibles enviadas desde index.html cuando el metodo es POST	

		patient_document = request.POST['NoDocumento']
		patient_clave = request.POST['Clave']
		request.session['patient_clave'] = patient_clave

		# se consulta si el usuario esta registrado en el sistema correctamente, validando su id_patient y la contrasena suministrada
		# en la IPS

		db2=MySQLdb.connect(host='localhost',user='indivo',passwd='indivo',db='IPS')
		cursor1=db2.cursor()
		sql1='SELECT nombre1, nombre2, apellido1, apellido2, genero, fecha_nacimiento, direccion, clave_verificacion FROM Usuarios_IPS WHERE idUsuario ='+'"'+patient_document+'"'+';'
		cursor1.execute(sql1)
		resultado = cursor1.fetchall()
		cursor1.close
		db2.close()

		nombre1 = resultado[0][0]
		nombre2 = resultado[0][1]
		apellido1 = resultado[0][2]
		apellido2 = resultado[0][3]
		genero = resultado[0][4]
		fecha_nacimiento = resultado[0][5]
		direccion = resultado[0][6]
		clave_verificacion = resultado[0][7]

		if resultado:
			
			clave = str(clave_verificacion)

			if clave == patient_clave:

				# si las claves coinciden, se envian las varibles a documento.xml, donde se validan y se procede al guardado
				# en la base de datos de indivo en la tabla "patient" con eso termina el registro del nuevo paciente

				request.session['patient_document'] = patient_document
				request.session['DateOfBirth'] = fecha_nacimiento
				request.session['Direccion'] = direccion
				parametros = {'documento' : request.POST['NoDocumento'], "record_id" : request.session['record_id'], "name1" : nombre1, "name2" : nombre2, "surname1" : apellido1, "surname2" : apellido2, "gender" : genero, "dob" : fecha_nacimiento, "address" : direccion, "clave_verificacion" : clave_verificacion}

				documento_xml = render_raw('documento', parametros, type='xml')

				# se anade documento
				client = get_indivo_client(request)
				resp, content = client.document_create(record_id=request.session['record_id'], body=documento_xml, content_type='application/xml')
       
				if resp['status'] != '200':
            				# TODO: handle errors
            				raise Exception("Error al guardar el documento: %s"%content)

				# al tener exito en el guardado del paciente, se redirige a def (general_information)

				return HttpResponseRedirect(reverse(index))
				

			else:
				# si el id_patient o la clave son invalidos, se retorna a la pagina index.html de nuevo
				id_patient2 = 0
				return render_template('index', {"id_patient" : id_patient2})
		else:
			id_patient3 = 0
			return render_template('index', {"id_patient" : id_patient3})


def general_information(request):
	#la solicitud al dar click en "Examenes Disponibles"
    if request.method == "GET":
	# va a urls.py y se carga en el iframe generalinformation.html

	# se estructura un objeto JSON con todos los nombres de las pruebas de laboratorio (CDA) alojados en "resultadocdas" 

	resultado3 = request.session['resultados']

	var=""
	var2=""
	i2=""

	a = len(resultado3)
	aS = str(a)

	if a>0:

		for i in range(a):
			var = var+'"examen'+str(i)+'" :'+'"'+str(resultado3[i][0])+' '+str(resultado3[i][2])+'", '
			i2 = i2+str(i)
		var = var+'"NoExamenes" :'+'"'+i2+'"'

		var2 = '{'+var+'}'
	
	decoded = simplejson.loads(var2)
	
	# se envia a generalinformation.html el JSON resultante

	return render_template('generalinformation', decoded)
    else:
	
	# al dar click en cualquiera de los titulos de los examenes, se envia una bandera "control" por POST igual a cero

	c = request.POST['control']
	ci = int(c)

	if ci == 0:

		# se recibe el numero del examen seleccionado, se recuperan los datos especificos del examen alojados en la variable de
		# sesion "resultados" y se envian a examenguardar.html

		num_examenP = request.POST['NoExamen']
		num_examen = int(num_examenP)
		request.session['NoExam'] = num_examen

		examen = request.session['resultados']

		examen_render = {'titulo' : examen[num_examen][0], 'codigo' : examen[num_examen][1], 'fecha' : examen[num_examen][2],
				'hvalue' : examen[num_examen][3], 'hvalueu' : examen[num_examen][4], 'lvalue' : examen[num_examen][5], 					'lvalueu' : examen[num_examen][6], 'value' : examen[num_examen][7], 'valueu' : examen[num_examen][8], 
				'namedoctor1' : examen[num_examen][13], 'namedoctor2' : examen[num_examen][14], 
				'namedoctor3' : examen[num_examen][15], 'namedoctor4' : examen[num_examen][16],
				'direccion' : examen[num_examen][17], 'ciudad' : examen[num_examen][18]}	
	
        	return render_template('examenguardar', examen_render)
	else:

		# la bandera "control" ahora es igual a 1, indicando que se tiene que importar el examen seleccionado		

		examen1 = request.session['resultados']
		NoExam = request.session['NoExam']
		num_examen1 = int(NoExam)

		examen_render1 = {'titulo' : examen1[num_examen1][0], 'codigo' : examen1[num_examen1][1], 'fecha' : examen1[num_examen1][2],
				'hvalue' : examen1[num_examen1][3], 'hvalueu' : examen1[num_examen1][4], 'lvalue' : examen1[num_examen1][5], 					'lvalueu' : examen1[num_examen1][6], 'value' : examen1[num_examen1][7], 'valueu' : examen1[num_examen1][8], 
				'namedoctor1' : examen1[num_examen1][13], 'namedoctor2' : examen1[num_examen1][14], 
				'namedoctor3' : examen1[num_examen1][15], 'namedoctor4' : examen1[num_examen1][16],
				'direccion' : examen1[num_examen1][17], 'ciudad' : examen1[num_examen1][18]}
		examen_xml = render_raw('examen', examen_render1, type='xml')
		examen_xml2 = render_raw('examenimportado', examen_render1, type='xml')

		# anade el examen en la tabla labresult y en la tabla labresultimported
		client = get_indivo_client(request)
		resp, content = client.document_create(record_id=request.session['record_id'], body=examen_xml, content_type='application/xml')
       		resp, content = client.document_create(record_id=request.session['record_id'], body=examen_xml2, content_type='application/xml')

		if resp['status'] != '200':
        	    # TODO: handle errors
        	    raise Exception("Error al guardar el examen: %s"%content)
		# se redirige a def problem_list
        	return HttpResponseRedirect(reverse(problem_list))
def problem_list(request):
    client = get_indivo_client(request)
    
    in_carenet = request.session.has_key('carenet_id')
    if not in_carenet:
        # get record info
        record_id = request.session['record_id']
        resp, content = client.record(record_id=record_id)
        if resp['status'] != '200':
            # TODO: handle errors
            raise Exception("Error reading Record info: %s"%content)
        record = parse_xml(content)
        
	# lee los examenes que ya se han compartido!!!!
        resp, content = client.generic_list(record_id=record_id, data_model="LabResultImported")
        if resp['status'] != '200':
            # TODO: handle errors
            raise Exception("Error reading examenes: %s"%content)
        probs = simplejson.loads(content)

    else:
        # get record info
        carenet_id = request.session['carenet_id']
        resp, content = client.carenet_record(carenet_id=carenet_id)
        if resp['status'] != '200':
            # TODO: handle errors
            raise Exception("Error reading examenes in carenet: %s"%content)
        record = parse_xml(content)

        
        # lee los examenes, guarda en probs lo obtenido
	resp, content = client.carenet_generic_list(carenet_id=carenet_id, data_model="LabResultImported")
        if resp['status'] != '200':
            # TODO: handle errors
            raise Exception("Error reading examenes from carenet: %s"%content)
        probs = simplejson.loads(content)
        
    probs = map(process_problem, probs)
    record_label = record.attrib['label']
    num_problems = len(probs)
    
    return render_template('share', {'record_label': record_label, 'num_problems' : num_problems, 
                                    'problems': probs, 'in_carenet':in_carenet, })

def shareanswer(request, poll_id):
    
	if request.method == "GET":

		client = get_indivo_client(request)
		record_id = request.session.get('record_id', None)
    
		if record_id:
			# get record info
			resp, content = client.record(record_id=record_id)
			if resp['status'] != '200':
				# TODO: handle errors
				raise Exception("Error reading Record info: %s"%content)
			record = parse_xml(content)
			
			# read the document
			resp, content = client.record_specific_document(record_id=record_id, document_id=poll_id)
			if resp['status'] != '200':
				# TODO: handle errors
				raise Exception("Error fetching document: %s"%content)
			doc_xml = content
	
			
		else:
			# get record info
			carenet_id = request.session['carenet_id']
			resp, content = client.carenet_record(carenet_id=carenet_id)
			if resp['status'] != '200':
				# TODO: handle errors
				raise Exception("Error reading Record info: %s"%content)
			record = parse_xml(content)
			
			# read the document
			resp, content = client.carenet_document(carenet_id=carenet_id, document_id=poll_id)
			if resp['status'] != '200':
				# TODO: handle errors
				raise Exception("Error fetching document from carenet: %s"%content)
			doc_xml = content
	
			
		doc = parse_xml(doc_xml)    
		problem = parse_sdmx_problem(doc, ns=True)
		
		record_label = record.attrib['label']
		surl_credentials = client.get_surl_credentials()
		
		return render_template('shareanswer', {'problem': problem, 'record_label': record_label, 'record_id': record_id, 'poll_id': poll_id, 'surl_credentials': surl_credentials})
	
	else:
		filepath = os.path.join("/var/www/CDA_Recibidos","examen"+request.session['patient_document']+".xml")
		nombre = request.session['resultados']

		if request.POST['collected_by_org_adr_street']:
		
			with open(filepath, 'wb') as out:
				out.write('<?xml version="1.0"?>')
				out.write('\n')
				out.write('<ClinicalDocument xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" moodCode="EVN" xmlns="urn:hl7-org:v3 CDA.xsd">')
				out.write('\n')
				out.write('	<typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040" />')
				out.write('\n')
				out.write('	<id root="2.16.840.1.113883.19.4" extension="c266" />')
				out.write('\n')
				out.write('	<code code="26436-6" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Laboratory Studies" />')
				out.write('\n')
				out.write('	<title>RESULTADO DE LABORATORIO</title>')
				out.write('\n')
				out.write('	<effectiveTime value="'+request.POST['collected_at']+'" />')
				out.write('\n')
				out.write('	<confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25" />')
				out.write('\n')
				out.write('	<languageCode codeSystem="2.16.840.1.113883.6.121" />')
				out.write('\n')
				out.write('	<recordTarget typeCode="RCT" contextControlCode="OP">')
				out.write('\n')
				out.write('		<patientRole classCode="PAT">')
				out.write('\n')
				out.write('			<id root="2.16.840.1.113883.19.5" extension="'+request.session['patient_document']+'" />')
				out.write('\n')
				out.write('			<addr use="HP">')
				out.write('\n')
				out.write('				<streetAddressLine>'+request.session['Direccion']+'</streetAddressLine>')
				out.write('\n')
				out.write('			</addr>')
				out.write('\n')
				out.write('			<patient classCode="PSN" determinerCode="INSTANCE">')
				out.write('\n')
				out.write('				<id root="2.16.840.1.113883.19.5" extension="'+request.session['patient_document']+'" />')
				out.write('\n')
				out.write('				<name>')
				out.write('\n')
				out.write('					<given>'+nombre[0][9]+'</given>')
				out.write('\n')
				out.write('					<given>'+nombre[0][10]+'</given>')
				out.write('\n')
				out.write('					<family>'+nombre[0][11]+'</family>')
				out.write('\n')
				out.write('					<family>'+nombre[0][12]+'</family>')
				out.write('\n')
				out.write('				</name>')
				out.write('\n')
				out.write('					<administrativeGenderCode code="M" codeSystem="2.16.840.1.113883.5.1" />')
				out.write('\n')
				out.write('				<birthTime value="'+request.session['DateOfBirth']+'" />')
				out.write('\n')
				out.write('			</patient>')
				out.write('\n')
				out.write('			<providerOrganization classCode="ORG" determinerCode="INSTANCE">')
				out.write('\n')
				out.write('				<id root="2.16.840.1.113883.19.5" extension="890.307.200-5" />')
				out.write('\n')
				out.write('				<name>')
				out.write('\n')
				out.write('					<suffix qualifier="LS">S.A.</suffix>Laboratorio Clinico Andes</name>')
				out.write('\n')
				out.write('				<telecom value="" />')
				out.write('\n')
				out.write('				<telecom value="" />')
				out.write('\n')
				out.write('				<telecom value="" />')
				out.write('\n')
				out.write('				<telecom value="" />')
				out.write('\n')
				out.write('				<telecom value="" />')
				out.write('\n')
				out.write('				<addr>')
				out.write('\n')
				out.write('					<streetAddressLine>'+request.POST['collected_by_org_adr_street']+'</streetAddressLine>')
				out.write('\n')
				out.write('					<city>'+request.POST['collected_by_org_adr_city']+'</city>')
				out.write('\n')
				out.write('					<state></state>')
				out.write('\n')
				out.write('					<country>Colombia</country>')
				out.write('\n')
				out.write('				</addr>')
				out.write('\n')
				out.write('			</providerOrganization>')
				out.write('\n')
				out.write('		</patientRole>')
				out.write('\n')
				out.write('	</recordTarget>')
				out.write('\n')
				out.write('	<author typeCode="AUT" contextControlCode="OP">')
				out.write('\n')
				out.write('		<time value="20090203001746" />')
				out.write('\n')
				out.write('		<assignedAuthor classCode="ASSIGNED">')
				out.write('\n')
				out.write('			<id root="2.16.840.1.113883.19.5" extension="KP00017" />')
				out.write('\n')
				out.write('			<assignedAuthoringDevice determinerCode="INSTANCE">')
				out.write('\n')
				out.write('				<code code="dev1" />')
				out.write('\n')
				out.write('				<manufacturerModelName>DEVMAN</manufacturerModelName>')
				out.write('\n')
				out.write('				<softwareName>DEVSOFT</softwareName>')
				out.write('\n')
				out.write('			</assignedAuthoringDevice>')
				out.write('\n')
				out.write('			<representedOrganization classCode="ORG" determinerCode="INSTANCE">')
				out.write('\n')
				out.write('				<id root="2.16.840.1.113883.19.5" extension="890.307.200-5" />')
				out.write('\n')
				out.write('			</representedOrganization>')
				out.write('\n')
				out.write('		</assignedAuthor>')
				out.write('\n')
				out.write('	</author>')
				out.write('\n')
				out.write('	<custodian typeCode="CST">')
				out.write('\n')
				out.write('		<assignedCustodian classCode="ASSIGNED">')
				out.write('\n')
				out.write('			<representedCustodianOrganization classCode="ORG" determinerCode="ASSIGNED">')
				out.write('\n')
				out.write('				<id root="2.16.840.1.113883.19.5" extension="890.307.200-5" />')
				out.write('\n')
				out.write('			</representedCustodianOrganization>')
				out.write('\n')
				out.write('		</assignedCustodian>')
				out.write('\n')
				out.write('	</custodian>')
				out.write('\n')
				out.write('	<informationRecipient>')
				out.write('\n')
				out.write('		<intendedRecipient>')
				out.write('\n')
				out.write('			<informationRecipient classCode="PSN" determinerCode="INSTANCE">')
				out.write('\n')
				out.write('				<name>')
				out.write('\n')
				out.write('					<given>'+request.POST['namedoctor1']+" "+request.POST['namedoctor2']+'</given>')
				out.write('\n')
				out.write('					<family>'+request.POST['namedoctor3']+" "+request.POST['namedoctor4']+'</family>')
				out.write('\n')
				out.write('				</name>')
				out.write('\n')
				out.write('			</informationRecipient>')
				out.write('\n')
				out.write('		</intendedRecipient>')
				out.write('\n')
				out.write('	</informationRecipient>')
				out.write('\n')
				out.write('	<legalAuthenticator typeCode="LA" contextControlCode="OP">')
				out.write('\n')
				out.write('		<time value="'+request.POST['collected_at']+'" />')
				out.write('\n')
				out.write('		<signatureCode codeSystem="2.16.840.1.113883.5.89" />')
				out.write('\n')
				out.write('		<assignedEntity classCode="ASSIGNED">')
				out.write('\n')
				out.write('			<id root="2.16.840.1.113883.19.5" extension="22417" />')
				out.write('\n')
				out.write('			<assignedPerson classCode="PSN" determinerCode="INSTANCE">')
				out.write('\n')
				out.write('				<name>')
				out.write('\n')
				out.write('					<given></given>')
				out.write('\n')
				out.write('					<given></given>')
				out.write('\n')
				out.write('					<family></family>')
				out.write('\n')
				out.write('					<family></family>')
				out.write('\n')
				out.write('				</name>')
				out.write('\n')
				out.write('			</assignedPerson>')
				out.write('\n')
				out.write('		</assignedEntity>')
				out.write('\n')
				out.write('	</legalAuthenticator>')
				out.write('\n')
				out.write('	<inFulfillmentOf>')
				out.write('\n')
				out.write('		<order moodCode="RQO">')
				out.write('\n')
				out.write('			<id root="CMABC" extension="12090046" />')
				out.write('\n')
				out.write('		</order>')
				out.write('\n')
				out.write('	</inFulfillmentOf>')
				out.write('\n')
				out.write('	<component>')
				out.write('\n')
				out.write('		<structuredBody classCode="DOCBODY" moodCode="EVN">')
				out.write('\n')
				out.write('			<component>')
				out.write('\n')
				out.write('				<section classCode="DOCSECT" moodCode="EVN">')
				out.write('\n')
				out.write('					<title>QUIMICA E INMUNOQUIMICA</title>')
				out.write('\n')
				out.write('					<component>')
				out.write('\n')
				out.write('						<section classCode="DOCSECT" moodCode="EVN">')
				out.write('\n')
				out.write('							<title>Glicemia en ayunas</title>')
				out.write('\n')
				out.write('							<entry>')
				out.write('\n')
				out.write('								<observation classCode="OBS" moodCode="EVN">')
				out.write('\n')
				out.write('									<code displayName="'+request.POST['test_name_title']+'" />')
				out.write('\n')
				out.write('									<value xsi:type="PQ" value="'+request.POST['quantitative_result_value_value']+'" unit="'+request.POST['quantitative_result_value_unit']+'" />')
				out.write('\n')
				out.write('									<referenceRange typeCode="REFV">')
				out.write('\n')
				out.write('										<observationRange moodCode="EVN.CRT">')
				out.write('\n')
				out.write('											<value xsi:type="IVL_PQ">')
				out.write('\n')
				out.write('												<low value="'+request.POST['quantitative_result_normal_range_min_value']+'" unit="'+request.POST['quantitative_result_normal_range_min_unit']+'" />')
				out.write('\n')
				out.write('												<high value="'+request.POST['quantitative_result_normal_range_max_value']+'" unit="'+request.POST['quantitative_result_normal_range_max_unit']+'" />')
				out.write('\n')
				out.write('											</value>')
				out.write('\n')
				out.write('										</observationRange>')
				out.write('\n')
				out.write('									</referenceRange>')
				out.write('\n')
				out.write('								</observation>')
				out.write('\n')
				out.write('							</entry>')
				out.write('\n')
				out.write('						</section>')
				out.write('\n')
				out.write('					</component>')
				out.write('\n')
				out.write('				</section>')
				out.write('\n')
				out.write('			</component>')
				out.write('\n')
				out.write('		</structuredBody>')
				out.write('\n')
				out.write('	</component>')
				out.write('\n')
				out.write('</ClinicalDocument>')

			download = file('/var/www/CDA_Recibidos/'+"examen"+request.session["patient_document"]+".xml", 'r')
			response = HttpResponse(download.read())
			response['Content-Disposition'] = 'attachment;'
			response['Content-Type'] = 'text/xml;'
		else:

			with open(filepath, 'wb') as out:	
			
				out.write('<?xml version="1.0"?>')
				out.write('\n')
				out.write('<ClinicalDocument xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" moodCode="EVN" xmlns="urn:hl7-org:v3 CDA.xsd">')
				out.write('\n')
				out.write('	<typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040" />')
				out.write('\n')
				out.write('	<id root="2.16.840.1.113883.19.4" extension="c266" />')
				out.write('\n')
				out.write('	<code code="5914-7 " codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Glicemia por medio de tiras reactivas (autoexamen)" />')
				out.write('\n')
				out.write('	<title>RESULTADO DE MEDICION DE GLICEMIA CASERO</title>')
				out.write('\n')
				out.write('	<effectiveTime value="'+request.POST['collected_at']+'" />')
				out.write('\n')
				out.write('	<confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25" />')
				out.write('\n')
				out.write('	<languageCode codeSystem="2.16.840.1.113883.6.121" />')
				out.write('\n')
				out.write('	<recordTarget typeCode="RCT" contextControlCode="OP">')
				out.write('\n')
				out.write('		<patientRole classCode="PAT">')
				out.write('\n')
				out.write('			<id root="2.16.840.1.113883.19.5" extension="'+request.session['patient_document']+'" />')
				out.write('\n')
				out.write('			<addr use="HP">')
				out.write('\n')
				out.write('				<streetAddressLine>'+request.session['Direccion']+'</streetAddressLine>')
				out.write('\n')
				out.write('			</addr>')
				out.write('\n')
				out.write('			<patient classCode="PSN" determinerCode="INSTANCE">')
				out.write('\n')
				out.write('				<id root="2.16.840.1.113883.19.5" extension="'+request.session['patient_document']+'" />')
				out.write('\n')
				out.write('				<name>')
				out.write('\n')
				out.write('					<given>'+nombre[0][9]+'</given>')
				out.write('\n')
				out.write('					<given>'+nombre[0][10]+'</given>')
				out.write('\n')
				out.write('					<family>'+nombre[0][11]+'</family>')
				out.write('\n')
				out.write('					<family>'+nombre[0][12]+'</family>')
				out.write('\n')
				out.write('				</name>')
				out.write('\n')
				out.write('					<administrativeGenderCode code="M" codeSystem="2.16.840.1.113883.5.1" />')
				out.write('\n')
				out.write('				<birthTime value="'+request.session['DateOfBirth']+'" />')
				out.write('\n')
				out.write('			</patient>')
				out.write('\n')
				out.write('			<providerOrganization classCode="ORG" determinerCode="INSTANCE">')
				out.write('\n')
				out.write('				<id root="2.16.840.1.113883.19.5"/>')
				out.write('\n')
				out.write('			</providerOrganization>')
				out.write('\n')
				out.write('		</patientRole>')
				out.write('\n')
				out.write('	</recordTarget>')
				out.write('\n')
				out.write('	<author typeCode="AUT" contextControlCode="OP">')
				out.write('\n')
				out.write('		<time value="'+request.POST['collected_at']+'" />')
				out.write('\n')
				out.write('		<assignedAuthor classCode="ASSIGNED">')
				out.write('\n')
				out.write('			<id root="2.16.840.1.113883.19.5" extension="KP00017" />')
				out.write('\n')
				out.write('			<assignedAuthoringDevice determinerCode="INSTANCE">')
				out.write('\n')
				out.write('				<code code="dev1" />')
				out.write('\n')
				out.write('				<manufacturerModelName>DEVMAN</manufacturerModelName>')
				out.write('\n')
				out.write('				<softwareName>DEVSOFT</softwareName>')
				out.write('\n')
				out.write('			</assignedAuthoringDevice>')
				out.write('\n')
				out.write('			<representedOrganization classCode="ORG" determinerCode="INSTANCE">')
				out.write('\n')
				out.write('				<id root="2.16.840.1.113883.19.5" extension="890.307.200-5" />')
				out.write('\n')
				out.write('			</representedOrganization>')
				out.write('\n')
				out.write('		</assignedAuthor>')
				out.write('\n')
				out.write('	</author>')
				out.write('\n')
				out.write('	<custodian typeCode="CST">')
				out.write('\n')
				out.write('		<assignedCustodian classCode="ASSIGNED">')
				out.write('\n')
				out.write('			<representedCustodianOrganization classCode="ORG" determinerCode="ASSIGNED">')
				out.write('\n')
				out.write('				<id root="2.16.840.1.113883.19.5" extension="891.500.319-2" />')
				out.write('\n')
				out.write('				<name>Universidad Del cauca</name>')
				out.write('\n')
				out.write('			</representedCustodianOrganization>')
				out.write('\n')
				out.write('		</assignedCustodian>')
				out.write('\n')
				out.write('	</custodian>')
				out.write('\n')
				out.write('	<inFulfillmentOf>')
				out.write('\n')
				out.write('		<order moodCode="RQO">')
				out.write('\n')
				out.write('			<id root="CMABC" extension="12090046" />')
				out.write('\n')
				out.write('		</order>')
				out.write('\n')
				out.write('	</inFulfillmentOf>')
				out.write('\n')
				out.write('	<component>')
				out.write('\n')
				out.write('		<structuredBody classCode="DOCBODY" moodCode="EVN">')
				out.write('\n')
				out.write('			<component>')
				out.write('\n')
				out.write('				<section classCode="DOCSECT" moodCode="EVN">')
				out.write('\n')
				out.write('					<title>QUIMICA E INMUNOQUIMICA</title>')
				out.write('\n')
				out.write('					<component>')
				out.write('\n')
				out.write('						<section classCode="DOCSECT" moodCode="EVN">')
				out.write('\n')
				out.write('							<title>Glicemia en ayunas</title>')
				out.write('\n')
				out.write('							<entry>')
				out.write('\n')
				out.write('								<observation classCode="OBS" moodCode="EVN">')
				out.write('\n')
				out.write('									<code displayName="'+request.POST['test_name_title']+'" />')
				out.write('\n')
				out.write('									<value xsi:type="PQ" value="'+request.POST['quantitative_result_value_value']+'" unit="'+request.POST['quantitative_result_value_unit']+'" />')
				out.write('\n')
				out.write('									<referenceRange 	typeCode="REFV">')
				out.write('\n')
				out.write('										<observationRange moodCode="EVN.CRT">')
				out.write('\n')
				out.write('											<value xsi:type="IVL_PQ">')
				out.write('\n')
				out.write('												<low value="'+request.POST['quantitative_result_normal_range_min_value']+'" unit="'+request.POST['quantitative_result_normal_range_min_unit']+'" />')
				out.write('\n')
				out.write('												<high value="'+request.POST['quantitative_result_normal_range_max_value']+'" unit="'+request.POST['quantitative_result_normal_range_max_unit']+'" />')
				out.write('\n')
				out.write('											</value>')
				out.write('\n')
				out.write('										</observationRange>')
				out.write('\n')
				out.write('									</referenceRange>')
				out.write('\n')
				out.write('								</observation>')
				out.write('\n')
				out.write('							</entry>')
				out.write('\n')
				out.write('						</section>')
				out.write('\n')
				out.write('					</component>')
				out.write('\n')
				out.write('				</section>')
				out.write('\n')
				out.write('			</component>')
				out.write('\n')
				out.write('		</structuredBody>')
				out.write('\n')
				out.write('	</component>')
				out.write('\n')
				out.write('</ClinicalDocument>')

			download = file('/var/www/CDA_Recibidos/'+"examen"+request.session["patient_document"]+".xml", 'r')
			response = HttpResponse(download.read())
			response['Content-Disposition'] = 'attachment;'
			response['Content-Type'] = 'text/xml;'

	return response

def agregarmuestra(request):
	
	if request.method == "GET":

		client = get_indivo_client(request)		
		record_id = request.session['record_id']		
		resp, content = client.generic_list(record_id=record_id, data_model="patient")
		datos_paciente = simplejson.loads(content)
		datos_paciente = map(process_patient, datos_paciente)
		num_p = len(datos_paciente)

		return render_template('agregarmuestra', {'datos_paciente' : datos_paciente})

	else:
	
		valor_muestra = request.POST['valormuestra']
		name1 = request.POST['name1']
		name2 = request.POST['name2']
		surname1 = request.POST['surname1']
		surname2 = request.POST['surname2']
		gender = request.POST['gender']
		dob = request.POST['dob']
		address = request.POST['address']
		
		client = get_indivo_client(request)		
		record_id = request.session['record_id']		
		resp, content = client.generic_list(record_id=record_id, data_model="patient")
		datos_paciente = simplejson.loads(content)
		datos_paciente = map(process_patient, datos_paciente)
		num_p = len(datos_paciente)
		today = datetime.now();
		dateFormat = today.strftime("%Y-%m-%d");
		
		examen_render3 = {'titulo' : "Glicemia en ayunas", 'codigo' : "5914-7", 'fecha' : dateFormat,
				'hvalue' : "115", 'hvalueu' : "mg/dl", 'lvalue' : "75", 'lvalueu' : "mg/dl", 'value' : valor_muestra, 					'valueu' : "mg/dl", 'namedoctor1' : name1, 'namedoctor2' : name2, 
				'namedoctor3' : surname1, 'namedoctor4' : surname2,
				'direccion' : address, 'ciudad' : "none"}
		examen_xml3 = render_raw('examen', examen_render3, type='xml')
		examen_xml4 = render_raw('examenimportado', examen_render3, type='xml')

		# anade el examen en la tabla labresult y en la tabla labresultimported
		client = get_indivo_client(request)
		resp, content = client.document_create(record_id=request.session['record_id'], body=examen_xml3, content_type='application/xml')
       		resp, content = client.document_create(record_id=request.session['record_id'], body=examen_xml4, content_type='application/xml')

		return HttpResponseRedirect(reverse(index))
		
		
		
		
		
