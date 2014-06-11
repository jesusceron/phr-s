<?php
	$patId = $_REQUEST['patId'];
	$patName1 = $_REQUEST['patName1'];
	$patName2 = $_REQUEST['patName2'];
	$patName3 = $_REQUEST['patName3'];
	$patName4 = $_REQUEST['patName4'];
	$patAddress = $_REQUEST['patAddress'];
	$patGender = $_REQUEST['patGender'];
	$patDobA = $_REQUEST['patDobA'];
	$patDobM = $_REQUEST['patDobM'];
	$patDobD = $_REQUEST['patDobD'];
	$patPass = $_REQUEST['patPass'];
	$patNum = $_REQUEST['patNum'];
	$patDob = "$patDobA-$patDobM-$patDobD";
	$conexion = mysql_connect('localhost','root','bmxarmy');
	if (!$conexion) {
   		die('No pudo conectarse: ' . mysql_error());
	}
	echo 'Conectado satisfactoriamente';
	mysql_select_db('IPS',$conexion);

	//Escribimos la sentencia SQL que ejecutaremos.
	$sql = "INSERT INTO Usuarios_IPS (idUsuario, nombre1, nombre2, apellido1, apellido2, genero, fecha_nacimiento, direccion, telefono, clave_verificacion, estado_enviado) VALUES ('$patId', '$patName1', '$patName2', '$patName3', '$patName4', '$patGender', '$patDob', '$patAddress', '$patNum', '$patPass', 0)";
	//Ejecutamos la sentencia SQL
	
	$comprobar = mysql_query($sql);
	//cierro conexion
	mysql_close($conexion);
?>
