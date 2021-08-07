import requests,pandas as pd,time,random

from bs4 import BeautifulSoup as bs


url = "https://www.kinguin.net/services/library/api/v1/products/search"

info=[]
i=0

# Each page has 10 items so scrape accordingly and responsibly by changing the x values

for x in range(i,51):
    print(f"Page:- {x}")
    
    # Add your user agent
    
    headers = {
        "cookie": "__cfruid=29c0d11e429364fa36b6b8b45dde248751a3911e-1627912783",
        "authority": "www.kinguin.net",
        "x-kl-ajax-request": "Ajax_Request",
        "accept": "application/json, text/plain, */*",
        "cfipcountry": "IN",
        "guest-user-id": "eil4qj7e5v8angafh0tnfkml09n2np",
        "sec-ch-ua-mobile": "?0",
        "User-Agent":""#User agent,
        "sec-ch-ua": "^\^Chromium^^;v=^\^92^^, ^\^"
    }
    querystring = {"sort":"bestseller.total,DESC","visible":"1","active":"1","size":"10","page":f"{x}","":["",""],"priceTo":"999"}
    
    r = requests.request("GET", url,  headers=headers, params=querystring)
    data=r.json()
        
    
    items=data["_embedded"]["products"]
    for item in items:
        externalid=item["externalId"]
        
        title=item["name"]
        titledash=title.replace(" ","-")
        link="https://www.kinguin.net/category/"+externalid+f"/{titledash}"
        try:
            final_price=int(item["price"]["lowestOffer"])-int(item["price"]["discount"])
        except:
            try:
                final_price=int(item["price"]["lowestOffer"])
                
            except:
                final_price=int(item["wholesale"]["lowestPrice"])
        try:
            score=int(item["attributes"]["metascore"])
        except:
            score=None
        game={"Title":title,"Price":final_price,"Score":score,"URL":link}
        info.append(game)
    if x==51:
        break
    time.sleep(random.randint(1,3))

df=pd.DataFrame(info)
print(df.columns)
df=df.sort_values("Price")

# add your favoured path while saving
file_path="               "

df.to_excel(file_path,sheet_name="Kinguin",index=False)

print(f"\n Kinguin Done")

info=[]

#Currently scraping for 500 items, fiddle with the x value to scrape for games accordingly

for x in range(0,500,50):
    url = "https://store.steampowered.com/search/results"
    querystring = {"query":"","start":x,"count":"50","dynamic_data":"","sort_by":"_ASC","snr":"1_7_7_2300_7","specials":"1","filter":"topsellers","infinite":"1"}

    payload = ""
    
    #Add User Agent
    
    headers = {
        "cookie": "steamCountry=IN%257C08d2be1e9500001d40e2457e1a6ad65f; browserid=2412226565181261149; sessionid=3a7c00541eeacb1187d1139c",
        "Connection": "keep-alive",
        "X-KL-Ajax-Request": "Ajax_Request",
        "Accept": "text/javascript, text/html, application/xml, text/xml, */*",
        "X-Prototype-Version": "1.7",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": ""#User agent,
        "sec-ch-ua": "^\^Chromium^^;v=^\^92^^, ^\^"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    jsondata=response.json()
    soup=bs(jsondata["results_html"],"html.parser")
    App_IDS=soup.find_all(class_="search_result_row ds_collapse_flag")
    games=soup.find_all(class_="responsive_search_name_combined")
    
    for game,idx in zip(games,App_IDS):
        title=game.find(class_="title").text
        price=game.find(class_="col search_price discounted responsive_secondrow")
        try:
            price=int(price.text.strip().replace(",", "")[-4:])
        except:
            price=int(price.text.strip().replace(",", "")[-3:])
        raw_id=idx["data-ds-itemkey"]
        raw_id=raw_id[raw_id.find("_")+1:]
        link=f"https://store.steampowered.com/app/{raw_id}/{title}/"
        review=game.find(class_="search_review_summary positive")
        
        try:
            review_raw=review["data-tooltip-html"]
            
            
            review=int(review_raw.split(">")[1][:2])
            no_of_reviewers=review_raw.split("the")[1].strip().replace(",", "")
            no_of_reviewers=int(no_of_reviewers[:no_of_reviewers.find(" ")])
        except:
            review=None
            no_of_reviewers=None
        
        game={"Title":title,"Price":price,"Rating":review,
                "No Of Reviewers":no_of_reviewers,"URL":link
                }
        info.append(game)
    print(info[49+x])
    
    # Implementing a buffer time in between requests,adjust as per wish
    
    time.sleep(random.randint(2,4))
     
    # Using the same file to append the steam data to the kinguin file.
df=pd.read_excel(file_path)


with pd.ExcelWriter(file_path) as writer:
    pd.DataFrame(info).to_excel(writer,sheet_name="Steam")
    df.to_excel(writer,sheet_name="Kinguin")


