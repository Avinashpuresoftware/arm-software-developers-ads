---
# User change
title: "Deploy MariaDB via Docker"

weight: 3 # 1 is first, 2 is second, etc.

# Do not modify these elements
layout: "learningpathall"
---


## Prerequisites

* An [AWS account](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=default&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start)
* [Docker](https://www.simplilearn.com/tutorials/docker-tutorial/how-to-install-docker-on-ubuntu)
* [Terraform](/install-tools/terraform.md)
* [Ansible](https://www.cyberciti.biz/faq/how-to-install-and-configure-latest-version-of-ansible-on-ubuntu-linux/)

Before Installing MariaDB using docker via Ansible [Generate Access Keys](/content/learning-paths/server-and-cloud/mysql/ec2_deployment.md#generate-access-keys-access-key-id-and-secret-access-key), [Generate key-pair using ssh keygen](/content/learning-paths/server-and-cloud/mysql/ec2_deployment.md#generate-key-pairpublic-key-private-key-using-ssh-keygen) and [Deploy EC2 instance via Terraform](/content/learning-paths/server-and-cloud/mariadb/ec2_deployment.md#deploy-ec2-instance-via-terraform).

## Deploy MariaDB container using Ansible
Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.

To run Ansible, we have to create a **.yml** file, which is also known as `Ansible-Playbook`.
In our **.yml** file, we use the `community.docker` collection to deploy the MariaDB container.
We also need to map the container port to the host port, which is `3306` in our case. Below is a **.yml** file named **mariadb_module.yml** that will do this for us.

```console
---
- hosts: all
  remote_user: root
  become: true
  tasks:
    - name: Update the Machine
      shell: apt-get update -y
    - name: Install docker
      shell: apt install docker.io -y
    - name: add user permissions
      shell: usermod -aG docker ubuntu
    - name: Reset ssh connection for changes to take effect
      meta: "reset_connection"
    - name: Installing PIP for enabling MariaDB Modules
      shell: apt -y install python3-pip
    - name: Installing dependencies
      shell: pip3 install PyMySQL
    - name: Installing docker dependencies
      shell: pip3 install docker
    - name: Install Mariadb-client
      shell: apt -y install mariadb-client
    - name: Log into DockerHub
      community.docker.docker_login:
        username: {{dockerhub_uname}}
        password: {{dockerhub_pass}}
    - name: Deploy mariadb docker container
      docker_container:
        image: mariadb:latest
        name: mariadb_test
        state: started
        ports:
          - "3306:3306"
        pull: true
        volumes:
         - "db_data:/var/lib/mysql:rw"
         - "mariadb-socket:/var/run/mysqld:rw"
         - "/tmp:/tmp:rw"
        restart: true
        env:
          MARIADB_ROOT_PASSWORD: {{your_mariadb_password}}
          MARIADB_USER: local_us
          MARIADB_PASSWORD: Armtest123
          MARIADB_DATABASE: arm_test
    - name: Copy database dump file
      copy:
       src: /home/ubuntu/table.sql
       dest: /tmp
    - name: Run a simple command to populate table
      community.docker.docker_container_exec:
       container: mariadb_test
       command: mariadb -u root -p{{your_mariadb_password}} -e "source /tmp/table.sql;"
       chdir: /root
      register: result

```
**NOTE:**- Replace `docker_container.env` variables with your MariaDB user and password. Also. replace `{{dockerhub_uname}}` and `{{dockerhub_pass}}` with your dockerhub credentials.

In the above **mariadb_module.yml** file, we are pre-populating our database with the [table.sql](https://github.com/Avinashpuresoftware/arm-software-developers-ads/files/10755199/table_dot_sql.txt) script file.

In our case, the inventory file will generate automatically after the `terraform apply` command.

### Ansible Commands
To run a Playbook, we need to use the `ansible-playbook` command.
```console
ansible-playbook {your_yml_file} -i {your_inventory_file} --key-file {path_to_private_key}
```
**NOTE:-** Replace `{your_yml_file}`, `{your_inventory_file}` and `{path_to_private_key}` with your values.

![Screenshot (383)](https://user-images.githubusercontent.com/92315883/218344988-42b141b1-18c3-4567-a1fe-9fc2c8ae1329.png)

Here is the output after the successful execution of the `ansible-playbook` command.

![Screenshot (382)](https://user-images.githubusercontent.com/92315883/218344992-46ab730e-d6b6-40bc-b917-45f57d7bff14.png)

## Connect to Database using EC2 instance

To connect to the database, we need the `public-ip` of the instance where MariDB is deployed. We also need to use the MariaDB Client to interact with the MariaDB database.

```console
apt install mariadb-client
```

```console
mariadb -h {public_ip of instance where MariaDB deployed} -P3306 -u {user_name of database} -p{password of database}
```

**NOTE:-** Replace `{public_ip of instance where MariaDB deployed}`, `{user_name of database}` and `{password of database}` with your values. In our case `user_name`= `local_us`, which we have created through the **mariadb_module.yml** file. 

![Screenshot (385)](https://user-images.githubusercontent.com/92315883/218345000-99d902bd-2e35-4e95-8be6-2236b342b470.png)


### Access Database and Tables

To access our database and tables, use below command:

```console
show databases;
```

```console
use {{your_database}}
```

```console
show tables;
```
![Screenshot (398)](https://user-images.githubusercontent.com/92315883/219525956-73468894-b90a-4bd7-b0b4-fa42a57876a0.png)

To view the content of the table

```console
select * from {{your_table}};
```
![Screenshot (399)](https://user-images.githubusercontent.com/92315883/219525937-ecb2ad70-127d-4231-9ea8-b5a98c5f4d5b.png)

To create a table, follow this [document](/content/learning-paths/server-and-cloud/mariadb/ec2_deployment.md#access-database-and-create-table).
