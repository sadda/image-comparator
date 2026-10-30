<p align="center">
  <a href="https://github.com/sadda/image-comparator/actions/workflows/ci.yml"><img src="https://github.com/sadda/image-comparator/actions/workflows/ci.yml/badge.svg" alt="sadda/image-comparator CI"></a>
  <a href="https://sadda.github.io/image-comparator/"><img src="https://img.shields.io/badge/docs-online-blue" alt="Documentation"></a>
</p>

# Image Comparator

This repo is part of a [larger pipeline](https://github.com/sadda/turtle_re_id) for animal re-identification. The detection and identification of individuals are performed automatically. To prevent machine errors, all automated predictions can be manually verified in this app. The outputs of this verification are meant to be pushed back into the pipeline. For a general overview, see the provided [Google Colab notebook](https://colab.research.google.com/github/sadda/turtle_re_id/blob/master/examples/introduction.ipynb).

<img src="https://github.com/sadda/image-comparator/raw/master/docs/resources/app.png" alt="App photo" width="500">

## Installation

See the [installation guide](https://sadda.github.io/image-comparator/installation/).

## Quick start

The app stores the dataset and your answers in the folder where it is started. To try it on a small example, run

```
mkdir example
cd example
image-comparator example --download
```

For a proper description, see the [documentation](https://sadda.github.io/image-comparator/quickstart/).

Press Same (Q), Different (W) or Unknown (E) for every pair. The answers are saved to `answers.csv`.

## Documentation

The [documentation](https://sadda.github.io/image-comparator/) explains how to run the app for real projects, all buttons and the format of the answers.
