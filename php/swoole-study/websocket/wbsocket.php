<?php
/**
 * 
 * @authors Yunyu2019 (yunyu2010@yeah.net)
 * @date    2017-08-14 15:04:32
 * @version $Id$
 * @descp   The document description
 */
use Swoole\Table;
use Swoole\Websocket\Server;

class Wbsocket {
    public $config;
    public $beforeSendMsgCallback = '';
    public $afterSendMsgCallback = '';
    public $authenticator = '';
    private $table;
    private $redis;
    protected $server;

    public function __construct($config=[]){
        $this->config=$config;
        $this->init();
    }

    public function init(){
        try {
            $redisOpt=$this->config['redis'];
            $this->redis=new \Redis();
            $this->redis->connect($redisOpt['host'],$redisOpt['port'],$redisOpt['timeout']);
            $this->redis->auth($redisOpt['auth']);
        } catch (Exception $e) {
            echo $e->message;
            return false;
        }

        $wsOpt=$this->config['websocket'];
        $this->server = new Server($wsOpt['host'], $wsOpt['port']);
        !empty($wsOpt['options']) && $this->server->set($wsOpt['options']);

        $this->beforeSendMsgCallback = function() {};
        $this->afterSendMsgCallback = function() {};
        $this->authenticator = function() {};
        $this->createTable();
        $this->bindEvents();
    }

    public function bindEvents(){
        $this->server->on('start',[$this,'onStart']);
        //如果设置了onHandShake回调函数,onOpen逻辑需要写在onHandShake中
        $this->server->on('handshake',[$this,'onHandShake']);
        $this->server->on('WorkerStart',[$this,'onWorkerStart']);
        //$this->server->on('open',[$this,'onOpen']);
        $this->server->on('message',[$this,'onMessage']);
        $this->server->on('close',[$this,'onClose']);
        $this->server->on('shutdown',[$this,'onShutdown']);
    }

    public function onStart($serv){
        echo "start websocket server,master_pid:{$serv->master_pid},manager_pid:{$serv->manager_pid}\n";
    }

    public function onHandShake($request,$response){
        if(!isset($request->header['sec-websocket-key'])){
            $response->end();
            return false;
        }

        if(0 === preg_match('#^[+/0-9A-Za-z]{21}[AQgw]==$#', $request->header['sec-websocket-key']) || 16 !== strlen(base64_decode($request->header['sec-websocket-key']))){
            $response->end();
            return false;
        }
        $curr_fd = $request->fd;
        $email=$request->get('email');
        $name=$request->get('name');
        if (!$this->auth($request)){
            echo "$curr_fd auth faild\n";
            $response->status(401);
            $response->end();
            return false;
        }

        $key = base64_encode(sha1($request->header['sec-websocket-key']. '258EAFA5-E914-47DA-95CA-C5AB0DC85B11',
        true));
        $headers = array(
            'Upgrade'               => 'websocket',
            'Connection'            => 'Upgrade',
            'Sec-WebSocket-Accept'  => $key,
            'Sec-WebSocket-Version' => '13',
            'KeepAlive'             => 'off'
        );
        foreach ($headers as $key => $val){
            $response->header($key, $val);
        }
        $response->status(101);
        $response->end();
        $serv=$this->server;
        $serv->defer(function () use ($curr_fd,$serv,$email,$name){
            $msg=["type"=>"auth","data"=>["name"=>$name,"email"=>$email,"message"=>"welcome"]];
            $serv->push($curr_fd,json_encode($msg,JSON_UNESCAPED_UNICODE));
            $this->table->set($email,array('fd'=>$curr_fd,'name'=>$name));
            $this->redis->hset('websocket',$curr_fd,$email);
            foreach ($serv->connections as $fd) {
                if ($fd==$curr_fd) continue;
                $msg=['type'=>'system',"data"=>["name"=>$name,"email"=>$email,"message"=>"加入了群聊"]];
                $serv->push($fd,json_encode($msg,JSON_UNESCAPED_UNICODE));
            }
        });
        return true;
    }

    public function onWorkerStart($serv,$worker_id){
        if ($worker_id==0) {
            $serv->tick(5000,function($id) use($serv){
                foreach ($serv->connections as $fd) {
                   $flag= $serv->exist($fd)==false || $serv->push($fd,"ping",0x9)==false;
                   if($flag) continue;
                }
            });
        }
    }

    /*public function onOpen($serv,$request){
        $curr_fd=$request->fd;
        $info=$this->getInfo($curr_fd);
        foreach ($serv->connections as $fd) {
            if ($fd==$curr_fd) continue;
            $msg=['type'=>'system',"data"=>["name"=>$info[1],"email"=>$info[0],"message"=>"加入了群聊"]];
            $serv->push($fd,json_encode($msg,JSON_UNESCAPED_UNICODE));
        }
    }*/

    public function onMessage($serv,$frame){
        call_user_func($this->beforeSendMsgCallback, $serv, $frame);
        $this->broadcast($serv,$frame);
        call_user_func($this->afterSendMsgCallback, $serv, $frame);
    }

    public function onClose($serv,$fd){
        echo "closing $fd\n";
        if($this->redis->hexists('websocket',$fd)){
            $info=$this->getInfo($fd);
            $this->table->del($info[0]);
            $this->redis->hdel('websocket',$fd);
            foreach ($this->table as $key=>$row) {
                $msg=["type"=>"system","data"=>["name"=>$info[1],"email"=>$info[0],"message"=>"已离开"]];
                $serv->push($row['fd'],json_encode($msg,JSON_UNESCAPED_UNICODE));
            }
        }
    }

    public function onShutdown($serv){
        $this->table->destroy();
        $this->redis->del('websocket');
        echo "websocket server shutdown\n";
    }

    private function createTable(){
        $this->table = new Table(1024);
        $this->table->column('fd',Table::TYPE_INT);
        $this->table->column('name',Table::TYPE_STRING,100);
        $this->table->create();
    }
    
    public function run(){
        $this->server->start();
    }

    public function __call($method, $params){
        $class_name = get_class($this->server);
        $class = new ReflectionClass($class_name);
        try {
            $class->getMethod($method);
        } catch (ReflectionException $e) {
            echo "Method $method is not exists\n";
            return;
        }
        call_user_func_array([$this->server, $method], $params);
    }

    public function broadcast($serv,$frame,$type="normal"){
        $fd=$frame->fd;
        switch ($frame->opcode) {
            case 0x1:
                $info=$this->getInfo($fd);
                $msg=["type"=>$type,"data"=>["name"=>$info[1],"email"=>$info[0],"message"=>$frame->data]];
                $serv->push($fd,json_encode($msg,JSON_UNESCAPED_UNICODE));
                break;
            case 0x2:
                echo "bin\n";
                break;
            case 0xa:
                echo "pong\n";
                break;
            default:
                echo $frame->data."\n";
                break;
        }
    }
    
    private function auth($request){
        $result = call_user_func($this->authenticator,$request);
        return $result;
    }

    public function getInfo($fd){
        $info=[];
        $email=$this->redis->hget('websocket',$fd);
        if($email==false){
            return $info;
        }
        array_push($info,$email,$this->table->get($email,'name'));
        return $info;
    }
}
date_default_timezone_set('Asia/Shanghai');
$config=[
    'websocket'=>[
        'host'=>'127.0.0.1',
        'port'=>3000,
        'options'=>[
            'daemonize' =>0,
            'log_level'=>3,
            'pid_file'=>'/data/www/swoole/wbsocket.pid',
            'log_file'=>'/data/www/swoole/wbsocket.log'
        ]
    ],
    'redis'=>[
        'host'=>'127.0.0.1',
        'port'=>6379,
        'timeout'=>2.5,
        'auth'=>'123456'
    ]
];
$server = new WbSocket($config);
$server->authenticator = function($request){
    $flag=(isset($request->get['access_token']) && $request->get['access_token'] =='access_token') || (isset($request->cookie) && $request->cookie['access_token']=='access_token');
    return $flag;
};

/*$server->beforeSendMsgCallback=function($server,$frame){
    echo  $frame->opcode;
};*/

$server->afterSendMsgCallback=function($serv,$frame) use($server) {
    $curr_fd=$frame->fd;
    $info=$server->getInfo($curr_fd);
    foreach($serv->connections as $fd){
        if($fd==$curr_fd) continue;
        $msg=["type"=>"normal","data"=>["name"=>$info[1],"email"=>$info[0],'message'=>$frame->data]];
        $serv->push($fd,json_encode($msg,JSON_UNESCAPED_UNICODE));
    }
};
$server->run();
