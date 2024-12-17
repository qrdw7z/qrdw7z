from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time
import csv

# Firefox ayarları
options = Options()
options.headless = False  # Tarayıcıyı başsız (headless) çalıştırmak istemiyorsanız False yapın

# Firefox WebDriver ayarları
service = Service(GeckoDriverManager().install())

# Firefox tarayıcısını başlatma
driver = webdriver.Firefox(service=service, options=options)

# URL'yi ziyaret et
url = 'https://allestock.com/collections/tofass'  # Burada kendi URL'nizi kullanabilirsiniz
driver.get(url)

# Sayfa tam olarak yüklendikten sonra 5 saniye bekle
time.sleep(5)

# Ürün başlıklarını ve fiyatlarını çekme
try:
    product_names = driver.find_elements(By.CSS_SELECTOR, '.product-title')
    product_prices = driver.find_elements(By.CSS_SELECTOR, '.product-price')

    # Ürün verilerini CSV'ye yazma
    if product_names and product_prices:
        with open('shopify_products.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Product Name', 'Price'])  # Başlık satırını yaz
            for name, price in zip(product_names, product_prices):
                writer.writerow([name.text, price.text])
        print('Ürünler başarıyla kaydedildi!')
    else:
        print('Ürünler bulunamadı! HTML yapısını kontrol edin.')

except Exception as e:
    print(f"Veri çekme sırasında hata: {e}")

# Tarayıcıyı kapat
driver.quit()
