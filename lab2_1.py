import re
from collections import Counter
import csv

with open("access_log.txt", "r") as file:
    access_file = file.read()
# Regex ifadəsi ilə URL-ləri və status kodlarını çıxarırıq
pattern = r'"(?:GET|POST) (http[s]?:\/\/[^\s]+) HTTP\/[0-9.]+" (\d{3})'
matches = re.findall(pattern, access_file)

# 404 status kodu ilə URL-ləri süzgəcdən keçirmək
url_with_404 = [url for url, status in matches if status == "404"]

# URL-lərin sayını hesablamaq
url_count = Counter(url_with_404)

# b. 404 xəta ilə URL-ləri CSV faylında saxlayırıq
with open("malware_candidates.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["URL", "404-lərin sayı"])  # Başlıq sütunları
    for url, count in url_count.items():
        csv_writer.writerow([url, count])
with open("url_status_report.txt", "w") as report_file:
    report_file.write("URL və HTTP Status Kodları:\n")
    for url, status in matches:
        report_file.write(f"{url} - {status}\n")
# Nəticələri çap edirik
print("404 Status kodlu URL-lər və sayları:")
for url, count in url_count.items():
    print(f"{url}: {count}")
    
print("Nəticələr müvəffəqiyyətlə yazıldı:")
print("- URL-lər və status kodları: url_status_report.txt")
print("- 404-lər və sayları: malware_candidates.csv")