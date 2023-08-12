import json
import re
import requests
import sys
import urllib.request


SERVER_BASE_LIEBLI = '771|EU|1|Global Server - Europe - Liebli'
SERVER_BASE_TILASHA = '771|EU|2|Global Server - Europe - Tilasha'
SERVER_BASE_NEPHTHYS = '771|EU|1|Global Server - Japan  -  Nephthys'
SERVER_BASE_TIANA = '771|JP|4|Global Server - Japan - Tiana'
SERVER_BASE_ARIEL = '771|SEA|5|Global Server - Asia - Ariel'
SERVER_BASE_VERDEHILE = '771|SEA|6|Global Server - Asia - Verdehile'
SERVER_BASE_LUPINUS = '771|SEA|7|Global Server - Asia - Lupinus'
SERVER_BASE_KATARINA = '771|US|8|North America Eastern Server - Katarina'
SERVER_BASE_TAOR = '771|US|9|North America Eastern Server - Taor'
SERVER_BASE_VELAJUEL = '771|US|10|North America Eastern Server - Velajuel'
SERVER_BASE_ANAVEL = '771|US|11|North America Western Server - Anavel'

ServerTAB=[SERVER_BASE_LIEBLI,SERVER_BASE_TILASHA,SERVER_BASE_NEPHTHYS,SERVER_BASE_TIANA,SERVER_BASE_ARIEL,SERVER_BASE_VERDEHILE,SERVER_BASE_LUPINUS,SERVER_BASE_KATARINA,SERVER_BASE_TAOR,SERVER_BASE_VELAJUEL,SERVER_BASE_ANAVEL]
if __name__ == '__main__':
    print('Choose server: \n1=LIEBLI\n2=TILASHA\n3=NEPHTHYS\n4=TIANA\n5=ARIEL\n6=VERDEHILE\n7=LUPINUS\n8=KATARINA\n9=TAOR\n10=VELAJUEL\n11=ANAVEL')
    server = int(input("Input Server: "))
    cs_code = input("CS_code: ")



    try:
        open('coupons.txt', 'r')
        with open('coupons.txt', 'r') as f:
            lines = f.readlines()
            coupons = [line.strip() for line in lines]
    except FileNotFoundError:
        print('Coupons.txt is not found! redownloading it')
        url = 'https://gitee.com/nsbcgwdgcshstz/summoners-war-chronicles-coupon-exchange/raw/master/coupons.txt'
        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8') 
        coupons = data.split('\r\n') 

    if server <12 and  0<server:
        serverFullName = ServerTAB[server]
    else:
        print('Server not selected!')
        sys.exit(1)

    headers = {
        'accept-language': 'en-US,en;q=0.9'
    }
    response = requests.get('https://coupon.withhive.com/771', headers=headers)
    pattern = r"'Page-Key': '(.+)'"
    matches = re.findall(pattern, response.text)
    pageKey = matches[0] if matches else ''

    if not pageKey:
        print('Failure Pagekey!(Report it on github)')
        sys.exit(1)

    print(f'Initialization PageKey={pageKey}')

    for coupon in coupons:
        data = {
            "language": "en",
            "server": serverFullName,
            "cs_code": cs_code,
            "coupon": coupon,
            "additional_info": pageKey
        }
        headers = {
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'page-key': pageKey
        }

        response = requests.post('https://coupon.withhive.com/tp/coupon/use',
                                 headers=headers, data=json.dumps(data))
        result = response.json()
        print(f"{cs_code} - {server} - {coupon} - {result['msg']}")

    input(f'End!!!')
