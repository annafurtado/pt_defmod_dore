[<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" />](http://creativecommons.org/licenses/by-nc-sa/4.0/)

***<span style="font-size: 3em;">:warning:</span>You must agree to the [license](https://github.com/annafurtado/pt_defmod_dore/blob/main/LICENSE.txt) and terms of use before using the dataset in this repo.***

# DORE: Definition MOdelling in PoRtuguEse
This repository introduces **DORE**, a comprehensive corpus of over 100,000 definitions from Portuguese dictionaries. Alongside **DORE**, we also introduce the models used to perform Portuguese DM. The release of **DORE** aims to fill in the gap of resources for Automatic Definition Generation, or Definition Modelling (DM), in Portuguese. **DORE** is the first dataset released for Portuguese DM.

## Data Collection

For **version 1.0**, we collected pairs of lemma, definition from two e-dictionaries in Portuguese. See the following table for more details. 

|     Source        |  Amount  |
|-------------------|----------|
| Wiktionary  *( <https://pt.wiktionary.org/wiki/Wikcion%C3%A1rio:P%C3%A1gina_principal> )*       |  19,038   |
| Dicio  *( <https://www.dicio.com.br/> )*       |  83,981   |
| **Total**         | **103,019** |

One of the .json files is shown below. 

```json
[{"id": "pt.024", "lemma": "trouxa", "gloss": "pessoa que se deixa enganar com facilidade; quem é facilmente enganado ou iludido: o trouxa ainda acredita em tudo que ele fala."},
{"id": "pt.025", "lemma": "boxeador", "gloss": "pugilista; lutador de boxe; pessoa que, profissionalmente ou não, pratica boxe ou pugilismo."}]
```

## Data
**DORE** is available in [HuggingFace](https://huggingface.co/datasets/multidefmod/dore) and can be downloaded using the following code. 

```python
from datasets import load_dataset

dore = load_dataset('multidefmod/dore')
```


## Citation
If you are using the dataset or the models, please cite the following paper.

~~~
﻿@inproceedings{dore2024,
author={Furtado, Anna B Dimas and Ranasinghe, Tharindu and Blain, Fréderic and Mitkov, Ruslan},
title={{DORE: A Dataset For Portuguese Definition Generation}},
booktitle={The 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)},
year={2024},
month={May},
}
~~~