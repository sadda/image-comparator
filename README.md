# Image Comparator

This repo provides an app for validating whether two images depict the same individual. It is part of a large, mostly automated pipeline that takes photos of one animal species as input and outputs photos showing the same individuals.

<img src="https://github.com/sadda/wildlife-app/raw/master/docs/resources/app.png" alt="App photo" width="500">

## Installation

All commands below are run in a terminal, a text window where commands are typed. To open it:
- Windows: press the Windows key, type `cmd` or `powershell` and press enter.
- Mac: press Cmd+Space, type `terminal` and press enter.
- Linux: press Ctrl+Alt+T.

Paste each command into the terminal and press enter. In case of problems, [contact us](mailto:wilddatasets@gmail.com).

### Step 1: Install Git and uv

[uv](https://docs.astral.sh/uv/) is a tool for installing Python apps. Run the commands for your system.

**Windows**
```
winget install --id Git.Git -e
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Mac**
```
xcode-select --install
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Linux** (Debian/Ubuntu)
```
sudo apt install git
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Install the app

Close the terminal and open a new one. Then run the following command, which is the same for all systems.

```
uv tool install git+https://github.com/sadda/wildlife-app
```

## Updating the app

Open a terminal and run
```
uv tool install --reinstall git+https://github.com/sadda/wildlife-app
```

## Running the app

The app stores the dataset and your answers in the folder where it is started. Therefore, first create a folder for your project and move into it. The first time, open a terminal and run
```
mkdir turtles_of_smsrc
cd turtles_of_smsrc
wildlife-app turtles_of_smsrc
```
Next time, open a terminal and run only
```
cd turtles_of_smsrc
wildlife-app turtles_of_smsrc
```
If you run a different project than TurtlesOfSMSRC, change the project name (such as `turtlewatch_egypt`). Always run the app from the same folder, otherwise it will not find your data and answers.

When the app starts for the first time, it will begin downloading the dataset, which may take half an hour. For TurtlewatchEgypt, some files cannot be downloaded and must be copied into the `data` subfolder manually. The app tells you which ones are missing.

## Using the app

Using the app should be straightforward. Press Same (Q), Different (W) or Unknown (E) for validating whether the two shown turtles are the same. Use Previous (A) and Next (S) to move to the following images without giving an answer or to check the previous answer. You can also move to the next body part if the matching was performed across multiple body parts. It is highly recommended to use the keyboard shortcuts Q, W, E, A and S. The answers are saved to the file `answers.csv`.

When a dataset is updated, it should be downloaded by the corresponding button. Similarly, when new predictions are available for verification, they can be automatically downloaded. The last button downloads segmentation masks, which are used to crop turtle heads and flippers.