# Image Comparator

Image Comparator is an app for checking whether two photos show the same individual animal. It is the manual step of a mostly automated re-identification pipeline:

1. The [animal_re_id](https://github.com/sadda/turtle_re_id) package compares new photos (the **query**) with photos of known individuals (the **database**) and proposes the most likely pairs.
2. In Image Comparator, you answer for every proposed pair whether the two animals are the same.
3. Your answers are used to assign identities to the new photos.

The computer does the time-consuming search through all photos. You only check a few of the most promising candidates, and every identity is confirmed by a human.

<img src="resources/app.png" alt="Image Comparator" width="600">

## What the app does for you

- **Shows the pairs one by one**, ordered from the most promising, together with the body part (for example the head) that produced the match.
- **Skips pairs whose answer is already known** from your previous answers.
- **Prevents contradictions** between your answers.
- **Saves every answer immediately**, so you can close the app at any time and continue later.

## Next steps

- [Installation](installation.md) of the app.
- [Usage](usage.md): running the app and answering the pairs.
