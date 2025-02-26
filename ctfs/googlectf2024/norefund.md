# no refund - google ctf - web


When requesting a refund, two parameters are used for the POST request, "reason" and "ticket_id".


Navigating the source for the page, you can see the id for each of the trips.

The solution lies in refunding the trip that is unrefundable (or supposed to be).

Modified burp request to capture flag:


![flag](https://github.com/user-attachments/assets/8896ae2a-2934-4be8-a19e-7c92c2713819)

