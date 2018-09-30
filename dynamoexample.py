import os
from boto3 import resource
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

dynamodb_resource = resource('dynamodb',
              aws_access_key_id=ACCESS_KEY,
              aws_secret_access_key=SECRET_KEY,
              region_name='us-east-1'
              )

def get_item_dynamo(table_name, primary_keys):
    """Get and item from dynamo table."""
    table = dynamodb_resource.Table(table_name)
    filter_key = primary_keys[0]
    if filter_key and primary_keys[1]:
        filtering_exp = Key(filter_key).eq(primary_keys[1])
        response = table.query(KeyConditionExpression=filtering_exp)
    else:
        response = table.query()
    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.query(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break
    return items

def add_attribute_dynamo(table_name, primary_keys, attr_name, attr_value):
    """Adding an attribute to a dynamo table."""
    table = dynamodb_resource.Table(table_name)
    item = get_item_dynamo(table_name, primary_keys)
    if not item:
        try:
            response = table.put_item(
                Item={
                    primary_keys[0]: primary_keys[1],
                    attr_name: attr_value
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError as e:
            print e
            return False
    else:
        return update_attribute_dynamo(
            table_name,
            primary_keys,
            attr_name,
            attr_value)

def update_attribute_dynamo(table_name, primary_keys, attr_name, attr_value):
    """Updating an attribute to a dynamo table."""
    table = dynamodb_resource.Table(table_name)
    try:
        response = table.update_item(
            Key={
                primary_keys[0]: primary_keys[1],
            },
            UpdateExpression='SET #attrName = :val1',
            ExpressionAttributeNames={
                '#attrName': attr_name
            },
            ExpressionAttributeValues={
                ':val1': attr_value
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError as e:
        print e
        return False

def delete_item_dynamo(table_name, primary_keys):
    """ Delete an item in a dynamo table."""
    table = dynamodb_resource.Table(table_name)
    try:
        response = table.delete_item(
            Key={
                primary_keys[0]: primary_keys[1],
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError as e:
        print e
        return False

def add_list_dynamo(table_name, primary_keys, attr_name, attr_value):
    """Adding list attribute in a table."""
    table = dynamodb_resource.Table(table_name)
    item = get_item_dynamo(table_name, primary_keys)
    if not item:
        try:
            response = table.put_item(
                Item={
                    primary_keys[0]: primary_keys[1],
                    attr_name: attr_value,
                }
            )
            resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
            return resp
        except ClientError as e:
            print e
            return False
    else:
        return update_list_dynamo(
            table_name,
            primary_keys,
            attr_value,
            attr_name,
            item
        )


def update_list_dynamo(table_name, primary_keys, attr_value, attr_name, item):
    """Update list attribute in a table."""
    table = dynamodb_resource.Table(table_name)
    try:
        if attr_name not in item[0]:
            table.update_item(
                Key={
                    primary_keys[0]: primary_keys[1],
                },
                UpdateExpression='SET #attrName = :val1',
                ExpressionAttributeNames={
                    '#attrName': attr_name
                },
                ExpressionAttributeValues={
                    ':val1': []
                }
            )
        update_response = table.update_item(
            Key={
                primary_keys[0]: primary_keys[1],
            },
            UpdateExpression='SET #attrName = list_append(#attrName, :val1)',
            ExpressionAttributeNames={
                '#attrName': attr_name
            },
            ExpressionAttributeValues={
                ':val1': attr_value
            }
        )
        resp = update_response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError as e:
        print e
        return False


def remove_list_dynamo(table_name, primary_keys, attr_name, index):
    """Remove list attribute in a table."""
    table = dynamodb_resource.Table(table_name)
    try:
        response = table.update_item(
            Key={
                primary_keys[0]: primary_keys[1],
            },
            UpdateExpression='REMOVE #attrName[' + str(index) + ']',
            ExpressionAttributeNames={
                '#attrName': attr_name
            }
        )
        resp = response['ResponseMetadata']['HTTPStatusCode'] == 200
        return resp
    except ClientError as e:
        print e
        return False



if __name__ == '__main__':
    table_name = "AsistentesMeetup"
    primary_keys = ["email", "xergioalex@gmail.com"]
    var = []
    var.append({"size": "M", "color": "blue"})
    response = add_attribute_dynamo(table_name, primary_keys, "name", "Sergio")
    # response = delete_item_dynamo(table_name, primary_keys)
    # response = add_attribute_dynamo(table_name, primary_keys, "loses", "0")
    # response = delete_item_dynamo(table_name, primary_keys)
    # response = add_list_dynamo(table_name, primary_keys, "tshirt", var)
    # response = remove_list_dynamo(table_name, primary_keys, "tshirt", 4)
    print response