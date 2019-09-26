# Attacks detection in distributed control system environment.

The project is a recrutation task for NASK.

6 virtual machines are created:

    * server 
        Simulates the dynamic process. The IP of the server should be
        20.0.0.1/32. However this address is used for communication with the
        host machine. Therefore, the address of the server is 20.0.0.2/32

    * client
        Monitors and controls the dynamic process

    * zaklocenie
        Produces the traffic for the server in order to disturb its correct
        operation

    * fw_router
        Serves as the router and firewall and copies the traffic for the
        snort module. Firewall rules are configured by the snort module.

    * snort
        Monitors the traffic between the router and the server. In case of an
        alert, it sends respective IP address to the firewall in order to block
        the traffic from the given address. Moreover, it writes information
        about the alert to the database.

    * db
        Database -- it records the events received from the snort module.

Code for each of the virtual machines is located in respective folders.

## Environment configuration

The environment is configured using Vagrant. 

In case of using proxy, install proxy-conf:

    $ vagrant plugin install vagrant-proxyconf 

Then configure proxy in Vagrantfile -- proxy settings are commented out at the
beginning of Vagrantfile.

In order to start the environment, go to the main directory and issue:

    $ vagrant up


Afterwards, in order to log into each of the machines, issue:

    $ vagrant ssh $<machine_name>

e.g.:

    $ vagrant ssh client


The folder /vagrant of the virtual machine is synchronised with the root of
the project on the host machine.
 

## Starting server process and client controller

In order to present the functionalities of the dynamic process and controller,
after logging to the server and client machines, run respective scripts:

In server:

    $ python3.6 /vagrant/server/server.py

In client:

    $ python3.6 /vagrant/client/client.py


The order of running the scripts is important -- You cannot control the process
which is not started.

## Dynamic process and controller configuration 

Client reads the configuration from init_data.json file. The following data
is provided:

    A, B, C - matrices describing the process simulated in the server. The
        process is described with following equations:
            
            x(t+1) = A * x(t) + B * v(t)

            y(t) = C * x(t)
        
        The same matrices are used to design the dead-beat controller:
            * observer matrix (L)
            * controller matrix (K)
        Controller can be modified afterwards using command-line interface.

    D - feed-forward matrix of the controller

    num_states - number of states in the simulated process

    num_inputs - number of inputs/outputs of the simulated process

    delay - delay of the output of the process (in number of samples)

    nonlinearity - function that introduces nonlinearity in the simulated process.
        Available values: unity, sin, pow2, pow3, exp. When nonlinearity is
        defined, the output value is described with the following equation: 

            y(t) = C * nonlinearity(x(t))

    error_dist_mu - value of noise normal distribution expectation

    error_dist_sigma - value of noise normal distribution expectation

    feed_forward - feed_forward input
 

The client sends configuration of the process to the server. The
process is configured with the use of Rest API. The Swagger documentation
of the API in .json format is automatically generated every time the server.py
script is run. The documentation is available in the same folder as the script.

## Command line interface

The client module exposes command-line interface. The following commands are
available:

    s - shows the information about the output of the dynamic process as well as
        the frequency of sending control signal to the dynamic process

    h - hides the above information

    exit - exits the client application

    controller_coeff - used to change coefficients of the controller. The
        following matrices could be modified: A, B, C, D, L or K. In case of
        modification of A, B or C - matrices L and K will be recalculated.
        (Only controller's coefficients will be modified. The simulated
        process in the server will remain unchanged)
        example:  
            controller_coeff A; [[0.1, 0.2, 0.3],[0.3, 0.4, 0.1],[0.2, 0.7, 0.4]] 


## Disruption of the server process
 
In order to start disturbing operation of the server, start zaklocenie machine:

    $ vagrant ssh zaklocenie


In virtual machine, start zaklocenie.py script: 

    $ python3.6 /vagrant/zaklocenie/zaklocenie.py


Description of the disruption produced by zaklocenie is available in README
file in zaklocenie folder.
After starting the script, there should be a lot of error messages produced by
the server.


The disruption could be stopped by firewall, configured by snort.
For that purpose login to the fw_router machine and start the firewall.py
script:

    $ vagrant ssh fw_router 


In virtual machine:

    $ sudo python3.6 /vagrant/fw_router/firewall.py 


It will start the service exposing REST API for the snort module, listening for
the IPs to block.


Then, login to the snort machine and start Snort software:

    $ vagrant ssh snort 

In virtual machine:

    $ sudo python3.6 /vagrant/snort/snort_run.py 

It will start Snort software with predefined rule. It will produce an alert
if during 3 seconds 400 packets are sent to 20.0.0.0/24 - local network where
the server is located.

When the alert is produced, the IP address that produced the alert is sent to
the firewall, which blocks respective address. Overmore, information about
the event is written to the database.


After a moment after starting snort, the operation of the server should come
back to normal.


In order to see the messages written into the database, login to db machine: 

    $ vagrant ssh db


In the virtual machine, run the script:

    $ python3.6 /vagrant/db/mongo_print.py  
 

It should print all the records in the database (in this case, one record).








