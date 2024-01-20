import argparse
import os
import time

from main_methods.AbbyyOnlineSdk import *
processor = None


def setup_processor():
	if "ABBYY_APPID" in os.environ:
		processor.ApplicationId = os.environ["ABBYY_APPID"]

	if "ABBYY_PWD" in os.environ:
		processor.Password = os.environ["ABBYY_PWD"]

	# Proxy settings
	if "http_proxy" in os.environ:
		proxy_string = os.environ["http_proxy"]
		print("Using http proxy at {}".format(proxy_string))
		processor.Proxies["http"] = proxy_string

	if "https_proxy" in os.environ:
		proxy_string = os.environ["https_proxy"]
		print("Using https proxy at {}".format(proxy_string))
		processor.Proxies["https"] = proxy_string


def recognize_file(file_path, language, output_format):
	print("Uploading..")
	settings = ProcessingSettings()
	settings.Language = language
	settings.OutputFormat = output_format
	task = processor.process_image(file_path, settings)
	if task is None:
		print("Error")
		return
	if task.Status == "NotEnoughCredits":
		print("Not enough credits to process the document. Please add more pages to your application's account.")
		return

	print("Id = {}".format(task.Id))
	print("Status = {}".format(task.Status))
	print("Waiting..")

	while task.is_active():
		time.sleep(5)
		print(".")
		task = processor.get_task_status(task)

	print("Status = {}".format(task.Status))

	if task.Status == "Completed":
		if task.DownloadUrl is not None:
			response = requests.get(task.DownloadUrl)
			if response.status_code == 200:
				try:
					return ' '.join([r.strip() for r in response.content.decode('utf-8').split()])
				except Exception as e:
					print(e.args)
					return None

			else:
				print("Failed to get the result")
		else:
			print("No download URL found")
	else:
		print("Error processing task")
	return None


def create_parser():
	parser = argparse.ArgumentParser(description="Recognize a file via web service")
	parser.add_argument('source_file')
	parser.add_argument('target_file')

	parser.add_argument('-l', '--language', default='Hebrew', help='Recognition language (default: %(default)s)')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-txt', action='store_const', const='txt', dest='format', default='txt')
	group.add_argument('-pdf', action='store_const', const='pdfSearchable', dest='format')
	group.add_argument('-rtf', action='store_const', const='rtf', dest='format')
	group.add_argument('-docx', action='store_const', const='docx', dest='format')
	group.add_argument('-xml', action='store_const', const='xml', dest='format')

	return parser


def recognize_file_from_code(file_path, language='Hebrew', output_format='txt'):
	global processor
	if not processor:
		processor = AbbyyOnlineSdk()
		setup_processor()

	if os.path.isfile(file_path):
		return recognize_file(file_path, language, output_format)
	else:
		print("No such file: {}".format(file_path))
		return None
