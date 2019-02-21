#Requires installing python3-matplotlib,python3-tk, and python3
#Download xml file from treasury yield
#Build Yield curves and display them in matplotlib

import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import os
from scipy.interpolate import make_interp_spline, BSpline

def loadxml():

    #get month and year
    d=dt.date.today()

    # url f xml
    url = 'https://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%20eq%20'+str(d.month)+'%20and%20year(NEW_DATE)%20eq%20'+str(d.year)
    # creating HTTP response object from given url
    resp = requests.get(url)

    #saving the xml file
    with open('DailyTreasuryYieldCurveRateData.xml','wb') as f:
        f.write(resp.content)

def parseXML(xmlfile):

    # create element tree object
    tree = ET.parse(xmlfile)

    #get root element
    root = tree.getroot()

    #Create dictionary for namespaces
    ns = {'rootns':'http://www.w3.org/2005/Atom','properties':'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata',
            'rates':'http://schemas.microsoft.com/ado/2007/08/dataservices'}

    #Delete xml file if it exists
    try:
        os.remove('~/DailyTreasuryYieldCurveRateData.xml')
    except OSError:
        pass
    try:
        os.remove('~/Documents/mypython/YieldCurve/DailyTreasuryYieldCurveRateData.xml')
    except OSError:
        pass

    #Create  values correspond to xmltags for plotting using matplot
    rate = []
    ratetbl=[]
    xlabels = ['1M','2M','3M','6M','1YR','2YR','3YR','5YR','7YR','10YR','20YR','30YR','10YR-2YR']
    datelabels=[]
    tag = [1,2,3,4,5,6,7,8,9,10,11,12]
    smoothtag = np.linspace(1,12)
    fig, ax = plt.subplots()
    ax.set( ylabel='Interest',title='Yield Curve')
    ax.grid
    plt.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0)
    plt.xticks([])

    #loop through the xml based on name space
    for entry in root.findall('rootns:entry',ns):
        for content in entry.findall('rootns:content',ns):
            for properties in content.findall('properties:properties',ns):
                #populate lists
                for child in properties:
                    #Get each individual element
                    if child.tag[55:] == 'NEW_DATE':
                        newdate = child.text[:10]
                        datelabels.append(child.text[:10])
                    if child.tag[55:] == 'BC_1MONTH':
                        rate.append(float(child.text))
                    if child.tag[55:] == 'BC_2MONTH':
                        rate.append(float(child.text))
                    if child.tag[55:] == 'BC_3MONTH':
                        rate.append(float(child.text))
                    if child.tag[55:] == 'BC_6MONTH':
                        rate.append(float(child.text))
                    if child.tag[55:] == 'BC_1YEAR':
                        rate.append(float(child.text))
                    if child.tag[55:] == 'BC_2YEAR':
                        rate.append(float(child.text))
                    if child.tag[55:] == 'BC_3YEAR':
                        rate.append(float(child.text))
                    if child.tag[55:] == 'BC_5YEAR':
                        rate.append(float(child.text))
                    if child.tag[55:] == 'BC_7YEAR':
                        rate.append(float(child.text))
                    if child.tag[55:] == 'BC_10YEAR':
                        rate.append(float(child.text))
                    if child.tag[55:] == 'BC_20YEAR':
                        rate.append(float(child.text))
                    if child.tag[55:] == 'BC_30YEAR':
                        rate.append(float(child.text))
                        ratetbl.append([r for r in rate])
                        smr = make_interp_spline(tag,rate)
                        rate_smooth = smr(smoothtag)
                        ax.plot(smoothtag,rate_smooth,ms=5,label=newdate)
                        rate.clear()

    #add column to rates that describes 10yr rate minus 2yr rate
    for r in ratetbl:
        r.extend([round(r[9]-r[5],2)])

    #create the table with the rate data
    the_table = plt.table(cellText=ratetbl,rowLabels=datelabels,colLabels=xlabels,loc='bottom')
    plt.subplots_adjust(left=0.06, bottom=0.5, right=0.97, top=0.96)
    ax.grid()
    ax.legend()
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()

def main():
    # load xml from web
    loadxml()

    #parse xml
    parseXML('DailyTreasuryYieldCurveRateData.xml')

if __name__ == "__main__":

    #calling main function
    main()
