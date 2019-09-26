#
Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/xenial64"
#    config.vm.box = "ubuntu/trusty64"
#    config.vm.box = "hashicorp/precise64"
#    config.vm.box = "bento/ubuntu-10.04-i386"

    config.vm.provider "virtualbox" do |v|
        v.memory = 512
    end

    config.vm.define :server do |server|
        server.vm.provision :shell, path: "bootstrap.sh"
        server.vm.network "private_network", ip: "20.0.0.2"
        server.vm.provision "shell",
            inline: "sudo ip route add 10.0.0.0/24 via 20.0.0.99"
        server.vm.provision "shell",
            inline: "python3.6 -m pip install flask"
        server.vm.provision "shell",
            inline: "python3.6 -m pip install flask_restplus"
        server.vm.provision "shell",
            inline: "python3.6 -m pip install numpy" 
        server.vm.provision "shell",
            inline: "python3.6 -m pip install control" 
    end

    config.vm.define :db do |db|
        db.vm.provision :shell, path: "bootstrap.sh"
        db.vm.network "private_network", ip: "40.0.0.3"
        db.vm.provision :shell, path: "db/db_conf.sh"
        db.vm.provision "shell",
            inline: "python3.6 -m pip install pymongo" 
        db.vm.provision "shell",
            inline: "python3.6 /vagrant/db/mongo.py" 
    end

    config.vm.define :fw_router do |fw_router|
        fw_router.vm.provision :shell, path: "fw_router/port_mirror.sh"
        fw_router.vm.provision :shell, path: "bootstrap.sh"
        fw_router.vm.network "private_network", ip: "10.0.0.99" # routing
        fw_router.vm.network "private_network", ip: "20.0.0.99" # routing
        fw_router.vm.network "private_network", ip: "30.0.0.99" # traffic copy
        fw_router.vm.network "private_network", ip: "40.0.0.99" # snort notiffications
        fw_router.vm.provision "shell",
            inline: "sysctl -w net.ipv4.ip_forward=1"
        fw_router.vm.provision "shell",
            inline: "python3.6 -m pip install cherrypy"
    end

    config.vm.define :snort do |snort|
        snort.vm.provision :shell, path: "bootstrap.sh"
        snort.vm.provision :shell, path: "snort/snort_conf.sh"
        snort.vm.network "private_network", ip: "30.0.0.2"
        snort.vm.network "private_network", ip: "40.0.0.2"
        snort.vm.provision "shell",
            inline: "python3.6 -m pip install requests" 
        snort.vm.provision "shell",
            inline: "python3.6 -m pip install pymongo" 
    end

    config.vm.define :client do |client|
        client.vm.provision :shell, path: "bootstrap.sh"
        client.vm.network "private_network", ip: "10.0.0.5"
        client.vm.provision "shell",
            inline: "sudo ip route add 20.0.0.0/24 via 10.0.0.99"
        client.vm.provision "shell",
            inline: "python3.6 -m pip install requests"
        client.vm.provision "shell",
            inline: "python3.6 -m pip install numpy" 
        client.vm.provision "shell",
            inline: "python3.6 -m pip install control" 
    end

    config.vm.define :zaklocenie do |zaklocenie|
        zaklocenie.vm.provision :shell, path: "bootstrap.sh"
        zaklocenie.vm.network "private_network", ip: "10.0.0.6"
        zaklocenie.vm.provision "shell",
            inline: "sudo ip route add 20.0.0.0/24 via 10.0.0.99"
        zaklocenie.vm.provision "shell",
            inline: "python3.6 -m pip install requests" 
    end

#    config.vm.define :zaklocenie2 do |zaklocenie2|
#        zaklocenie2.vm.provision :shell, path: "bootstrap.sh"
#        zaklocenie2.vm.network "private_network", ip: "10.0.0.7"
#        zaklocenie2.vm.provision "shell",
#            inline: "sudo ip route add 20.0.0.0/24 via 10.0.0.99"
#        zaklocenie2.vm.provision "shell",
#            inline: "python3.6 -m pip install requests" 
#    end
#
#    config.vm.define :zaklocenie3 do |zaklocenie3|
#        zaklocenie3.vm.provision :shell, path: "bootstrap.sh"
#        zaklocenie3.vm.network "private_network", ip: "10.0.0.8"
#        zaklocenie3.vm.provision "shell",
#            inline: "sudo ip route add 20.0.0.0/24 via 10.0.0.99"
#        zaklocenie3.vm.provision "shell",
#            inline: "python3.6 -m pip install requests" 
#    end

end
