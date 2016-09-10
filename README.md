# OWASP ZAP Example

This was done using Ubuntu 14.04.4 LTS, Google Chorme Version 51.0.2704.103 (64-bit), OWASP ZAP v2.5.0.

## Setting up
### Install and run ZAP
* Downloaded from https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project
```bash
tar -xf ZAP_2.5.0_Linux.tar.gz
cd ZAP_2.5.0
./zap.sh
```

### Configure SSL Certificates
#### In ZAP
* Tools > Options > Dynamic SSL Certificates.
* Clicked save.

#### In Chrome
I had problems trying to add the ZAP certificate in Firefox, neither [adding the certificate in
Firefox's settings](https://2buntu.com/articles/1517/adding-ssl-certificates-from-owasp-zap-a-visual-walkthrough/) 
nor adding the certificate using ubuntu's update-ca-certificates seemed to work for me.
I didn't spend much time looking into this but tried Chrome instead.
* Started chrome with, `google-chrome-stable --proxy-server=localhost:8080`
* settings > + show advanced options > click Manage certificates button (under HTTPS/SSL)
* selected 'Autorities' tab and clicked import
* selected owasp certificate and clicked open
* checked all 'Trust this certificate for ...' check boxes
* clicked 'ok'
* I could now see the OWASP certificate in the list
* clicked 'finished'
* navigated to a https site in chrome to test this all worked

## Quick start
I created a simple Django web site and ran it on http://localhost:1911/ so that I could test against this.
In ZAP GUI: 
* I selected the 'Quick Start' tab,
* entered my site's address (http://localhost:1911/),
* and clicked 'Attack'

Information about the Attack is shown in the bottom pane of the ZAP GUI, e.g.
* pages crawled
* vulnerabilities found

TODO: 
* Add login form
* Add robots.txt and sitemap.xml to help the spider.
* Look through current vulnerabilities with runserver.
* Run with wsgi and apache and check vulnerabilities.
* Look into configuring a spider.
* Look into AJAX spider.
* Drive yourself using ZAP proxy, which will inspect the requests and responses
and record vulnerabilities (could drive with Selenium?).
* Try out Active scanning.
