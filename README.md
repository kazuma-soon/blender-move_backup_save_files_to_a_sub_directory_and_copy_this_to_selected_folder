# blender-move_backup_save_files_to_a_sub_directory_and_copy_this_to_selected_folder

## overview
Blender creates files with extensions like blend1, blend2 for backup. 
However, these files are created in the same directory as the blend file you are working with. 
This clutters your working directory. 

So this addon automatically organizes your working directory by saving backup files in a subfolder called "<your-blender-file-name>-backup".
And copy this folder to a directory you want to save.

As a use, for example, when you save blender, you can automatically store the backup(.blend1, .blend2...) 
in the designated folder of google drive.


## Operation verification environment
Does not work on Windows.
- Apple M1 Pro, macOS Ventura 13.2.1
- blender 3.4.1


## Usage
- Download source file
  - Download `blender_move_backup_save_files_to_a_sub_directory.py` from here.
  - **edit python file As described below**
  ```Python
  # Enter the copy destination folder in "<>" with an absolute path.
  # The trailing "/" is required.
  # Create the specified folder in advance.
  backup_dir2 = "<Absolute path to the directory where you want to save>/" + backup_folder_name
  ```
- Install addon
  - Open blener and move Edit > Preferences > add-ons.
  - Click "Install an add-on".
  - Select the downloaded `blender_move_backup_save_files_to_a_sub_directory.py`.
  - Check "System: Move Backup Save Files To A Sub Directory" to enable the addon.
  - Press "Save Preferences".

The first time you save a blend file, a subfolder named <your-blender-file-name>-backup is created in the directory containing the blend file. 
After the second save, blend1, blend2... will be saved in that folder.
Then <your-blender-file-name>-backup is copied to your selected folder.

## Options
I think there are some people who don't need the copy function.
I have also created a version without the copy function. </br>
- Using  [`blender_move_backup_save_files_to_a_sub_directory.py`](https://github.com/kazuma-soon/blender_move_backup_save_files_to_a_sub_directory/blob/main/blender_move_backup_save_files_to_a_sub_directory.py), create a subfolder named `backup.blend`. </br>
- Using [`blender_move_backup_save_files_to_a_sub_directory.py2`](https://github.com/kazuma-soon/blender_move_backup_save_files_to_a_sub_directory/blob/main/blender_move_backup_save_files_to_a_sub_directory2.py), create a subfolder named `<blend-file-name>_backup.blend`. </br>

- Change how many backup files are created in Edit > Preferences > Save & Load > Save Versions.




## Thanks for "Jonathan Stroem" and "Paul Mohr"
I created this addon with reference to [this page](https://blender.stackexchange.com/questions/6940/config-blender-to-save-backup-files-in-subfolder). Thanks to them I am able to create and share this. 
Thank you.
