# Introduction
Digital Steganography allows user to hide confidential information by embedded secret data into media outlets known as a "Vessel Data".
It conceals the payload(secret data) from plain sight in the form of text/image file in a vessel image via **BPCS Method (Bit-Plane Complexity Segmentation)** 

The aim of the project is to utilize and implement the BPCS method of steganography, which in this case, will serve to hide an image in another(encode) and to be recovered(decode). This method consists in hiding pixels from the image in blocks of a bit plane whose bits are from. If the image possess a noisy behavior, it takes advantage of the characteristic of human vision to concentrate not to reconcile patterns and shapes. Hence, for a 'normal' image, roughly 50% of the data might be replaceable with secret data before image degradation becomes apparent.

## Demo - Image (Payload)
![Demo_image](https://user-images.githubusercontent.com/50063565/94983567-87f21080-0576-11eb-914b-877b7cc7657b.gif)


## Tkinter

Tkinter is Python's de-fecto standard GUI toolkit.

## Prerequisites
 1. Numpy
 2. Imageio
 3. OpenCV
 4. PIL, pillow

## Installation

The `requirements.txt` file should list all Python libraries that your notebooks depend on, and they will be installed using:

 ```bash
 $pip install -r requirements.txt 
 ```
In this case, your requirement file contains a pinned version of everything that was installed when pip freeze was run:

 ```bash
 $pip freeze > requirements.txt
 ```
Please make sure to update tests as whenever appropriate.

## Features
 - Upon running `GUI_BPCS.py`, 
 
 ![image](https://user-images.githubusercontent.com/50063565/94983687-b7554d00-0577-11eb-825b-fa4a2207d211.png)
 
 Payload type options: Text(in `.txt`) / Images (in `.png`)
 Methods available: Encode / Decode
 ```
 For text payload:
 ```
  Encryption is solely depend on the text file. Upon Decryption, MessageBox will display the payload text.
 ```
 For image payload:
 ```
  Encryption is based on image file. Stego Image file will be saved as `finalstego.png`
  Upon Decryption, the image payload will be saved to local directory. Recovered Stego Image file will be saved as `RecoveredHiddenImage.png`
  
## Notes
All the images used are non-directory "images" and the forms removed and modified from the site [Pexels](https://www.pexels.com/public-domain-images/), being transformed into `.png` and reduced or size for simpler tests.

The main methods used are: read, save and manipulate the images using the imageio and numpy python libraries; transform imagem from Pure Binary Code to Canonical Gray Code and vice-versa; Check if a block of a bit plane is considered complex.

By Git do not receive files larger than 25MB, some repository images and two tests will not be available.

Alpha Value: `.png` images follows the RGBA color model. It is an extension of the RGB channels, representing the transparency of pixels. From a range of 0 to 255, in which 0 means image will be total transparent while 255 means image will be opaque. 

Disclaimer: Payload Image **should not** have be of a bigger image size as compared to the Vessel Image.
