#
Vagrant.configure("2") do |config|
    config.vm.box = "hashicorp/precise64"
#    config.vm.box = "bento/ubuntu-10.04-i386"
    config.vm.provision :shell, path: "bootstrap.sh"
    


    config.vm.define :client do |client|
        client.vm.network "private_network", ip: "10.0.0.5"

#        config.vm.provision "shell",
#          run: "always",
#          inline: "eval `route -n | awk '{ if ($8 ==\"eth0\" && $2 != \"0.0.0.0\") print \"route del default gw \" $2; }'`"
    end  



    config.vm.define :server do |server|
        server.vm.network "private_network", ip: "20.0.0.2"
    end  

    config.vm.define :fw_router do |fw_router|
#        fw_router.vm.network "private_network", ip: "20.0.0.3"
    end  

    config.vm.define :zaklocenie do |zaklocenie|
    end  

    config.vm.define :snort do |snort|
    end  

    config.vm.define :db do |db|
    end  



end
