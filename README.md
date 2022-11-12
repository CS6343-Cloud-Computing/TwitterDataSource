Twitter Data Source

1. Build the image
     ```bash
     sudo docker image build -t tw .
     ```
2. Run the Container.     
   ``` bash
   docker run --name twit --env kafkaserver=10.176.128.170:9090 --env workflow=abcd --env query=#ukraine twit
   ```
