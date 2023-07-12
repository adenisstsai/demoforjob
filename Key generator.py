from key_generator import key_generator
import ntplib
import time

c = ntplib.NTPClient() 
response = c.request('pool.ntp.org') 
ts = response.tx_time 
Key_date = time.strftime('%Y%m%d%H',time.localtime(ts)) 
key = key_generator.generate(seed = int(Key_date)+19831024+19910508)
print(key.get_key())