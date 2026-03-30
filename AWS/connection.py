import boto3
import botocore
import yaml
with open('secrets.yaml','r') as file:
    secrets = yaml.safe_load(file)





class AWSConnection:
    def __init__(self,conncection_type : str):
        self.connection_type = conncection_type


    def connection(self):
        try :
            aws_client = boto3.client(self.connection_type,
            aws_access_key_id=secrets.get('aws_access_key_id'),
            aws_secret_access_key=secrets.get('aws_secret_access_key'),
            region_name=secrets.get('region')
            )
            print(f"Connection Successfully create to AWS for {self.connection_type} !")
            return aws_client

        except Exception as e:
            print(f"There was some issue making connection with aws! {e}")



if __name__ == '__main__':
    aws_obj = AWSConnection(conncection_type= 'cloudwatch')
    cloudwatch = aws_obj.connection()

    print(cloudwatch.list_metrics())
