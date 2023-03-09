---
# User change
title: "Deploy MariaDB via Docker"

weight: 3 # 1 is first, 2 is second, etc.

# Do not modify these elements
layout: "learningpathall"
---


## Before you begin

Any computer which has the required tools installed can be used for this section. 

You will need an [AWS account](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=default&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start). Create an account if needed.

Three tools are required on the computer you are using. Follow the links to install the required tools.
* [Terraform](/install-tools/terraform)
* [Ansible](https://www.cyberciti.biz/faq/how-to-install-and-configure-latest-version-of-ansible-on-ubuntu-linux/)
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

Before installing MariaDB via a docker container with Ansible. First [Generate Access Keys](/learning-paths/server-and-cloud/aws/terraform#generate-access-keys-access-key-id-and-secret-access-key) and an [ssh key-pair using the keygen tool](/learning-paths/server-and-cloud/aws/terraform#generate-key-pairpublic-key-private-key-using-ssh-keygen). Also have an [EC2 instance deployed](/learning-paths/server-and-cloud/mariadb/ec2_deployment#deploy-ec2-instance-via-terraform). After successful deployment of the EC2 instance, we will need to configure the MariaDB docker container on the same.

## Deploy MariaDB container using Ansible
Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.

To run Ansible, we have to create a **.yml** file, which is also known as `Ansible-Playbook`.
In our **.yml** file, we use the **community.docker** collection to deploy the MariaDB container.
We also need to map the container port to the host port, which is `3306`. Below is a **.yml** file named **mariadb_module.yml** that will do this for us.

```console
---
- hosts: all
  remote_user: root
  become: true
  tasks:
    - name: Update the Machine and Install dependencies
      shell: |
             apt-get update -y
             apt-get -y install mariadb-client
             apt-get install docker.io -y
             usermod -aG docker ubuntu
             apt-get -y install python3-pip
             pip3 install PyMySQL
             pip3 install docker
      become: true
    - name: Reset ssh connection for changes to take effect
      meta: "reset_connection"
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

```
**NOTE:**- Replace **docker_container.env** variables of **Deploy mariadb docker container** task with your own MariaDB user and password. Also, replace **{{dockerhub_uname}}** and **{{dockerhub_pass}}** with your dockerhub credentials.

In our case, the inventory file will generate automatically after the `terraform apply` command.

### Ansible Commands
To run a Playbook, we need to use the following `ansible-playbook` command.
```console
ansible-playbook {your_yml_file} -i {your_inventory_file} --key-file {path_to_private_key}
```
**NOTE:-** Replace **{your_yml_file}**, **{your_inventory_file}** and **{path_to_private_key}** with your values.

![Screenshot (434)](https://user-images.githubusercontent.com/92315883/223045927-18735e29-56d1-45cf-989c-a5b59dcae7f5.png)


Here is the output after the successful execution of the `ansible-playbook` command.

![Screenshot (435)](https://user-images.githubusercontent.com/92315883/223045950-81c25f03-6d7d-4e7e-8859-577076028ce7.png)


## Connect to Database

To connect to the database, we need the **public-ip** of the instance where MariaDB is deployed, which can be found in **inventory.txt** file. We also need to use the MariaDB Client to interact with the MariaDB database.

```console
apt install mariadb-client
```

```console
mariadb -h {public_ip of instance where MariaDB deployed} -P3306 -u {user_name of database} -p{password of database}
```

**NOTE:-** Replace **{public_ip of instance where MariaDB deployed}**, **{user_name of database}** and **{password of database}** with your values. In our case, **user_name**= **root**. 

![Screenshot (436)](https://user-images.githubusercontent.com/92315883/223045846-7a909b26-5153-4498-bdeb-6997fb0177bf.png)


### Create Database and Table

Use the below command to create a database.

```console
show databases;
```
```console
create database {{your_database_name}};
```
```console
use {{your_database_name}};
```

![Screenshot (446)](https://user-images.githubusercontent.com/92315883/223372080-22df1da5-42c4-437b-aaa4-319192e209ed.png)

To create and access a table, follow this [document](/learning-paths/server-and-cloud/mariadb/ec2_deployment.md#create-database-and-table).
