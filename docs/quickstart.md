# Quick start

## Starting the app

The app stores the photos and your answers in the folder where it is started. Therefore, first create a folder for your project and move into it. To try the app on a small example, run

```
mkdir example
cd example
image-comparator example --download
```

Next time, run only

```
cd example
image-comparator example
```

!!! warning
    Always start the app from the same folder, otherwise it will not find your photos and answers. The app refuses to start in your home folder.

### The example

The example is a small subset of [SeaTurtleID2022](https://www.kaggle.com/datasets/wildlifedatasets/seaturtleid2022) with 6 query encounters and 4 turtles in the database. Four of the query turtles are in the database. The remaining two (`t048` and `t323`) are new individuals, so all their pairs should be answered **Different**. The true identity is visible in the encounter name (such as `unknown_t048`) so that you can check your answers. The first 4 pairs are wrong matches, because they show a new individual.

## Answering the pairs

The app shows a pair of photos: a query encounter on the left and a candidate on the right. An **encounter** is a group of photos of one animal taken at one occasion, for example on one day. The title shows the number of the pair and the similarity (the number of matched keypoints). Decide whether the two photos show the same individual.

| Button | Key | Meaning |
|--------|-----|---------|
| **Same** | Q | The two photos show the same individual. |
| **Different** | W | The two photos show different individuals. |
| **Unknown** | E | You cannot decide. The pair stays unanswered. |
| **Previous** | A | Go back to the previous pair, for example to change an answer. |
| **Next** | S | Go to the next pair without answering. |
| **Next encounter** / **Next body part** | – | Jump to the first unanswered pair of the next encounter or body part. |
| **Toggle heads left / right** | R / F | Show other head photos of the left or right individual. |
| **Reset** | V | Show the original pair again. |

!!! tip
    Use the keyboard shortcuts Q, W, E, A and S. They make the verification much faster.

!!! tip
    Answer **Unknown** if you are not sure. An unanswered pair is better than a wrong answer.

Pairs whose answer already follows from your previous answers are skipped automatically. For example, once an encounter was answered **Same**, its remaining candidates are not shown. If an answer would contradict your previous answers, it is not accepted and a message is shown. To change it, go back and change the previous answer.

The text box below the photos shows the progress of the verification.

### Finishing

When all pairs are answered or skipped, the app shows a message and closes.

## Your answers

The answers are saved after every click to `answers.csv` in the folder where the app is started. You can close the app at any time and continue later from where you left off.

`answers.csv` contains all proposed pairs (the same rows as `verification_data.csv`) with two additional columns:

| Column | Content |
|--------|---------|
| `answer` | `same`, `different`, or empty for unanswered pairs |
| `time` | Seconds spent on the pair |

Send this file back to the person who prepared the verification.

!!! warning
    `answers.csv` belongs to one `verification_data.csv`. When you receive new pairs (`--download-files`), first move the old `answers.csv` to another folder or rename it. Otherwise the app reports that `answers.csv` has wrong format and closes.
