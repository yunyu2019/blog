<?php
/**
 * 
 * @authors Yunyu2019 (yunyu2010@yeah.net)
 * @date    2017-08-22 11:35:08
 * @version $Id$
 * @descp   The document description
 */
use Swoole\Http\Client;

$cli=new Client('127.0.0.1',3000);
$cli->set(['timeout' => 3.0]);
$cli->setCookies(['access_token'=>"access_token"]);
$cli->on('message', function ($cli, $frame) {
    switch ($frame->opcode) {
        case 0x1:
            echo $frame->data;
            break;
        case 0x2:
            echo 'bin';
            break;
        case 0x9:
            echo 'ping';
            //$cli->push('pong',0xa,true);
            break;
        default:
            echo $frame->data;
            break;
    }
});

$cli->upgrade('/', function ($cli) {
    if ($cli->statusCode>=400) {
        echo "auth faild\n";
        $cli->close();
        return false;
    }
    $cli->push("server在吗?");
});
