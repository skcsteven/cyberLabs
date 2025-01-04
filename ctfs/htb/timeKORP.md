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

The key file however that tells us how the "format" parameter handles user input is TimeModel.php:

```
<?php
class TimeModel
{
    public function __construct($format)
    {
        $this->command = "date '+" . $format . "' 2>&1";
    }

    public function getTime()
    {
        $time = exec($this->command);
        $res  = isset($time) ? $time : '?';
        return $res;
    }
}
```

As we can see, the line with $this->command handles the input. This is an insecure way to handle user input because a well crafted payload can easily escape the date command and run different commands.

#### 3. Run locally with Docker

After building the image with the .sh file provided, start the container;

```
docker run -p 8080:80 <image_name> #navigate to localhost:8080
```

Now, with knowledge how the input is handled we can add a payload to the format parameter that will "escape" the "date" command. For example, "?format='; pwd ' will be treated in the PHP code as "date '+'; pwd '' 2>&1". Whenever two commands in linux are separated with ";" only the second command runs, so the command effectively becomes "pwd '' 2>&1" which prints the current directory.

Now that this injection vulnerability is confirmed, I will make a payload to find the flag file as seen below:

![first](https://github.com/user-attachments/assets/ea956474-1cea-436d-a872-0281c54bdcf7)

Great, the flag path is /flag. Now to read it:

![second](https://github.com/user-attachments/assets/59f6a45e-10ac-479c-823e-6657cb2d126d)

Nice, the flag was acquired.

#### 4. Run on live instance

All we have to do now is to perform the same payload to read the flag locally on the live instance/address provided on the HTB CTF platform to pwn timeKORP!

