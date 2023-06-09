# https://blender.stackexchange.com/questions/6940/config-blender-to-save-backup-files-in-subfolder
bl_info = {
    "version": (1, 3),
    "blender": (3, 4),
    "name": "Ver.3-Move Backup Save Files To A Sub Directory and copy Sub Directory to selected folders",
    "author": "Jonathan Stroem, Paul Mohr, Kazuma Hashimoto",
    "description": """Move the backup save files to a sub-directory instead of the Blender-file's current directory. A new folder called "<blend-file-name>_backup" will be created and all save-files will be moved there instead of the default folder. And backup folder are copied to selected folders.""" ,
    "category": "System",
    "location": """""",
    }

#IMPORTS
import bpy, os
import shutil
from bpy.app.handlers import persistent
from distutils.dir_util import copy_tree
import time
from stat import *


@persistent
def move_handler(dummy):

    #fullpath = Full path to the data file.
    #directory = Directory the data file is in.
    #name = Name of file, without extension.
    #extension = Extension of files.
    #backup_amount = Max amount of backups to store.
    #backup_directory = The name of the backup directory. (Where the files should be moved.) So change this if you want to change where the backups are saved.

    file = {"fullpath":bpy.data.filepath, \
            "directory":os.path.dirname(bpy.data.filepath), \
            "name":bpy.path.display_name_from_filepath(bpy.data.filepath), \
            "extension":".blend", \
            "backup_amount":bpy.context.preferences.filepaths.save_version, \
            "backup_directory":os.path.splitext(os.path.basename(bpy.data.filepath))[0] + "_backup" \
            }

    #Create backup directory if it doesn't exist.
    if file["backup_directory"] not in os.listdir(file["directory"]):
        os.chdir(file["directory"])
        os.mkdir(file["backup_directory"])

    #Get current save files from the backup directory.
    current_dir_blend_files_list = []
    backup_dir = file["directory"] + "/" + file["backup_directory"]
    backup_blend_file_no = range(1, int(file["backup_amount"]) + 1)

    for f in [f for f in os.listdir(backup_dir) for c in backup_blend_file_no if f == file["name"] + file["extension"] + str(c) if os.path.isfile(os.path.join(backup_dir, f))]:
        current_dir_blend_files_list.append(f)

    #All this is moving the correct file.
    if len(current_dir_blend_files_list) < 1 : #If no files, then no need to check.
        if os.path.isfile(file["fullpath"] + "1") :
            shutil.move(file["fullpath"] + "1", file["directory"] + "/" + file["backup_directory"] + "/" + file["name"] + ".blend1")
    else : #If the max backup amount has been reached, then check for the oldest file and overwrite that one.
        if file["backup_amount"] <= len(current_dir_blend_files_list) :
            replaceFile = {"modified_date":None, \
                           "fullname":""}
            for f in current_dir_blend_files_list :
                stats = os.stat(file["directory"] + "/" + file["backup_directory"] + "/" + f) #Get attributes from a file.
                if replaceFile["fullname"] == "" : #This will happen only the first time.
                    replaceFile["fullname"] = f
                    replaceFile["modified_date"] = time.asctime(time.localtime(stats[ST_MTIME]))
                else : # Is the previous file older or newer? If it's older, then you'd want to overwrite that one instead. Go through all backup-files.
                    temp_modified = time.asctime(time.localtime(stats[ST_MTIME]))
                    if replaceFile["modified_date"] > temp_modified :
                        replaceFile["fullname"] = f
                        replaceFile["modified_date"] = temp_modified

            #When the loop is finished, the oldest file has been found, and will be overwritten.
            shutil.move(file["fullpath"] + "1", file["directory"] + "/" + file["backup_directory"] + "/" + replaceFile["fullname"])
        else : #If the max backup amount hasn't been reached, and the folder isn't empty.
            #Then check for the next number, and then just move the file over with the correct number.
            replaceFile = "" #Location.
            for f in current_dir_blend_files_list :
                for c in range(1, int(file["backup_amount"]) + 1) :
                    if not os.path.isfile(file["directory"] + "/" + file["backup_directory"] + "/" + file["name"] + file["extension"] + str(c)) :
                        shutil.move(file["fullpath"] + "1", file["directory"] + "/" + file["backup_directory"] + "/" + file["name"] + file["extension"] + str(c))
                        replaceFile = f
                        break
                if replaceFile != "" : #File to replace has been found, break out.
                    break

    if os.path.exists(backup_dir):
        backup_folder_name = os.path.splitext(os.path.basename(backup_dir))[0]
        backup_dir2 = "<Absolute path to the directory where you want to save>/" + backup_folder_name

        copy_tree(backup_dir, backup_dir2)


#When enabling the addon.
def register():
    bpy.app.handlers.save_post.append(move_handler)

#When disabling the addon.
def unregister():
    bpy.app.handlers.save_post.remove(move_handler)

#So that Blender recognize it as an addon.
if __name__ == "__main__":
    register()


