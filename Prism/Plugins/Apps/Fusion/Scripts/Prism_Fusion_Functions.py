# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2019 Richard Frangenberg
#
# Licensed under GNU GPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.



import os, sys
import traceback, time
from functools import wraps

try:
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	psVersion = 2
except:
	from PySide.QtCore import *
	from PySide.QtGui import *
	psVersion = 1



class Prism_Fusion_Functions(object):
	def __init__(self, core, plugin):
		self.core = core
		self.plugin = plugin


	def err_decorator(func):
		@wraps(func)
		def func_wrapper(*args, **kwargs):
			exc_info = sys.exc_info()
			try:
				return func(*args, **kwargs)
			except Exception as e:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				erStr = ("%s ERROR - Prism_Plugin_Fusion - Core: %s - Plugin: %s:\n%s\n\n%s" % (time.strftime("%d/%m/%y %X"), args[0].core.version, args[0].plugin.version, ''.join(traceback.format_stack()), traceback.format_exc()))
				args[0].core.writeErrorLog(erStr)

		return func_wrapper


	@err_decorator
	def instantStartup(self, origin):
	#	qapp = QApplication.instance()

		with (open(os.path.join(self.core.prismRoot, "Plugins", "Apps", "Fusion", "UserInterfaces", "FusionStyleSheet", "Fusion.qss"), "r")) as ssFile:
			ssheet = ssFile.read()

		ssheet = ssheet.replace("qss:", os.path.join(self.core.prismRoot, "Plugins", "Apps", "Fusion", "UserInterfaces", "FusionStyleSheet").replace("\\", "/") + "/")
		#ssheet = ssheet.replace("#c8c8c8", "rgb(47, 48, 54)").replace("#727272", "rgb(40, 40, 46)").replace("#5e90fa", "rgb(70, 85, 132)").replace("#505050", "rgb(33, 33, 38)")
		#ssheet = ssheet.replace("#a6a6a6", "rgb(37, 39, 42)").replace("#8a8a8a", "rgb(37, 39, 42)").replace("#b5b5b5", "rgb(47, 49, 52)").replace("#999999", "rgb(47, 49, 52)")
		#ssheet = ssheet.replace("#9f9f9f", "rgb(31, 31, 31)").replace("#b2b2b2", "rgb(31, 31, 31)").replace("#aeaeae", "rgb(35, 35, 35)").replace("#c1c1c1", "rgb(35, 35, 35)")
		#ssheet = ssheet.replace("#555555", "rgb(27, 29, 32)").replace("#717171", "rgb(27, 29, 32)").replace("#878787", "rgb(37, 39, 42)").replace("#7c7c7c", "rgb(37, 39, 42)")
		#ssheet = ssheet.replace("#4c4c4c", "rgb(99, 101, 103)").replace("#5b5b5b", "rgb(99, 101, 103)").replace("#7aa3e5", "rgb(65, 76, 112)").replace("#5680c1", "rgb(65, 76, 112)")
		#ssheet = ssheet.replace("#5a5a5a", "rgb(35, 35, 35)").replace("#535353", "rgb(35, 35, 41)").replace("#373737", "rgb(35, 35, 41)").replace("#858585", "rgb(31, 31, 31)").replace("#979797", "rgb(31, 31, 31)")
		#ssheet = ssheet.replace("#4771b3", "rgb(70, 85, 132)").replace("#638dcf", "rgb(70, 85, 132)").replace("#626262", "rgb(45, 45, 51)").replace("#464646", "rgb(45, 45, 51)")
		#ssheet = ssheet.replace("#7f7f7f", "rgb(60, 60, 66)").replace("#6c6c6c", "rgb(60, 60, 66)").replace("#565656", "rgb(35, 35, 41)").replace("#5d5d5d", "rgb(35, 35, 41)")
		#ssheet = ssheet.replace("white", "rgb(200, 200, 200)")
		if "parentWindows" in origin.prismArgs:
			origin.messageParent.setStyleSheet(ssheet)
		#	origin.messageParent.resize(10,10)
		#	origin.messageParent.show()
			origin.parentWindows = True
		else:
			qapp = QApplication.instance()
			qapp.setStyleSheet(ssheet)
			appIcon = QIcon(os.path.join(self.core.prismRoot, "Scripts", "UserInterfacesPrism", "p_tray.png"))
			qapp.setWindowIcon(appIcon)

		self.isRendering = [False,""]

		return False


	@err_decorator
	def startup(self, origin):
		if not hasattr(self, "fusion"):
			return False

		origin.timer.stop()
		return True


	@err_decorator
	def onProjectChanged(self, origin):
		pass


	@err_decorator
	def sceneOpen(self, origin):
		pass


	@err_decorator
	def executeScript(self, origin, code, preventError=False):
		if preventError:
			try:
				return eval(code)
			except Exception as e:
				msg = '\npython code:\n%s' % code
				exec("raise type(e), type(e)(e.message + msg), sys.exc_info()[2]")
		else:
			return eval(code)


	@err_decorator
	def getCurrentFileName(self, origin, path=True):
		curComp = self.fusion.GetCurrentComp()
		if curComp is None:
			currentFileName = ""
		else:
			currentFileName = self.fusion.GetCurrentComp().GetAttrs()["COMPS_FileName"]

		return currentFileName


	@err_decorator
	def getSceneExtension(self, origin):
		return self.sceneFormats[0]


	@err_decorator
	def saveScene(self, origin, filepath, details={}):
		try:
			return self.fusion.GetCurrentComp().Save(filepath)
		except:
			return ""


	@err_decorator
	def getImportPaths(self, origin):
		return False


	@err_decorator
	def getFrameRange(self, origin):
		startframe = self.fusion.GetCurrentComp().GetAttrs()["COMPN_GlobalStart"]
		endframe = self.fusion.GetCurrentComp().GetAttrs()["COMPN_GlobalEnd"]

		return [startframe, endframe]


	@err_decorator
	def setFrameRange(self, origin, startFrame, endFrame):
		self.fusion.GetCurrentComp().SetPrefs({ "Comp.Unsorted.GlobalStart": startFrame, "Comp.Unsorted.GlobalEnd": endFrame})


	@err_decorator
	def getFPS(self, origin):
		return self.fusion.GetCurrentComp().GetPrefs()["Comp"]["FrameFormat"]["Rate"]


	@err_decorator
	def setFPS(self, origin, fps):
		return self.fusion.GetCurrentComp().SetPrefs({ "Comp.FrameFormat.Rate": fps})


	@err_decorator
	def updateReadNodes(self):
		updatedNodes = []

		selNodes = self.fusion.GetCurrentComp().GetToolList(True, "Loader")
		for k in selNodes:
			i = selNodes[k]
			curPath = i.GetAttrs()["TOOLST_Clip_Name"][1]

			newPath = self.core.getLatestCompositingVersion(curPath)

			if os.path.exists(os.path.dirname(newPath)) and not curPath.startswith(os.path.dirname(newPath)):
				firstFrame = i.GetInput("GlobalIn")
				lastFrame = i.GetInput("GlobalOut")

				i.Clip = newPath

				i.GlobalOut = lastFrame
				i.GlobalIn = firstFrame
				i.ClipTimeStart = 0
				i.ClipTimeEnd = lastFrame - firstFrame
				i.HoldLastFrame = 0

				updatedNodes.append(i)

		if len(updatedNodes) == 0:
			QMessageBox.information(self.core.messageParent, "Information", "No nodes were updated")
		else:
			mStr = "%s nodes were updated:\n\n" % len(updatedNodes)
			for i in updatedNodes:
				mStr += i.GetAttrs()["TOOLS_Name"] + "\n"

			QMessageBox.information(self.core.messageParent, "Information", mStr)


	@err_decorator
	def getAppVersion(self, origin):
		return self.fusion.Version
		

	@err_decorator
	def onProjectBrowserStartup(self, origin):
		origin.loadOiio()
		origin.actionStateManager.setEnabled(False)


	@err_decorator
	def projectBrowserLoadLayout(self, origin):
		pass


	@err_decorator
	def setRCStyle(self, origin, rcmenu):
		pass


	@err_decorator
	def openScene(self, origin, filepath, force=False):
		if os.path.splitext(filepath)[1] not in self.sceneFormats:
			return False

		comp = self.fusion.LoadComp(filepath)

		return True


	@err_decorator
	def correctExt(self, origin, lfilepath):
		return lfilepath


	@err_decorator
	def setSaveColor(self, origin, btn):
		btn.setPalette(origin.savedPalette)


	@err_decorator
	def clearSaveColor(self, origin, btn):
		btn.setPalette(origin.oldPalette)


	@err_decorator
	def importImages(self, origin): 
		fString = "Please select an import option:"
		msg = QMessageBox(QMessageBox.NoIcon, "Fusion Import", fString, QMessageBox.Cancel)
		msg.addButton("Current pass", QMessageBox.YesRole)
		msg.addButton("All passes", QMessageBox.YesRole)
	#	msg.addButton("Layout all passes", QMessageBox.YesRole)
		self.core.parentWindow(msg)
		action = msg.exec_()

		if action == 0:
			self.fusionImportSource(origin)
		elif action == 1:
			self.fusionImportPasses(origin)
		else:
			return


	@err_decorator
	def fusionImportSource(self, origin):
		self.fusion.GetCurrentComp().Lock()

		sourceData = origin.compGetImportSource()
		for i in sourceData:
			filePath = i[0]
			firstFrame = i[1]
			lastFrame = i[2]

			filePath = filePath.replace('####', "%04d" % firstFrame)

			tool = self.fusion.GetCurrentComp().AddTool("Loader", -32768, -32768)
			tool.Clip = filePath
			tool.GlobalOut = lastFrame
			tool.GlobalIn = firstFrame
			tool.ClipTimeStart = 0
			tool.ClipTimeEnd = lastFrame - firstFrame
			tool.HoldLastFrame = 0

		self.fusion.GetCurrentComp().Unlock()


	@err_decorator
	def fusionImportPasses(self, origin):
		self.fusion.GetCurrentComp().Lock()

		sourceData = origin.compGetImportPasses()

		for i in sourceData:
			filePath = i[0]
			firstFrame = i[1]
			lastFrame = i[2]

			filePath = filePath.replace('####', "%04d" % firstFrame)

			self.fusion.GetCurrentComp().CurrentFrame.FlowView.Select()
			tool = self.fusion.GetCurrentComp().AddTool("Loader", -32768, -32768)
			tool.Clip = filePath
			tool.GlobalOut = lastFrame
			tool.GlobalIn = firstFrame
			tool.ClipTimeStart = 0
			tool.ClipTimeEnd = lastFrame - firstFrame
			tool.HoldLastFrame = 0

		self.fusion.GetCurrentComp().Unlock()


	@err_decorator
	def setProject_loading(self, origin):
		pass


	@err_decorator
	def onPrismSettingsOpen(self, origin):
		pass


	@err_decorator
	def createProject_startup(self, origin):
		pass


	@err_decorator
	def editShot_startup(self, origin):
		origin.loadOiio()


	@err_decorator
	def shotgunPublish_startup(self, origin):
		pass


	@err_decorator
	def getOutputPath(self, node, render=False):
		self.isRendering = [False, ""]

		taskName = node.GetInput('PrismTaskControl')
		origComment = node.GetInput('PrismCommentControl')
		if origComment is None:
			comment = ""
			
		comment = self.core.validateStr(origComment)
		
		if len(origComment) != len(comment):
			node.SetInput('PrismCommentControl', comment)

		FormatID = node.GetInput("OutputFormat")
		fileType = ''
		if FormatID == 'PIXFormat':
			# Alias PIX
			fileType = 'pix'
		elif FormatID == 'IFFFormat':
			# Amiga IFF
			fileType = 'iff'
		elif FormatID == 'CineonFormat':
			# Kodak Cineon
			fileType = 'cin'
		elif FormatID == 'DPXFormat':
			# DPX
			fileType = 'dpx'
		elif FormatID == 'FusePicFormat':
			# Fuse Pic
			fileType = 'fusepic'
		elif FormatID == 'FlipbookFormat':
			# Fusion Flipbooks
			fileType = 'fb'
		elif FormatID == 'RawFormat':
			# Fusion RAW Image
			fileType = 'raw'
		elif FormatID == 'IFLFormat':
			# Image File List (Text File)
			fileType = 'ifl'
		elif FormatID == 'IPLFormat':
			# IPL
			fileType = 'ipl'
		elif FormatID == 'JpegFormat':
			# JPEG
			fileType = 'jpg'
			# fileType = 'jpeg'
		elif FormatID == 'Jpeg2000Format':
			# JPEG2000
			fileType = 'jp2'
		elif FormatID == 'MXFFormat':
			# MXF - Material Exchange Format
			fileType = 'mxf'
		elif FormatID == 'OpenEXRFormat':
			# OpenEXR
			fileType = 'exr'
		elif FormatID == 'PandoraFormat':
			# Pandora YUV
			fileType = 'piyuv10'
		elif FormatID == 'PNGFormat':
			# PNG
			fileType = 'png'
		elif FormatID == 'VPBFormat':
			# Quantel VPB
			fileType = 'vpb'
		elif FormatID == 'QuickTimeMovies':
			# QuickTime Movie
			fileType = 'mov'
		elif FormatID == 'HDRFormat':
			# Radiance
			fileType = 'hdr'
		elif FormatID == 'SixRNFormat':
			# Rendition
			fileType = '6RN'
		elif FormatID == 'SGIFormat':
			# SGI
			fileType = 'sgi'
		elif FormatID == 'PICFormat':
			# Softimage PIC
			fileType = 'si'
		elif FormatID == 'SUNFormat':
			# SUN Raster
			fileType = 'RAS'
		elif FormatID == 'TargaFormat':
			# Targa
			fileType = 'tga'
		elif FormatID == 'TiffFormat':
			# TIFF
			#fileType = 'tif'
			fileType = 'tiff'
		elif FormatID == 'rlaFormat':
			# Wavefront RLA
			fileType = 'rla'
		elif FormatID == 'BMPFormat':
			# Windows BMP
			fileType = 'bmp'
		elif FormatID == 'YUVFormat':
			# YUV
			fileType = 'yuv'
		else:
			# EXR fallback format 
			fileType = 'exr'

		localOut = node.GetInput('SaveLocalControl')
		useLastVersion = node.GetInput('RenderLastVersionControl')

		if taskName is None or taskName == "":
			msg = QMessageBox(QMessageBox.Warning, "Prism Warning", "Please choose a taskname")
			self.core.parentWindow(msg)
			if self.core.useOnTop:
				msg.setWindowFlags(msg.windowFlags() ^ Qt.WindowStaysOnTopHint)
			msg.exec_()
			return ""

		if useLastVersion:
			msg = QMessageBox(QMessageBox.Warning, "Prism Warning", "\"Render as previous version\" is enabled.\nThis may overwrite existing files.")
			self.core.parentWindow(msg)
			msg.exec_()

		outputName = self.core.getCompositingOut(taskName, fileType, useLastVersion, render, localOut, comment, ignoreEmpty=True).replace('####', '')

		node.Clip[self.fusion.TIME_UNDEFINED] = outputName
		node.FilePathControl = outputName

		return outputName


	@err_decorator
	def startRender(self, node):
		fileName = self.getOutputPath(node, render=True)

		if fileName == "FileNotInPipeline":
			QMessageBox.warning(self.core.messageParent, "Prism Warning", "The current file is not inside the Pipeline.\nUse the Project Browser to create a file in the Pipeline.")
			return

		self.core.saveScene(versionUp=False)