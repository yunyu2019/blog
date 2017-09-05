## 运行说明  
* 依赖  
    [swoole扩展](https://wiki.swoole.com/wiki/page/6.html)  

* 运行环境  
    nginx  
    redis  

* nginx代理websocket配置  
    参考[WebSocket proxying](http://nginx.org/en/docs/http/websocket.html)  
    ```
    http {  
        include       mime.types;  
        default_type  application/octet-stream;  
        sendfile        on;  
        keepalive_timeout  65;  
        map $http_upgrade $connection_upgrade {  
            default upgrade;  
            ''      close;  
        }  
        ...  
        server{  
             listen       80;  
             server_name  wbsocket.com;  
             charset utf-8;  
             access_log  off;  
             error_log /data/www/logs/error_wbsocket.log;  
             proxy_connect_timeout 3s;  
             proxy_read_timeout 600s;  
             proxy_send_timeout 600s;  
             location / {  
                  proxy_pass http://127.0.0.1:3000;  
                  proxy_http_version 1.1;  
                  proxy_set_header Upgrade $http_upgrade;  
                  proxy_set_header Connection $connection_upgrade;  
     
             }  
        }  
        ...  
    }  
    ```

