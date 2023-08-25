[![GitHub Stars](https://img.shields.io/github/stars/wjbmattingly/number-spacy?style=social)](https://github.com/wjbmattingly/number-spacy)
[![PyPi Version](https://img.shields.io/pypi/v/number-spacy)](https://pypi.org/project/number-spacy/0.0.1/)
[![PyPi Downloads](https://img.shields.io/pypi/dm/number-spacy)](https://pypi.org/project/number-spacy/0.0.1/)

# Number spaCy

![number spacy logo](https://github.com/wjbmattingly/number-spacy/blob/main/images/number-spacy-logo.png?raw=true)

Number spaCy is a custom spaCy pipeline component that enhances the identification of number entities in text and fetches the parsed numeric values using spaCy's token extensions. It uses RegEx to identify number entities written in words and then leverages the [word2number](https://github.com/akshaynagpal/w2n) library to convert those words into structured numeric data. The output numeric value is stored in a custom entity extension: `._.number`.

This lightweight component can be seamlessly added to an existing spaCy pipeline or integrated into a blank model. If using within an existing spaCy pipeline, ensure to insert it before the NER model.

## Installation

To install Number spaCy, execute:

```bash
pip install number-spacy
```

## Usage

### Integrating the Component into your spaCy Pipeline

Begin by importing the `find_numbers` component and then integrating it into your spaCy pipeline:

```python
import spacy
from number_spacy import find_numbers

# Initialize your preferred spaCy model
nlp = spacy.blank('en')

# Integrate the component into the pipeline
nlp.add_pipe('find_numbers')
```

### Text Processing with the Pipeline

Post the component addition, you can process text as you typically would:

```python
doc = nlp("I have three apples. She gave me twenty-two more, and now I have twenty-five apples in total.")
```

### Retrieving the Parsed Numbers

You can loop through the entities in the `doc` and access the specific number extension:

```python
for ent in doc.ents:
    if ent.label_ == "NUMBER":
        print(f"Text: {ent.text} -> Parsed Number: {ent._.number}")
```

This should output:

```
Text: three -> Parsed Number: 3
Text: twenty-two -> Parsed Number: 22
Text: twenty-five -> Parsed Number: 25
```
