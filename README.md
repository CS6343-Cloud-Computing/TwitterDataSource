Twitter Data Source

1.) Build the image
    docker image build -t twitterDataImage .
2.) Run the Container
    docker run --network netflow --env KafkaServer=kafkaserv:9092 --name=twitterdatacontainer twitterDataImage
