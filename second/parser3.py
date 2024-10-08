import requests
import json
import time

# Load the brands and their IDs from the JSON file
# with open("brands.json", "r", encoding="utf-8") as json_file:
#     brands = json.load(json_file)

# Define headers (use the same headers as before
headers = {
    "Cookie":"v_sid=a58a713aa16231031562a144f2c5547f; v_udt=REhRL2ptdHNHTGwrdGVEeEt0Mmt4Q3RFL0VIYi0td0hzTDMySEZIWmduVXhPaC0tMXJLdFV4SCs3dFlvSnlVcnhkMTNXZz09; anon_id=152fb059-d70c-4127-ba66-1074ea9a2db8; domain_selected=true; ab.optOut=This-cookie-will-expire-in-2025; OptanonAlertBoxClosed=2024-09-02T10:59:52.930Z; eupubconsent-v2=CQET0DgQET0DgAcABBENBFFsAP_gAAAAAChQKYtV_G__bXlj8X71aftkeY1f9_h7rsQxBhfJk-4FyLvW_JwX32EzNA36pqYKmRIAu3bBIQNlGIDUTUCgaogVryDMak2coTNKJ6BkiFMRe2cYCF5vmwlD-QKY5vr_91d52R-t7dr83dzyz4VHv3a5_2a1WJCdA58tDfv9bROb-9IOd_x8v4v8_FgAAAAAABAAAAAAAAAAAAAAAAAAABcAAAAAAAAOB_--AAAAoJBAAAQAAuACgAKgAcAA8ACCAGQAagA8ACIAEwAKoAbwA9AB-AEJAIYAiQBHACWAE0AMOAZQBlgDZAHfAPYA-IB9gH6AQAAikBFwEYAI0AUEAqABVwC5gGKANEAbQA3ABxAEOgJEATsAocBR4CkQFsALkAXeAvMBhoDJAGTgMuAZzA1gDWQGxgNvAbqA4IByYDlwHjgPaAhCBC8IAdAAcACQAc4BBwCfgI9ASKAlYBNoCnwFhALyAYgAxaBkIGRgNGAamA2gBtwDdIHkgeUA-QB-4EBAIGQQRBBMCDAEKwIXDgGIACIAHAAeABcAEgAPwA0ADnAHcAQCAg4CEAERAJ-AVAAvQB0gEIAI9ASKAlYBMQCZQE2gKQAUmArsBagC6AGIAMWAZCAyYBowDTQGpgNeAbQA2wBtwDj4HOgc_A8kDygHxAPtgfsB-4EDwIIgQYAg2BCsdBKAAXABQAFQAOAAgABdADIANQAeABEACYAFWALgAugBiADeAHoAP0AhgCJAEsAJoAUYAwwBlADRAGyAO8Ae0A-wD9AH_ARQBGACggFXALEAXMAvIBigDaAG4AOIAdQBDoCLwEiAJkATsAocBR4CmgFWALFgWwBbIC4AFyALtAXeAvMBfQDDQGPAMkAZOAyqBlgGXAM5AaqA1gBt4DdQHFgOTAcuA8cB7QD6wIAgQtIAEwAEABoAHOAWIBHoCbQFJgLyAamA2wBtwDn4HkgeUA-IB-wEDwIMAQbAhWQgPAALAAoAC4AKoAXAAxABvAD0AI4Ad4A_wCKAEpAKCAVcAuYBigDaAHUAU0AsUBaIC4AFyAMnAZyA1UB44EKAIWkoEIACAAFgAUAA4ADwAIgATAAqgBcADFAIYAiQBHACjAGyAO8AfgBVwDFAHUAQ6Ai8BIgCjwFigLYAXmAycBlgDOQGsANvAe0BA8kAPAAuAO4AgABUAEegJFASsAm0BSYDFgG5APKAfuBBECDBSBsAAuACgAKgAcABBADIANAAeABEACYAFIAKoAYgA_QCGAIkAUYAygBogDZAHfAPsA_QCLAEYAKCAVcAuYBeQDFAG0ANwAh0BF4CRAE7AKHAWKAtgBcAC5AF2gLzAX0Aw0BkgDJ4GWAZcAzmBrAGsgNvAbqA4IByYDxwHtAQhAhaUARAAXABIAI4Ac4A7gCAAEiALEAXUA14B2wD_gI9ASKAmIBNoCkAFPgK7AXQAvIBiwDJgGpgNeAeUA-KB-wH7gQMAgeBBMCDAEGwIVgA.f_wAAAAAAAAA; OTAdditionalConsentString=1~43.46.55.61.70.83.89.93.108.117.122.124.135.143.144.147.149.159.192.196.202.211.228.230.239.259.266.286.291.311.318.320.322.323.327.367.371.385.394.397.407.413.415.424.430.436.445.453.486.491.494.495.522.523.540.550.559.560.568.574.576.584.587.591.737.802.803.820.821.839.864.899.904.922.931.938.979.981.985.1003.1027.1031.1040.1046.1051.1053.1067.1092.1095.1097.1099.1107.1135.1143.1149.1152.1162.1166.1186.1188.1205.1215.1226.1227.1230.1252.1268.1270.1276.1284.1290.1301.1307.1312.1345.1356.1364.1375.1403.1415.1416.1421.1423.1440.1449.1455.1495.1512.1516.1525.1540.1548.1555.1558.1570.1577.1579.1583.1584.1591.1603.1616.1638.1651.1653.1659.1667.1677.1678.1682.1697.1699.1703.1712.1716.1721.1725.1732.1745.1750.1765.1782.1786.1800.1810.1825.1827.1832.1838.1840.1842.1843.1845.1859.1866.1870.1878.1880.1889.1899.1917.1929.1942.1944.1962.1963.1964.1967.1968.1969.1978.1985.1987.2003.2008.2027.2035.2039.2047.2052.2056.2064.2068.2072.2074.2088.2090.2103.2107.2109.2115.2124.2130.2133.2135.2137.2140.2147.2150.2156.2166.2177.2183.2186.2205.2213.2216.2219.2220.2222.2225.2234.2253.2279.2282.2292.2305.2309.2312.2316.2322.2325.2328.2331.2334.2335.2336.2337.2343.2354.2357.2358.2359.2370.2376.2377.2387.2400.2403.2405.2407.2411.2414.2416.2418.2425.2440.2447.2461.2465.2468.2472.2477.2481.2484.2486.2488.2493.2498.2501.2510.2517.2526.2527.2532.2535.2542.2552.2563.2564.2567.2568.2569.2571.2572.2575.2577.2583.2584.2596.2604.2605.2608.2609.2610.2612.2614.2621.2628.2629.2633.2636.2642.2643.2645.2646.2650.2651.2652.2656.2657.2658.2660.2661.2669.2670.2677.2681.2684.2687.2690.2695.2698.2713.2714.2729.2739.2767.2768.2770.2772.2784.2787.2791.2792.2798.2801.2805.2812.2813.2816.2817.2821.2822.2827.2830.2831.2834.2838.2839.2844.2846.2849.2850.2852.2854.2860.2862.2863.2865.2867.2869.2873.2874.2875.2876.2878.2880.2881.2882.2883.2884.2886.2887.2888.2889.2891.2893.2894.2895.2897.2898.2900.2901.2908.2909.2916.2917.2918.2919.2920.2922.2923.2927.2929.2930.2931.2940.2941.2947.2949.2950.2956.2958.2961.2963.2964.2965.2966.2968.2973.2975.2979.2980.2981.2983.2985.2986.2987.2994.2995.2997.2999.3000.3002.3003.3005.3008.3009.3010.3012.3016.3017.3018.3019.3025.3028.3034.3038.3043.3048.3052.3053.3055.3058.3059.3063.3066.3068.3070.3073.3074.3075.3076.3077.3089.3090.3093.3094.3095.3097.3099.3100.3106.3109.3112.3117.3119.3126.3127.3128.3130.3135.3136.3145.3150.3151.3154.3155.3163.3167.3172.3173.3182.3183.3184.3185.3187.3188.3189.3190.3194.3196.3209.3210.3211.3214.3215.3217.3219.3222.3223.3225.3226.3227.3228.3230.3231.3234.3235.3236.3237.3238.3240.3244.3245.3250.3251.3253.3257.3260.3270.3272.3281.3288.3290.3292.3293.3296.3299.3300.3306.3307.3309.3314.3315.3316.3318.3324.3328.3330.3331.3531.3731.3831.4131.4531.4631.4731.4831.5231.6931.7235.7831.7931.8931.9731.10231.10631.10831.11031.11531.12831.13632.13731.14237.14332.15731.16831.16931.21233.23031.25731.25931.26031.26831.27731.27831.28031.28731.28831.29631.31631.32531.33631; _gcl_au=1.1.955176475.1725274794; _ga=GA1.1.1226875194.1725274795; _tt_enable_cookie=1; _ttp=F7TdDzRTNCKh_m55UK-TDJyq7r0; _fbp=fb.1.1725274795598.879842942944496429; _cc_id=a391c297d83499fc408165b09b87b6e7; panoramaId_expiry=1725879600350; panoramaId=50b9cf229383dc5e2c3eeb78ef4c185ca02cbccb838b9e6cb6b08832c17f367c; panoramaIdType=panoDevice; anonymous-locale=en-fr; cf_clearance=v0OFR6Gm1AnS4E0E.pWkr8qiKJthE9SSVUMXtTqex4U-1725283439-1.2.1.1-bLoWH38t4W9KWv5lS_Llmjoh7WKT32ndcUCaGkeu2XQl05KeYRNlAjFZLTEnBsEKaII0fdVQ8UYIhqUFmSLd8ktf6JV6ZOmA39.vLUrwy8lECOm6OGQNbcHWO6rC.Cq2zHIA3fZ7mTN9CwAuP9_2U24rsxLUHP6mx5qKTZDEgF0gu27kyCqVx0HF95n4cZUYkVVWOdbLz9m813SHvVfUfuuKhbVAkfNSP4UCv5tCS5XjsiwvUMHDJCuOPXpYAM63IkO9TOtSJxYJ76hjEDoizl1gi6mbxV9XQUcv9BKEBHoBR3b7IEmgb6wyzRCUFLPk8gGDWLL_PmA8iBh19wZQfSaACchM9i1K.izFnqj4a.xr1K0e4eudqcEMM4Hjk7jYxQ7.UUmWrE.TncWoqyZfIw; cto_bidid=ljcYtV9mSEVIa1JwT2VaMlo1JTJCNTd1clUxWGZCN083NDhBRkJVWWZudkJyQUl4TXN5NFhLWFpSTjN4ZHpIUmtNbzNRTENabjRpcTJ2WkZldUVqRkxkUCUyRjNmcVdnMm1obHZybFNNMjR2MWFKM2xWWno1RnBNb1hub3ZTQnpTRWpqYVRvcXl2dWdoZ1p2RHpyMHg0RTBxZEFUdEpBJTNEJTNE; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Sep+02+2024+18%3A24%3A03+GMT%2B0500+(%D0%97%D0%B0%D0%BF%D0%B0%D0%B4%D0%BD%D1%8B%D0%B9+%D0%9A%D0%B0%D0%B7%D0%B0%D1%85%D1%81%D1%82%D0%B0%D0%BD)&version=202312.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=152fb059-d70c-4127-ba66-1074ea9a2db8&interactionCount=14&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CV2STACK42%3A1%2CC0015%3A1&geolocation=KZ%3B71&AwaitingReconsent=false; _uetsid=7c7cae00691a11efab629d0b97f861b6; _uetvid=7c7cb6b0691a11ef968e1de2fc6af383; cto_bundle=uMSJL19yb3FLZXhWZGhwYUd1VnhpcjVDT0IlMkJoeWZoYld4dVA3YU1nbm4lMkJZSDlzc0pZM0JnQyUyRlViNzREdm5sNjdBN3hZaUZKWU9tRUxlakNzczJxYzNLR0tlY3VUdjFUbFM1UGF2ZTloUUJycjBQOXVDYXdaU1dTeHdqVU5MZUZjb25KZ3dseHh0Z3NJaVM3YlE2aU9CQ1k4Q1ElM0QlM0Q; datadome=5X3C1JUpLv4ngY~S5gJVSc_85CA63CZ7PkbVZI8AW1oIDES45h6nt5ikv4My8eYPEs4rLb8I8SgpS~EJ016a8LLw81C3j7DXgnh7ENXVhGcj_JmQxOuP64yn9WoM4BsA; __cf_bm=xw7TC6HdW3qZZXK8GHrVR1qfc39HQPDSCLz1sBy4luQ-1725284516-1.0.1.1-sxg7nDRfMYJwa4vFXmdiMU4nw45FZXqJHlif7yIO4PQHY3ZAErYqrd5I1paF3mG01tzZoiyX.0fyCgOk0tjaTyj5ihxQ_EyP3GvOd0eT1Ec; __gads=ID=2ae7890c206a1440:T=1725274801:RT=1725284516:S=ALNI_Mb6YTYg-8nxUi9BX0khtoXE2VLV0A; __eoi=ID=eddb348baba7741c:T=1725274801:RT=1725284516:S=AA-AfjaA65N6tcjrTNzsBz9vvTDR; viewport_size=740; _ga_762HZ9XYEN=GS1.1.1725278250.2.1.1725284533.0.0.0; _ga_ZJHK1N3D75=GS1.1.1725278250.2.1.1725284533.0.0.0; _vinted_fr_session=aFNEMU45K2ZtVUgwOVJiWUZ6R1ExdVFpNHlFRGdLSURlU085TWRvN3NXaWlyVTFNcitHVG5Ebmd6dTFJdC94cjV2M08vNVBWNnJSbGFJY3VNaEo5QjFMdDdOL1RyejRXRHN2U2V2Tjg5empTamVWRElxYit2bHMwWDNFQjNSa1k3ODBMWkpac3AzYkIyZ2t2Z3FGUGdEZUVoblByTHVjRWh4aG9pZnNINDBYTHhRRVhqZTY2QW9YNVl1cUIxVENFcDBVRjZrYUF3WUFUSjllS3hWa1pncEtaalRGU05HQy9yNlROZG9qTUVuOVROQ2NYOHpOejF5WE5MWU8raVVMaUVjUWViUkR4clJKa3pLbHI3S2ZtY2V4Qys3Y1lCWVpja09PeXVBMnQzYVBCL3NrNFg4VGtyTjdLY3ZGL1dydGx6My9mVlNwdUVPbVJmY3hWZXZzb2J4VGxoaGtsV3JaWW9JREorOUJSV1A1ZXZCclhmMW5pYlR4YjBTdUlaOTJ5ZC91dVNLNlVQY2dXa1hDdk51Mnp1N0dMbm96dG9Pd0FmdklBaXAyOEliOXpkU2RwK3MrVWFmNmhCZ2ZuWlkraGVQUnM4UFRBRmNKanBZa3JqUWtUMGxoWGFrSzBmWGZMN0JpMzFkRG1FQzhqYzdCRS9OUWRkWVoxSzBobk13cVRncTBOVUMrVmZub0pCRkhoSXVQSTA5MnRaQ0lCcFc1VEcvSHJycXBOZ0xLMTNGMVQ1d25vOU5kQ0svcGdOT3FBUHc4NEZ6Tnd3SmpiVlhUajh4d2g3S2o1MkdqZFdZTkE2d2dmN2Q1MTYvTEpnb1VjdlVwOCtxbURiSEl5VktqaVpwSHk0bzJ4VXU5NXJzQlo1cGlVdmIyOWc5YWg0TGFKZ0tZREVPUGl5UDlhakFOWGFLUldkMlZ0REdwTkk3RXZiUnVQbU5SMU9PU3FaQTJ3Y1VJTmdRaS8vSnRyaUwxLzRXd2t4UU5uTVRJdW14UTdYcElyVk8rV2hhWnRWdU1OcDJ4ZEFNeUlocElDcVpwbm5nR0M0cHo0S1hDNzgweWY1WGZvMGRySUNMTC9Ic2d3YU5RclZJUnlkRWpkRTIyenVtKzh1L0c2UmdoMlV1Wk14WXBOZ0NHZnk1b3N1T2YwcXZtcG1PdnZuQUdsdi8wVlkrbUpka2RjYk5TajNUbHhOVVhGanhMNGFVb0gxRFpIbW5xUGRKNlZmOEpKdnBhNUJoSWEvcWJKME1ucE82K0o0L2pzaWhnclUxZ3ZkNjk2blpzTDI1WHZsMjV3eTQzZm1GS3UvbGxSSmVUdXR4Q2pCOWI3ZmJYbzZPVWRXTW92WTVrTU1ldzZkQ0pzbVlrUzJTQVVWeDJTVlBra1JiWnFlVHBkdnVoaW5EQ3NkWDhGaTVkV3FPS2Rndlc5Q1poYkI5UllTTzJ5U21wQitnTndUNUV4eWNVSktQYjVyckpnTGlqcWNyMjhUa3FkR0VrSmorTkxUYTZ6VXIvOG01R2pwTVN0UDdtTytJUUNXNnB0TU1JcVpIcnpKR2dxNTZ5eTlMdTZONjBkZXYzQzZPZ0VUY0hnK3dqcUdUWUZWRGdVSlZidDR4YklmNkhycDR5blF0ZkIwSmFiLzF4TkVEU1cvcDhvQS9neTUyNmo2amorQmRZdWtseC92dWkyTG00WEFOKzZwMTdyeHprc01IWjE5OUMxY3g2VkNORzRUYStOMXNtNXhoOTNIbC9ETUFZM3ViYUJsbzdQbFI3UE9jd2lzdnRtZWMyejBLS0ZGdTRDM3E3RFUzVmQ1WEU2Mkt3SUFKVVRtV3kyaGlqUEQ1M3JybXIzWTZrbGlHNEQ5WUEyZEZ3OXNrRmh0NUhRbjNwajFOM1FMaG1GSk4vZlFRcGdqY0MrS1U5Y0Zkc3Y1V0xVRFNDQ0dhN0FLN3hJRDBXdmFxRXhCT2VyanFFN3hBRVRDdVlQSWg0aVJVU1Fpc3c5bEptYUJET01QNmt1c3ljVUNUTEFsemxHTlVlUjZGNVNTQjdyUXVGR2tYWldJZVYrT1FQaFNtVXFqZ1g5Q3Zlc0NIWUNoVWtyaW8wek01ZEgwc2ZzMW9UQUVaaGhLdEx3UXk5QUkzakxVYVFBTFVXbXhXV1ppNVNieDRKb1hRYVNtczYwUW9CNWpUa0tCdk9wL29iMVRnSkFQc3Y1TDkxZEs2Q2k4dFY4eTNtNE9aYi9HUUYweG1Dd1FzTklKQ0FDM3RWUUNjVHREeTNpNVFzcHRiKzZCM0dEbnJiN3gyaFRoVXh2dGR1YkUvMFdaUmRxeXVaRXd2dlhZa2RDMVZkV1krcTNvR2wxMHJvWUUrWGhzaUZtTkxkWHM2TzBPMjNXZGs0cHZlYUtkSmQ0SVJQWmlzMmhYVFlOWElNSC9qRkV2RnZHS2NON3ViOW53azd5S0RERlNoak1MVUJ4eXk0SnI5Nmk4aXovRVdjMVlOSkFmK1BhVnptMGl6N2drL2JZenlvVHdWcTNVanNjU1NIdFI0aGljWDBlZmVWMHB3ZG5DeEhDTG9OdEJ3cUNiSDk1bXB5QmwrbEFvZHhqLzhJYmZEUUxQUStwYURNVnlqeHNvb3dpQU1tbW5Fdk12RU9SU1BqcmxzVXI3cG1PMHZaSnhUMjZ2eHBTaVQwZThRU1dFY0ZEdHc9PS0tWm9BNWJwRmw3bDd4c29iRlc2eTlMdz09--d15f03479da9de005d7ccdaad4dc7dee47bc298d; _dd_s=rum=2&id=f992b24f-0862-4991-95e9-15fe3a006028&created=1725283438552&expire=1725285437118",
    "User-Agent": "PostmanRuntime/7.41.2",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}
# Base URL for the items API endpoint
base_url = "https://www.vinted.pl/api/v2/catalog/items"

# Initialize a dictionary to store the count of products for each brand
brand_entries_count = {}

# Iterate over each brand and its ID
for brand_id in range(20001, 30000):
    # Define the parameters for the request
    if (brand_id % 1000 == 0) and len(brand_entries_count) > 0:
        with open(f"count_brands_from_{brand_id}.json", "w", encoding="utf-8") as json_file:
            json.dump(brand_entries_count, json_file, ensure_ascii=False, indent=4)
        brand_entries_count = {}
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

    # Send the GET request to the endpoint
    response = requests.get(base_url, headers=headers, params=params)
    # print("Requesting data for brand:", brand_name)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        dominant_brand = data.get("dominant_brand")
        if dominant_brand:
            brand_name = dominant_brand.get("title", "Unknown Brand")
            total_entries = data.get("pagination", {}).get("total_entries", 0)
            item_count_historical = dominant_brand.get("item_count", 0)
            final = [total_entries, item_count_historical]
            brand_entries_count[brand_name] = final
            print(f"Total entries for brand: {brand_name} ", total_entries, "Item count historical: ", item_count_historical)
        else:
            print(f"Brand with id {brand_id} not found or 'dominant_brand' is None")
    else:
        print(f"Brand with id {brand_id} not found")
        print(response.status_code)
    # Sleep between requests to avoid overwhelming the server
    # time.sleep(1)

# Save the results to a JSON file
with open("count_brand_entries.json", "w", encoding="utf-8") as json_file:
    json.dump(brand_entries_count, json_file, ensure_ascii=False, indent=4)

print("Brand product counts have been saved to count_brand_entries.json")


# Save the results to a JSON file
with open("count_brand_entries.json", "w", encoding="utf-8") as json_file:
    json.dump(brand_entries_count, json_file, ensure_ascii=False, indent=4)

print("Brand product counts have been saved to count_brand_entries.json")