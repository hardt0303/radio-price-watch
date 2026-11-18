import json
import re
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

SITES={
"R&L Electronics":"https://www.randl.com/index.php?main_page=product_info&cPath=14_300&products_id=76616",
"Ham Radio Outlet":"https://www.hamradio.com/detail.cfm?pid=71-005028",
"DX Engineering":"https://www.dxengineering.com/part/icom/id-5200a/8910884",
"Associated Radio":"https://associatedradio.com/nitem.php?cat_id=78&item_id=2108&manuf=Icom",
"MTC Radio":"https://mtcradio.com/products/icom-id-5200a-50w-144-430mhz-dual-band-transceiver",
"GigaParts":"https://www.gigaparts.com/icom-id-5200-50w-144-430mhz-dual-band-transceiver.html"}
class Page(HTMLParser):
 def __init__(self): super().__init__(); self.scripts=0; self.jsonld=False; self.buffers=[]; self.text=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=="script":
   self.scripts+=1; self.jsonld=a.get("type")=="application/ld+json"
   if self.jsonld:self.buffers.append("")
  elif tag in ("h1","h2"):self.text.append("\n")
 def handle_endtag(self,tag):
  if tag=="script":self.scripts-=1;self.jsonld=False
 def handle_data(self,data):
  if self.scripts and self.jsonld:self.buffers[-1]+=data
  elif not self.scripts and data.strip():self.text.append(data.strip())
def offers(obj):
 if isinstance(obj,dict):
  name=str(obj.get("name",""))
  if re.search(r"ID[- ]?5200",name,re.I):
   off=obj.get("offers",{})
   for item in off if isinstance(off,list) else [off]:
    try:
     p=float(item.get("price") or item.get("lowPrice"))
     if p>0:return round(p*100)
    except (AttributeError,TypeError,ValueError):pass
  for v in obj.values():
   p=offers(v)
   if p:return p
 if isinstance(obj,list):
  for v in obj:
   p=offers(v)
   if p:return p
 return None
def scrape(url):
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 RadioPriceWatch/1.0"})
 with urllib.request.urlopen(req,timeout=25) as response: raw=response.read().decode("utf-8","replace")
 page=Page();page.feed(raw)
 for block in page.buffers:
  try:
   price=offers(json.loads(block))
   if price:return price
  except json.JSONDecodeError:pass
 text=" ".join(page.text)
 match=re.search(r"ID[- ]?5200A?",text,re.I)
 if match:
  nearby=text[max(0,match.start()-120):match.start()+1800]
  prices=re.findall(r"\$\s*([0-9,]+\.\d{2})",nearby)
  if prices:return round(float(prices[0].replace(",",""))*100)
 raise ValueError("Could not verify product price")
path=Path("prices.json")
try:data=json.loads(path.read_text())
except Exception:data={"stores":{},"drops":[]}
now=datetime.now(timezone.utc).isoformat()
stores=data.setdefault("stores",{});drops=data.setdefault("drops",[])
for name,url in SITES.items():
 old=stores.get(name,{})
 try:
  price=scrape(url); previous=old.get("price")
  if previous and price<previous:drops.insert(0,{"store":name,"previous":previous,"price":price,"at":now})
  stores[name]={"price":price,"previous":previous if previous and previous!=price else old.get("previous"),"status":"Verified "+now}
 except Exception as error:
  stores[name]={**old,"status":"Could not verify on latest check"}
data["drops"]=drops[:50];data["updated_at"]=now
path.write_text(json.dumps(data,indent=2)+"\n")
