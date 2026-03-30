from connection import AWSConnection


class AwsS3:
    def __init__(self,aws_obj):
        self.aws_obj = aws_obj
        self.s3_obj = self.aws_obj.connection()

    def create_bucket(self, bucket_name : str):
        '''THis method is to create bucket in given s3 account'''
        try:
            response = self.s3_obj.create_bucket(bucket = bucket_name)
            print(f"Bucket sucessfully created ! {bucket_name}")
            return True
        except Exception as e:
            print(f"There is some issue Creating  S3 bucket ! {e}")

    def list_bucket(self):
        '''This method is to get list of buckets inside connected accounts'''
        try:
            response = self.s3_obj.list_buckets()
            buckets = []
            for bucket in response['Buckets']:
                buckets.append(bucket['Name'])
            return buckets
        except Exception as e:
            print(f"There is some issue fetching S3 bucket ! {e}")

    def list_objects_in_bucket(self, bucket_name : str):
        '''This method is to get list object in given bucket 
        input > bucket_name : str'''
        try:
            response = self.s3_obj.list_objects_v2(Bucket = bucket_name)
            data = response.get('Contents')
            objects_name =[]
            if data:
                for item in data:
                    objects_name.append(item.get("Key"))
            else:
                print("Looks like there is no data in this bucket ")
                return False

            return objects_name
        except Exception as e:
            print(f"There is some issue fetching Objects in given bucket  {bucket_name} ! {e}")

    def upload_into_bucket(self, file , bucket_name : str , file_name : str):
        '''This method is to upload a file in given bucket 
        input 
        file : location of file in the system
        bucket_name : bucket name in aws s3
        file_name : file_name to be added with this file in s3'''
        try:
            response = self.s3_obj.upload_file(file, bucket_name, file_name)
            print(f"File successfully uploaded in to bucket {bucket_name}, with file name {file_name}")
            return True
        except Exception as e:
            print(f"There is some issue uploading object  S3 bucket ! {e}")

    def delete_object_from_bucket(self, bucket_name : str , object_name : str):
        '''
        This method is to delete an object in given bucket 
        input
        bucket_name : name to the bucket where you want to delete the object
        object_name : object name to be deleted'''
        try:
            response = self.s3_obj.delete_object(Bucket = bucket_name , Key = object_name)
            print(f"Object deleted successfully  {bucket_name}, with object name {object_name}")
            return True
        except Exception as e:
            print(f"There is some issue deleting object {object_name} in  {bucket_name} bucket ! {e}")


    def download_file_from_s3(self, bucket_name, object_name, temp_file):
        '''
        This method is to downlaod an object in given bucket 
        input
        bucket_name : name to the bucket where you want to delete the object
        object_name : object name to be deleted
        temp_file : the file will be creted in current location with name'''
        try:
            response = self.s3_obj.download_file(bucket_name ,object_name,temp_file)
            print(f"Object downlaoded successfully  {bucket_name}, with object name {object_name}")
            return True
        except Exception as e:
            print(f"There is some issue downloading object {object_name} in  {bucket_name} bucket ! {e}")

    

if __name__ == '__main__':
    aws_connection = AWSConnection('s3')
    s3obj = AwsS3(aws_connection)

    # list_bucket = s3obj.list_bucket()
    # list_objects = s3obj.list_objects_in_bucket('testrehanaatif95')
    # print(list_objects)
    # upload_object = s3obj.upload_into_bucket('/Users/rehanaatif/Desktop/Projects/pythonProjects/AWS/test.txt','testrehanaatif95','testfilefors3')
    # delete_object = s3obj.delete_object_from_bucket('testrehanaatif95','testfilefors3' )
    download_file = s3obj.download_file_from_s3('testrehanaatif95','testfilefors3','/Users/rehanaatif/Desktop/Projects/pythonProjects/AWS/downloaded_from_s3.txt')