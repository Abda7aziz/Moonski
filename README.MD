	
## Install Docker and Run it
1. install Docker from the following website https://docs.docker.com/get-docker/
2. make sure Docker is running in the background
3. Test the installatiion by running the command 'docker' in the terminal or cmd

## Setup and configuration:
To setup this project, execute the following commands:
1. Open Terminal or CMD
2. CD into the folder [Portofolio] where Dockerfile is located.
3. Build the docker image: 'Docker build portofolio .' (Notice the dot)

## Starting(Running) The applicatoin:
1. Run the container: 'docker run -d -p 8050:8050 portofolio'
2. open the app from the browser 'http://localhost:8050' or 'http://127.0.0.1:8050'
