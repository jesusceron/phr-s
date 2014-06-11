<?php
  $fecha_actual = localtime(time(),1);
  $anyo_actual = $fecha_actual['tm_year'] + 1900;
  $mes_actual = $fecha_actual['tm_mon'] + 1;
  $dia_actual = $fecha_actual['tm_mday'];
  $hour_actual = $fecha_actual['tm_hour'];
  $min_actual = $fecha_actual['tm_min'];
  $line00 = $_REQUEST['patId'];
  $line .=$anyo_actual;
  $line .=$mes_actual;
  $line .=$dia_actual;
  $line .=$hour_actual;
  $line .=$min_actual;
  $line15 =$line00;
  $line15 .=$line;
  $line15 .='.xml';
  $ar=fopen($line15,"a") or
    die("Problemas en la creacion");
  fputs($ar,'<?xml version="1.0"?>');
  fputs($ar, "\n");
  fputs($ar, '<ClinicalDocument xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" moodCode="EVN" xmlns="urn:hl7-org:v3 CDA.xsd">');
  fputs($ar, "\n");
  fputs($ar, '	<typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040" />');
  fputs($ar,"\n");
  fputs($ar, '	<id root="2.16.840.1.113883.19.4" extension="c266" />');
  fputs($ar,"\n");
  fputs($ar, '	<code code="26436-6" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Laboratory Studies" />');
  fputs($ar,"\n");
  fputs($ar, '	<title>RESULTADO DE LABORATORIO</title>');
  fputs($ar,"\n");
  $line0 ='	<effectiveTime value="';
  $line0 .=$anyo_actual;
  $line0 .="-";
  $line0 .=$mes_actual;
  $line0 .="-";
  $line0 .=$dia_actual;
  $line0 .='" />';
  fputs($ar, $line0);
  fputs($ar,"\n");
  fputs($ar, '	<confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25" />');
  fputs($ar,"\n");
  fputs($ar, '	<languageCode codeSystem="2.16.840.1.113883.6.121" />');
  fputs($ar,"\n");
  fputs($ar, '	<recordTarget typeCode="RCT" contextControlCode="OP">');
  fputs($ar,"\n");
  fputs($ar, '		<patientRole classCode="PAT">');
  fputs($ar,"\n");
  $line1 ='			<id root="2.16.840.1.113883.19.5" extension="';
  $line1 .=$_REQUEST['patId'];
  $line1 .='" />';
  fputs($ar, $line1);
  fputs($ar,"\n");
  fputs($ar, '			<addr use="HP">');
  fputs($ar,"\n");
  $line7 ='				<streetAddressLine>';
  $line7 .=$_REQUEST['patAddress'];
  $line7 .='</streetAddressLine>';
  fputs($ar, $line7);
  fputs($ar,"\n");
  fputs($ar, '			</addr>');
  fputs($ar,"\n");
  fputs($ar, '			<patient classCode="PSN" determinerCode="INSTANCE">');
  fputs($ar,"\n");
  fputs($ar, $line1);
  fputs($ar,"\n");
  fputs($ar, '				<name>');
  fputs($ar,"\n");
  $line2 ='					<given>';
  $line2 .=$_REQUEST['patName1'];
  $line2 .='</given>';
  fputs($ar, $line2);
  fputs($ar,"\n");
  $line3 ='					<given>';
  $line3 .=$_REQUEST['patName2'];
  $line3 .='</given>';
  fputs($ar, $line3);
  fputs($ar,"\n");
  $line4 ='					<family>';
  $line4 .=$_REQUEST['patName3'];
  $line4 .='</family>';
  fputs($ar, $line4);
  fputs($ar,"\n");
  $line5 ='					<family>';
  $line5 .=$_REQUEST['patName4'];
  $line5 .='</family>';
  fputs($ar, $line5);
  fputs($ar,"\n");
  fputs($ar, '				</name>');
  fputs($ar,"\n");
  fputs($ar, '					<administrativeGenderCode code="M" codeSystem="2.16.840.1.113883.5.1" />');
  fputs($ar,"\n");
  $line6 ='				<birthTime value="';
  $line6 .=$_REQUEST['patDob'];
  $line6 .='" />';
  fputs($ar, $line6);
  fputs($ar,"\n");
  fputs($ar, '			</patient>');
  fputs($ar,"\n");
  fputs($ar, '			<providerOrganization classCode="ORG" determinerCode="INSTANCE">');
  fputs($ar,"\n");
  fputs($ar, '				<id root="2.16.840.1.113883.19.5" extension="890.307.200-5" />');
  fputs($ar,"\n");
  fputs($ar, '				<name>');
  fputs($ar,"\n");
  fputs($ar, '					<suffix qualifier="LS">S.A.</suffix>Laboratorio Clinico</name>');
  fputs($ar,"\n");
  fputs($ar, '				<telecom value="fax: 92 3265723" />');
  fputs($ar,"\n");
  fputs($ar, '				<telecom value="tel: 92 3265738" />');
  fputs($ar,"\n");
  fputs($ar, '				<telecom value="tel: 92 3265733" />');
  fputs($ar,"\n");
  fputs($ar, '				<telecom value="mailto: laboratorio@centromedicoabc.com.co" />');
  fputs($ar,"\n");
  fputs($ar, '				<telecom value="http: http://www.centromedicoabc.com.co" />');
  fputs($ar,"\n");
  fputs($ar, '				<addr>');
  fputs($ar,"\n");
  fputs($ar, '					<streetAddressLine>Carrera 18 No. 122-135</streetAddressLine>');
  fputs($ar,"\n");
  fputs($ar, '					<city>Cali</city>');
  fputs($ar,"\n");
  fputs($ar, '					<state>Valle</state>');
  fputs($ar,"\n");
  fputs($ar, '					<country>Colombia</country>');
  fputs($ar,"\n");
  fputs($ar, '				</addr>');
  fputs($ar,"\n");
  fputs($ar, '			</providerOrganization>');
  fputs($ar,"\n");
  fputs($ar, '		</patientRole>');
  fputs($ar,"\n");
  fputs($ar, '	</recordTarget>');
  fputs($ar,"\n");
  fputs($ar, '	<author typeCode="AUT" contextControlCode="OP">');
  fputs($ar,"\n");
  $line14 = '		<time value="';
  $line14 .= $line;
  $line14 .= '" />';
  fputs($ar,$line14);
  fputs($ar,"\n");
  fputs($ar, '		<assignedAuthor classCode="ASSIGNED">');
  fputs($ar,"\n");
  fputs($ar, '			<id root="2.16.840.1.113883.19.5" extension="KP00017" />');
  fputs($ar,"\n");
  fputs($ar, '			<assignedAuthoringDevice determinerCode="INSTANCE">');
  fputs($ar,"\n");
  fputs($ar, '				<code code="dev1" />');
  fputs($ar,"\n");
  fputs($ar, '				<manufacturerModelName>DEVMAN</manufacturerModelName>');
  fputs($ar,"\n");
  fputs($ar, '				<softwareName>DEVSOFT</softwareName>');
  fputs($ar,"\n");
  fputs($ar, '			</assignedAuthoringDevice>');
  fputs($ar,"\n");
  fputs($ar, '			<representedOrganization classCode="ORG" determinerCode="INSTANCE">');
  fputs($ar,"\n");
  fputs($ar, '				<id root="2.16.840.1.113883.19.5" extension="890.307.200-5" />');
  fputs($ar,"\n");
  fputs($ar, '			</representedOrganization>');
  fputs($ar,"\n");
  fputs($ar, '		</assignedAuthor>');
  fputs($ar,"\n");
  fputs($ar, '	</author>');
  fputs($ar,"\n");
  fputs($ar, '	<custodian typeCode="CST">');
  fputs($ar,"\n");
  fputs($ar, '		<assignedCustodian classCode="ASSIGNED">');
  fputs($ar,"\n");
  fputs($ar, '			<representedCustodianOrganization classCode="ORG" determinerCode="ASSIGNED">');
  fputs($ar,"\n");
  fputs($ar, '				<id root="2.16.840.1.113883.19.5" extension="890.307.200-5" />');
  fputs($ar,"\n");
  fputs($ar, '			</representedCustodianOrganization>');
  fputs($ar,"\n");
  fputs($ar, '		</assignedCustodian>');
  fputs($ar,"\n");
  fputs($ar, '	</custodian>');
  fputs($ar,"\n");
  fputs($ar, '	<informationRecipient>');
  fputs($ar,"\n");
  fputs($ar, '		<intendedRecipient>');
  fputs($ar,"\n");
  fputs($ar, '			<informationRecipient classCode="PSN" determinerCode="INSTANCE">');
  fputs($ar,"\n");
  fputs($ar, '				<name>');
  fputs($ar,"\n");
  fputs($ar, '					<given>Medico</given>');
  fputs($ar,"\n");
  fputs($ar, '					<family>Medico</family>');
  fputs($ar,"\n");
  fputs($ar, '				</name>');
  fputs($ar,"\n");
  fputs($ar, '			</informationRecipient>');
  fputs($ar,"\n");
  fputs($ar, '		</intendedRecipient>');
  fputs($ar,"\n");
  fputs($ar, '	</informationRecipient>');
  fputs($ar,"\n");
  fputs($ar, '	<legalAuthenticator typeCode="LA" contextControlCode="OP">');
  fputs($ar,"\n");
  $line16 = '		<time value="';
  $line16 .= $line;
  $line16 .= '" />';
  fputs($ar,$line16);
  fputs($ar,"\n");
  fputs($ar, '		<signatureCode codeSystem="2.16.840.1.113883.5.89" />');
  fputs($ar,"\n");
  fputs($ar, '		<assignedEntity classCode="ASSIGNED">');
  fputs($ar,"\n");
  fputs($ar, '			<id root="2.16.840.1.113883.19.5" extension="22417" />');
  fputs($ar,"\n");
  fputs($ar, '			<assignedPerson classCode="PSN" determinerCode="INSTANCE">');
  fputs($ar,"\n");
  fputs($ar, '				<name>');
  fputs($ar,"\n");
  fputs($ar, '					<given>Patricia</given>');
  fputs($ar,"\n");
  fputs($ar, '					<given>Elena</given>');
  fputs($ar,"\n");
  fputs($ar, '					<family>Gomez</family>');
  fputs($ar,"\n");
  fputs($ar, '					<family>Uribe</family>');
  fputs($ar,"\n");
  fputs($ar, '				</name>');
  fputs($ar,"\n");
  fputs($ar, '			</assignedPerson>');
  fputs($ar,"\n");
  fputs($ar, '		</assignedEntity>');
  fputs($ar,"\n");
  fputs($ar, '	</legalAuthenticator>');
  fputs($ar,"\n");
  fputs($ar, '	<inFulfillmentOf>');
  fputs($ar,"\n");
  fputs($ar, '		<order moodCode="RQO">');
  fputs($ar,"\n");
  fputs($ar, '			<id root="CMABC" extension="12090046" />');
  fputs($ar,"\n");
  fputs($ar, '		</order>');
  fputs($ar,"\n");
  fputs($ar, '	</inFulfillmentOf>');
  fputs($ar,"\n");
  fputs($ar, '	<component>');
  fputs($ar,"\n");
  fputs($ar, '		<structuredBody classCode="DOCBODY" moodCode="EVN">');
  fputs($ar,"\n");
  fputs($ar, '			<component>');
  fputs($ar,"\n");
  fputs($ar, '				<section classCode="DOCSECT" moodCode="EVN">');
  fputs($ar,"\n");
  fputs($ar, '					<title>QUIMICA E INMUNOQUIMICA</title>');
  fputs($ar,"\n");
  fputs($ar, '					<component>');
  fputs($ar,"\n");
  fputs($ar, '						<section classCode="DOCSECT" moodCode="EVN">');
  fputs($ar,"\n");
  $line12 ='							<title>';
  $line12 .=$_REQUEST['examName'];
  $line12 .='</title>';
  fputs($ar, $line12);
  fputs($ar,"\n");
  fputs($ar, '							<entry>');
  fputs($ar,"\n");
  fputs($ar, '								<observation classCode="OBS" moodCode="EVN">');
  fputs($ar,"\n");
  fputs($ar, '									<code displayName="Glicemia en ayunas" />');
  fputs($ar,"\n");
  $line13 ='									<value xsi:type="PQ" value="';
  $line13 .=$_REQUEST['examValue'];
  $line13 .='" unit="mg/dl" />';
  fputs($ar, $line13);
  fputs($ar,"\n");
  fputs($ar, '									<referenceRange typeCode="REFV">');
  fputs($ar,"\n");
  fputs($ar, '										<observationRange moodCode="EVN.CRT">');
  fputs($ar,"\n");
  fputs($ar, '											<value xsi:type="IVL_PQ">');
  fputs($ar,"\n");
  fputs($ar, '												<low value="75" unit="mg/dl" />');
  fputs($ar,"\n");
  fputs($ar, '												<high value="115" unit="mg/dl" />');
  fputs($ar,"\n");
  fputs($ar, '											</value>');
  fputs($ar,"\n");
  fputs($ar, '										</observationRange>');
  fputs($ar,"\n");
  fputs($ar, '									</referenceRange>');
  fputs($ar,"\n");
  fputs($ar, '								</observation>');
  fputs($ar,"\n");
  fputs($ar, '							</entry>');
  fputs($ar,"\n");
  fputs($ar, '						</section>');
  fputs($ar,"\n");
  fputs($ar, '					</component>');
  fputs($ar,"\n");
  fputs($ar, '				</section>');
  fputs($ar,"\n");
  fputs($ar, '			</component>');
  fputs($ar,"\n");
  fputs($ar, '		</structuredBody>');
  fputs($ar,"\n");
  fputs($ar, '	</component>');
  fputs($ar,"\n");
  fputs($ar, '</ClinicalDocument>');
	
  fclose($ar);
  echo "Los datos se cargaron correctamente.";
  $nombre = $_REQUEST['patName1'];
  $apellido = $_REQUEST['patName3'];
  $numero = $_REQUEST['patNum'];
  echo '';

  $sms = system( "echo 'Hola $nombre $apellido, el resultado de su prueba de Glicemia ya esta disponible en indivo.unicauca.edu.co' | gammu -c /etc/gammurc sendsms TEXT $numero",$valor_sms); 
	
  ?>
