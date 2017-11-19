# HMO1002
Program for controlling the oscilloscope from the terminal.

![demo](demo.png)

## Linux instalation:
require python3 or higher  
install python library for serial communication  
`sudo aptitude install python3-serial`  
clone repository  
`git clone git@github.com:wykys/HMO1002.git`  
change directory  
`cd HMO1002`  
creating a symbolic link  
`sudo ln -s $(pwd)/osc.py /usr/bin/osc`  
run  
`osc` or `./osc.py` or `python3 osc.py`  
remove  
`sudo rm /usr/bin/osc`  


## Agruments
### main help
`osc -h`
```  
usage: osc [-h] {screenshot,autoscale,fgen} ...  

positional arguments:  
{screenshot,autoscale,fgen}  
                      commands  
  screenshot          save screenshot  
  autoscale           autoscale oscilloscope  
  fgen                function generator  

optional arguments:  
-h, --help            show this help message and exit  
```
### screenshot
`osc screenshot -h`  
```
usage: osc screenshot [-h] [-f FILE] [-c {color,gray,invert}] [-d]  

positional arguments:  
  screenshot            save screenshot  

optional arguments:  
  -h, --help            show this help message and exit  
  -f FILE, --file FILE  image name, withtou siffix  
  -c {color,gray,invert}, --color {color,gray,invert}  
                        image colors  
  -d, --date            add the current date before the name  
```
