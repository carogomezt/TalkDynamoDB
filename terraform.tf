variable "access_key" {}
variable "secret_key" {}
variable "region" {
  default = "us-east-1"
}

provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region     = "${var.region}"
}

resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "GameScores"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "UserId"

  attribute {
    name = "UserId"
    type = "S"
  }
}

resource "aws_dynamodb_table" "AsistentesMeetupPythonPereira" {
  name           = "AsistentesMeetup"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "email"

  attribute {
    name = "email"
    type = "S"
  }
}