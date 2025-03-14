# Lab: HTTP request smuggling, confirming a CL.TE vulnerability via differential responses

This lab involves a front-end and back-end server, and the front-end server doesn't support chunked encoding.

To solve the lab, smuggle a request to the back-end server, so that a subsequent request for / (the web root) triggers a 404 Not Found response.

## Solution

First, I change the protocol to HTTP1 with Inspector, disable auto-update content length header and turn on new line markers.

When I send a post request with a body that doesn't match the content length and has the transfer encoding set to chunked, there is a proxy error and long delay which signals a CL TE vulnerability:

![image](https://github.com/user-attachments/assets/70e6be38-1498-48f3-810a-59136b340331)

Now to use differential responses

This first request will send the portion after the GET in the second request beginning:

![image](https://github.com/user-attachments/assets/217c7bda-fb30-4575-b5f3-1378cf2b8fae)


So this below request returns an error when it should not:

![image](https://github.com/user-attachments/assets/d81c544c-b3d5-4369-a9d6-a8fccd71eaf3)

This shows how a http smuggle CLTE can affect web applications with a proxy service.


