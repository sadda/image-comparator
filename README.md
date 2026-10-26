# Image Comparator

This repo provides an app for validating whether two images depict the same individual. It is part of a large, mostly automated pipeline that takes photos of one animal species as input and outputs photos showing the same individuals.

<img src="https://github.com/sadda/wildlife-app/raw/master/docs/resources/app.png" alt="App photo" width="500">

## Installation

We provide two ways of installation. Both are for Windows only. If you need to use the app on a different operating system, [contact us](mailto:wilddatasets@gmail.com). The first one is simpler but requires significantly more internet bandwidth.

### Installation 1

- Download the [zip file](https://1drv.ms/u/c/8621a316a2cb40fa/IQBqMmLdqfzsRqTgyCWCzIHVAd969AvuAbk2FRJtETXhqHU?e=b37zRi).
- Extract the downloaded zip file.
- Go to the `config` folder inside the extracted folder and rename your project config file (such as `turtles_of_smsrc.json`) into `config.json`.

### Installation 2

- Open PowerShell (press the Windows key, type `powershell` and press enter). It is a text window where commands are typed. Run in it (type or paste it and press enter)
  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
  This installs [uv](https://docs.astral.sh/uv/), a tool for installing Python apps. Close PowerShell afterwards.
- Open a new PowerShell and run
  ```
  uv tool install https://github.com/sadda/wildlife-app/archive/refs/heads/master.zip
  ```
  This will install Python, the app and the required Python packages.

## Updating the app

For Installation 1, the whole process must be repeated. For Installation 2, open PowerShell and run
```
uv tool install --reinstall --refresh https://github.com/sadda/wildlife-app/archive/refs/heads/master.zip
```

## Running the app

For Installation 1, run the exe file.

For Installation 2, create an empty folder for your project (such as `turtles_of_smsrc`). The dataset and your answers will be stored there. Open the folder in File Explorer, type `powershell` into the address bar and press enter. This opens PowerShell in this folder. Run
```
wildlife-app turtles_of_smsrc
```
If you run a different project than TurtlesOfSMSRC, change the last keyword (such as `turtlewatch_egypt`). Always run the app from the same folder, otherwise it will not find your data and answers.

When the app starts for the first time, it will begin downloading the dataset, which may take half an hour. For TurtlewatchEgypt, some files cannot be downloaded and must be copied into the `data` subfolder manually. The app tells you which ones are missing.

## Using the app

Using the app should be straightforward. Press Same (Q), Different (W) or Unknown (E) for validating whether the two shown turtles are the same. Use Previous (A) and Next (S) to move to the following images without giving an answer or to check the previous answer. You can also move to the next body part if the matching was performed across multiple body parts. It is highly recommended to use the keyboard shortcuts Q, W, E, A and S. The answers are saved to the file `answers.csv`.

When a dataset is updated, it should be downloaded by the corresponding button. Similarly, when new predictions are available for verification, they can be automatically downloaded. The last button downloads segmentation masks, which are used to crop turtle heads and flippers.