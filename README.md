# simpleCaptcha

This git project contains solution to the simple Captcha recognition task. The complete
reasoning and process behind the provided solution can be seen in the included notebook `solution-approach.ipynb`.

The solution code is provided in a single python script `solution.py`. A simple test script `test.py` is provided to quickly
test the solution.

The input images and output text labels are not included in this git repository -- please download and place them under
the `input` and `output` folders, respectively.

## Installation

Requirements in terms of the python environment are minimal, and are given in `requirements.txt`. It should work on 
any recent 3.x python version. Here is an example using `conda`, assuming running from the project folder:
```
>> conda create -n captcha python=3.9
>> conda activate captcha
>> pip install -r requirements.txt
```

## Testing

To test the solution after setting up the environment, first make sure the `input` and `output` folders have been downloaded
and placed in the project folder. Then:
```
>> python test.py
```
will build the model, test it on the input image `input/input100.jpg`, and print the output text file.




