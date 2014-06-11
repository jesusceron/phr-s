<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<link rel="stylesheet" href="style.css">
<title>Registrar Paciente</title>
</head>

<body>

<form method="POST" action="saveclient.php">
    <table border="0">
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
            <td colspan="3"><h1>Laboratorio</h1>
            </td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
		<tr>
            <td><h2>Datos del Paciente</h2></td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Cedula</td>
            <td><input type="text" size="10" name="patId"></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Primer nombre</td>
            <td><input type="text" size="10" name="patName1"></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Segundo nombre</td>
            <td><input type="text" size="10" name="patName2"></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Primer apellido</td>
            <td><input type="text" size="10" name="patName3"></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Segundo apellido</td>
            <td><input type="text" size="10" name="patName4"></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Dirección</td>
            <td><input type="text" size="10" name="patAddress"></td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Género</td>
            <td><select name="patGender">    
       		<option value="Masculino">Masculino</option>
       		<option value="Femenino" selected="selected">Femenino</option>
   		</select>
	    </td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>   </td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Fecha de Nacimiento</td>
            <td>Año:<input type="text" size="10" name="patDobA"> Mes:<input type="text" size="10" name="patDobM"> Día:<input type="text" size="10" name="patDobD"></td>
            <td>&nbsp;</td>
        </tr>
                <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Número teléfono móvil</td>
            <td><input type="text" size="10" name="patNum"></td>
            <td>&nbsp;</td>
        </tr>
                <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>Clave de confirmación</td>
            <td><input type="password" size="10" name="patPass"></td>
            <td>&nbsp;</td>
        </tr>
                <tr>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
        <tr>
            <td>&nbsp;</td>
            <td><input type="submit" name="B1" value="Guardar"></td>
            <td>&nbsp;</td>
        </tr>
    </table>
</form>
</body>
</html>
