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

 *For text payload:*
 
   Encryption is solely depend on the text file. Upon Decryption, MessageBox will display the payload text.
 
 *For image payload:*
 
   Encryption is based on image file. Stego Image file will be saved as `finalstego.png`
   Upon Decryption, the image payload will be saved to local directory. Recovered Stego Image file will be saved as `RecoveredHiddenImage.png`
   
 *Summary for Image payload:*
 
1.	Upon selection of image from ‘<select>’ button, image will be compressed into a 200 x 300        dimension and previewed in the image panel of the GUI
2.	Dimensions and size of the original vessel image will be shown in the GUI as well
3.	Same concept goes to the selection of the target Image
   a.	If both target and vessel image does not pop up inside the image panel, restart your             program, or select a different image
      i.	This is due to the fact that the image is too big to be compressed into the 200 x 300            format
4.	Embedding of the image goes like this:
   a.	Vessel image will be converted into PBC (Pure Binary Code) 
   b.	Then it will be converted into CGC (Cannonical Gray Code)
   c.	This makes the insertion of the BPCS planes less intrusive
   d.	Image will be iterated through
      i.	Separates the image, bit plane wise 
      ii.	Iterates each plane and for each complex plane located, it breaks the loop
   e.	Meanwhile, target image is transformed into CGC as well and separated into 8 bit planes
   f.	Once a complex plane is found inside the the vessel image, program inserts bit (target           image) into the said plane and continues the loop of iteration of the vessel image plane
   g.	Upon insertion, the conjugation method is called to mark the area that has been conjugated
   h.	Each bit of the conjugation map represents a target image block
   i.	Once conjugation is complete, program transforms image back to PBC from CGC
5.	Recovery of hidden image goes like this:
   a.	Program transforms vessel image to CGC from PBC
   b.	Iteration is executed to loop through the vessel image planes
   c.	Program checks whether a target shape exists
   d.	If exists, conjugation map is printed out from the bits located inside the complex planes       and recovered
   e.	Bits are reassembled and recovered into an Image named `RecoveredHiddenImage.png`

   
  
## Notes
All the images used are non-directory "images" and the forms removed and modified from the site [Pexels](https://www.pexels.com/public-domain-images/), being transformed into `.png` and reduced or size for simpler tests.

The main methods used are: read, save and manipulate the images using the imageio and numpy python libraries; transform imagem from Pure Binary Code to Canonical Gray Code and vice-versa; Check if a block of a bit plane is considered complex.

By Git do not receive files larger than 25MB, some repository images and two tests will not be available.

Alpha Value: `.png` images follows the RGBA color model. It is an extension of the RGB channels, representing the transparency of pixels. From a range of 0 to 255, in which 0 means image will be total transparent while 255 means image will be opaque. 

Disclaimer: Payload Image **should not** have be of a bigger image size as compared to the Vessel Image.
