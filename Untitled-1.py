#!/usr/bin/python3
import os
import sys
import json
import sharepy
import time
import logging
 
def uploadToSharepoint(SPUrl, siteName, libraryName, FolderPath):
    #check is the session files exists
    if os.path.isfile("sp-session.pkl"):
        s = sharepy.load()
    else:
        s = sharepy.connect(SPUrl)
        s.save()
    #check is system is windows
    if os.name == 'nt':
        folder = FolderPath.split('\\')
    else:
        folder = FolderPath.split('/')
        print(folder)
 
    #check to see if the FolderPath is a directory
    if os.path.isdir(FolderPath):
 
        #creates the folder in sharepoint
        p = s.post("https://"+SPUrl+"/sites/"+siteName+"/_api/web/folders",
        json={
            "__metadata": { "type": "SP.Folder" },
            "ServerRelativeUrl": libraryName +'/' + folder[-2]
            })
             
        logging.info("Created Folder %s: with response %s", folder, p.content)
 
        filesToUpload = os.listdir(FolderPath)
         
        #uploads files to sharepoint
        for fileToUpload in filesToUpload:
            headers = {"accept": "application/json;odata=verbose",
            "content-type": "application/x-www-urlencoded; charset=UTF-8"}
             
            with open(os.path.join(FolderPath, fileToUpload), 'rb') as read_file:
                content = read_file.read()
             
            p = s.post(f"https://{SPUrl}/sites/{siteName}/_api/web/GetFolderByServerRelativeUrl('{libraryName}/{folder[-2]}')/Files/add(url='{fileToUpload}',overwrite=true)", data=content, headers=headers)
             
            logging.info("Uploaded %s: with response %s", folder, p.content)
            print(folder)
        
if __name__ == "__main__":
 
    SPUrl = "tenant.sharepoint.com"
    siteName = "Site1"
    libraryName = "library1"
    logging.basicConfig(filename="UploadedFiles.log",
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
 
    path = sys.argv[1] if len(sys.argv) else '.'
 
    uploadToSharepoint(SPUrl, siteName, libraryName, path)