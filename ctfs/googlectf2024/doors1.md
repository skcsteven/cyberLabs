# Doors Every (Part I) - google ctf - web

A security update about profiles? There's no way there could be a flag there. Unless?

https://secuweb-web.2024-bq.ctfcompetition.com/

![home](https://github.com/user-attachments/assets/e56b783c-3d2f-4385-aab0-e937381b852f)


Theres a login page

![login](https://github.com/user-attachments/assets/f6deaa24-03d7-48a3-b47f-d267dedd14b2)



First I login to the guest account to check out the page. It seems to be a simple blog.

There are some interesting (useless) blog posts, a profile page, and a secret message function that is locked for the guest account.

The solution lies in a hint on the home page of guest:

![secUpdate](https://github.com/user-attachments/assets/60fa6f73-9743-4c1d-92a6-221f7617b2a7)


After this I go to the profile page for guest and notice that it is at the /profile/guest endpoint, I test /profile/admin and there the flag is!
