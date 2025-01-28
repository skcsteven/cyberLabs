## Path Traversal

Path traversal is also known as directory traversal. These vulnerabilities enable an attacker to read arbitrary files on a server:

- application code & data
- credentials
- sensitive OS files

Attacker may be able to write to arbitrary files on the server, modify application data & behavior, and take control of server.


## Lab

This lab contains a path traversal vulnerability in the display of product images.

To solve the lab, retrieve the contents of the /etc/passwd file. 

Home page:

![pathTraversalSimpleHome](https://github.com/user-attachments/assets/ec2ac751-0338-4db7-bf84-f6f97209f7de)


Clicking on any of the products brings up the product method with a productId parameter that locates the product page to display:

```
https://0acf008004a9f09686e95742003a0064.web-security-academy.net/product?productId=4
```

This parameter doesn't look like it is vulnerable to directory traversal as it doesn't seem to be requesting a specific file, rather an index.

Upon inspecting the elements of one of the product pages, we see a html src locator for the image:

```
src="/image?filename=43.jpg"
```

This looks susceptible to directory traversal as the parameter filename is retrieving a file from the server. Let's try directory traversal with ../ and see if we can get the /etc/passwd file. 

With filename parameter set to "../../../etc/passwd" the page returns an empty image rather than a file not found error. Let's check burpsuite to see what's going on.

With burpsuite we can see the response contains the /etc/passwd file:

![pathTraversalSimpleHosts](https://github.com/user-attachments/assets/b6e5c948-5bf4-406b-94b5-97cfe0a8390b)
