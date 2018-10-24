# CHPefficiency
## Test Bench for Determining Efficiency (Python and LabVIEW)

### Context of the development
In the context of the ηNet energy management project a test bench was developed that allows the energetic analysis of energy systems. On the basis of the energy flows at a combined heat and power plant the efficiency should to be determined as a function of of the operating conditions. A Raspberry PI 3 (Rasbian) was used for the data acquisition of the energy flows. The system can also be controlled via relays.  

### Setup of data acquisition system
* Data Infrastructure: 
  * [Router](https://avm.de/produkte/fritzbox/fritzbox-7490/) - Fritz!Box 7490
  * [Raspberry Pi 3 (Client)](https://www.raspberrypi.org/) 
* Electrical Energy Acquisition:
  * [RS232-Patine](http://www.produktinfo.conrad.com/datenblaetter/1300000-1399999/001337093-an-01-ml-RASPBERRY_PI_GPIO_TX___RX_ZU_de_en_fr_nl.pdf) - renkforce
  * [Power Analyzer (RS232)](https://www.infratek-ag.com/) - Power Analysator Infratek 107A
* Thermal Energy Acquisition:
  * [MBus Master](https://www.wachendorff-prozesstechnik.de/produktgruppen/gateways-und-protokollwandler/produkte/m-bus/pegelwandler-ethernet/Gateway-Protokollwandler-M-Bus-Master-auf-Ethernet-HD67030B2/) - MBus to Ethernet converter, master MBus up to 160 slaves
  * [Heat Meter (M-Bus)](https://www.zenner.de/kategorie/kategorie/ultraschall-kompakt-waermezaehler/produkt/waermezaehler_kompakt_zelsius_ultraschall.html) - 2x Zelsius C5 IUF
* Chemical Energy Acquisition:
  * [A/D Converter (I2C)](https://www.adafruit.com/product/1085) - adafruit ADS1115
  * [Mass Flow Meter](https://www.bronkhorst.com/products/gas-flow/low-p-flow/f-103e/) - Bronkhost LOW-ΔP-FLOW F-103E
  * [Gas Analyzer](https://products.inficon.com/en-us/nav-products/product/detail/micro-gc-fusion-gas-analyzer/) - Inficon Micro GC Fusion
* Controlling:  
  * [Relais-Modul](https://www.conrad.de/de/makerfactory-4-kanal-relais-modul-1612775.html) - MAKERFACTORY 4-Kanal Relais-Modul
 
### Schematic Overview of Energy System
  ![alt text](https://github.com/IKKUengine/CHPefficiency/blob/master/measurement_system.png)
  
### UML-Class Diagram of Python-Client Application
The diagram is created with [Violet UML Editor](http://alexdp.free.fr/violetumleditor/page.php) and can also be viewed via a browser. Details have been omitted for a better overview.

![alt text](https://github.com/IKKUengine/CHPefficiency/blob/master/class_diagram_python-client.png)


### Prerequisites
#### Rasberry Pi 3
 * [Download the latest version of Rasbian](https://www.raspberrypi.org/downloads/raspbian/). Follow the instructions on the page to get your RPI 3 up and running. Best is to use the desktop version.
 * Organize all or part of above components.
 
 * Starting with your RPI 3 and a new Rasbian operating system, the following external Python modules are to be installed:
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

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details


