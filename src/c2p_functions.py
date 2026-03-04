"""
c2p_functions.py

Core pipeline utilities for extracting and transforming contract/pipeline-style data.

Note:
- Live authentication endpoints, credentials, and MFA handling are intentionally omitted.
- This public version focuses on transformation, validation patterns, and pipeline structure.
"""

import pandas as pd
import requests
import numpy as np

BASE_URL = "https://<REDACTED_VENDOR_HOST>"


def get_cookies(driver):
        cookies = driver.get_cookies()

        cookiedf = pd.DataFrame(cookies)

        cookiedf['cookiePairs'] = [x + '=' + y for x,y in zip(cookiedf['name'], cookiedf['value'])]
        
        allCookies = cookiedf['cookiePairs'].str.cat(sep="; ")

        cookie_value = str(allCookies)
        print("...Cookies received (redacted).")
        return cookie_value



def getPipelinePages(url, headers):
        x=1

        oppResponse = requests.request("POST", url, headers=headers, data="FieldsToGet%5B%5D=BusinessOpportunityID&take=100&skip=0&pageSize=100&page="+str(x)+""
                )
        oppNum = oppResponse.json()['Total']
        print(oppNum)
        if (oppNum % 100 !=0):
                totalOppPages = (oppNum//100 +2)
        else:
                totalOppPages = (oppNum//100 +1)
        print("...Total Opportunity pages :", totalOppPages)
        print("...Total Opportunities :", oppNum)
        return totalOppPages


def getPipelineFilters(customfieldIdList, pipelineFields):
        customFilter =[]
        pipelineFilter =[]

        for x in range(len(customfieldIdList)):
                customFilter.append("FieldsToGet%5B%5D=customFields."+str(customfieldIdList[x])+"&")

        customFieldIdCombine = ''.join(customFilter) 

        for x in range(len(pipelineFields)):
                pipelineFilter.append("FieldsToGet%5B%5D="+str(pipelineFields[x])+"&")

        pipelineFilterCombine = ''.join(pipelineFilter)

        return customFieldIdCombine, pipelineFilterCombine

#---------------------------------------------#
#Function to get all the data in the pipeline #
#---------------------------------------------#
def getAllPipeline(totalOppPages, customFieldIdCombine, pipelineFilterCombine, url, headers):
        res = []
        for x in range(1, totalOppPages):
                payload = pipelineFilterCombine+customFieldIdCombine+"take=100&skip=0&pageSize=100&page="+str(x)+""
        
                response = requests.request("POST", url, headers=headers, data=payload)
                data = response.json()
        

                for p in data['Data']:
                        res.append(p)
       

        opp_df = pd.json_normalize(res)

        # Debug outputs omitted in public version
        # opp_df.to_csv("Allresults.csv", index=False)
        # opp_df.to_json("Allrecords.json")
        print("...All Pipeline captured")
        return opp_df

#----------------------------------------------------#
#Function to get all the custom category field names #
#----------------------------------------------------#
def getCustomCategories(cookies):

        customCaptureUrl = "https://<REDACTED_VENDOR_HOST>/<REDACTED_CUSTOM_CAPTURE_READ_PATH>"
        customCapturepayload = ""
        customCaptureheaders = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Cookie": cookies,
        }


        response = requests.request("POST", customCaptureUrl, headers=customCaptureheaders, data=customCapturepayload)
        
        categories = response.json()

        capHeader_df = pd.json_normalize(categories['Data'])
        capHeaderList = capHeader_df['CategoryId'].to_list()

        print(capHeaderList)
        # Debug outputs omitted in public version
        # capHeader_df.to_csv("captureHeaders.csv", index=False)

        return capHeaderList


def getCustomFieldNames(headers, customCaptureHeaders):
        payload = "sort=&group=&filter="

        categoryID = customCaptureHeaders  # public version uses passed-in IDs

        print("Custom Capture Headers: ", customCaptureHeaders)
        print(categoryID)

        fieldRes =[]

        for x in range(len(categoryID)):
                currentID = categoryID[x]
                url = f"{BASE_URL}/<REDACTED_CUSTOM_FIELD_READ_PATH>?categoryId={currentID}"
                response = requests.request("POST", url, headers=headers, data=payload)
                data = response.json()
        
                for p in data['Data']:
                        fieldRes.append(p)

        customField_df = pd.json_normalize(fieldRes)
        customField_df = customField_df[[ 'FieldName', 'FieldId', 'FieldDescription','CategoryId']]
        customField_df.drop(customField_df[customField_df.FieldId < 0].index, inplace=True)
        print("...FieldName, FieldId, Field Description, CategoryID captured")

        allCustomFieldIDs = customField_df['FieldId'].to_list()
        # Debug outputs omitted in public version
        # customField_df.to_csv("customFieldNames.csv", index=False)

        return allCustomFieldIDs, customField_df


def cleanCustomCapture(opportunity_DataFrame, customField_df):
        #Create a dataframe with Custom capture items
        #print(customField_df)
        customDF = pd.DataFrame(opportunity_DataFrame['CustomFields'].tolist())

        try:
                print(customDF.iloc[0, 0].get("FieldId"))
        except Exception:
                print("FieldId preview unavailable (structure differs).")

        customDF_OldColNames = customDF.columns.values.tolist()
        print("Old Column Name: ", customDF_OldColNames)
        customDF_NewColNames = [customDF[i][0].get('FieldId', 9999) if customDF[i][0].get('FieldId', 9999) is not None else '' for i in customDF]
        # customDF_NewColNames = []
        # for i in range(len(customDF)):
        #         customDF_NewColNames.append(customDF[i][0].get('FieldId'))
        print(customDF_NewColNames)
        
        renameMapper = {customDF_OldColNames[i]: customDF_NewColNames[i] for i in range(len(customDF_OldColNames))}
        #Rename columns to their Fields IDs
        customDF.rename(columns=renameMapper, inplace=True)

        #Extract Custom Capture data value for each cell
        for row in range(customDF.shape[0]):
                for col in customDF_NewColNames:
                        try:
                                customDF.at[row, col] = customDF.at[row,col].get('Answers')[0]
                        except Exception as e:
                                pass


        #Convert the FieldId to a string for mapping
        customField_df['FieldId'] = customField_df['FieldId'].astype(str)
        #Convert the Field Names from Excel to a dictionary list for mapping
        fieldNameDict = customField_df.to_dict('records')

        #Map Fields ID to matching string value
        mapping = {d['FieldId']:d['FieldName'] for d in fieldNameDict}
        customDF.rename(columns=mapping, inplace=True)

        #Final combined dataset
        c2pPipeline = pd.concat([pd.DataFrame(opportunity_DataFrame),customDF], axis=1)
        c2pPipeline = formatDates(c2pPipeline)

        #print(c2pPipeline.head())
        print("...Cleaned Pipeline complete")
        return c2pPipeline
        

def formatDates(dfToFormat):
        #---- Format all the date columns ----#
        dateColumns = [col for col in dfToFormat.columns if "Date" in col]

        for i in range(len(dateColumns)):
                dfToFormat[dateColumns[i]]=dfToFormat[dateColumns[i]].astype(str).apply(lambda d: d.strip()[6:-2])
                dfToFormat[dateColumns[i]]=pd.to_datetime(dfToFormat[dateColumns[i]], unit='ms',)

        dfToFormat = dfToFormat.replace({np.nan: None})
        #print(dfToFormat[dateColumns])
        return dfToFormat