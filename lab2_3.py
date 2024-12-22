import json
from collections import Counter
from bs4 import BeautifulSoup

# Access log faylını oxuyuruq
with open("access_log.txt", "r") as file:
    access_log = file.readlines()

# Qara siyahı faylını oxuyuruq
with open("threat_feed.html", "r") as file:
    soup = BeautifulSoup(file, "html.parser")

# Qara siyahıdakı domenləri əldə edirik
blacklisted_domains = [li.text.strip() for li in soup.find_all("li")]

# Access log-dan URL və status kodlarını çıxarırıq
log_data = []
for line in access_log:
    parts = line.split()
    ip = parts[0]
    url = parts[6]
    status_code = parts[8]
    log_data.append({"ip": ip, "url": url, "status": status_code})

# Qara siyahı ilə uyğun gələn URL-ləri tapırıq
alerts = []
for entry in log_data:
    for domain in blacklisted_domains:
        if domain in entry["url"]:
            alerts.append(entry)

# Alert məlumatlarını JSON formatında saxlayırıq
with open("alert.json", "w") as alert_file:
    json.dump(alerts, alert_file, indent=4)

# Xülasə hesabatını hazırlayırıq
summary = {
    "total_requests": len(log_data),
    "total_alerts": len(alerts),
    "unique_blacklisted_domains": len(set([entry["url"] for entry in alerts])),
    "blacklisted_domain_counts": Counter([entry["url"] for entry in alerts]),
}

# Xülasə məlumatlarını JSON formatında saxlayırıq
with open("summary_report.json", "w") as summary_file:
    json.dump(summary, summary_file, indent=4)

print("JSON faylları uğurla yaradıldı!")
