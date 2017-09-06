## 将markdown转换成html  
* **required**  
  use python3  
  **markdown**  `pip install markdown`  
  **Pygments**  
  ```pip install Pygments   
  pygmentize -S default -f html > default.css  
  ```
  使用[github样式](https://gist.github.com/andyferra/2554919)  

* **command**  
  python3 mk2html.py -h  
  usage: md2html [-h] -s SOURCE -o OUTPUT [-e [EXCLUDE [EXCLUDE ...]]]  
               [-c [FILTER [FILTER ...]]]  
  transfer markdown file to html file  
  optional arguments:  
  -h, --help            show this help message and exit  
  -s SOURCE, --source SOURCE  
                        source markdown file path  
  -o OUTPUT, --output OUTPUT  
                        the output file path  
  -e [EXCLUDE [EXCLUDE ...]], --exclude [EXCLUDE [EXCLUDE ...]]  
                        the exclude file path  
  -c [FILTER [FILTER ...]], --filter [FILTER [FILTER ...]]  
                        choose extensions file  

* **demo**  
  python3 mk2html.py -s d:/www/sw/swoole-docs -o d:/www/swoole-doc -e .git static -c md



