# Image Comparator

This repo provides an app for validating whether two images depict the same individual. It is part of a large, mostly automated pipeline that takes photos of one animal species as input and outputs photos showing the same individuals.

<img src="https://github.com/sadda/image-comparator/raw/master/docs/resources/app.png" alt="App photo" width="500">

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
uv tool install git+https://github.com/sadda/image-comparator
```

## Updating the app

Open a terminal and run
```
uv tool install --reinstall git+https://github.com/sadda/image-comparator
```

## Running the app

The app stores the dataset and your answers in the folder where it is started. Therefore, first create a folder for your project and move into it. To try the app on a small example, open a terminal and run
```
mkdir example
cd example
image-comparator example --download
```
Next time, open a terminal and run only
```
cd example
image-comparator example
```
Always run the app from the same folder, otherwise it will not find your data and answers.

The example is a small subset of [SeaTurtleID2022](https://www.kaggle.com/datasets/wildlifedatasets/seaturtleid2022) with 6 query encounters and 4 turtles in the database. Four of the query turtles are in the database. The remaining two (`t048` and `t323`) are new individuals, so all their pairs should be answered Different. The true identity is visible in the encounter name (such as `unknown_t048`) so that you can check your answers. The example data were created by the [introduction notebook](https://github.com/sadda/turtle_re_id/blob/master/examples/introduction.ipynb). Note that the first 4 pairs shown are wrong matches as they show a new individual not present in the database.

For a real project, replace `example` with the project name, such as `turtles_of_smsrc`. The `--download` option downloads the dataset, which may take tens of minutes, together with the segmentation and the data for verification. Use it also when you are told that a new version of the dataset is available. When only new verification data or segmentation is available, use `--download-files` instead, which skips the slow dataset download.

## Using the app

Using the app should be straightforward. Press Same (Q), Different (W) or Unknown (E) for validating whether the two shown turtles are the same. Use Previous (A) and Next (S) to move to the following images without giving an answer or to check the previous answer. You can also move to the next body part if the matching was performed across multiple body parts. It is highly recommended to use the keyboard shortcuts Q, W, E, A and S. The answers are saved to the file `answers.csv`.
