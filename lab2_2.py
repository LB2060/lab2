from bs4 import BeautifulSoup
import re

# a. Qara siyahıya alınmış domenləri silmək
with open("threat_feed.html", "r") as file:
    soup = BeautifulSoup(file, "html.parser")

# Qara siyahıdakı domenlərin siyahısını hazırlayırıq
blacklisted_domains = [li.text for li in soup.find_all("li")]

# Qara siyahıdan domenləri silirik
for li in soup.find_all("li"):
    li.decompose()

# HTML sənədini yenidən yazırıq
with open("updated_threat_feed.html", "w") as file:
    file.write(str(soup))

print("Yenilənmiş threat feed: updated_threat_feed.html faylında saxlanıldı.")

# b. Jurnal faylındakı URL-ləri qara siyahı ilə müqayisə etmək
with open("access_log.txt", "r") as log_file:
    log_data = log_file.read()

# Regex ilə URL-ləri çıxarırıq
pattern = r'"(?:GET|POST) (http[s]?:\/\/[^\s]+) HTTP\/[0-9.]+"'
urls_in_logs = re.findall(pattern, log_data)

# Qara siyahı ilə uyğunluğu yoxlayırıq
matching_urls = [url for url in urls_in_logs if any(domain in url for domain in blacklisted_domains)]

# Nəticələri çap edirik
if matching_urls:
    print("Qara siyahıya uyğun gələn URL-lər tapıldı:")
    for url in matching_urls:
        print(url)
else:
    print("Jurnal faylında qara siyahıya uyğun gələn URL yoxdur.")
