import boto3
import json
import datetime
from blcks import blcks


MY_FAAS_METHOD_NAME = "blcksdescribeinstances"
aws_session_type = 'ec2'
aws_region_name = 'ap-northeast-1'


@blcks
def main(event, context):
    pass


@blcks.script(MY_FAAS_METHOD_NAME)
def process(key_id):
    print(key_id)

    cloud_account_manager = blcks.createService(
        blcks.ServiceName.CloudAccountManager)
    account_info = cloud_account_manager.getCloudAccount(
        key_id["provider_id"],
        key_id["cloud_account_id"]
    )["data"][0]

    credential = find_credential(
        account_info["credentials"],
        key_id["cloud_credential"]
    )

    if not credential:
        raise Exception("Credential Not Found")

    accessKeyId = credential["accessKeyId"]
    secretAccessKey = credential["secretAccessKey"]

    session = boto3.Session(
        aws_access_key_id=accessKeyId,
        aws_secret_access_key=secretAccessKey,
    )
    client = session.client(
        aws_session_type,
        region_name=aws_region_name
    )

    ret = json.dumps(
        client.describe_instances(),
        default=default
    )

    return {"resp": ret}


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def find_credential(credentials, cid):
    for c in credentials:
        if c["id"] == cid:
            return c["credential"]
    return None
