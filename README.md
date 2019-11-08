This script automates the process of checking the
balance and overdue balance of users in spotify family plan.

It uses Google drive and google sheet APIs to get access and check the spotify balance
file. It fills out the charge for current month and checks if there are users with
overdue balance; if there such users the script sends email to users with their negative balance.
I use SMTP with SSL (Secure Socket Layer) for email broadcast.

The script can also update the credit for users : run ./getData.py "name of the user as it appears in googledoc" "amount of credit"

For automatic run of the script I am using CRONTAB - job scheduler for unix-like systems.
