#!/usr/bin/python
# -*- coding: utf-8 -*-

import boto
import cgi
import cgitb
import csv
cgitb.enable()


conn = boto.connect_s3().get_bucket(bucket_name)


def listing(sql):
    try:
        summary, cache_filename, description = dbaccess2(sql)

        d = []
        dd = []
        for desc in description:
            col_name = str(desc[0])
            d.append(col_name)
        dd.append(d)
        csvoutput = dd + summary

        csvfilename = cache_filename + '.csv'
        csvwriter = csv.writer(open(csvfilename, 'wb'), dialect='excel')
        csvwriter.writerows(csvoutput)


        html = "<table class='t1' width=1000px><tr>"
        i = 0
        for desc in d:
            i += 1
            if i >= 7:
                html += "<th class='tg1'>" + str(desc) + "</th>"
            elif i >= 4:
                html += "<th class='tg2'>" + str(desc) + "</th>"
            else:
                html += "<th>" + str(desc) + "</th>"

        html += "</tr>"

        html = html.replace("linkedaccountid", "アカウントID")
        html = html.replace("linkedaccountname", "アカウント名")
        html = html.replace("blendedcost", "請求金額<br>(税抜)")
        html = html.replace("unblended_tax", "正利用料<br>(税)")
        html = html.replace("unblended_total", "正利用料<br>(税込)")
        html = html.replace("unblended", "正利用料<br>(税抜)")
        html = html.replace("tax_ratio", "請求金額<br>(税)")
        html = html.replace("ratio", "想定税率")

        for data in summary:
            html += "<tr>"
            i = 0
            for dat in data:
                i += 1
                if str(dat)=="None":
                    html += "<td style='background: #CCCCCC;'>N/A</td>"
                else:
                    if i >= 7:
                        html += "<td class='tg1'>$" + str(dat) + "</td>"
                    elif i == 6:
                        html += "<td class='tg2'>" + str(dat) + "%</td>"
                    elif i >= 4:
                        html += "<td class='tg2'>$" + str(dat) + "</td>"
                    else:
                        html += "<td>" + str(dat) + "</td>"

            html += "</tr>"
        html += '<tr>'
        html += '<td class ="tp1" colspan=' + str(len(description)) + '>'
        html += '<form method = "get" action="' + csvfilename + '">'
        html += '<br><button type="submit">Download</button></form>'
        html += "</td></tr>"
        html += "</table>"

        jsondata = jsontrans2(summary, ["linkedaccountid","linkedaccountname","recordtype","blendedcost","tax","tax_ratio","unblended","unblended_tax","unblended_total"])
        # jsondata = ""

    except:
        html = 'document.write("<p align=center>Database Error.</p>");'
        raise

    return html, jsondata


def listing2(sql):
    try:
        summary, cache_filename, description = dbaccess2(sql)
        d = []
        dd = []
        for desc in description:
            col_name = str(desc[0])
            d.append(col_name)
        dd.append(d)
        csvoutput = dd + summary

        csvfilename = cache_filename + '.csv'
        csvwriter = csv.writer(open(csvfilename, 'wb'), dialect='excel')
        csvwriter.writerows(csvoutput)

        html = "<table class='t1' width=1200px><tr>"
        i = 0
        for desc in d:
            i += 1
            if i >= 7:
                html += "<th class='tg1'>" + str(desc) + "</th>"
            elif i >= 4:
                html += "<th class='tg2'>" + str(desc) + "</th>"
            else:
                html += "<th>" + str(desc) + "</th>"

        html += "</tr>"

        html = html.replace("blendedcost_tax", "請求金額<br>税合計")
        html = html.replace("blendedcost_total", "請求金額合計<br>(税込)")
        html = html.replace("blendedcost", "請求金額合計<br>(税抜)")
        html = html.replace("unblended_tax", "正利用料<br>税合計")
        html = html.replace("unblended_total", "正利用料合計<br>(税込)")
        html = html.replace("unblended", "正利用料合計<br>(税抜)")
        html = html.replace("beforetax_error", "税抜差分")
        html = html.replace("tax_error", "税額差分")
        html = html.replace("total_error", "税込差分")

        for data in summary:
            html += "<tr>"
            i = 0
            for dat in data:
                i += 1
                if str(dat)=="None":
                    html += "<td style='background: #CCCCCC;'>N/A</td>"
                else:
                    if i >= 7:
                        html += "<td class='tg1' style='font-size: 24px;'>$" + str(dat) + "</td>"
                    elif i >= 4:
                        html += "<td class='tg2' style='font-size: 24px;'>$" + str(dat) + "</td>"
                    else:
                        html += "<td style='font-size: 24px;'>$" + str(dat) + "</td>"
            html += "</tr>"
        html += "</table>"

    except:
        html = 'document.write("<p align=center>Database Error.</p>");'
        raise

    return html


# Show target
html = "<hr><h2>請求金額一覧</h2>"
html += table1

# Show target
f = open("view.htm", 'r')
bottom_html_skel = f.read()
f.close()
html = bottom_html_skel.replace("**tablelist**",tablelist).replace("**table**",html).replace("**title**",title)


# Final assemble
print "Content-type: text/html\n"
print html
