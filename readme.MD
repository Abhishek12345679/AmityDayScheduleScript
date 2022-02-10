# Amity Scheduler

Note: This will only work for Amity University Students, i.e., it works if you have amizone and know your username and passsword, and your amity.edu (university email address) and password.

## run via launchd

To bootstrap the process:
```bash
sudo launchctl bootstrap gui/<userid> <plist file>
```

To get the userid run:
```bash
id -u <username>
```

To start the process:
```bash
sudo launchctl kickstart -k gui/<userid>/<plist file without the .plist>
```

## TODO

- [ ] Add Support for Whatsapp integration

## How to Use : 

1. Get your User-id (Enrollment Number) and Password, and your `<yourname>.s.amity.edu` email address and its password you can find it in your amizone after logging in like this:

![image](/Assets/usernamepass.jpg)

<!-- <img src="AmityDayScheduleScript/../2020-12-12_01:41.png" style="width:1500px;height:800px;"> -->

1. Fork and clone this repo or simply download this repo and open script.py and follow the instructions in the comments.

2. create a cronjob using `crontab -e`
