# EtaNetPythonClients
## Clients infrastructure for the ηNet energy management system (Python 3)

### Context of the development
Within the framework of the energy management project ηNet a cyber-physical system was developed which enables the energetic analysis and control of energy systems. Based on the energy flows, the operating conditions of the individual systems are determined and modified with the help of a management algorithm. For this project a Raspberry PI 3 (Rasbian) was used to collect and modify data on energy flows. 

### Schematic Overview of Energy System
  ![alt text](https://github.com/IKKUengine/CHPefficiency/blob/master/measurement_system.png)
  
### UML-Class Diagram of Python-Client Application
The diagram is created with [Violet UML Editor](http://alexdp.free.fr/violetumleditor/page.php) and can also be viewed via a browser. Details have been omitted for a better overview.

![alt text](https://github.com/IKKUengine/CHPefficiency/blob/master/class_diagram_python-client.png)

### Prerequisites
#### Rasberry Pi 3
 * [Download the latest version of Rasbian](https://www.raspberrypi.org/downloads/raspbian/). Follow the instructions on the page to get your RPI 3 up and running. Best is to use the desktop version. After the new installation the interfaces (Serial, I2C) must be enabeled on the RPI ([Tutorial](https://www.raspberrypi.org/documentation/configuration/raspi-config.md))
 * Organize all or part of above components.

 * Starting with your RPI 3 and a new Rasbian operating system, the following external Python modules are to be installed: 
 ```
 sudo apt-get install git build-essential python-dev
 cd ~
 git clone https://github.com/adafruit/Adafruit_Python_ADS1x15.git
 cd Adafruit_Python_ADS1x15
 sudo python3 setup.py install
 cd ~
 git clone https://github.com/ganehag/pyMeterBus.git
 cd pyMeterBus
 sudo python3 setup.py install
 ```
   * [adafruit/Adafruit_Python_ADS1x15](https://github.com/adafruit/Adafruit_Python_ADS1X15) - follow the readme instructions
   * [ganehag/pyMeterBus](https://github.com/ganehag/pyMeterBus) - follow the readme instructions
 

 
 #### NI LabVIEW
The server application has not yet been checked in, but is coming very soon... for starters, all values of the system will be output via a simple graphical interface by RPI client. 

### Deployment and Starting of Python-Client

If so far everything is installed, then open a terminal in your RPI 3 and clone this repro:

```
cd ~
git clone https://github.com/IKKUengine/CHPefficiency.git
cd CHPefficiency
python3 main.py
```

or download [it](https://github.com/IKKUengine/CHPefficiency/archive/master.zip) to your home directory and open a terminal:
```
cd ~
cd CHPefficiency
python3 main.py
```

### Activate Analysis Mode

The software project has a parameterization that works with globally variables. The purpose of this parameterization is:

* to print messages on a terminal during the runtime of the application, 
* to shwitch on or off the fullscreen mode and 
* to set time trigger for all threads.

Here you can see what has to be done to enable this analysis mode and to change the times. 
Open a terminal on your RPI:

```
cd ~
cd CHPefficiency
nano parameter.py
```

Inside of the nano editor change the corresponding places with True and False:
```
...
global fullscreen
fullscreen = **True**

global printMessages
printMessages = **False**
...
```
Write out the file and exit the editor. 
Start now the application:
```
cd ~
cd CHPefficiency
python3 main.py
```

## Authors

* **Ferhat Aslan**


## License

This project is licensed under MIT - see the [LICENSE](LICENSE) file for details


