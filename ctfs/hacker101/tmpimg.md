## TempImage - Hacker101 CTF - Web (moderate)



#### Initial recon

Looks like a very simple page with an upload file function.

___


The upload only seems to take images, and when I click upload with no files, I get an error message

---

When I try another file format (.md) I get the another error response:

```
ERROR: Only PNG format supported in trial.
```

It looks like this challenge will be looking at file upload vulnerabilities. I'll open up burpsuite and mess around with different file uploading requests to see how the server handles the files.

When a legitimate png image is uploaded, the site adds the png to a location "files/<random_numbers>_<name_of_your_file>.png", next the client is redirected to a GET request for the png based on the location and then the server responds with the image.

When I upload a non-png file and try to change the filename extension to .png or change the Content-Type: header to image/png the server still is able to detect that the file is not a PNG.

I try POSTing the shell of a valid PNG (removing all the actual data but leaving the filename, headers) and I get a different error getimagesize():

-------

To find a workaround, I create a "minimal" png image with the correct headers for a png.

```
echo -ne "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde" > h.png
```

Once this passes the validation, I try modifying the extension to php and html. Both work but when I use the .php extension, the server does not process the file as a php file. Whereas when I simply append html or javascript to the file when it has an .html extension I get what I expect:

____

____


This likely is due to configuration settings for the file directory, so I try playing around with the name of the file.

I notice that the server renames the file first and then gives this back in the format above. So I try to rename my file to /h.png to see what happens:

---

Ok great, so we know that this creates another error and that the server first converts the file into a tmp file. I repeat the same input but the name of the tmp file changes each time. 

Next I try to see if a directory traversal could work, I try the name "/../h.png". The first flag!

---

Ok this means we are on the right track for flag 2. With the directory traversal vulnerability, I will try to now use my modified png shell with php in it, the inside looks like this:

```
PNG

IHDR<random png bytes n stuff>

<?php echo "hello";?>
```

Next I rename it with the .php extension to tell the server to run it as a php file not a png.

The response lets me know that with a directory traversal name of /../../h.php the php code is executed by the server!

---

From here, I will use a php payload to give us remote code execution:

```
<?php system($_GET['cmd']); ?>
```

With this tagged at the end of the png shell and renamed as a php file we should have remote code execution when we use the cmd parameter in the url.

We got it:

---

From here I just use grep to get the final flag;



#### Resources

https://www.php.net/manual/en/function.getimagesize.php
https://stackoverflow.com/questions/13170819/what-is-htaccess-file
