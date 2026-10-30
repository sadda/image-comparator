# Installation

All commands below are run in a terminal, a text window where commands are typed. To open it:

- **Windows**: press the Windows key, type `cmd` or `powershell` and press Enter.
- **Mac**: press Cmd+Space, type `terminal` and press Enter.
- **Linux**: press Ctrl+Alt+T.

Paste each command into the terminal and press Enter.

## Step 1: Install Git and uv

[uv](https://docs.astral.sh/uv/) is a tool for installing Python apps. Run the commands for your system.

=== "Windows"

    ```
    winget install --id Git.Git -e
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

=== "Mac"

    ```
    xcode-select --install
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Linux (Debian/Ubuntu)"

    ```
    sudo apt install git
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

## Step 2: Install the app

Close the terminal and open a new one. Then run the following command, which is the same for all systems:

```
uv tool install git+https://github.com/sadda/image-comparator
```

## Updating the app

Open a terminal and run

```
uv tool install --reinstall git+https://github.com/sadda/image-comparator
```

In case of problems, [contact us](mailto:wilddatasets@gmail.com).
