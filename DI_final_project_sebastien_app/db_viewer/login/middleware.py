import datetime
from .models import IPData
from ipaddress import ip_address, IPv4Address
import requests
from datetime import datetime



class IPDataMiddleware:
     def __init__(self, get_response):
        self.get_response = get_response

     def __call__(self, request):
        response = self.get_response(request)

        ip = self.get_client_ip()

        if ip is not None and not self.is_private_ip(ip) and not self.is_loopback_ip(ip):
            ip_data, created = IPData.objects.get_or_create(ip_address=ip)
            if not created:
                ip_data.session_start = datetime.now()
                ip_data.save()

            # Get org and country information using IPWHOIS API
            r = requests.get(f'http://ipwhois.app/json/{ip}')
            if r.status_code == 200:
                data = r.json()
                ip_data.org = data['org']
                ip_data.country = data['country']
                ip_data.save()

        return response

     def get_client_ip(self):
        r = requests.get('https://api.ipify.org?format=json')
        if r.status_code == 200:
            return r.json()['ip']
        else:
            return None

     def is_private_ip(self, ip):
        return ip_address(ip).is_private

     def is_loopback_ip(self, ip):
        return ip_address(ip) == IPv4Address('127.0.0.1')