# Custom datasets

The built-in projects (`example`, `turtles_of_smsrc`, `turtlewatch_egypt`) download everything they need. To verify your own photos, you describe your dataset in a config file. No coding is needed.

## What the app needs

The app uses the files created by [animal_re_id](https://github.com/sadda/turtle_re_id) in its [introduction notebook](https://colab.research.google.com/github/sadda/turtle_re_id/blob/master/examples/introduction.ipynb):

- **Photos**: the folder with the `query` and `database` subfolders (`data` in the notebook), including `metadata.csv` and `segmentation.csv` created by the notebook. Do not change them after the pairs were created, otherwise the app reports that some entries are mismatched.
- **Pairs**: `verification_data.csv` exported by the notebook. Copy it to the folder where the app is started. It must keep this name.

The app creates `answers.csv` in the folder where it is started. Use a separate folder for every dataset.

## Config file

Create a config file, for example `my_project.json`:

```json
{
  "dataset": "Example",
  "root": "/path/to/turtle_re_id/examples/data",
  "url": null
}
```

| Key | Meaning |
|-----|---------|
| `dataset` | Type of the dataset. `Example` is a general dataset with a `query` and a `database` folder. |
| `root` | Folder containing `query` and `database`. A relative path is relative to the folder where the app is started. |
| `url` | Link to a zip file with the `query` and `database` folders, downloaded by `--download`. Use `null` if the data are already in place. |
| `downloads` | Optional. Files downloaded by `--download` and `--download-files`, as `{"path": "link"}`. |

Then start the app from the folder with `verification_data.csv`:

```
image-comparator my_project --config my_project.json
```

The first argument is only a name. For a name that is not a built-in project, `--config` is required.

## Sharing a dataset with annotators

If other people verify the pairs, upload the data and let the app download them:

1. Zip the `query` and `database` folders into one file and upload it.
2. Upload `verification_data.csv`.
3. Send the annotators the config file with both links:

```json
{
  "dataset": "Example",
  "root": "data",
  "url": "https://example.org/my_project/data.zip",
  "downloads": {
    "verification_data.csv": "https://example.org/my_project/verification_data.csv"
  }
}
```

The annotators save the config file in an empty folder and run there

```
image-comparator my_project --config my_project.json --download
```

When you prepare new pairs, upload the new `verification_data.csv` to the same link. The annotators move their old `answers.csv` away and run the app with `--download-files`, which skips the download of the photos.

## Changing a built-in project

The config file is merged into the config of a built-in project. Only the keys in your file are changed. For example, to store the example data in another folder, create `my_example.json` with

```json
{
  "root": "/path/to/my/data"
}
```

and run `image-comparator example --config my_example.json`. The built-in configs are in [image_comparator/configs](https://github.com/sadda/image-comparator/tree/master/image_comparator/configs).

## Limitations

- The `Example` dataset type always compares the query with the database (identification). Discovery, where the query is compared with itself, is available only for the built-in `turtles_of_smsrc` project.
- Other folder structures need a new dataset type in the code. It is a subclass of `WildlifeDataset` in `image_comparator/datasets/datasets.py` with the methods `download_dataset`, `is_downloaded` and `load`, registered in `DATASETS` in `image_comparator/main.py`. If `load` sets `query` and `database` to the same dataset, the app uses discovery.
