#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import shutil
from zipfile import ZipFile

srcApkPath = "app\\outputs\\apk\\release\\app-release.apk"
channelFile = "channels.txt"
outDir = "allchannels"
channelTem = "META-INF"
version = "5.7.0"  #打包文件版本
apksZip = "apks.zip"  #所有渠道安装包压缩
bakApk = "app\\bakApk"
baksZip = "tinkerApk.zip" # tinker 基础包压缩保存
apkName = "test"


def log(content):
    print("------------>", content , "<------------")

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)

    if not isExists:
        os.makedirs(path)
        log(path + 'create success')
        return True
    else:
        log(path + 'is exist')
        return False

try:
    os.remove(apksZip)
except:
    log("clear apks.zip")
try:
    shutil.rmtree(channelTem)
except:
    log("clear "+channelTem)
try:
    shutil.rmtree(outDir)
except:
    log("clear "+outDir)
# try:
#     shutil.rmtree(bakApk)
# except:
#     log("clear " + bakApk)

log("start to clean")
commandClean = os.popen('.\gradlew clean')
log(commandClean.read())
log("start to release")
commandRelease = os.popen('.\gradlew assembleRelease')
log(commandRelease.read())

log("create dirs")
mkdir(outDir)
mkdir(channelTem)



def addFileIntoZipfile(file, fp):
    fp.write(file)


def zipFiles(srcDir, desZipfile):
    with ZipFile(desZipfile, mode='a') as fp:
        for subpath in os.listdir(srcDir):
            addFileIntoZipfile(srcDir+"/"+subpath , fp)

def zipFile(file, desZipfile):
    with ZipFile(desZipfile, mode='a') as fp:
        addFileIntoZipfile(file, fp)


content = open(channelFile, "r")
for channel in content.buffer.readlines():
    channelStr = str(channel.decode().strip())
    log("read channel----"+channelStr)
    if channelStr.__contains__(apkName):
        newApkName = outDir + '\\'+apkName+'_' + version + '.apk'
    elif channelStr.startswith("#"):
        break
    else:
        newApkName = outDir+'\yonglibao_'+version+'_'+channelStr+'.apk'
    shutil.copyfile(srcApkPath, newApkName)
    file = open(channelTem+'\channel_'+channelStr, 'w')
    zipFile(file.name, newApkName)
zipFiles(outDir, apksZip)
zipFiles(bakApk, baksZip)


content.close()


