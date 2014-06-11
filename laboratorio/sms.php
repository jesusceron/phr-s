<?php
$nombre = "Gerard";
$telefono = "3104724700";
$sms = system( "echo 'hola nuevo mundo $nombre' | gammu -c /etc/gammurc sendsms TEXT $telefono",$valor_sms); 

echo '
Texto SMS: ' . $sms.'
Valor SMS: ' . $valor_sms;
?>
