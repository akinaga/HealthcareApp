#!/usr/bin/python
# -*- coding: utf-8 -*-

import boto
import cgi
import cgitb
import datetime
import zipfile
import sys
import urllib
cgitb.enable()

bucket_name = "slimee-userfiles-mobilehub-1950104086"
bucket = boto.connect_s3().get_bucket(bucket_name)

def listing(keys):
    html = "<table class='t1' width=600px><tr>"
    html += '<th nowrap>チェック<br><input type="checkbox" name="all" onClick="AllChecked();"></th>'
    html += "<th nowrap>ファイル名</th>"
    html += "<th nowrap>ファイル<br>サイズ</th>"
    html += "<th nowrap>最終更新</th>"
    # html += "<th nowrap>削除</th>"
    html += "</tr>"
    for key in keys:
        fullkeyname = str(key.name)
        keyname = str(key.name).replace("public/", "")
        keysize = str(key.size)
        lastmodified = str(key.last_modified)
        # if len(keyname) > 0 and keysize != "0":
        if len(keyname) > 0 :
            html += "<tr>"
            html += '<td align=center width=50px nowrap><input type ="checkbox" name="flag" value="' + fullkeyname + '"></td>'
            html += "<td width=200px nowrap style='text-align:left;'><a href='" + bucket.get_key(fullkeyname).generate_url(600) + "'>" + keyname + "</a></td>"
            html += "<td width=100px nowrap style='text-align:right;'>" + keysize + "</td>"
            html += "<td width=200px nowrap style='text-align:right;'>" + str(lastmodified).replace("T"," ").replace(".000Z","") + "</td>"
            # html += "<td width=50px nowrap><a href='view.py?delete=" + urllib.quote(fullkeyname) + "'><img src='dis.gif'></a></td>"
            html += "</tr>"
    html += "</table>"

    return html

# Form value
form = cgi.FieldStorage()
if 'download' in form:
    download = form.getlist('flag')
    filename = "download_" + datetime.datetime.today().strftime('%Y%m%d%H%M%S') + ".zip"
    sys.stderr.write(str(download)+"\n")
    with zipfile.ZipFile("/tmp/" + filename, "w", zipfile.ZIP_DEFLATED) as zf:
        for key in download:
            downloadfilename = "download/" + key.split("/")[-1]
            bucket.get_key(key).get_contents_to_filename(downloadfilename)
            zf.write(downloadfilename)
    print "Content-Type: application/zip;\r\nContent-Disposition: attachment; filename=" + filename + "\r\n\r\n",
    f = open("/tmp/" + filename, "rb")
    sys.stdout.write(f.read())
    f.close()
    exit()

if 'delete' in form:
    deletefile = form.getlist('flag')
    for key in deletefile:
        try:
            bucket.get_key(key).delete()
        except:
            pass
    print "Location: view.py\n\n"
    print ""
    exit()

# Get S3 keys
filelist = bucket.list(prefix='public/')
table1 = listing(filelist)

# Show target
html = table1
f = open("view.html", 'r')
bottom_html_skel = f.read()
f.close()
html = bottom_html_skel.replace("**table**", html)

# Final assemble
print "Content-type: text/html\n"
print html
