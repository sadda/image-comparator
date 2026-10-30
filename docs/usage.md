# Usage

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

### Real projects

For a real project, replace `example` by the project name, such as `turtles_of_smsrc`:

| Option | When to use it |
|--------|----------------|
| `--download` | The first time, or when you are told that a new version of the dataset is available. Downloads the photos, which may take tens of minutes, and the files for verification. |
| `--download-files` | When only new pairs for verification are available. Skips the slow download of the photos. |
| no option | Every other time. |

## Identification and discovery

The app works in one of two modes. The mode is selected automatically by the project.

| | **Identification** | **Discovery** |
|---|---|---|
| Question | Which known individual is this? | Which of these photos show the same individual? |
| Left photo | Query encounter | Query encounter |
| Right photo | Database identity | Another query encounter |
| Result | Every query encounter gets one identity from the database, or is marked as new. | Query encounters are grouped into individuals. |
| Projects | `example`, `turtlewatch_egypt` | `turtles_of_smsrc` |

**Identification** is used when there is a database of known individuals, for example a catalogue of photo-identified turtles. **Discovery** is used when there is no such database, or when the new photos may contain many individuals that are not in it. It finds which encounters belong together, so that each group can be given a new identity.

An **encounter** is a group of photos of one animal taken at one occasion, for example on one day. Answers are always given for whole encounters, not for single photos.

## Answering the pairs

The app shows a pair of photos. The title shows the number of the pair and the similarity (the number of matched keypoints). Decide whether the two photos show the same individual.

| Button | Key | Meaning |
|--------|-----|---------|
| **Same** | Q | The two photos show the same individual. |
| **Different** | W | The two photos show different individuals. |
| **Unknown** | E | You cannot decide. The pair stays unanswered. |
| **Previous** | A | Go back to the previous pair, for example to change an answer. |
| **Next** | S | Go to the next pair without answering. |
| **Next encounter** / **Next body part** | – | Jump to the next group of pairs (see below). |
| **Toggle heads left / right** | R / F | Show other head photos of the left or right individual. |
| **Reset** | V | Show the original pair again. |

!!! tip
    Use the keyboard shortcuts Q, W, E, A and S. They make the verification much faster.

!!! tip
    Answer **Unknown** if you are not sure. An unanswered pair is better than a wrong answer.

Pairs whose answer already follows from your previous answers are skipped automatically. The rules differ between the two modes.

### Identification

The pairs are grouped by query encounter, starting with the most similar candidates. **Next encounter** jumps to the first unanswered pair of the next query encounter. **Toggle heads** shows other head photos of the query encounter (left) or of the database identity (right).

A pair is skipped when

- the query encounter was already answered **Same** for some identity, or
- the query encounter was already answered **Different** for this identity, for example on another body part.

A query encounter can be the same as only one identity. If you answer **Same** for a second identity, the answer is not accepted and a message is shown. To change it, go back and change the first answer.

The text box below the photos shows how many query encounters are

- **identified**: one candidate was answered Same,
- **new**: all candidates were answered Different, so the individual is most likely not in the database,
- **open**: still waiting for answers.

### Discovery

The pairs are grouped by body part (for example heads first, then flippers), starting with the most similar pairs. **Next body part** jumps to the first unanswered pair of the next body part. **Toggle heads** shows other head photos of the left or right encounter.

Answering **Same** joins the two encounters into one individual. These groups grow as you answer: if A is the same as B and B is the same as C, then A, B and C are one individual. A pair is skipped when

- the two encounters are already in the same group, or
- the two groups were already answered **Different** by another pair.

Encounters that already have a known identity are treated as that identity.

The text box below the photos shows for every body part how many pairs were **answered** by you and how many are **decided**, either by your answer or by the rules above.

### Finishing

When all pairs are answered or skipped, the app shows a message and closes.

## Your answers

The answers are saved after every click to `answers.csv` in the project folder. You can close the app at any time and continue later from where you left off.

`answers.csv` contains all proposed pairs (the same rows as `verification_data.csv`) with two additional columns:

| Column | Content |
|--------|---------|
| `answer` | `same`, `different`, or empty for unanswered pairs |
| `time` | Seconds spent on the pair |

Send this file back to the person who prepared the verification.

!!! warning
    `answers.csv` belongs to one `verification_data.csv`. When you receive new pairs (`--download-files`), first move the old `answers.csv` to another folder or rename it. Otherwise the app reports that `answers.csv` has wrong format and closes.
