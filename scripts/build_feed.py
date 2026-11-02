import datetime as dt, email.utils, html, json, os, re, subprocess, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'out'/'site';SITE.mkdir(parents=True,exist_ok=True)
REPO=os.environ.get('GITHUB_REPOSITORY','cooprush/morning-distraction')
owner,name=REPO.split('/')
base=f'https://{owner}.github.io/{name}/'
data=json.loads(subprocess.check_output(['gh','api',f'repos/{REPO}/releases','-f','per_page=30','--method','GET'],text=True))
rss=ET.Element('rss',version='2.0')
channel=ET.SubElement(rss,'channel')
def elem(root,tag,value):ET.SubElement(root,tag).text=str(value)
for tag,val in [('title','The Morning Distraction'),('link',base),('description','Original, humorous British morning podcast with political satire, parenting and curiosities.'),('language','en-gb')]:elem(channel,tag,val)
items=[]
for release in data:
    assets=[a for a in release.get('assets',[]) if a.get('name','').endswith('.mp3')]
    if not assets:continue
    asset=assets[0];notes=release.get('body','')
    d=re.search(r'DurationSeconds:\s*(\d+)',notes)
    duration=int(d.group(1)) if d else 0
    item=ET.SubElement(channel,'item')
    title=release.get('name') or release.get('tag_name')
    url=asset['browser_download_url']
    for tag,val in [('title',title),('description',re.sub(r'DurationSeconds:\s*\d+','',notes).strip()),('link',url),('guid',url),('pubDate',email.utils.format_datetime(dt.datetime.fromisoformat(release['published_at'].replace('Z','+00:00'))))]:elem(item,tag,val)
    ET.SubElement(item,'enclosure',url=url,length=str(asset.get('size',0)),type='audio/mpeg')
    items.append((title,url,duration))
ET.ElementTree(rss).write(SITE/'feed.xml',encoding='utf-8',xml_declaration=True)
rows=''.join(f'<li><a href="{html.escape(url)}">{html.escape(title)}</a> ({int(duration//60)} min)</li>' for title,url,duration in items)
(SITE/'index.html').write_text(f'<!doctype html><html lang="en"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Morning Distraction</title><body style="font-family:system-ui;max-width:650px;margin:2em auto;padding:1em"><h1>The Morning Distraction 🎙️</h1><p>Original daily UK comedy, satire and curiosities.</p><p><a href="feed.xml">Subscribe to podcast feed</a></p><ol>{rows}</ol></body></html>',encoding='utf8')
print('RSS entries',len(items))
