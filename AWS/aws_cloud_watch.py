from connection import AWSConnection
import time


class CloudWatchLogs:

    def __init__ (self):
        self.aws_obj = AWSConnection(conncection_type= 'logs')
        self.cloudwatchlogs = self.aws_obj.connection()

    def create_log_group(self, log_group_name):
        try:
            self.cloudwatchlogs.create_log_group(logGroupName=log_group_name)
            print("Log group created")
        except self.cloudwatchlogs.exceptions.ResourceAlreadyExistsException:
            print("Log group already exists")

    def put_log(self, log_group_name, log_stream_name, message):
        timestamp = int(time.time() * 1000)

        response = self.cloudwatchlogs.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': message
                }
            ]
        )

        print("Log inserted successfully to cloud watch")
        return response




if __name__ == '__main__':
    logs_obj = CloudWatchLogs()
    # logs_obj.create_log_group('testing_logs')
    logs_obj.put_log()


