# BloxPayload
BloxPayload: Roblox Account Hacking Tool. Systematically brute-force millions of Roblox accounts to find credentials fast. The ultimate key-finder for the Roblox ecosystem. Get instant access!

## How It Works
BloxPayload targets the Roblox reset flow. It first initiates a password/account reset request, triggering the 6-digit verification code. The tool then systematically cycles through all possible 6-digit combinations (000000 to 999999) until it finds the correct code, instantly granting access to the target account.

Simply put, BloxPayload hacks the 'Forgot Password' process. It automatically tries every possible 6-digit code that Roblox generates during the reset, making it a highly efficient automated guessing game to unlock the account.

## How To Set Up
To install it on Kali Linux
Install these package first
```
pip install selenium
pip install selenium webdriver-manager
```

Now download this github to your Kali Linux
```
git clone https://github.com/yuhertz/BloxPayload
cd BloxPayload
```

Now download the chrome driver for it to run
Go to https://googlechromelabs.github.io/chrome-for-testing/ and download version 151.0.7874.0
After installing open the file you will see "chromedriver" move that to this file.

Before Running, you need to modify the code in main.py
change username123 to the target username
change example@gmail.com to any email you want, changing it to the email related to target email is recommended


To run, type this command
```
python3 main.py
```

