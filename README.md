# CHPefficiency

Setup of data acquisition system:
* Data Infrastructure: 
  * [Router](https://avm.de/produkte/fritzbox/fritzbox-7490/) - Fritz!Box 7490
  * [Raspberry Pi 3 (Client)](https://www.raspberrypi.org/) 
* Electrical Energy Flow:
  * [RS232-Patine](http://www.produktinfo.conrad.com/datenblaetter/1300000-1399999/001337093-an-01-ml-RASPBERRY_PI_GPIO_TX___RX_ZU_de_en_fr_nl.pdf) - renkforce
  * [Power Analyzer (RS232)](https://www.infratek-ag.com/) - Power Analysator Infratek 107A
* Thermal Energy Flow:
  * [MBus Master](https://www.wachendorff-prozesstechnik.de/produktgruppen/gateways-und-protokollwandler/produkte/m-bus/pegelwandler-ethernet/Gateway-Protokollwandler-M-Bus-Master-auf-Ethernet-HD67030B2/) - MBus to Ethernet converter, master MBus up to 160 slaves
  * [Heat Meter (M-Bus)](https://www.zenner.de/kategorie/kategorie/ultraschall-kompakt-waermezaehler/produkt/waermezaehler_kompakt_zelsius_ultraschall.html) - 2x Zelsius C5 IUF
* Chemical Energy Flow:
  * [A/D Converter (I2C)](https://www.adafruit.com/product/1085) - adafruit ADS1115
  * [Mass Flow Meter](https://www.bronkhorst.com/products/gas-flow/low-p-flow/f-103e/) - Bronkhost LOW-ΔP-FLOW F-103E
  * [Gas Analyzer](https://products.inficon.com/en-us/nav-products/product/detail/micro-gc-fusion-gas-analyzer/) - Inficon Micro GC Fusion
  
  

### Context of the development
In the context of the ηNet energy management project a test bench was developed that allows the energetic analysis of energy systems. On the basis of the energy flows at a combined heat and power plant the efficiency should to be determined as a function of of the operating conditions. A Rasbarry PI 3 (Rasbian) was used for the data acquisition of the energy flows. The system can also be controlled via relays.  


### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

