# Synopsis
Script to scrape website *www.bazos.sk*.

# Hot to use
1. Download the project from GitHub.
2. Run *scripts\createVenv.ps1* to create a virtual envirnment.
3. Run *scripts\installRequirements.ps1* to install all necessary packages.
4. Input the filter link in *config\config_PROD.ini*.
5. Run *main.py*, ideally in Visual Studio Code. Input argument should be the name of config file.
6. Find the exported data in *data* folder.

# Directory struture
*config* - contains only config files. The default that is automatically read is named *config.ini*.  
*data* - files used during run of the script.
*logs* - all log files will be stored here.  
*scripts* - contains "helper" scripts to build virutal environment and install requirements.  
*src* - *.py* files should be stored here.

# Disclaimer
Before using the script check the Terms & Conditions of the website. Do not use if you do not have the permissions of the owner of the website. If you do not have the permissions, use it strictly for informational and educational purposes only.

More at [martinautomates.com](https://www.martinautomates.com)