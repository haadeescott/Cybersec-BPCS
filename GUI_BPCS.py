import cv2
import numpy as np
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import PIL
import imageio
import math
import os
from pathlib import Path
from PIL import Image
from PIL import ImageTk
import time
import ctypes
import bpcs
import image_bpcs_process


try:
	import Tkinter as tk
except:
	import tkinter as tk

image_display_width = 300
image_display_height = 200

class MainApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self._frame = None
		self.switch_frame(MenuPage)

	def switch_frame(self, frame_class):
		new_frame = frame_class(self)
		if self._frame is not None:
			self._frame.destroy()
		self._frame = new_frame
		self._frame.pack()


class MenuPage(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.master.title('BPCS Steganography')
		tk.Label(self, text="BPCS Steganography", font=('Helvetica', 40, "bold")).pack(side="top", fill="x", pady=5)
		tk.Label(self,text="Please Choose Type Of Payload",font=('Helvetica',20,"bold")).pack(side="top")
		tk.Button(self, text="Text File",
				  command=lambda: master.switch_frame(TextSteganography),height=3,width=30,font=('Aerial',20,"bold")).pack(pady=10)
		tk.Button(self, text="Image",
				  command=lambda: master.switch_frame(ImageSteganography),height=3,width=30,font=('Aerial',20,"bold")).pack(pady=10)



# Interface for Text Payload Steganography
class TextSteganography(tk.Frame):
	def __init__(self,master):
		tk.Frame.__init__(self, master)
		tk.Label(self, text="BPCS Steganography", font=('Helvetica', 40, "bold")).pack(side="top", fill="x", pady=5)
		tk.Label(self,text="Payload Type: Text File",font=('Helvetica',20,"bold")).pack(side="top")
		tk.Button(self, text="Encode",
				  command=lambda: master.switch_frame(EncodeText),height=3,width=30,font=('Aerial',20,"bold")).pack(pady=10)
		tk.Button(self, text="Decode",
				  command=lambda: master.switch_frame(DecodeText),height=3,width=30,font=('Aerial',20,"bold")).pack(pady=10)
		tk.Button(self, text="Back",
				  command=lambda: master.switch_frame(MenuPage), height=3, width=30,font=('Aerial', 20, "bold")).pack(pady=10)

# Interface for Image Payload Steganography
class ImageSteganography(tk.Frame):
	left_img = None
	left_photo = None
	right_img = None
	right_photo = None
	stego_img = None
	stego_photo = None
	def __init__(self,master):
		tk.Frame.__init__(self, master)
		self.file_name = ''
		self.pack()
		self.create_widgets()

	def open_file(self):
		# inside window open file window, only PNG files are selected
		self.file_name = askopenfilename(filetypes=[('PNG File', '*.PNG')])

		# to store file name as vessel name in BPCS.py
		image_bpcs_process.vessel_name = self.file_name

		# deletes path and only extracts the filename
		filename_only = Path(self.file_name).stem

		# to change label text dynamically according to file name
		self.name_label['text'] = 'Name: ' + filename_only

		#  left image/photo is the picture that is uploaded
		global left_img
		left_img = None
		global left_photo
		left_photo = None

		left_img = Image.open(self.file_name)

		# once file is uploaded, clear image in target canvas
		self.stego_img_canvas.delete("all")
		self.stego_img_canvas.create_text(150, 100, fill="darkblue", font="Times 10 bold",
										  text="Stego/Hidden Img will be displayed here")

		# to retrieve and display dimensions(in px) and size(in KB) of uploaded image
		width, height = left_img.size
		imageKBsize = os.path.getsize(self.file_name) / 1000
		self.dimensions_label['text'] = 'Dimensions: ' + str(width) + 'px' + ' x ' + str(height) + 'px'
		self.size_label['text'] = 'Size: ' + str(imageKBsize) + 'KB'

		# resize image
		scale_width = image_display_width / width
		scale_height = image_display_height / height

		# get smallest compression capability of image
		scale = min(scale_width, scale_height)
		new_width = math.ceil(scale * width)
		new_height = math.ceil(scale * height)

		# Image.NEAREST http://pillow.readthedocs.io/en/4.1.x/releasenotes/2.7.0.html
		# image resize takes a resampling argument which tells which filter to use for resampling
		# image.nearest takes in nearest pixel from input image
		left_img = left_img.resize((new_width, new_height), Image.NEAREST)
		left_photo = ImageTk.PhotoImage(left_img)

		self.left_img_canvas.create_image(image_display_width / 2, image_display_height / 2, anchor=tk.CENTER,
										  image=left_photo)

	def open_targetFile(self):
		# inside window open file window, only PNG files are selected
		self.file_nameTarget = askopenfilename(filetypes=[('PNG File', '*.PNG')])

		# to store file name as Target name in BPCS.py
		image_bpcs_process.target_name = self.file_nameTarget

		# deletes path and only extracts the filename
		filename_only = Path(self.file_nameTarget).stem

		# to change label text dynamically according to file name
		self.name_labelTarget['text'] = 'Name: ' + filename_only

		# right image/photo is the picture that is produced by program
		global right_img
		right_img = None
		global right_photo
		right_photo = None

		right_img = Image.open(self.file_nameTarget)

		# to retrieve and display dimensions(in px) and size(in KB) of uploaded image
		width, height = right_img.size
		imageKBsize = os.path.getsize(self.file_nameTarget) / 1000
		self.dimensions_labelTarget['text'] = 'Dimensions: ' + str(width) + 'px' + ' x ' + str(height) + 'px'
		self.size_labelTarget['text'] = 'Size: ' + str(imageKBsize) + 'KB'

		# resize image
		scale_width = image_display_width / width
		scale_height = image_display_height / height

		# get smallest compression capability of image
		scale = min(scale_width, scale_height)
		new_width = math.ceil(scale * width)
		new_height = math.ceil(scale * height)

		# Image.NEAREST http://pillow.readthedocs.io/en/4.1.x/releasenotes/2.7.0.html
		# image resize takes a resampling argument which tells which filter to use for resampling
		# image.nearest takes in nearest pixel from input image
		right_img = right_img.resize((new_width, new_height), Image.NEAREST)
		right_photo = ImageTk.PhotoImage(right_img)

		self.target_img_canvas.create_image(image_display_width / 2, image_display_height / 2, anchor=tk.CENTER,
											image=right_photo)

	# call operation 1 == embedding target image into vessel image from BPCS.py
	def embedImageMethod(self):
		self.stego_img_canvas.delete("all")
		self.stego_img_canvas.create_text(150, 100, fill="green", font="Times 10 bold",
										  text="Loading. . .")

		vessel_name = self.file_name
		print(str(vessel_name))
		V = imageio.imread(vessel_name).astype(np.uint8)
		Vmult = V.shape[0] * V.shape[1] * V.shape[2]

		target_name = self.file_nameTarget
		T = imageio.imread(target_name).astype(np.uint8)
		Tmult = T.shape[0] * T.shape[1] * T.shape[2]

		final_name = "finalstego.png"

		t = time.time()
		F = image_bpcs_process.BPCS_hide(V, T)
		t = time.time() - t

		f = open(final_name.split('.')[0] + ".txt", "w+")
		f.write("Vessel: " + vessel_name + "\n\tSize: " + str(os.path.getsize(vessel_name)) + " bytes\n")
		f.write("Target: " + target_name + "\n\tSize: " + str(os.path.getsize(target_name)) + " bytes\n")
		f.write("Percentage:\t" + str.format("%.5f" % (100 * Tmult / Vmult)) + "\n")

		if F is None:
			f.write("Insufficient complex blocks to image be inserted.")
			print("Insufficient complex blocks to image be inserted.")
		else:
			imageio.imwrite(final_name, F)
			f.write("Time:\t\t" + str.format("%.5f" % t) + " seconds\n")
			f.write("RMSE:\t\t" + str.format("%.5f" % image_bpcs_process.compareRMSE(V, F)) + "\n")

		f.close()

		# resize stego image for preview

		global stego_img
		stego_img = None
		global stego_photo
		stego_photo = None

		stego_img = Image.open(final_name)

		width, height = stego_img.size
		scale_width = image_display_width / width
		scale_height = image_display_height / height

		# get smallest compression capability of image
		scale = min(scale_width, scale_height)
		new_width = math.ceil(scale * width)
		new_height = math.ceil(scale * height)
		# Image.NEAREST http://pillow.readthedocs.io/en/4.1.x/releasenotes/2.7.0.html
		# image resize takes a resampling argument which tells which filter to use for resampling
		# image.nearest takes in nearest pixel from input image
		stego_img = stego_img.resize((new_width, new_height), Image.NEAREST)
		stego_photo = ImageTk.PhotoImage(stego_img)

		stego_photo = ImageTk.PhotoImage(stego_img)

		self.stego_img_canvas.create_image(image_display_width / 2, image_display_height / 2, anchor=tk.CENTER,
										   image=stego_photo)

		ctypes.windll.user32.MessageBoxW(0, "Target Image has been embedded into Vessel Image!", "Success!", 1)

	# Recover Image Method
	def recoverImgMethod(self):

		self.target_img_canvas.delete("all")
		self.target_img_canvas.create_text(150, 100, fill="darkblue", font="Times 10 bold",
										   text="Target Img will be displayed here")

		vessel_name = self.file_name
		V = imageio.imread(vessel_name).astype(np.uint8)

		final_name = "RecoveredHiddenImage.png"

		t = time.time()
		F = image_bpcs_process.BPCS_unhide(V)
		t = time.time() - t

		if F is None:
			print("Error... Vessel image contains no message.")
			# pop up message box to inform user
			ctypes.windll.user32.MessageBoxW(0, "Error... Vessel  image contains no message", "Error", 1)
		else:
			f = open(final_name.split('.')[0] + ".txt", "w+")
			f.write("Time: " + str.format("%.5f" % t) + " seconds\n")
			imageio.imwrite(final_name, F)
			f.close()

		global stego_img
		stego_img = None
		global stego_photo
		stego_photo = None

		stego_img = Image.open(final_name)

		width, height = stego_img.size
		scale_width = image_display_width / width
		scale_height = image_display_height / height
		# get smallest compression capability of image
		scale = min(scale_width, scale_height)
		new_width = math.ceil(scale * width)
		new_height = math.ceil(scale * height)
		# Image.NEAREST http://pillow.readthedocs.io/en/4.1.x/releasenotes/2.7.0.html
		# image resize takes a resampling argument which tells which filter to use for resampling
		# image.nearest takes in nearest pixel from input image
		stego_img = stego_img.resize((new_width, new_height), Image.NEAREST)
		stego_photo = ImageTk.PhotoImage(stego_img)

		stego_photo = ImageTk.PhotoImage(stego_img)

		self.stego_img_canvas.create_image(image_display_width / 2, image_display_height / 2, anchor=tk.CENTER,
										   image=stego_photo)

	def create_widgets(self):
		# functions are defined on top, now to pack the widgets onto GUI
		# LEFT FRAME of GUI
		# ______________________________________________________________
		left_frame = tk.Frame(self)
		left_frame.pack(side=tk.LEFT)

		show_frame = tk.Frame(left_frame)
		show_frame.pack(side=tk.TOP)

		open_frame = tk.Frame(show_frame)
		open_frame.pack(side=tk.TOP)

		open_label = tk.Label(open_frame, text='Open Vessel Image (PNG File):')
		open_label.pack(side=tk.LEFT)

		# open file button
		open_button = tk.Button(open_frame, text='<select>', command=self.open_file, bg="white", fg="green")
		open_button.pack(side=tk.LEFT)

		# recover target image button
		recoverImg_button = tk.Button(open_frame, text='Recover Target Image', command=self.recoverImgMethod,
								   bg="black", fg="white")
		recoverImg_button.pack(side=tk.RIGHT)

		# details about vessel image
		LabelFrame = tk.Frame(show_frame)
		LabelFrame.pack(side=tk.LEFT)

		self.name_label = tk.Label(LabelFrame, text='Name: ')
		self.name_label.pack(side=tk.TOP)

		self.dimensions_label = tk.Label(LabelFrame, text='Dimensions: ')
		self.dimensions_label.pack(side=tk.TOP)

		self.size_label = tk.Label(LabelFrame, text='Size: ')
		self.size_label.pack(side=tk.TOP)
		# ============================

		# ============================

		canvas_frame = tk.Frame(left_frame)
		canvas_frame.pack(side=tk.BOTTOM)

		self.left_img_canvas = tk.Canvas(canvas_frame, bg='grey', width=image_display_width, height=image_display_height)
		self.left_img_canvas.create_text(150, 100, fill="darkblue", font="Times 10 bold",
										 text="Vessel Img will be displayed here.")
		self.left_img_canvas.pack(side=tk.LEFT)

		self.stego_img_canvas = tk.Canvas(canvas_frame, bg='grey', width=image_display_width, height=image_display_height)
		self.stego_img_canvas.create_text(150, 100, fill="darkblue", font="Times 10 bold",
										  text="Stego/Hidden Img will be displayed here.")
		self.stego_img_canvas.pack(side=tk.RIGHT)

		# RIGHT part of GUI
		# ______________________________________________________________
		right_frame = tk.Frame(self)
		right_frame.pack(side=tk.RIGHT)

		showright_frame = tk.Frame(right_frame)
		showright_frame.pack(side=tk.TOP)

		# insert open file button, label, etc. to allow user to choose which image to embed
		open_labelTarget = tk.Label(showright_frame, text='Open Target Image (PNG File):')
		open_labelTarget.pack(side=tk.LEFT)

		open_buttonTarget = tk.Button(showright_frame, text='<select>', command=self.open_targetFile, bg="white",
								   fg="green")
		open_buttonTarget.pack(side=tk.LEFT)

		embedImg_button = tk.Button(showright_frame, text='Embed Target Image', command=self.embedImageMethod,
								 bg="white", fg="black")
		embedImg_button.pack(side=tk.LEFT)

		back_button = tk.Button(showright_frame,text="Back",command=lambda: self.master.switch_frame(MenuPage))
		back_button.pack(side=tk.LEFT)

		self.name_labelTarget = tk.Label(right_frame, text='Name: ')
		self.name_labelTarget.pack(side=tk.TOP)

		self.dimensions_labelTarget = tk.Label(right_frame, text='Dimensions: ')
		self.dimensions_labelTarget.pack(side=tk.TOP)

		self.size_labelTarget = tk.Label(right_frame, text='Size: ')
		self.size_labelTarget.pack(side=tk.TOP)
		# =====================================================================

		# TARGET image canvas
		self.target_img_canvas = tk.Canvas(right_frame, bg='grey', width=image_display_width, height=image_display_height)
		self.target_img_canvas.create_text(150, 100, fill="darkblue", font="Times 10 bold",
										   text="Target Img will be displayed here.")
		self.target_img_canvas.pack(side=tk.LEFT)


class EncodeText(tk.Frame):
	image = None
	messageInput = None
	image_path_location = None
	payload_path_location = None
	stego_img = None
	imagePanel = None
	stegoImagePanel = None
	alpha = None
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.pack()
		top_frame = tk.Frame(self)
		top_frame.pack(side=tk.TOP)


		# Left Portion -----------------------------------------------------------
		left_frame = tk.Frame(top_frame)
		left_frame.pack(side=tk.LEFT)

		open_frame = tk.Frame(left_frame)
		open_frame.pack(side=tk.TOP)

		image_frame = tk.Frame(left_frame)
		image_frame.pack(side=tk.TOP)

		open_label = tk.Label(open_frame, text='Load Image File',font=('Helvetica', 20, "bold"))
		open_label.pack(side=tk.TOP)

		self.image_path_location = tk.Entry(open_frame)
		self.image_path_location.pack(side=tk.LEFT,padx=10)

		open_button = tk.Button(open_frame, text='Browse Image',command=self.get_image)
		open_button.pack(side=tk.LEFT,pady=36)

		self.imagePanel = tk.Canvas(image_frame,bg='black',width=image_display_width,height=image_display_height)
		self.imagePanel.pack(side=tk.BOTTOM,pady=48,padx=5)


		# Right Portion ------------------------------------------------------
		right_frame = tk.Frame(top_frame)
		right_frame.pack(side=tk.RIGHT,padx=30,fill=tk.Y)

		load_payload_frame = tk.Frame(right_frame)
		load_payload_frame.pack(side=tk.TOP,padx=30)

		alpha_section = tk.Frame(right_frame)
		alpha_section.pack(side=tk.TOP)

		extra_section = tk.Frame(right_frame)
		extra_section.pack(side=tk.TOP)

		stego_image_frame = tk.Frame(right_frame)
		stego_image_frame.pack(side=tk.TOP)

		open_label = tk.Label(load_payload_frame, text='Load Payload',font=('Helvetica', 20, "bold"))
		open_label.pack(side=tk.TOP)

		self.payload_path_location= tk.Entry(load_payload_frame)
		self.payload_path_location.pack(side=tk.LEFT,padx=10)

		open_button = tk.Button(load_payload_frame, text='Browse File',command=self.get_file)
		open_button.pack(side=tk.LEFT,pady=36)

		alpha_label = tk.Label(alpha_section,text="Alpha Value",font=('Helvetica',9,"bold"))
		alpha_label.pack(side=tk.LEFT)
		self.alpha = tk.Entry(alpha_section)
		self.alpha.pack(side=tk.LEFT,padx=10)

		encode_button = tk.Button(extra_section, text='Encode', command=self.encode)
		encode_button.pack(side=tk.LEFT,padx=10)

		back_button = tk.Button(extra_section, text='Back', command=lambda:self.master.switch_frame(TextSteganography))
		back_button.pack(side=tk.RIGHT)

		self.stegoImagePanel = tk.Canvas(stego_image_frame,bg='black',width=image_display_width,height=image_display_height)
		self.stegoImagePanel.pack(side=tk.BOTTOM,padx=10)

		#Bottom Area
		bottom_frame = tk.Frame(self)
		bottom_frame.pack(side=tk.TOP)

		message_section = tk.Frame(bottom_frame)
		message_section.pack(side=tk.BOTTOM)
		tk.Label(message_section, text="MESSAGE LOG", font=('Helvetica', 15, 'bold')).pack(side=tk.TOP)
		self.messageInput = tk.Text(message_section, height=10,pady=10)
		self.messageInput.pack(side=tk.BOTTOM,fill=tk.X)

	def get_file(self):
		filename=askopenfilename()
		self.payload_path_location.insert(tk.END,filename)


	def get_image(self):
		path = askopenfilename()
		if not isinstance(path,str):
			return
		else:
			self.image_path_location.insert(tk.END,path)
			self.image = Image.open(path)
			image_width,image_height = self.image.size
			scale_width = image_display_width/ image_width
			scale_height = image_display_height/image_height
			scale = min(scale_width,scale_height)
			new_width =math.ceil(scale * image_width)
			new_height = math.ceil(scale * image_height)
			self.image =self.image.resize((new_width,new_height),Image.NEAREST)
			image_resized = ImageTk.PhotoImage(self.image)
			self.imagePanel.create_image(image_display_width/2,image_display_height/2,anchor=tk.CENTER,
										 image=image_resized)
			self.imagePanel.image =image_resized



	def encode(self):
		image_location = self.image_path_location.get()
		file_location = self.payload_path_location.get()
		alpha_value = float(self.alpha.get())

		try:
			# embed msgfile in vslfile, write to encfile
			bpcs.encoderClass(image_location, file_location, image_location, alpha_value).encode()
			#Opens the new stego image and displays on the window
			embed_image = Image.open(image_location)
			stego_image_width,stego_image_height = embed_image.size
			scale_width = image_display_width / stego_image_width
			scale_height = image_display_height / stego_image_height
			scale = min(scale_width, scale_height)
			new_width = math.ceil(scale * stego_image_width)
			new_height = math.ceil(scale * stego_image_height)
			self.stego_img = embed_image.resize((new_width, new_height), Image.NEAREST)
			stego_image_resized = ImageTk.PhotoImage(self.stego_img)
			self.stegoImagePanel.create_image(image_display_width/2,image_display_height/2,anchor=tk.CENTER,
											  image=stego_image_resized)
			self.stegoImagePanel.image=stego_image_resized
			self.messageInput.insert(tk.END,'Success: Your Image is now a Stego Image')
		except Exception as e:
			self.messageInput.insert(tk.END, 'Error: Something Went Wrong in the Encoding Process, {}'.format(e))



class DecodeText(tk.Frame):
	image = None
	messageInput = None
	image_path_location = None
	payload_path_location = None
	stego_img = None
	imagePanel = None
	stegoImagePanel = None
	alpha = None
	def __init__(self, master):
		tk.Frame.__init__(self, master)

		top_frame = tk.Frame(self)
		top_frame.pack(side=tk.TOP)
		# do not try to use grid and pack in the same window
		# Left Portion -----------------------------------------------------------
		left_frame = tk.Frame(top_frame)
		left_frame.pack(side=tk.LEFT)

		open_frame = tk.Frame(left_frame)
		open_frame.pack(side=tk.TOP)

		open_label = tk.Label(open_frame, text='Load Image File',font=('Helvetica', 20, "bold"))
		open_label.pack(side=tk.TOP)

		self.image_path_location = tk.Entry(open_frame)
		self.image_path_location.pack(side=tk.LEFT,padx=10)

		open_button = tk.Button(open_frame, text='Browse Image',command=self.get_image)
		open_button.pack(side=tk.LEFT,pady=36)

		# Right Portion ------------------------------------------------------
		right_frame = tk.Frame(top_frame)
		right_frame.pack(side=tk.RIGHT,padx=30,fill=tk.Y)

		set_directory_frame = tk.Frame(right_frame)
		set_directory_frame.pack(side=tk.TOP,padx=30)

		alpha_section = tk.Frame(right_frame)
		alpha_section.pack(side=tk.TOP)

		open_label = tk.Label(set_directory_frame, text='Set Directory',font=('Helvetica', 20, "bold"))
		open_label.pack(side=tk.TOP,pady=11)

		self.text_file_path_location= tk.Entry(set_directory_frame)
		self.text_file_path_location.pack(side=tk.LEFT,padx=10,pady=36)

		open_button = tk.Button(set_directory_frame, text='Browse File',command=self.get_file)
		open_button.pack(side=tk.LEFT)

		tk.Label(alpha_section,text="Enter Alpha",font=('Helvetica',9,'bold')).pack(side=tk.LEFT)
		self.alpha = tk.Entry(alpha_section)
		self.alpha.pack(side=tk.RIGHT)

# 		#Bottom Section
		bottom_frame = tk.Frame(self)
		bottom_frame.pack(side=tk.TOP)

		image_frame = tk.Frame(bottom_frame)
		image_frame.pack(side=tk.TOP)

		extra_section = tk.Frame(bottom_frame)
		extra_section.pack(side=tk.TOP)

		message_section = tk.Frame(bottom_frame)
		message_section.pack(side=tk.BOTTOM)

		self.imagePanel = tk.Canvas(image_frame, bg='black', width=image_display_width, height=image_display_height)
		self.imagePanel.pack(side=tk.BOTTOM, pady=50, padx=5)

		encode_button = tk.Button(extra_section, text='Decode', command=self.decode)
		encode_button.pack(side=tk.TOP, padx=10)

		back_button = tk.Button(extra_section, text='Back', command=lambda: self.master.switch_frame(TextSteganography))
		back_button.pack(side=tk.TOP)

		tk.Label(message_section, text="MESSAGE LOG", font=('Helvetica', 15, 'bold')).pack(side=tk.TOP)
		self.messageInput = tk.Text(message_section, height=10, pady=10)
		self.messageInput.pack(side=tk.BOTTOM, fill=tk.X)

	def get_file(self):
		filelocation =askopenfilename()
		self.text_file_path_location.insert(tk.END, filelocation)

	def get_image(self):
		path = askopenfilename()
		if not isinstance(path, str):
			return
		else:
			self.image_path_location.insert(tk.END, path)
			self.image = Image.open(path)
			image_width, image_height = self.image.size
			scale_width = image_display_width / image_width
			scale_height = image_display_height / image_height
			scale = min(scale_width, scale_height)
			new_width = math.ceil(scale * image_width)
			new_height = math.ceil(scale * image_height)
			self.image = self.image.resize((new_width, new_height), Image.NEAREST)
			image_resized = ImageTk.PhotoImage(self.image)
			self.imagePanel.create_image(image_display_width / 2, image_display_height / 2, anchor=tk.CENTER,
										 image=image_resized)
			self.imagePanel.image = image_resized

	def decode(self):
		image_location = self.image_path_location.get()
		file_location = self.text_file_path_location.get()
		alpha_value = float(self.alpha.get())
		try:
			bpcs.decoderClass(image_location, file_location, alpha_value).decode()
			self.messageInput.insert(tk.END, 'Success: A Text File Containing the Secret Message Has been Created At Your Chosen Directory')
		except Exception as e:
			self.messageInput.insert(tk.END,'Error: Something Went Wrong with the Decoding Process {}'.format(e))



if __name__ == "__main__":
	app= MainApp()
	app.mainloop()


