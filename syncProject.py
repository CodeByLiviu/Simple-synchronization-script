"""
The problem:
Implement a program that synchronizes two folders: source and replica.
The program should maintain a full, identical copy of destination folder at replica folder.
Requirements:
•	Synchronization must be one-way: after the synchronization content of the replica folder
should be modified to exactly match content of the source folder;
•	Synchronization should be performed periodically;
•	File creation/copying/removal operations should be logged to a file and to the console output;
•	Folder paths, synchronization interval and log file path should be provided using the command line arguments.
"""

"The solution:"
# import relevant modules
from datetime import datetime
from dirsync import sync
import time
import os
import shutil



def syncing(interval, source, target):
    """
    This method is used to sync both source and target folder one-way every time interval you choose.
    :param interval: time in seconds between each sync
    :param source: is the path to a folder from which you want to make a copy
    :param target: is the path to a folder that you want to copy to
    :return: returns a bool that can stop the process if there is something wrong.
    """
    try:
        text = sync(source, target, 'sync')
        deleteDifferencesFromPath(target, source)
        time.sleep(interval)
        return text
    except:
        print("One of the paths are invalid! Please try again")
        return False


def deleteFilesAndFoldersFromPath(path):
    """
    This method is used to delete a file if you give its path
    :param path: the absolute path to the file that you want to delete
    :return:
    """
    try:
        shutil.rmtree(path)
    except:
        os.remove(path)


def compareFilesInFolders(pathToFolder1, pathToFolder2):
    """
    Returns a list of differences. What is in Folder1 but isn't in Folder2
    :param pathToFolder1: a path to the first folder
    :param pathToFolder2: a path to the second folder
    :return: listOfDifferences
    """
    listOfDifferences = []
    for file in os.listdir(pathToFolder1):
        if file not in os.listdir(pathToFolder2):
            listOfDifferences.append(file)
    return listOfDifferences


def deleteDifferencesFromPath(pathToFolder1, pathToFolder2):
    """
    This method is used to delete differences between Folder1 and Folder2.
    If there is something inside Folder1 and that's not present in Folder2 it will be deleted.
    :param pathToFolder1: a path to the first folder
    :param pathToFolder2: a path to the second folder
    :return:
    """
    listOfDifferences = compareFilesInFolders(pathToFolder1, pathToFolder2)
    for file in listOfDifferences:
        file = pathToFolder1 + file
        deleteFilesAndFoldersFromPath(file)


def writeFileReport(text, path):
    """
    This method writes the file report to a text file.
    :param text: the text that you want to write
    :param path: the to the .txt file
    :return:
    """
    with open(path, 'a') as fileReport:
        fileReport.write(str(datetime.now()))
        fileReport.write(text)
        fileReport.close()


def createReport(pathToFolder1, pathToFolder2):
    """
    This method creates the report to be printed or write.
    :param pathToFolder1: the path to the first folder
    :param pathToFolder2: the pat to the second folder
    :return:  a text that you can print to the terminal or write to a file
    """
    filesToRemove = compareFilesInFolders(pathToFolder2, pathToFolder1)
    filesToRemove_text = f"List of files removed: {filesToRemove}"
    filesCreated = compareFilesInFolders(pathToFolder1, pathToFolder2)
    filesCreated_text = f"List of files created: {filesCreated}"
    return [filesToRemove_text, filesCreated_text]


def mainLoop(interval, source, target, pathToReport):
    """
    This is the main method that starts the program.
    :param interval: time in seconds between each sync
    :param source: is the path to a folder from which you want to make a copy
    :param target: is the path to a folder that you want to copy to
    :return:
    """
    fileReportName = "fileReport.txt"
    pathToReport = f"{pathToReport}{fileReportName}"
    while True:
        try:
            interval = int(interval)
        except:
            print("The interval that you've specified should be an integer! Please try again.")
            return

        filesRemoved, filesCreated = createReport(source, target)
        status = syncing(interval, source, target)
        textForReport = f"""
        {filesRemoved}
        {filesCreated}
        """
        writeFileReport(textForReport, pathToReport)
        if status == False:
            print("The program will stop!")
            return

# Exemple:
# be sure you will use this "/" not this "\"
# sourceFolderPath = 'C:/Users/Liviu/Desktop/test/New folder/source/'
# replicaFolderPath = 'C:/Users/Liviu/Desktop/test/New folder/replica/'
# fileReportFolder = 'C:/Users/Liviu/Desktop/test/New folder/'
# setInterval = 10

sourceFolderPath = input("Input your source folder path: ")
replicaFolderPath = input("Input your replica folder path: ")
fileReportPath = input("Input where should be stored the fileReport.txt: ")
setInterval = input("Input the syncing interval: ")

mainLoop(setInterval, sourceFolderPath, replicaFolderPath, fileReportPath)

