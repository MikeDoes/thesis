# Evaluation Algorithm from SpanOIE
The code original code is based from Gabriel's Stanovsky's and al. [OIE2016 repository](https://github.com/gabrielStanovsky/oie-benchmark). 
Then, it was adapted for newer labels (Re-OIE2016) by Zhan and al. [SpanOIE repository](https://github.com/zhanjunlang/Span_OIE/).
Finally, it was updated to functional programming for the [master thesis](https://github.com/MikeDoes/thesis).

The command to run the code is <br>
```python evaluate.py``` <br>
```sentence confidence_score predicate arg0 arg1 arg2 ...``` <br>
The script will output the AUC and best F1 score of the system. And the output file is used to draw the pr-curve. The script to draw the pr-curve is [here](https://github.com/gabrielStanovsky/oie-benchmark/blob/master/pr_plot.py).
