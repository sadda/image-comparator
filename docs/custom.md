# Custom datasets

The provided example downloads everything it needs. To verify your own photos, you describe your dataset in a config file. No coding is needed.

## Identification and discovery

The app supports two types of tasks:

- **Identification**: for projects with an established database, where new photos are matched with known individuals.
- **Discovery**: for new projects without an established database, where new photos are matched among themselves.

## What the app needs

The app uses the files created by [animal_re_id](https://github.com/sadda/turtle_re_id), for example in its [introduction notebook](https://colab.research.google.com/github/sadda/turtle_re_id/blob/master/examples/introduction.ipynb):

- **Photos**: `metadata.csv` and `segmentation.csv` created by animal_re_id. The data structure must be the same as the one passed to animal_re_id. The photos are usually in the local `data` folder, but can be anywhere by using the config below.
- **Pairs**: `verification_data.csv` exported by animal_re_id. Copy it to the folder where the app is started.

The app creates `answers.csv` in the folder where it is started. Use a separate folder for every dataset.

## Running the app

The app has two built-in configs, `identification` and `discovery`, which read the data from the folder `data`. The tabs below show the commands for both. Selecting a tab switches all tabs on this page. To start the app, run

=== "Identification"

    ```
    image-comparator identification
    ```

    The folder `data` contains the folders `query` and `database`, each containing `metadata.csv` and `segmentation.csv`.

=== "Discovery"

    ```
    image-comparator discovery
    ```

    The folder `data` contains `metadata.csv` and `segmentation.csv`.

## Custom config

If the data are elsewhere, create a config file, for example `my_project.json`, with the path to the data and run the app with it:

=== "Identification"

    ```json
    {
      "root": "/path/to/turtle_re_id/examples/data"
    }
    ```

    ```
    image-comparator identification --config my_project.json
    ```

=== "Discovery"

    ```json
    {
      "root": "/path/to/my/query"
    }
    ```

    ```
    image-comparator discovery --config my_project.json
    ```

The config file is merged into the built-in config, so it only needs the keys you want to change:

| Key | Meaning |
|-----|---------|
| `root` | Folder with the data described in [Running the app](#running-the-app). A relative path is relative to the folder where the app is started. Default `data`. |
| `url` | Optional. Link to a zip file with the content of `root`, downloaded by `--download`. |
| `downloads` | Optional. Files downloaded by `--download` and `--download-files`, as `{"path": "link"}`. |

## Sharing a dataset with annotators

If other people verify the pairs, upload the data and let the app download them:

=== "Identification"

    1. Zip the folders `query` and `database` into one file and upload it.
    2. Upload `verification_data.csv`.
    3. Send the annotators the config file with both links:

    ```json
    {
      "url": "https://example.org/my_project/data.zip",
      "downloads": {
        "verification_data.csv": "https://example.org/my_project/verification_data.csv"
      }
    }
    ```

    The annotators save the config file in an empty folder and run there

    ```
    image-comparator identification --config my_project.json --download
    ```

    !!! warning
        The option `--download` downloads the data, which may take a long time. Use it only the first time. Next time, run in the same folder only

        ```
        image-comparator identification --config my_project.json
        ```

=== "Discovery"

    1. Zip `metadata.csv`, `segmentation.csv` and the photos into one file and upload it.
    2. Upload `verification_data.csv`.
    3. Send the annotators the config file with both links:

    ```json
    {
      "url": "https://example.org/my_project/data.zip",
      "downloads": {
        "verification_data.csv": "https://example.org/my_project/verification_data.csv"
      }
    }
    ```

    The annotators save the config file in an empty folder and run there

    ```
    image-comparator discovery --config my_project.json --download
    ```

    !!! warning
        The option `--download` downloads the data, which may take a long time. Use it only the first time. Next time, run in the same folder only

        ```
        image-comparator discovery --config my_project.json
        ```

The zip file is extracted into `root`. Therefore, the files and folders must be at the top level of the zip file, not inside another folder. The paths in `metadata.csv` must be relative and the photos must be inside the zip file, otherwise the annotators cannot find them.

When you prepare new pairs, upload the new `verification_data.csv` to the same link. The annotators move their old `answers.csv` away and run the app with `--download-files` instead of `--download`, which downloads only `verification_data.csv` and skips the slow download of the photos.
