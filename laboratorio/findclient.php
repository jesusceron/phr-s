<?php

	$patId = $_REQUEST['patId'];
	$conexion = mysql_connect('localhost','root','bmxarmy');
	if (!$conexion) {
   		die('No pudo conectarse: ' . mysql_error());
	}
	
	mysql_select_db('IPS',$conexion);

	//Escribimos la sentencia SQL que ejecutaremos.
	$sql = "SELECT nombre1, nombre2, apellido1, apellido2, genero, fecha_nacimiento, direccion, telefono FROM Usuarios_IPS WHERE idUsuario = $patId";
	//Ejecutamos la sentencia SQL
	
	$resultado = mysql_query($sql);
	
	$row=mysql_fetch_array($resultado);

	//cierro conexion
	mysql_close($conexion);
	
	if($row){

	$nombre1 = $row['nombre1'];
	$nombre2 = $row['nombre2']; 
	$apellido1 = $row['apellido1']; 
	$apellido2 = $row['apellido2']; 
	$genero = $row['genero']; 
	$fecha_nacimiento = $row['fecha_nacimiento']; 
	$direccion = $row['direccion'];
	$celular = $row['telefono']; 

	echo "
	<tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
	<tr>
            <td>&nbsp;</td>
            <td><input type='hidden' name='patId' value=$patId></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Primer nombre</td>
            <td>$nombre1<input type='hidden' name='patName1' value=$nombre1></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Segundo nombre</td>
            <td>$nombre2<input type='hidden' name='patName2' value=$nombre2></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Primer apellido</td>
            <td>$apellido1<input type='hidden' name='patName3' value=$apellido1></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Segundo apellido</td>
            <td>$apellido2<input type='hidden' name='patName4' value=$apellido2></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Direccion</td>
            <td>$direccion<input type='hidden' name='patAddress' value=$direccion></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Genero</td>
            <td>$genero<input type='hidden' name='patGender' value=$genero></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Numero Celular</td>
            <td>$celular<input type='hidden' name='patNum' value=$celular></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Fecha de Nacimiento</td>
            <td>$fecha_nacimiento<input type='hidden' name='patDob' value=$fecha_nacimiento></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td><h2>Datos del Examen</h2></td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Valor:</td>
            <td><input type='text' size='20' name='examValue'></td>
            <td>mg/dl</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td><input type='submit' name='B1' value='Guardar'></td>
            <td>&nbsp;</td>
        </tr>
    </table>";
	
	}
else{

echo "<tr>
            <td>&nbsp;</td>
            <td>No existe un paciente con esa identificacion</a></td>
            <td>&nbsp;</td>
        </tr>";

}

?>
