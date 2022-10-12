Twitter Data Source

1. Build the image
     ```bash
     sudo docker image build -t tw .
     ```
2. Run the Container.     
   ``` bash
   sudo docker run --network host --env KafkaServer=192.168.1.82:9092 --env ContainerName=first_step --name=twitterdatacontainer tw
   ```
