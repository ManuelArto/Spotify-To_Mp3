from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time


class SpotifyMp3:
	def __init__(self, url, path):
		try:
			os.mkdir("./files")
		except Exception as e:
			pass
		options = Options()
		options.headless = True
		prefs = {"profile.managed_default_content_settings.images": 2}
		options.add_experimental_option("prefs", prefs)
		self.driver = webdriver.Chrome(
			options=options, executable_path="/home/manuel/Downloads/chromedriver"
		)
		self.path = path
		self.url = url

	def closeBrowser(self):
		self.driver.quit()

	def start(self):
		self.get_titles()
		self.get_links()
		self.download_from_yt()

	def get_titles(self):
		print("getting titles")
		driver = self.driver
		try:
			driver.get(self.url)
			time.sleep(7)
			titles = driver.find_elements_by_class_name("da0bc4060bb1bdb4abb8e402916af32e-scss")
			artists = driver.find_elements_by_class_name("_966e29b71d2654743538480947a479b3-scss")
			if self.path == "":
				self.path = str(driver.title)  
			songs = []
			with open("./files/songs.txt", "w+") as file:
				for title, artist in zip(titles, artists):
					songs.append(f"{title.text} {artist.text}")
					file.write(f"{title.text} {artist.text}\n")
		except Exception as e:
			print(e)
		return songs

	def get_links(self):
		print("getting links")
		driver = self.driver
		file = open("./files/songs.txt", "r")
		songs = [song.strip("\n") for song in file.readlines()]
		file = open("./files/links.txt", "w+")
		links = []
		for song in songs:
			try:
				driver.get("http://www.youtube.com/results?search_query=" + song)
				link = (
					WebDriverWait(driver, 5)
					.until(
						EC.visibility_of_all_elements_located((By.ID, "video-title"))
					)[0]
					.get_attribute("href")
				)
				if link == "":
					link = (
						WebDriverWait(driver, 5)
						.until(
							EC.visibility_of_all_elements_located((By.ID, "video-title"))
						)[1]
						.get_attribute("href")
					)
				file.write(link + "\n")
				links.append(link)
			except Exception as e:
				print(song + " at number " + str(songs.index(song)) + ", ERROR: " + e)
				continue
		file.close()
		self.closeBrowser()
		return links

	def download_from_yt(self, write_download, songs):
		try:
			self.closeBrowser()
			print("downloading")
			file = open("./files/links.txt", "r")
			links = [link.strip("\n") for link in file.readlines()]
			if self.path == "":
				self.path = "songs"
			try:
				os.mkdir(self.path)
			except Exception as e:
				pass
			os.chdir(self.path)

			# youtube-dl cli
			counter = 0
			for link in links:
				os.system(f"youtube-dl -x --audio-format mp3 {link}")
				write_download(counter, links[counter])
				counter += 1

			# youtube_dl library
			# import youtube_dl
			# download_options = {
			# 	"format": "bestaudio/best",
			# 	"postprocessors": [
			# 		{
			# 			"key": "FFmpegExtractAudio",
			# 			"preferredcodec": "m4a",
			# 			"preferredquality": "192",
			# 		}
			# 	],
			# 	"postprocessor_args": ["-ar", "16000"],
			# 	"prefer_ffmpeg": True,
			# 	"keepvideo": True,
			# }
			# with youtube_dl.YoutubeDL(download_options) as dl:
			# 	dl.download(links)
		except Exception as e:
			print(e)
