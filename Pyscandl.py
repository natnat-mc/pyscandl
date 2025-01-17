import img2pdf
import requests
import os


class Pyscandl:
	def __init__(self, fetcher, chapstart:int=1, output:str=".", keepimage:bool=False, all:bool=False, link:str=None, manga:str=None, download_number:int=1, quiet:bool=False, skip:int=0):
		# must have either a link or a manga
		if link is not None and manga is None or link is None and manga is not None:
			self.fetcher = fetcher(link=link, manga=manga, chapstart=chapstart)
		else:
			# TODO: make custom exception one day to implement them here
			pass

		# creating output folder
		self.output = (output[-1]=="/" and output or output+"/") + self.fetcher.manga_name + "/"
		if not os.path.exists(self.output):
			os.makedirs(self.output)

		self.skip = skip
		self.quiet = quiet
		self.keepimage = keepimage
		self.all = all
		self.download_number = download_number
		self.path = f"{self.output}{self.fetcher.chapter_name} ch.{self.fetcher.chapter_number}/"  # save path for images
		self._img_bin_list = []

	def _dl_image(self):
		# single image download
		img_bin = requests.get(self.fetcher.image).content

		if not os.path.exists(self.path):
			os.makedirs(self.path)

		with open(f"{self.path}{self.fetcher.npage}{self.fetcher.ext}", "wb") as img:
			img.write(img_bin)
			if not self.quiet:
				print(".", end="", flush=True)

	def _full_chapter(self):
		# fetching binary data an entire chapter
		if not self.quiet:
			print(f"fetching: ch.{self.fetcher.chapter_number} {self.fetcher.chapter_name}")
		while not self.fetcher.is_last_image():
			self._img_bin_list.append(requests.get(self.fetcher.image).content)
			if not self.quiet:
				print(".", end="", flush=True)
			self.fetcher.next_image()
		self._img_bin_list.append(requests.get(self.fetcher.image).content)
		if not self.quiet:
			print(".", end="", flush=True)

	def _keep_full_chapter(self):
		# download a full chapter
		if not self.quiet:
			print(f"downloading: ch.{self.fetcher.chapter_number} {self.fetcher.chapter_name}")
		while not self.fetcher.is_last_image():
			self._dl_image()
			self.fetcher.next_image()
		self._dl_image()

	def _skip(self):
		for loop in range(self.skip):
			self.fetcher.next_image()

	def _create_pdf(self):
		print("\nconverting...", end=" ")
		# loading the downloaded images if keep mode
		if self.keepimage:
			for loop in range(1, self.fetcher.npage+1):
				with open(f"{self.path}{loop}{self.fetcher.ext}", "rb") as img:
					self._img_bin_list.append(img.read())

		with open(f"{self.output}{self.fetcher.manga_name} - {self.fetcher.chapter_name} ch.{self.fetcher.chapter_number}.pdf", "wb") as pdf:
			pdf.write(img2pdf.convert(self._img_bin_list))
		print("converted")

	def _next_chapter(self):
		# changes to the next chapter and prepare the next image folder
		self.fetcher.next_chapter()
		self.path = f"{self.output}{self.fetcher.chapter_name} ch.{self.fetcher.chapter_number}/"
		self._img_bin_list = []

	def full_download(self):
		# download the full request
		# emulating a do while
		self._skip()
		counter = 1
		if self.keepimage:
			self._keep_full_chapter()
		else:
			self._full_chapter()
		self._create_pdf()
		while not self.fetcher.is_last_chapter() and self.all or counter < self.download_number:
			self._next_chapter()
			if self.keepimage:
				self._keep_full_chapter()
			else:
				self._full_chapter()
			self._create_pdf()
			counter += 1
		self.fetcher.quit()
		print("end of the download")
