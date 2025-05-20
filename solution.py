import os
import numpy as np
from PIL import Image
from sklearn.neighbors import KNeighborsClassifier


def extract_signals(im,font_width,col_start,n_char,signal_cutoff):
    """
    Threshold image im by signal_cutoff, cut into pieces specified by the parameters
    font_width, col_start, n_char, signal_cutoff (see class Captcha for parameter descriptions).
    Return:
       list of binary image pieces
    """
    ##we simply take the first channel and apply the cutoff
    x0=np.array( ~(im[:,:,0]<signal_cutoff), dtype='float32' )
    return [x0[:,col_start+j*font_width:col_start+(j+1)*font_width] for j in range(n_char)]


def load_input_output(input_path,output_path):
    """
    Load all jpg images from input_path, find matching output label text file in output_path.
    Only add matching input/output pairs into the returned lists.
    Return (2-tuple):
       list of input images
       list of matching output texts
    """
    inputs=[]
    outputs=[]
    for fname in os.listdir(input_path):
        if fname.startswith('input') and fname.endswith('.jpg'):
            idx=fname.split('.')[0][5:]
            out_fname=os.path.join(output_path,'output{}.txt'.format(idx)) ##find matching output file
            if os.path.exists(out_fname):
                inputs.append(np.array(Image.open(os.path.join(input_path,fname))))
                with open(out_fname,'r') as fp:
                    lines=fp.readlines()
                outputs.append(lines[0])
    return inputs,outputs


class Captcha(object):
    def __init__(self, input_path, output_path, 
                 font_width=9, col_start=5, n_char=5, signal_cutoff=100 ):
        """ 
        Read and process all input/output pairs in the specified folders.
        Build a 1NN classifier with the input/output pairs.
        Optional parameters provide a little extra flexibility in case there is a change in input structure.
        
        args:
            input_path (str): folder path of input jpg files
            output_path (str): folder path of output (one-line) txt files
            font_width (int): font width in pixels
            col_start (int): starting offset of first Captcha character (in pixels from left)
            n_char (int): number of Captcha characters
            signal_cutoff (int): pixel cutoff value for signal
        """
        inputs,outputs=load_input_output(input_path,output_path)
        
        label2prototype={}
        for im,y in zip(inputs,outputs):
            li_pieces = extract_signals(im,font_width,col_start,n_char,signal_cutoff)
            for x,label in zip(li_pieces,y):
                label2prototype[label]=x ## simply keep one prototype per class

        ## Build a 1NN classifier
        prototype_features=np.array([label2prototype[label].flatten() for label in sorted(label2prototype.keys())])
        self.classifier = KNeighborsClassifier(n_neighbors=1)
        self.classifier.fit(prototype_features,sorted(label2prototype.keys()))

        self.font_width=font_width
        self.col_start=col_start
        self.n_char=n_char
        self.signal_cutoff=signal_cutoff
                    
    def __call__(self, im_path, save_path):
        """
        For inference, load an input Captcha image and save output labels to a one-line text file.
        
        args:
            im_path (str): .jpg image path to load and to infer
            save_path (str): output file path to save the one-line outcome
        """
        if os.path.exists(im_path):
            try:
                im = np.array(Image.open(im_path))
                li_pieces = extract_signals(im,self.font_width,self.col_start,self.n_char,self.signal_cutoff)
                input_features = np.array([x.flatten() for x in li_pieces])
                predicted = self.classifier.predict(input_features)
                with open(save_path,'w') as fp:
                    fp.write(''.join(predicted.tolist())+'\n')
            except:
                print('Something went wrong...') ## we omit error handling for this example
        else:
            print('Image',im_path,'not found!')
            
