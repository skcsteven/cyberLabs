## Ben 10 - SRDNLEN CTF - WEB (50)

![login](https://github.com/user-attachments/assets/9aa9bc26-fd26-4cda-b51d-4be01dbf36ee)

This is a fun ben 10 themed challenge with multiple pages/routes:

1. Registering an account
2. resetting password
3. Viewing ben 10 forms!

![home](https://github.com/user-attachments/assets/e2437719-02d6-4c33-bb2b-901f6c65da9b)


We are provided source code for this challenge and the key file to analyze is app.py.

After analyzing the file, SQLi is ruled out because of the use of parametrized queries. But what is interesting is that each time an account is registered, an admin account is also created based on the new accounts username:

```
        admin_username = f"admin^{username}^{secrets.token_hex(5)}"
        admin_password = secrets.token_hex(8)
```

The admin_username then can be found on the home page of the logged in user from devtools.

All thats left is to figure out the password, right?

Wrong, we can make use of a logic error in the code for resetting a password. The reset password flow/methodology is below:

```
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Handle password reset."""
    if request.method == 'POST':
        username = request.form['username']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template('forgot_password.html', reset_token=reset_token)

        user = get_user_by_username(username)
        if not user:
            flash("User not found.", "error")
            return render_template('forgot_password.html', reset_token=reset_token)

        if not username.startswith('admin'):
            token = get_reset_token_for_user(username)
            if token and token[0] == reset_token:
                update_password(username, new_password)
                flash(f"Password reset successfully.", "success")
                return redirect(url_for('login'))
            else:
                flash("Invalid reset token for user.", "error")
        else:
            username = username.split('^')[1]
            token = get_reset_token_for_user(username)
            if token and token[0] == reset_token:
                update_password(request.form['username'], new_password)
                flash(f"Password reset successfully.", "success")
                return redirect(url_for('login'))
            else:
                flash("Invalid reset token for user.", "error")

    return render_template('forgot_password.html', reset_token=request.args.get('token'))
```

If we look carefully at the block that checks if the username starts with admin "if not username.startswith('admin')" and the second to last else statement block, we see a vulnerability. When we get to this page routed by the /reset_password page, we are given a token if we enter a legitimate user account that isn't an admin. But with the logic in the else statement, if we simply use that token with the admin username that is created and found earlier, we can change the admin password to whatever we want.

The specific lines to look at are in the else statement mentioned above. If we enter the admin username, the application splits it up based on the ^ delimiter and gets the normal user account username which is in position 1 after the split function. With this username, it checks if the token is legitimate. But the line "update_password(request.form['username'], new_password)" tells us that the password will be updated for the entered username rather than the username that was just acquired from the split function and matched to the token. So we simply have to enter our newly created admin username, token (should already be filled in) and a new password of our choosing.

With this you can log into the admin account and view the flag which is hidden behind the 10th ben 10 image:

![flag](https://github.com/user-attachments/assets/125b73bb-44a7-40bb-8863-ae4be74bcc73)
