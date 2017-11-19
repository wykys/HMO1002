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
  `sudo ln -s \`pwd\`/osc.py /usr/bin/osc`  
  run  
  `osc` or `./osc.py` or `python3 osc.py`  
  remove  
  `sudo rm /usr/bin/osc`  
