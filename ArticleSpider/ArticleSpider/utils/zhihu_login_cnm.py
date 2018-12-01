from bs4 import BeautifulSoup
import requests

url = 'https://www.zhihu.com/explore'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36',
    'cookies':'zap=1d5a9bec-5c04-4fb0-b93c-68335961df3b; d_c0="AEDoruszWg6PTs_aRT1l3ReB66LkzH0XNIo=|1539351577"; _xsrf=keC74qVbmxajv2gABmK6RnLJyGaSlFzT; tst=r; q_c1=e25e7b6592d44aeb9ef4f7db7f3d5b42|1540290795000|1540290795000; l_n_c=1; n_c=1; l_cap_id="ODViY2ZiMjRjN2I2NDEzZjliNGQxNjliOTIzOWE1NTk=|1540456525|1307e9d9b5d6c4f6fe1c7b4b133cafa47e6ac17e"; r_cap_id="MmQ3ODYwOTI3NGFhNDE3YWIwZDJmNTA3MDc0NzRmMTU=|1540456525|15a2e77f7b2c72ab2b0a06b7ef91d4d787266430"; cap_id="ZjdmNjdmNjA1NDQ3NGRkYjg0ZjZkNmI0MjJlM2IwY2E=|1540456525|e9efc1e48520ae294a412e305d8836cf4a0afe08"; capsion_ticket="2|1:0|10:1540456731|14:capsion_ticket|44:ZTkyZWVjYjA0OTY3NDc0NDgyNDJhZjQxMDczNWU2ZWU=|379d8f144faeff7e4757ea4614ca7d6755a6bec972e77b81563c0e992c67a36b"; z_c0="2|1:0|10:1540456736|4:z_c0|92:Mi4xbWRDbEFnQUFBQUFBUU9pdTZ6TmFEaVlBQUFCZ0FsVk5JTS0tWEFDWEYtd1I2eXdNYk1HSXd3LU8yREhVMGdfN0NR|bccec55392a6f715ad361d8cc1c7a8feb4b8c9cef15aa0ec4b36944bed28cb53"; tgw_l7_route=860ecf76daf7b83f5a2f2dc22dccf049'
           }

response = requests.get(url, headers=headers)
with open('cnm.html', 'wb') as f:
    f.write(response.text.encode('utf-8'))
    f.close()
soup = BeautifulSoup(response.text, 'lxml')
print(soup.prettify())