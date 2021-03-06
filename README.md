# OWASP ZAP Example

This was done using Ubuntu 14.04.4 LTS, Google Chrome Version 51.0.2704.103 (64-bit), OWASP ZAP v2.5.0.

## Introduction
The [OWASP Zed Attack Proxy (ZAP)](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project) is a
penetration testing tool for finding vulnerabilities in web applications.

Once ZAP is installed the steps for finding vulnerabilites are,
1. proxy browser based tests (e.g. using Selenium) through ZAP in order to
   explore the application in a realistic way,
3. use the spiders to discover content not covered by regression tests,
4. run the active scanner to attack the application,
5. read the alerts found and report any new vulnerabilities.

## Setting up
### Install and run ZAP
* Downloaded from https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project
```bash
tar -xf ZAP_2.5.0_Linux.tar.gz
cd ZAP_2.5.0
./zap.sh
```

### Configure SSL Certificates
This is necessary if the website to be tested uses https.

#### In ZAP
* Tools > Options > Dynamic SSL Certificates.
* Clicked save (make a note of the location for the next step).

#### In Chrome
I had problems trying to add the ZAP certificate in Firefox, neither [adding the certificate in
Firefox's settings](https://2buntu.com/articles/1517/adding-ssl-certificates-from-owasp-zap-a-visual-walkthrough/) 
nor adding the certificate using ubuntu's update-ca-certificates seemed to work for me.
I didn't spend much time looking into this but tried Chrome instead.
* Started chrome with, `google-chrome-stable --proxy-server=localhost:8080`,
* settings > + show advanced options > click Manage certificates button (under HTTPS/SSL),
* selected 'Authorities' tab and clicked import,
* selected owasp certificate and clicked open,
* checked all 'Trust this certificate for ...' check boxes,
* clicked 'OK',
* I could now see the OWASP certificate in the list,
* clicked 'finished',
* navigated to a https site in chrome to test this all worked.

## Quick start

You can use this to do a quick scan of a site without the need for running the
functional tests and spidering the site.  As users aren't configured it will not
cover as much of the site as the scan shown later.
I created a simple Django web site and ran it on http://localhost:8081/ so that I could test against this.
In ZAP GUI:
* I selected the 'Quick Start' tab,
* entered my site's address (http://localhost:8081/),
* and clicked 'Attack'

Information about the Attack is shown in the bottom pane of the ZAP GUI, e.g.
* pages crawled
* vulnerabilities found

## Full Scan (manual)
## Run functional tests through ZAP
* In ZAP, File > New Session,
* Run tests using port 8081 (make sure the Django server that was started
  earlier has been stopped)

```bash
DJANGO_LIVE_TEST_SERVER_ADDRESS=localhost:8081 python manage.py test
```
* Urls from the web server that was browser during tests now appear in the Sites
  tree. 

![alt text](http://tdpreece.github.io/assets/img/owasp_zap_example/zap-scan-after-fts.png "After running functional tests through ZAP.")

The PhantomJS browser will not use proxy if proxy is running on 127.0.1.1 so I used Firefox for this
example, see: https://github.com/ariya/phantomjs/issues/11342, https://github.com/ariya/phantomjs/issues/12407.
I have successfully used PhantomsJS with ZAP by running ZAP on a separate host.

## Define a context
* right-click on folder in 'Sites' > 'Include context' > 'Default context' > click 'OK' ,

## Configure a user
* Check that detection of anti CSRF tokens in enabled: settings >
  Anti CSRF Tokens, checked name of token that matches the one I was using
  (csrfmiddlewaretoken).

### Manual
* In 'Session Management' check that Cookie-based Session Management is selected.
* In 'Authentication', select 'Form-based Authentication',
    * enter "http://localhost:8081/login/" into 'Login Form Targert Url' field.
    * enter "username=y&password=x" into 'Login Request POST Data' field
    * select "username" in 'Username' select box
    * select "password" in 'Password' select box
    * Add logged in/ logged out indicators (`\QLogged in\E` and `\QLogged out\E`)
* In Users, click 'Add' and enter User Name: john, username: john, password, johnpassword

### Automatic
* Open up 'Sites' and 'http://localhost:8081' > right-click on 'POST:login...' > 'Flag as context' > 'Form-based Auth Login Request'
* Select username and password fields
* Add logged in/ logged out indicators (`\QLogged in\E` and `\QLogged out\E`)
   
## Spider website
* Start up Django server
```bash
python manage.py runserver localhost:8081
```
* Open up 'Sites' and 'http://localhost:8081', right-click on 'http://localhost:8081' > Spider,
* select the user that was used to run the tests (John),
* click 'Start Scan' button.
* New urls that weren't accessed during the functional tests may now be added to the Site tree.

![alt text](http://tdpreece.github.io/assets/img/owasp_zap_example/zap-scan-after-spider.png "After running Spider")

## Attack website
* Open up 'Sites' and 'http://localhost:8081', right-click on 'http://localhost:8081' > Active Scan,
* select the user that was used to run the tests (John),
* click 'Start Scan' button.
* The alerts tab at the bottom of the gui shows a list of possible security
  vulnerabilities.

![alt text](http://tdpreece.github.io/assets/img/owasp_zap_example/zap-scan-xss-vulnerability.png "XSS vulnerability found by scan")

# Extensions
## AJAX Spider
The standard spider will not find links that are dynamically generated via javascript.  For this case
the AJAX spider will need to be used.

## Automate
By default ZAP runs on port 8080.  If you open http://localhost:8080 in a browser you'll be able
to browse ZAP's REST API.  There is also a Python library for working with the REST SPI: 
https://github.com/zaproxy/zaproxy/wiki/ApiPython

```pyhthon
# Gist of a scan in a LiveServerTestCase
class TestLogin(StaticLiveServerTestCase):
    ...
    
    
    def test_scan(self):
        # At this point have a dev server running and a browser.
        # Can set up the Zap session, run the spider and scan using
        # the api.
```

## Wrap scans in BDD
Though the report given by ZAP is very clear you may want to only test regressions, 
maintain a list of known false positives and/or have more fine grained scans.
This can be done quite nicely with the use of a BDD style testing framework
(e.g. [Behave for Python](http://pythonhosted.org/behave/)).
This is an example in Java: https://github.com/continuumsecurity/bdd-security/blob/master/src/test/resources/features/passive_scan.feature.

## Live Threat Model
Results of the scans could be fed back into a live threat modelling tool (see [Irius Risk](https://www.continuumsecurity.net/)).

# References
YouTube video on ["ZAP Tutorial - Authentication, Session and Users Management" by Cosmin Stefan](https://www.youtube.com/watch?v=cR4gw-cPZOA)

