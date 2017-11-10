
def getBox(result, box):
	#result = str(bin(result)[2:]).zfill(8)
#	for i in range(0, (8 - len(result))):
#		result = "0" + result
#	print("converted result = " + str(result))
	#print("result = " + str(result[box]))
	result = result[::-1]
	return result[box]


def getLeds(result):
	LEDS = [0,1,3,7,15,31]
	goodLeds = 0
	for n in result:
		if n == str(0):
			goodLeds = goodLeds + 1
	if LEDS[goodLeds] == 31:
		return 159
	else:
		return LEDS[goodLeds]