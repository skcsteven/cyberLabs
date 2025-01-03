#### 1. View instance

The web application appears to be a simple time displayer with two options: the time (17:27:26) and the date (2025-1-1).

For each of these options, there is the parameter "format"

```
http://94.237.59.180:30337/?format=%Y-%m-%d
http://94.237.59.180:30337/?format=%H:%M:%S
```

Playing around with the format parameter shows me that an injection vulnerability is the solution.

For example, with "http://94.237.59.180:30337/?format=%b-%999-%a" puts ">It's Jan-�9-Thu" on the web app.

#### 2. View provided files

The files provided allow a local instance of the web app. There are config files: 

- FPM (FastCGI Process Manager): A PHP implementation designed to improve performance, commonly used with Nginx for handling PHP scripts. It is configured using an fpm.conf file to manage workers, set timeouts, and define pools.

- Nginx Configuration: The nginx.conf file defines how Nginx handles incoming web requests, including server blocks, locations, and upstreams.

- supervisord.conf: Configuration file for Supervisor, a process control system that ensures services (like FPM or background tasks) stay running. It defines how services are started, stopped, and monitored.

Docker files:

- build_docker.sh
- Dockerfile

As well as all the web app files: php, css, etc.
Also, there is a flag file which states that it is for testing purposes - likely for when you run the app locally and come across the solution.

#### 3. Run locally with Docker

After building the image with the .sh file provided, start the container;

```
docker run -p 8080:80 <image_name> #navigate to localhost:8080
```
