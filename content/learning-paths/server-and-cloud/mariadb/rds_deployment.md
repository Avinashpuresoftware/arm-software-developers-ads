---
# User change
title: "Deploy MariaDB using RDS"

weight: 4 # 1 is first, 2 is second, etc.

# Do not modify these elements
layout: "learningpathall"
---
## Prerequisites

* An [AWS account](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=default&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start)
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* [AWS IAM authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html)
* [Terraform](/install-tools/terraform)

## Deploy MariaDB RDS instances

RDS is a Relational database service provided by AWS. More information can be found [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.MariaDB.html). 
To generate an access key and secret key, follow the instructions mentioned in this [document](/content/learning-paths/server-and-cloud/mariadb/ec2_deployment.md#generate-access-keys-access-key-id-and-secret-access-key).
To deploy an RDS instance of MariaDB, we have to create a Terraform file called **main.tf**. Below is the complete **main.tf**.

```console

provider "aws" {
  region = "us-east-2"
  access_key  = var.access_key # access through credential file.
  secret_key   = var.secret_key
}

resource "aws_db_parameter_group" "default" {
  name   = "mariadb"
  family = "mariadb10.6"
}

resource "aws_db_instance" "Testing_mariadb" {
  identifier           = "mariadbdatabase"
  allocated_storage    = 10
  db_name              = "mydb"
  engine               = "mariadb"
  engine_version       = "10.6.10"
  instance_class       = "db.m6g.large"
  parameter_group_name = "mariadb"
  skip_final_snapshot  =  true
  username              = var.username
  password              = var.password
  availability_zone     = "us-east-2a"
  publicly_accessible  = true
  deletion_protection   = false

  tags = {
        name                 = "TEST MariaDB"
  }

}
output "end_point" {
 value = aws_db_instance.Testing_mariadb.endpoint
}


```  

We also need to create a **credential.tf** file, for passing our secret keys and password. Below is the **credential.tf** file

```console
variable "username"{
      default  = "admin"
}

variable "password"{
      default  = "Armtest"    #we_can_choose_any_password, except special_characters.
}

variable "access_key"{
      default  = "AKIXXXXXXXXXXXXXX"
}

variable "secret_key"{
      default  = "EXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}


```
**NOTE:** Replace **secret_key** and **access_key** with the your AWS credentials.

To run Graviton (Arm) based DB instance, we need to select Amazon **M6g** and **R6g** as a [instance type](https://aws.amazon.com/blogs/database/key-considerations-in-moving-to-graviton2-for-amazon-rds-and-amazon-aurora-databases/). Here, we select **db.m6g.large** as a **instance_class**. 

Now, use the Terraform commands below to deploy **main.tf** file.


## Terraform commands

**Initialize Terraform**

Run `terraform init` to initialize the Terraform deployment. This command is responsible for downloading all dependencies which are required for the AWS provider.

```console
terraform init
```
![Screenshot (369)](https://user-images.githubusercontent.com/92315883/218339605-a38f5ee1-d0f6-475d-b0c2-ac766837cc5a.png)

**Create a Terraform execution plan**

Run `terraform plan` to create an execution plan.

```console
terraform plan
```

**NOTE:** The **terraform plan** command is optional. You can directly run **terraform apply** command. But it is always better to check the resources about to be created.

### Apply a Terraform execution plan

Run `terraform apply` to apply the execution plan to your cloud infrastructure. The below command creates all required infrastructure.

```console
terraform apply
```      

![Screenshot (371)](https://user-images.githubusercontent.com/92315883/218339620-80e3f741-d295-4693-a057-4b6cd1e762aa.png)


To verify the setup on AWS console, go to **RDS » Databases**, you should see the instance running.  

![Screenshot (374)](https://user-images.githubusercontent.com/92315883/218340185-097c876e-2c3c-4630-adef-ac9b905c08ec.png)


## Connect to RDS using EC2 instance

To access the RDS instance, make sure that our instance is correctly associated with a security group and VPC. To access RDS outside the VPC, follow this [document](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.Connect.html).

To connect to the RDS instance, we need the **Endpoint** of the RDS instance. To find the Endpoint, go to **RDS »Dashboard » {{YOUR_RDS_INSTANCE}}**.

![Screenshot (372)](https://user-images.githubusercontent.com/92315883/218339661-0ac51c95-8789-42bc-962c-0b43fc64fb5b.png)


Now, we can connect to RDS by using the above **Endpoint**. Use the **user** and **password** mentioned in the **credential.tf** file.

```console
mariadb -h {{Endpoint}} -u {{user}} -p {{password}}
```
**NOTE:** Replace **{{Endpoint}}**, **{{user}}** and **{{password}}** with your values.

![Screenshot (367)](https://user-images.githubusercontent.com/92315883/218339637-ecfb3c9f-d17f-43dc-a25f-27e5c330f750.png)

### Create Database and Table
Use the below command to create a database.

```console
create database {name_of_your_database};
```
```console
show databases;
```
```console
use {name_of_your_database};
```
![Screenshot (373)](https://user-images.githubusercontent.com/92315883/218339705-fef60d7b-cd76-406d-9fc2-4374cf1d5ee4.png)

To create and access a table, follow this [document](/content/learning-paths/server-and-cloud/mariadb/ec2_deployment.md#access-database-and-create-table).
