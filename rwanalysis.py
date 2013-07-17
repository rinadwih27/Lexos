from matplotlib import pyplot, pylab
from os import path
import re
import pickle

def RollingAverageA(fileString, keyLetter, windowSize):
	"""
	Computes the rolling average of one letter over a certain window (size in characters).
	aka. Letter average in a window of letters.

	Args:
		fileString: the text from file
		keyLetter: the letter to count and average
		windowSize: the number of letters to have in the window

	Returns:
		List of averages, each index representing the window number
	"""
	windowStart = 0
	windowEnd = windowStart + windowSize

	# Rolling count, to be divided for average
	count = 0

	debug = ""

	# Count the initial window
	for i in xrange(windowStart, windowEnd):
		if fileString[i] == keyLetter:
			count += 1
			
	# Create list with initial value
	averages = [float(count) / windowSize]

	while windowEnd < len(fileString):
		if fileString[windowEnd] == keyLetter:
			count +=1
		if fileString[windowStart] == keyLetter:
			count -= 1

		averages.append(float(count) / windowSize)

		# Increment window indices
		windowEnd += 1
		windowStart += 1

	return averages

def RollingAverageB(splitList, keyLetter, windowSize):
	"""
	Computes the rolling average of one letter over a certain window (size in words or lines).
	aka. Letter average in a window of words or lines.

	Args:
		splitList: the text already split by words or lines, as chosen
		keyLetter: the letter to count and average
		windowSize: the number of words or lines to have in the window

	Returns:
		List of averages, each index representing the window number
	"""
	windowStart = 0
	windowEnd = windowStart + windowSize

	# Rolling count, to be divided for average
	count = 0

	# Count the initial window
	numberOfCharsInWindow = 0
	for i in xrange(windowStart, windowEnd):
		numberOfCharsInWindow += len(splitList[i])

		for next_char in splitList[i]:
			if next_char == keyLetter:
				count += 1
		debug += fileString[i]

	print debug, count

	# Create list with initial value
	averages = [float(count) / numberOfCharsInWindow]
	
	while windowEnd < len(splitList):
		for char in splitList[windowEnd]:
			if char == keyLetter:
				count += 1
		for char in splitList[windowStart]:
			if char == keyLetter:
				count -= 1

		debug = debug[1:] + fileString[windowEnd]
		print debug, count

		# Adjust window size
		numberOfCharsInWindow += len(splitList[windowEnd])
		numberOfCharsInWindow -= len(splitList[windowStart])

		averages.append(float(count) / numberOfCharsInWindow)

		# Increment window indices
		windowEnd += 1
		windowStart += 1

	return averages



def RollingAverageC(splitList, keyWord, windowSize):
	"""
	Computes the rolling average of one word over a certain window (size in words).
	aka. Word average in a window of words.

	Args:
		splitList: the text already split by words or lines, as chosen
		keyWord: the word to count and average
		windowSize: the number of words to have in the window

	Returns:
		List of averages, each index representing the window number
	"""
	windowStart = 0
	windowEnd = windowStart + windowSize
	
	# Rolling count, to be divided for average
	count = 0

	words = splitList

	# Count the initial window
	for i in xrange(windowStart, windowEnd):
		if words[i] == keyWord:
			count += 1

	# Create list with initial value
	averages = [float(count) / windowSize]

	while windowEnd < len(words):
		if words[windowEnd] == keyWord:
			count += 1
		if words[windowStart] == keyWord:
			count -= 1

		averages.append(float(count) / windowSize)
	
		# Increment window indices
		windowEnd += 1
		windowStart += 1

	return averages


def RollingAverageD(splitList, keyWord, windowSize):
	"""
	Computes the rolling average of one word over a certain window (size in lines).
	aka. Word average in a window of lines.

	Args:
		splitList: the text already split by words or lines, as chosen
		keyWord: the word to count and average
		windowSize: the number of lines to have in the window

	Returns:
		List of averages, each index representing the window number
	"""
	windowStart = 0
	windowEnd = windowStart + windowSize
	
	# Rolling count, to be divided for average
	count = 0
		
	windowWordLength = 0 # window length (in # of words)
	lines = splitList

	# Split the lines into words for comparison and counting
	for i in xrange(len(lines)):
		lines[i] = lines[i].split()

	# Count the initial window
	for i in xrange(windowStart, windowEnd):
		windowWordLength += len(lines[i])
		for word in lines[i]:
			if word == keyWord:
				count += 1

	# Create list with initial value
	averages = [float(count) / windowWordLength]

	while windowEnd < len(lines):
		for word in lines[windowEnd]:
			if word == keyWord:
				count += 1
		for word in lines[windowStart]:
			if word == keyWord:
				count -= 1

		# Adjust window size
		windowWordLength += len(lines[windowEnd])
		windowWordLength -= len(lines[windowStart])

		averages.append(float(count) / windowWordLength)

		# Increment window indices
		windowEnd += 1
		windowStart += 1

	return averages


def RollingRatioA(filestring, firstLetter, secondLetter, windowSize):
	"""
	Computes the rolling ratio of one letter to another over a certain window
	(size in letters).
	aka. Letter ratio in a window of letters.

	Args:
		fileString: the text from file
		firstLetter: the letter to count, for the ratio's numerator
		secondLetter: the letter to count, for the ratio's denominator
		windowSize: the number of letters to have in the window

	Returns:
		List of ratios, each index representing the window number
	"""
	windowStart = 0
	windowEnd = windowStart + windowSize

	# Rolling counts, to be divided for ratio
	first = 0
	second = 0

	# Count the initial window
	for i in xrange(windowStart, windowEnd):
		if filestring[i] == firstLetter:
			first += 1
		if filestring[i] == secondLetter:
			second += 1
	
	# Create list with initial value
	if first == 0 and second == 0:
		ratios = [0]
	else:
		ratios = [float(first) / (first+second)]

	while windowEnd < len(filestring):
		# Checks only the first and last (the characters exiting and entering 
		# the window, respectively) characters.
		if filestring[windowEnd] == firstLetter:
			first += 1
		if filestring[windowEnd] == secondLetter:
			second += 1

		if filestring[windowStart] == firstLetter:
			first -= 1
		if filestring[windowStart] == secondLetter:
			second -= 1


		if first == 0 and second == 0:
			ratios.append(0)
		else:
			ratios.append(float(first) / (first+second))


		# Increment window indices
		windowEnd += 1
		windowStart += 1

	return ratios

def RollingRatioB(splitList, firstLetter, secondLetter, windowSize):
	"""
	Computes the rolling ratio of one letter to another over a certain window
	(size in words or lines).
	aka. Letter ratio in a window of words or lines.

	Args:
		splitList: the text already split by words or lines, as chosen
		firstLetter: the letter to count, for the ratio's numerator
		secondLetter: the letter to count, for the ratio's denominator
		windowSize: the number of words or lines to have in the window

	Returns:
		List of ratios, each index representing the window number
	"""
	windowStart = 0
	windowEnd = windowStart + windowSize
	
	# Rolling counts, to be divided for ratio
	first = 0
	second = 0
	
	# Count the initial window
	for i in xrange(windowStart, windowEnd):
		for char in splitList[i]:
			if firstLetter == splitList[i][char]:
				first += 1
			if secondLetter ==  splitList[i][char]:
				second += 1

	# Create list with initial value
	if first == 0 and second == 0:
		ratios = [0]
	else:
		ratios = [float(first) / (first+second)]

	while windowEnd < len(splitList):
		for char in splitList[windowEnd]:
			if char == firstLetter:
				first += 1
			if char == secondLetter:
				second += 1
		for char in splitList[windowStart]:
			if char == firstLetter:
				first -= 1
			if char == secondLetter:
				second -= 1

		if first == 0 and second == 0:
			ratios.append(0)
		else:
			ratios.append(float(first) / (first+second))

		# Increment window indices
		windowEnd += 1
		windowStart += 1

	return ratios
	
def RollingRatioC(splitList, firstWord, secondWord, windowSize):
	"""
	Computes the rolling ratio of one word to another over a certain window
	(size in words).
	aka. Word ratio in a window of words.

	Args:
		splitList: the text already split by words or lines, as chosen
		firstWord: the word to count, for the ratio's numerator
		secondWord: the word to count, for the ratio's denominator
		windowSize: the number of words to have in the window

	Returns:
		List of ratios, each index representing the window number
	"""
	windowStart = 0
	windowEnd = windowStart + windowSize

	# Rolling counts, to be divided for ratio
	first = 0
	second = 0

	words = splitList

	# Count the initial window
	for i in xrange(windowStart, windowEnd):
		if firstWord == words[i]:
			first += 1
		if secondWord == words[i]:
			second += 1

	# Create list with initial value
	if first == 0 and second == 0:
		ratios = [0]
	else:
		ratios = [float(first) / (first+second)]
		
	while windowEnd < len(words):
		if words[windowEnd] == firstWord:
			first += 1
		if words[windowEnd] == secondWord:
			second += 1
		if words[windowStart] == firstWord:
			first -= 1
		if words[windowStart] == secondWord:
			second -= 1
		
		if first == 0 and second == 0:
			ratios.append(0)
		else:
			ratios.append(float(first) / (first+second))

		# Increment window indices
		windowEnd += 1
		windowStart += 1

	return ratios
	
def RollingRatioD(splitList, firstWord, secondWord, windowSize):
	"""
	Computes the rolling ratio of one word to another over a certain window
	(size in lines).
	aka. Word ratio in a window of lines.

	Args:
		splitList: the text already split by words or lines, as chosen
		firstWord: the word to count, for the ratio's numerator
		secondWord: the word to count, for the ratio's denominator
		windowSize: the number of lines to have in the window

	Returns:
		List of ratios, each index representing the window number
	"""
	windowStart = 0
	windowEnd = windowStart + windowSize

	# Rolling counts, to be divided for ratio
	first = 0
	second = 0

	words = splitList

	# Count the initial window
	for i in xrange(windowStart, windowEnd):
		for word in lines[i]:
			if word == firstWord:
				first += 1
			if word == secondWord:
				second += 1

	# Create list with initial value
	if first == 0 and second == 0:
		ratios = [0]
	else:
		ratios = [float(first) / (first+second)]

	while windowEnd < len(lines):
		for word in lines[windowEnd]:
			if word == firstWord:
				first += 1
			if word == secondWord:
				second += 1

		for word in lines[windowStart]:
			if word == firstWord:
				first -= 1
			if word == secondWord:
				second -= 1

		if second == 0 and first == 0:
			ratios.append(0)
		else:
			ratios.append(float(first) / (first+second))

		# Increment window indices
		windowEnd += 1
		windowStart += 1
			
	return ratios


def rollinganalyze(fileString, analysisType, inputType, windowType, keyWord, secondKeyWord, windowSize, filepath, widthWarp):
	"""
	Creates a rolling window plot depending on the specifications chosen by the user.

	Args:

	Returns:

	"""
	windowSize = int(windowSize)
	widthWarp = float(widthWarp)

	if windowType == 'word':
		splitList = fileString.split()
	elif windowType == 'line':
		if re.search('\r', fileString) != None:
			splitList = fileString.split('\r')
		else:
			splitList = fileString.split('\n')

	if windowType == 'word' or windowType == 'line':
		splitList = [i for i in splitList if i != '']


	if analysisType == 'average':
		if inputType == 'letter':
			if windowType == 'letter':				
				plotList = RollingAverageA(fileString, keyWord, windowSize)

			else: # windowType == 'word' or windowType == 'line'
				plotList = RollingAverageB(splitList, keyWord, windowSize)
		
		else: # inputType == 'word'
			if windowType == 'word':
				plotList = RollingAverageC(splitList, keyWord, windowSize)
			else: # windowType == 'line'
				plotList = RollingAverageD(splitList, keyWord, windowSize)

	elif analysisType == 'ratio':
		if inputType == 'letter':
			if windowType == 'letter':
				plotList = RollingRatioA(fileString, keyWord, secondKeyWord, windowSize)

			else: # by word or line
				plotList = RollingRatioB(splitList, keyWord, secondKeyWord, windowSize)

		else: # inputType == 'word'
			if windowType == 'word':
				plotList = RollingRatioC(splitList, keyWord, secondKeyWord, windowSize)
			else: # windowType == 'line'
				plotList = RollingRatioD(splitList, keyWord, secondKeyWord, windowSize)


	if inputType == 'letter':
		countUnitLabel = 'characters'
	elif inputType == 'word':
		countUnitLabel = 'words'
	else:
		countUnitLabel = 'lines'


	if analysisType == 'average':
		graphLabel = "Average number of " + keyWord + "'s in a window of " + str(windowSize) + " " + countUnitLabel + "."
	else:
		graphLabel = "Ratio of " + keyWord + "'s to (number of" + keyWord + "'s + number of " + secondKeyWord + ") in a window of " + str(windowSize) + " " + countUnitLabel + "."


	# fig = pyplot.figure(figsize=(10*widthWarp/100, 10))
	# pyplot.plot(plotList)
	# ax= pyplot.subplot(111)
	# ax.set_xlabel('Window number (left-most point in each window)')
	# ax.set_ylabel(Y_AXIS_LABEL)
	# pyplot.axis([0, len(plotList)-1, -0.01, max(plotList)+(max(plotList)/20)])
	# pyplot.savefig(open(filepath, 'w'), format='png')

	return True, plotList, graphLabel