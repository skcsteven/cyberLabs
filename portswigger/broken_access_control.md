# Broken Access Control Lab - Portswigger Academy

Access control is the application of constraints on who or what is authorized to perform actions or access resources. In the context of web applications, access control is dependent on authentication and session management:

- Authentication confirms that the user is who they say they are.
- Session management identifies which subsequent HTTP requests are being made by that same user.
- Access control determines whether the user is allowed to carry out the action that they are attempting to perform.

Broken access controls are common and often present a critical security vulnerability. Design and management of access controls is a complex and dynamic problem that applies business, organizational, and legal constraints to a technical implementation. Access control design decisions have to be made by humans so the potential for errors is high.

## Vertical Privilege Escalation

If a user can gain access to functionality that they are not permitted to access then this is vertical privilege escalation. For example, if a non-administrative user can gain access to an admin page where they can delete user accounts, then this is vertical privilege escalation.

### Unprotected Functionality

At its most basic, vertical privilege escalation arises where an application does not enforce any protection for sensitive functionality. For example, administrative functions might be linked from an administrator's welcome page but not from a user's welcome page. However, a user might be able to access the administrative functions by browsing to the relevant admin URL.

For example, a website might host sensitive functionality at the following URL:

```
https://insecure-website.com/admin
```

This might be accessible by any user, not only administrative users who have a link to the functionality in their user interface. In some cases, the administrative URL might be disclosed in other locations, such as the robots.txt file:

```
https://insecure-website.com/robots.txt
```

Even if the URL isn't disclosed anywhere, an attacker may be able to use a wordlist to brute-force the location of the sensitive functionality.

---
#### Lab: Unprotected Admin Functionality

This lab has an unprotected admin panel.

Solve the lab by deleting the user carlos.

Home page:

![image](https://github.com/user-attachments/assets/452babaf-0d6b-46aa-8f3f-01de1ef31abd)

There is a login page, but we are looking for an admin panel. I'll check to see if there is a robots.txt entry for the web crawlers:

![image](https://github.com/user-attachments/assets/f58a14b0-3959-4fa9-9cc6-4b5e53e9be64)

Great, let's check this page:

![image](https://github.com/user-attachments/assets/d825bf74-86f1-4026-8c47-0dabc3d7c138)

Delete carlos to solve this lab.

---

### Unprotected functionality continued

In some cases, sensitive functionality is concealed by giving it a less predictable URL. This is an example of so-called "security by obscurity". However, hiding sensitive functionality does not provide effective access control because users might discover the obfuscated URL in a number of ways.

Imagine an application that hosts administrative functions at the following URL:

```
https://insecure-website.com/administrator-panel-yb556
```

This might not be directly guessable by an attacker. However, the application might still leak the URL to users. The URL might be disclosed in JavaScript that constructs the user interface based on the user's role:

```
<script>
	var isAdmin = false;
	if (isAdmin) {
		...
		var adminPanelTag = document.createElement('a');
		adminPanelTag.setAttribute('href', 'https://insecure-website.com/administrator-panel-yb556');
		adminPanelTag.innerText = 'Admin panel';
		...
	}
</script>
```

This script adds a link to the user's UI if they are an admin user. However, the script containing the URL is visible to all users regardless of their role.

#### Lab: unprotected admin functionality with unpredictable URL

This lab has an unprotected admin panel. It's located at an unpredictable location, but the location is disclosed somewhere in the application.

Solve the lab by accessing the admin panel, and using it to delete the user carlos.

Analyzing the source for the home page, I see the following script that tells us where the admin panel is:

```
                            <script>
var isAdmin = false;
if (isAdmin) {
   var topLinksTag = document.getElementsByClassName("top-links")[0];
   var adminPanelTag = document.createElement('a');
   adminPanelTag.setAttribute('href', '/admin-72wx4j');
   adminPanelTag.innerText = 'Admin panel';
   topLinksTag.append(adminPanelTag);
   var pTag = document.createElement('p');
   pTag.innerText = '|';
   topLinksTag.appendChild(pTag);
}
</script>
```

After visiting the panel and deleting carlos again, the lab is solved.

### Parameter-based access control methods

Some applications determine the user's access rights or role at login, and then store this information in a user-controllable location. This could be:

- A hidden field.
- A cookie.
- A preset query string parameter.

The application makes access control decisions based on the submitted value. For example:

```
https://insecure-website.com/login/home.jsp?admin=true
https://insecure-website.com/login/home.jsp?role=1
```

This approach is insecure because a user can modify the value and access functionality they're not authorized to, such as administrative functions.

#### Lab: User role controlled by request parameter

This lab has an admin panel at /admin, which identifies administrators using a forgeable cookie.

Solve the lab by accessing the admin panel and using it to delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

First, I log into wiener account. Viewing the cookies we can see an Admin cookie set to false:

![image](https://github.com/user-attachments/assets/d9169c27-a7c2-4081-b125-5789dfd8582e)

Let's change that to true and see what happens. With admin cookie set to true we can access the admin page:

![image](https://github.com/user-attachments/assets/44b8b9ec-2349-4f1a-be60-9addd94ae37a)

Once again, bye byte to carlos to solve the lab.

## Horizontal privilege escalation

Horizontal privilege escalation occurs if a user is able to gain access to resources belonging to another user, instead of their own resources of that type. For example, if an employee can access the records of other employees as well as their own, then this is horizontal privilege escalation.

Horizontal privilege escalation attacks may use similar types of exploit methods to vertical privilege escalation. For example, a user might access their own account page using the following URL:

```
https://insecure-website.com/myaccount?id=123
```

If an attacker modifies the id parameter value to that of another user, they might gain access to another user's account page, and the associated data and functions.

This is an example of an insecure direct object reference (IDOR) vulnerability. This type of vulnerability arises where user-controller parameter values are used to access resources or functions directly.

In some applications, the exploitable parameter does not have a predictable value. For example, instead of an incrementing number, an application might use globally unique identifiers (GUIDs) to identify users. This may prevent an attacker from guessing or predicting another user's identifier. However, the GUIDs belonging to other users might be disclosed elsewhere in the application where users are referenced, such as user messages or reviews.

#### Lab: User ID controlled by request parameter, with unpredictable user IDs

This lab has a horizontal privilege escalation vulnerability on the user account page, but identifies users with GUIDs.

To solve the lab, find the GUID for carlos, then submit his API key as the solution.

You can log in to your own account using the following credentials: wiener:peter

![image](https://github.com/user-attachments/assets/4dab51c2-4b17-4b38-9d19-90b814c918bf)


First, let's see how where we can find the GUIDs by logging into wiener's account. Once, logged in we can view and edit the GUID from the url:

```
https://0a5a007703e20690812e1b600057000d.web-security-academy.net/my-account?id=84b2879d-aa64-452f-95ed-c9fcf727ad39
```
8f5f04c0-7408-4060-b296-857399e86fa5
So now we just need to figure out how to determine other user GUIDs.

These are disclosed in the blogs and comments.

For example, when we go to a post from user named "administrator" we see their GUID in the url:

```
https://0a5a007703e20690812e1b600057000d.web-security-academy.net/blogs?userId=8f5f04c0-7408-4060-b296-857399e86fa5
```

Next, let's go to one of carlos posts and get his api key using this logic.

Carlos's blog url:

```
https://0a5a007703e20690812e1b600057000d.web-security-academy.net/blogs?userId=7fa6be95-90c2-402a-bffd-bd52849d91f8
```

Carlos's API key:

![image](https://github.com/user-attachments/assets/923a1108-4cae-4ea9-be74-fe41755f4ae0)

## Horizontal to vertical privilege escalation

Often, a horizontal privilege escalation attack can be turned into a vertical privilege escalation, by compromising a more privileged user. For example, a horizontal escalation might allow an attacker to reset or capture the password belonging to another user. If the attacker targets an administrative user and compromises their account, then they can gain administrative access and so perform vertical privilege escalation.

An attacker might be able to gain access to another user's account page using the parameter tampering technique already described for horizontal privilege escalation:

```
https://insecure-website.com/myaccount?id=456
```

If the target user is an application administrator, then the attacker will gain access to an administrative account page. This page might disclose the administrator's password or provide a means of changing it, or might provide direct access to privileged functionality.

#### Lab:  User ID controlled by request parameter with password disclosure

This lab has user account page that contains the current user's existing password, prefilled in a masked input.

To solve the lab, retrieve the administrator's password, then use it to delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Once we log into wiener's account and inspect elements, we can see the masked password in plaintext. From here let's try accessing the administrator account with a simple misconfigured id parameter:

```
https://0afb00460301804faee2a230003c0071.web-security-academy.net/my-account?id=administrator
```

This logs us in to the administrator account:

![image](https://github.com/user-attachments/assets/2c9a2d71-4b48-4a3e-b1d6-5bceabf2b8c6)

We can find the password for administrator and it is: rgc85kbrbpot31351qe2

Once we login to administrator we have the option to view admin panel and once again say bye bye to poor carlos to solve the lab.
