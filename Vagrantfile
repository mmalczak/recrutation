#
Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/xenial64"
#    config.vm.box = "ubuntu/trusty64"
#    config.vm.box = "hashicorp/precise64"
#    config.vm.box = "bento/ubuntu-10.04-i386"
    config.vm.provision :shell, path: "bootstrap.sh"

    config.vm.define :client do |client|
        client.vm.network "private_network", ip: "10.0.0.5"
        client.vm.provision "shell", 
            inline: "sudo ip route add 20.0.0.0/24 via 10.0.0.99"  
    end  

    config.vm.define :server do |server|
        server.vm.network "private_network", ip: "20.0.0.2"
        server.vm.provision "shell", 
            inline: "sudo ip route add 10.0.0.0/24 via 20.0.0.99"  
    end  

    config.vm.define :fw_router do |fw_router|
        fw_router.vm.network "private_network", ip: "10.0.0.99"
        fw_router.vm.network "private_network", ip: "20.0.0.99"
        fw_router.vm.provision "shell", 
            inline: "sysctl -w net.ipv4.ip_forward=1"  
    end  

#    config.vm.define :zaklocenie do |zaklocenie|
#    end  
#
#    config.vm.define :snort do |snort|
#    end  
#
#    config.vm.define :db do |db|
#    end  



end
