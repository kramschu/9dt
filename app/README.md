To start app/app info:

1. Navigate to app/ directory and run
    'docker-compose up'

NOTE: Docker must be installed to run this app, see [https://docs.docker.com/get-docker/]

2. App is using port:4444. If this port is already taken you must kill the current process or change ports in the docker-compose.yml file

3. App data will not persist, database is a simple sqlite database. If you stop the docker container you will lose your current data. If I were to finalize the app, I would use a live database instead.

4. Test with an API testing development. I used Postman, see screenshots in screenshots/ for examples.

5. To stop container, run
    'docker ps' to get container id
    'docker stop <container-id>' to stop container
    'docker rm <container-id>' to remove container
    'docker image rm app_app' to remove image