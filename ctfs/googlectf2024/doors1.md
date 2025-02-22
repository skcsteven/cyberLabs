# Doors Every (Part I) - google ctf - web

A security update about profiles? There's no way there could be a flag there. Unless?

https://secuweb-web.2024-bq.ctfcompetition.com/

---

Theres a login page

---


First I login to the guest account to check out the page. It seems to be a simple blog.

There are some interesting (useless) blog posts, a profile page, and a secret message function that is locked for the guest account.

The solution lies in a hint on the home page of guest:

---

After this I go to the profile page for guest and notice that it is at the /profile/guest endpoint, I test /profile/admin and there the flag is!