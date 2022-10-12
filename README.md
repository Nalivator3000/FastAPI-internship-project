1. How to run the application?
   - Save current repository on you local machine
   - Open the directory of the application in shell
      OR
   - Enter the command: docker build -t meduzzen:0.1 .
   - docker run -r 8000:8000 --name test-meduzzen meduzzen:0.1
      OR
   - docker-compose up
   - Open localhost (http://127.0.0.1:8000)