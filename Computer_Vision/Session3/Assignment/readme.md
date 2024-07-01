# Your favorite wildlife in Africa!

## Quicklook
This notebook is run on Kaggle P100 to detect all or specific kinds of animals in a image.

The model used are:
* YOLO v5n
* YOLO V8m

Both of the selected models complish the obeject detection work however, accodring to the result of validation, the M50 of V5n is better than V8m.
The reason could be the data used in trainning doesn't need a complex model.

## Content
1. You can find the [notebook](https://github.com/callmeeric5/Epita_AIS/blob/main/Computer_Vision/Session3/Assignment/object-detection.ipynb) to check the experiments have done, incase of the render problems on github please go to [nbviewer](https://nbviewer.org/github/callmeeric5/Epita_AIS/blob/main/Computer_Vision/Session3/Assignment/object-detection.ipynb)
Reminder: The notebook used several sessions on Kaggle but Kaggle doesn't store the cell output of previous session, it may be confusing for readers who pay attention on cell excecution index

2. You can find or download the fine tuned model, YOLO V5n trained in the notebook from here [finetuned model](https://github.com/callmeeric5/Epita_AIS/tree/main/Computer_Vision/Session3/Assignment/model), YOLO V8m can be uploaded due to the size limit of github, but you can train it by running the notebook (it may need over 1 hour)
   
## Evaluation
* Documentation(markdown) ✅
* Code(python) ✅
* Performances ✅
* Application (bonus) ✅
