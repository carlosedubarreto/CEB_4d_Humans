# CEB 4D Human
## Windows Only

This is an addon for blender (https://www.blender.org/) that enables you to have a simpler way to use the projects 4D Humans (https://github.com/shubham-goel/4D-Humans), WHAM (https://github.com/yohanshin/WHAM) and SLAHMR (https://github.com/vye16/slahmr).

Since those projects needs a lot of python packages that are not bundled in Blendere, and to avoid installing in it (to avoid problems) the solution used was to bundle with the addon, portable python, that will create virtual environment with everything needed to run those projects.

Since all of the projects uses SMPL Model, you need to download the file bellow
![opera_lLF3myId5Z](https://github.com/carlosedubarreto/CEB_4d_Human/assets/4061130/b7efa763-16d6-461c-be99-dd4cb49305b1)

After downloading it you will see that it was saves as:  mpips_smplify_public_v2.zip

Unzip it, and search inside the **\smplify_public\code\models** to find the file **basicModel_neutral_lbs_10_207_0_v1.0.0.pkl**

The file **basicModel_neutral_lbs_10_207_0_v1.0.0.pkl** you will have to load using the option that is insider the **Venv and Model 4D Humans** called **Import basicModel_neutral_lbs_10_207_0_v1.0.0.pkl**

![image](https://github.com/carlosedubarreto/CEB_4d_Human/assets/4061130/918b559f-a778-4af1-99a7-20e926d86a7b)


I started talkking about the smpl model import because its what was added since the version 1.11 to release here at github.
But to make it work, you also have to install using the **Create Venv**, **Install Pre Detectron on Venv**, **Install Pytorch on Venv** and **Install Detectron on Venv**

After that you can try to use the 4d human addon, it will try to download the models automatically, but if you get an error downloading, you can install them using the offline model files.
To get it you'll have to go to https://carlosedubarreto.gumroad.com/l/dependency/2jhtxqo to download it for free and you will fond the file **4d_humans_offline_v2.zip** on the CEB 4d Humans part of the site.

Having the file you can load at the **Models Offline Install** part

![image](https://github.com/carlosedubarreto/CEB_4d_Human/assets/4061130/81e87e1c-96d2-48c8-957f-242f4879f339)


If you watn more information you can go to the old gumroad page and read the info there, while I dont update it here (gumroad is disabled so its not possible anymore to get the files there)
https://carlosedubarreto.gumroad.com/l/ceb4dhumans
