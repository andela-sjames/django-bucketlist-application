

private_key_path = File.join(Dir.home, ".ssh", "id_rsa")
public_key_path = File.join(Dir.home, ".ssh", "id_rsa.pub")
insecure_key_path = File.join(Dir.home, ".vagrant.d", "insecure_private_key")

private_key = IO.read(private_key_path)
public_key = IO.read(public_key_path)


Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/precise64"
  config.vm.hostname = "bucketlist-dev"
  config.vm.network "private_network", ip: "192.168.50.4"
  
  config.ssh.insert_key = false
  config.ssh.private_key_path = [
    private_key_path,
    insecure_key_path # to provision the first time
  ]
  
  # reference: https://github.com/hashicorp/vagrant/issues/992 @dwickern 
  # use personal public and private key for security reasons
  config.vm.provision :shell, :inline => <<-SCRIPT
    set -e
    mkdir -p /home/vagrant/.ssh/

    echo '#{private_key}' > /home/vagrant/.ssh/id_rsa
    chmod 600 /home/vagrant/.ssh/id_rsa

    echo '#{public_key}' > /home/vagrant/.ssh/authorized_keys
    chmod 600 /home/vagrant/.ssh/authorized_keys
  SCRIPT


  config.vm.provision "shell" do |s|
    s.path = "setup_python.sh"
    s.args = ["bucketlist_app"]
  end
  
  # if Vagrant.has_plugin?("vagrant-vbguest")
  #   config.vbguest.auto_update = false  
  # end
  

  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.vm.synced_folder '.', '/home/vagrant'
  
  config.vm.provider 'virtualbox' do |v|
    v.memory = 2048
    v.cpus = 2
  end

  config.vm.post_up_message = "At this point use `vagrant ssh` and change dir into /vagrant"
end
