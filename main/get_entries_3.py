import requests
import json
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of User Agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Vivaldi/4.0.2312.38",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Vivaldi/4.0.2312.38"
    # Add more user agents as needed
]

# List of Proxy Servers (if available)
PROXIES = [
    # "http://username:password@proxy_ip:proxy_port",  # Format for proxy with authentication
    # "http://proxy_ip:proxy_port",                   # Format for proxy without authentication
    # Add more proxies if available
]

# Load the brands and their IDs from the JSON file
with open("/Users/zeinaddinzurgambayev/Desktop/parser/nurbek/enries3.json", "r", encoding="utf-8") as json_file:
    brands = json.load(json_file)

# Base URL for the items API endpoint
base_url = "https://www.vinted.pl/api/v2/catalog/items"

# Initialize a dictionary to store the count of products for each brand
brand_entries_count = {}

# Function to send a single GET request
def send_request(session, headers, params, proxy=None):
    try:
        # Use proxy if available
        response = session.get(base_url, headers=headers, params=params, proxies={"http": proxy, "https": None} if proxy else None)
        if response.status_code == 200:
            data = response.json()
            brand_name = data.get("dominant_brand", {}).get("title", "")
            total_entries = data.get("pagination", {}).get("total_entries", 0)
            item_count_historical = data.get("dominant_brand", {}).get("item_count", 0)
            final = {"total_entries": total_entries, "item_count_historical": item_count_historical}
            brand_entries_count[brand_name] = final
            print(f"Total entries for brand: {brand_name} ", total_entries, "Item count historical: ", item_count_historical)
            with open("count_brand_entries_third.json", "w", encoding="utf-8") as json_file:
                json.dump(brand_entries_count, json_file, ensure_ascii=False, indent=4)
            print(f"Brand with id {params['brand_ids']} seved to count_brand_entries_third.json")
        elif response.status_code == 429:
            print("Too many requests. Trying again...")
            send_request(session, headers, params, proxy=None)
        else:
            print(f"Brand with id {params['brand_ids']} not found")
            print(response.status_code)
    except requests.RequestException as e:
        print(f"Request failed: {e}")

# Function to handle multiple requests concurrently
def send_requests_concurrently(total_requests, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        with requests.Session() as session:
            futures = []
            for brand_id in brands.keys():
                user_agent = random.choice(USER_AGENTS)
                proxy = random.choice(PROXIES) if PROXIES else None

                headers = {
                    "Cookie":"v_udt=REhRL2ptdHNHTGwrdGVEeEt0Mmt4Q3RFL0VIYi0td0hzTDMySEZIWmduVXhPaC0tMXJLdFV4SCs3dFlvSnlVcnhkMTNXZz09; anon_id=152fb059-d70c-4127-ba66-1074ea9a2db8; domain_selected=true; ab.optOut=This-cookie-will-expire-in-2025; eupubconsent-v2=CQET0DgQET0DgAcABBENBFFsAP_gAAAAAChQKYtV_G__bXlj8X71aftkeY1f9_h7rsQxBhfJk-4FyLvW_JwX32EzNA36pqYKmRIAu3bBIQNlGIDUTUCgaogVryDMak2coTNKJ6BkiFMRe2cYCF5vmwlD-QKY5vr_91d52R-t7dr83dzyz4VHv3a5_2a1WJCdA58tDfv9bROb-9IOd_x8v4v8_FgAAAAAABAAAAAAAAAAAAAAAAAAABcAAAAAAAAOB_--AAAAoJBAAAQAAuACgAKgAcAA8ACCAGQAagA8ACIAEwAKoAbwA9AB-AEJAIYAiQBHACWAE0AMOAZQBlgDZAHfAPYA-IB9gH6AQAAikBFwEYAI0AUEAqABVwC5gGKANEAbQA3ABxAEOgJEATsAocBR4CkQFsALkAXeAvMBhoDJAGTgMuAZzA1gDWQGxgNvAbqA4IByYDlwHjgPaAhCBC8IAdAAcACQAc4BBwCfgI9ASKAlYBNoCnwFhALyAYgAxaBkIGRgNGAamA2gBtwDdIHkgeUA-QB-4EBAIGQQRBBMCDAEKwIXDgGIACIAHAAeABcAEgAPwA0ADnAHcAQCAg4CEAERAJ-AVAAvQB0gEIAI9ASKAlYBMQCZQE2gKQAUmArsBagC6AGIAMWAZCAyYBowDTQGpgNeAbQA2wBtwDj4HOgc_A8kDygHxAPtgfsB-4EDwIIgQYAg2BCsdBKAAXABQAFQAOAAgABdADIANQAeABEACYAFWALgAugBiADeAHoAP0AhgCJAEsAJoAUYAwwBlADRAGyAO8Ae0A-wD9AH_ARQBGACggFXALEAXMAvIBigDaAG4AOIAdQBDoCLwEiAJkATsAocBR4CmgFWALFgWwBbIC4AFyALtAXeAvMBfQDDQGPAMkAZOAyqBlgGXAM5AaqA1gBt4DdQHFgOTAcuA8cB7QD6wIAgQtIAEwAEABoAHOAWIBHoCbQFJgLyAamA2wBtwDn4HkgeUA-IB-wEDwIMAQbAhWQgPAALAAoAC4AKoAXAAxABvAD0AI4Ad4A_wCKAEpAKCAVcAuYBigDaAHUAU0AsUBaIC4AFyAMnAZyA1UB44EKAIWkoEIACAAFgAUAA4ADwAIgATAAqgBcADFAIYAiQBHACjAGyAO8AfgBVwDFAHUAQ6Ai8BIgCjwFigLYAXmAycBlgDOQGsANvAe0BA8kAPAAuAO4AgABUAEegJFASsAm0BSYDFgG5APKAfuBBECDBSBsAAuACgAKgAcABBADIANAAeABEACYAFIAKoAYgA_QCGAIkAUYAygBogDZAHfAPsA_QCLAEYAKCAVcAuYBeQDFAG0ANwAh0BF4CRAE7AKHAWKAtgBcAC5AF2gLzAX0Aw0BkgDJ4GWAZcAzmBrAGsgNvAbqA4IByYDxwHtAQhAhaUARAAXABIAI4Ac4A7gCAAEiALEAXUA14B2wD_gI9ASKAmIBNoCkAFPgK7AXQAvIBiwDJgGpgNeAeUA-KB-wH7gQMAgeBBMCDAEGwIVgA.f_wAAAAAAAAA; OTAdditionalConsentString=1~43.46.55.61.70.83.89.93.108.117.122.124.135.143.144.147.149.159.192.196.202.211.228.230.239.259.266.286.291.311.318.320.322.323.327.367.371.385.394.397.407.413.415.424.430.436.445.453.486.491.494.495.522.523.540.550.559.560.568.574.576.584.587.591.737.802.803.820.821.839.864.899.904.922.931.938.979.981.985.1003.1027.1031.1040.1046.1051.1053.1067.1092.1095.1097.1099.1107.1135.1143.1149.1152.1162.1166.1186.1188.1205.1215.1226.1227.1230.1252.1268.1270.1276.1284.1290.1301.1307.1312.1345.1356.1364.1375.1403.1415.1416.1421.1423.1440.1449.1455.1495.1512.1516.1525.1540.1548.1555.1558.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1659.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1782.1786.1800.1810.1825.1827.1832.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.1985.1987.2003.2008.2027.2035.2039.2047.2052.2056.2064.2068.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2135.2137.2140.2147.2150.2156.2166.2177.2183.2186.2205.2213.2216.2219.2220.2222.2225.2234.2253.2279.2282.2292.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2370.2376.2377.2387.2400.2403.2405.2407.2411.2414.2416.2418.2425.2440.2447.2461.2465.2468.2472.2477.2481.2484.2486.2488.2493.2498.2501.2510.2517.2526.2527.2532.2535.2542.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2596.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2636.2642.2643.2645.2646.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2687.2690.2695.2698.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2821.2822.2827.2830.2831.2834.2838.2839.2844.2846.2849.2850.2852.2854.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2916.2917.2918.2919.2920.2922.2923.2927.2929.2930.2931.2940.2941.2947.2949.2950.2956.2958.2961.2963.2964.2965.2966.2968.2973.2975.2979.2980.2981.2983.2985.2986.2987.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3025.3028.3034.3038.3043.3048.3052.3053.3055.3058.3059.3063.3066.3068.3070.3073.3074.3075.3076.3077.3089.3090.3093.3094.3095.3097.3099.3100.3106.3109.3112.3117.3119.3126.3127.3128.3130.3135.3136.3145.3150.3151.3154.3155.3163.3167.3172.3173.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3270.3272.3281.3288.3290.3292.3293.3296.3299.3300.3306.3307.3309.3314.3315.3316.3318.3324.3328.3330.3331.3531.3731.3831.4131.4531.4631.4731.4831.5231.6931.7235.7831.7931.8931.9731.10231.10631.10831.11031.11531.12831.13632.13731.14237.14332.15731.16831.16931.21233.23031.25731.25931.26031.26831.27731.27831.28031.28731.28831.29631.31631.32531.33631; _gcl_au=1.1.955176475.1725274794; _ga=GA1.1.1226875194.1725274795; _tt_enable_cookie=1; _ttp=F7TdDzRTNCKh_m55UK-TDJyq7r0; _fbp=fb.1.1725274795598.879842942944496429; _cc_id=a391c297d83499fc408165b09b87b6e7; panoramaId_expiry=1725879600350; panoramaId=50b9cf229383dc5e2c3eeb78ef4c185ca02cbccb838b9e6cb6b08832c17f367c; panoramaIdType=panoDevice; anonymous-locale=en-fr; v_sid=3c53827428fa6ffb1319aa8657bd4dfd; OptanonAlertBoxClosed=2024-09-02T18:32:47.794Z; viewport_size=812; cf_clearance=0sim1hsBf5GO3eSwd25jujVbukBdq.ejiRb3ca9edtw-1725316976-1.2.1.1-uw6ne3CbYiuC67yDan1eJUprS8GxSjKP943840PVuQS5qWOQudARUEx4hYFpOvPQVIzFqV0IOYu2k8uB_9MhQyII2BeKOBgsp39.bMJAledu4I9T8Br8CCuknX.Zc8gwFDoAG1UEWIDPmScoCJF3p03MSIZby8MlzHjuhoX155LoKzqRgkwcm_xsVE5FlJ0yQhfYoTaduCvjtf1zqP4xVZf5CFzqEznhTA80VBIlCIHOWNQXtqcIAeoQNJT3YXxlnvKJQzdJ9ucsG0odcPqXIz1u4_U1hsj8CufkAMEhASWpWG.p9ev16BTA5sxU2LSXql2.X_Dy8meYsdm26rJ905laCtOZIFZDp5RLS0YtTQmRnIzl08Akr9uRpYBhrZ6gtfL_wt5p1fe2FE5fTzakzw; _uetsid=c17119f0695911ef83c505f9358ddcb2; _uetvid=c1712210695911efb747a5a2a4475bbb; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Sep+03+2024+03%3A43%3A03+GMT%2B0500+(%D0%97%D0%B0%D0%BF%D0%B0%D0%B4%D0%BD%D1%8B%D0%B9+%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D1%82%D0%B0%D0%BD)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=152fb059-d70c-4127-ba66-1074ea9a2db8&interactionCount=6&hosts=&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CV2STACK42%3A1%2CC0015%3A1&landingPath=NotLandingPage&geolocation=KZ%3B71&AwaitingReconsent=false; cto_bidid=NYydbV8zWXUlMkJOZGg5eUdCbzdPcE03ZHNrY1pvbm5IMTI3UzRmQ0tJdkZuWEJlciUyQmNQakRIamFtSXhmeEE5bU5ic1VteFRMWXNldVVsJTJGdjFHSGo2NWdKWlpLTEU2Z2Y4Yk1BZXRuMnNPRSUyQlUyWHc3cSUyRjQ3eWw3ejB6WFFzNTUwbUtDdmJqM0tUYVNobWRpSCUyQkRqaERBSFRCSUElM0QlM0Q; cto_bundle=wFSMeV9hb0tHWEY1dW5UTnVPcTNyRURqaFdkcjZCR1BWSmFVTzJpVHJpdU40M0p3Snd2dVV0VnVsOHBJbGVJck9ZUWtKWFJpT0FmZGtRZ2glMkJsNks5TkNjN25VTE1zMDVHUWdZV1IzUEJyNThnVm1OUzZJSHBDRUV1JTJGcER5clBVT1VCVmRQRW5YVHdFS1lISUc3VFVFZFJsVjF3JTNEJTNE; datadome=MD0vo2MZ9CxI3QJ1LZy4cPcN~7CJcJTIGT8MzQZIqRZcUKaFZkrbPxHWUT2DTNynFiJzuXWAZ5fSeCl6wCmplRMr4nPSqkC0I2ScILWgQc_xm7d22NF0RrmeB_fRTYMT; _ga_ZJHK1N3D75=GS1.1.1725320477.8.0.1725320477.0.0.0; _ga_762HZ9XYEN=GS1.1.1725320477.8.0.1725320477.0.0.0; __gads=ID=7e855f4af8998040:T=1725301701:RT=1725320497:S=ALNI_MZFaY_a7YplnpAjnMABWlJSpuj2Hw; __eoi=ID=131c8353349f372d:T=1725301701:RT=1725320497:S=AA-AfjaYxa0y_JPsTobdROfdK4V3; __cf_bm=w6Awa8hUwEUZz6o0x_.44fnc5vBIn20FuS8WJqfAhbU-1725324838-1.0.1.1-biii8yZN8flsWpTuw8FDDoAzaNJTjCiR.Gn2gYBnlwttt5oie1K41Dpk0819mopW1q0XDaLyr47WkyeuOeDLW0liNH0n_inCw3J3DTpyslM; _vinted_fr_session=ZTBNZ00yVWxJL0hzSE9UMVRLc3Z6UWZjaFBMT3FjYzQ3Y3NKTEwvWGUwbC96ZGszaEtZSktXb3pHWWRQdkNndzVXcXVKamErWWJ3d2dkNE1KbEc2b0FJRHFabDBwa0dRcy9HM2dyRGJ1VmllOUZhbWpZdHgwa3NOeks4RGc1NmdKbElhRHV2dHpsTWhOeTdvblZNeDBWczBIdzR1ZU5ucG9LZmlvV2JTSFQzdTJyR0xzTHRaTWtjN0xJR243TlczTmpRSExaM3Z5eitZZzN6ZEpBRmMxVnJIRU5MS04ybWxUaHV0Mk9WdlNETFU3Q3ROS3RhRHJtc0krS1h1RWJGK0FYeldBV01ZRVhQNnBkd1d5WWVEamM0VDJ4T1V6OHkzSVRjdzgzN2ZVVHdJeU1vN0c5OXdLaUhZSVBhejdiS1FGdmV5d1dLVXhlUmhoNDgvem1iSm1SclA5LzZVbWdtd2JMamQ4cHNHb2NhR0NTbUFxVjM2WUduVXI0VHZyTVp4UjUzYjdaOTE2M2I1aXZSRkdXNHdMV1Y4MXQ1bk9vR0VVMUl4aHF1anlrOUcvS29XdnQ3T1NKWGpyeTJvRHlKdGJRV2JGbFQ4Q1RKVWJtaEJKeFJvY0l4Z0thbUR1bUZIbERiS1MzUENFQ0pEM1NmdmF4UTd1VHYvY1Y3Zno5M0c3Z1BWVHBXNGNCR21TZDF4b1ZwZzZ4QkFuSGtESmlqK3hCb0JUcUozOFdkS0wvNlhObCtMTXBNT1Rrdll6V3ZHS1hlREhXbnl0bGJRUDE1R2FLOHlCVUdZQlU1bGFEcm5YVzFrY0JoMklHbG40aGZWVDZWWWY5RFpKbzAyZGk2UURxRzBDbkM1MlFDSFczNy9FRzB6ZFdWSHBvWGhVT3RySVFVNGNaRjlhVTlxK0lpQ1B3YWRxS3V3TTZ0Y1FyTHdGcVVGVU4vNjAzMVRhZmtkeEhGWXlQeDZZNXRSSFJia0kzY3haWStQaDFSVTRwUW9iYytGV085ZGJCQThjQWxSOTJjbktFZmp3ZjVHNVg2U3hrRE9JTFVUYzNSRWJIek9aR2tOUGQxajVRWnV3cnk5M2duYUtDdi9lK2FGTXd3T0hOSTNmdTBIc25ZUzlvY1Y1eS9zUGwwbmhyYUhYZllDVTRha2IzMEhreDlJRUtXK21wdjBNalNzck5sZTd3RGNWT2dFNEgvZ20wbVVNS3YzUXN4aFlrN3ZmSUxLbGozKzRRRWttSnFvS0ZRcXhyMTlPbHk0bzJmcTR5Y3V3eHRGME9WMFFnWklOVHo0ZGwycElwS0p0a2p6SWdtVzF2VCtSaWJvNzZEeVBZbGNETjFHajVFa1VHSHBaRTRqNEJMekgzT2ErVlpETGF3NHFHMHIxWml4QWZPSEQ4dGI0VmhHMEJ0MkdoVUxQM0FkNFp2SXhIU0lPUWpQa2E4Z2tQcDBDMGkzc2I4TWFvbmlTRUtwY2x0aXRqV2lZbVhFZ014TnVhNUUyR1ZLRnZkeVNpYmJmTnB1ZGpyc2E2TVNwTmhZb2IzbHp3cXlCbWlWM2ZwNUJONmFKVUEzb0pJb1BKWE5BODI1OWh5Y25oZlpBRlRwZzF2UTRHdTNUdmxYL0NxZkJGajNYeVFVWURIZDJvRFRZVWM5VVk4aGdEeFg4NlR1eHJCNnNteTR0QlZkVHAzYjZGcGdjeGE1WU11dXhCQis3ZW1aYnF3TDZSdXpDMkZQRytmU1J1YUkwOER0Q1Ztb3NFc0ZobW1HS2JSRHkrU0JQWE9uOTJZZ1pkWE1RMlJZOWpPVm1Zall6TWFybXFhT24zQzBiWUZRRVlHRFpVb1o4M0IwMzR4MFc3aEw5R1RyN290SWtIN25wdS9zcWhtMm9Jdy94MXVGZlNOZEtzd2dJZGRFMTlnWlcyYytUMUVjTzNTdDZERTl1TGdyWHhkSTVYVzJaY3VCN0Ntd3dXM2lZY2FDbEhqYjZDSDIrNzNFWkpoY0xSdVF2cTkxeDdTWEJxcHVuUmhqc29oVFJiaE90N1YwTmtPMVFkWGIvWFpHZWZoNGdPMmxjNDFsUXVjemlrbURFYUJ3bEg2Yk9HaEpXWWxZd1FMZXZyd1FwSmFNdGFXS0dDZDdPQXh0UUNRVmVVMGdlTnU0TXJBRnJRNUtYTnl5WHQySkpyNGxvajNXd1h0cHYvZFc2QS9YM1FvM2tkTjJua3ZGUldNSEg0V0NKdWRmdGdzb01WTlJQY0pMTnN3S3B0azZkZGxyZjkzWXBWenNHdlpjeFhmNUVIMk5XYzVMVUNiNUhVUnJIN3ZianQ2NExEaVJVTWIvU2pSQjRpTmNoTWJGa25rTjZzT3JpZUZ2dUlSL1d5Q0VqWjlDM2luQ3ZGSzdLWXhuSFlmYVVlclhma004bUtKZ2UzZklXcTZPQUJDdWk3aXFEdFBFdGQvWnVaenBrVk09LS1zc0RpQzZocHBBNzhGSzZPcUJXV29nPT0%3D--13132ffd828141093c68061a5ce26f8b72dab661; _dd_s=rum=2&id=e697fecd-f6ff-456b-a9b0-bc72a9c9f028&created=1725324838123&expire=1725325738123",
                    "User-Agent": user_agent,
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive"
                }

                params = {
                    "page": 1,
                    "per_page": 96,
                    "search_text": "",
                    "catalog_ids": "",
                    "size_ids": "",
                    "brand_ids": brand_id,
                    "status_ids": "",
                    "color_ids": "",
                    "material_ids": ""
                }

                futures.append(executor.submit(send_request, session, headers, params, proxy))
                time.sleep(random.uniform(0.1, 2))  # Random delay between requests

            # Wait for all futures to complete
            for future in as_completed(futures):
                future.result()

    # Save the results to a JSON file
    

    print("Brand product counts have been saved to count_brand_entries_third.json")

# Main function to run the script
if __name__ == "__main__":
    TOTAL_REQUESTS = len(brands)  # Number of requests to send
    MAX_WORKERS = 5  # Number of concurrent threads
    
    send_requests_concurrently(TOTAL_REQUESTS, MAX_WORKERS)
