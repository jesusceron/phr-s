<html>

<head>
	<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
	<link rel="stylesheet" href="style.css">
	<title>Laboratorio</title>
</head>

<body>

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
            <td><a href='clientgenerate.php'>Registrar nuevo paciente</a></td>
            <td>&nbsp;</td>
        </tr>
		<tr>
            <td><h2>Datos del Paciente</h2></td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
        </tr>
<form method="POST" action="">
        <tr>
            <td>Cedula</td>
            <td><input type="text" size="20" name="patId"></td>
            <td><input type="submit" name="B2" value="Buscar Paciente"></td>
        </tr>
</form>
<form method="POST" action="">
	<?php

	if(isset($_POST['B2'])){
		require("findclient.php");
	}

	?>



<?php

	if(isset($_POST['B1'])){
		require("docgenerate.php");
	}

?>
</form>
</body>
</html>
