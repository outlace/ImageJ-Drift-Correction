
from ij import IJ
from ij.plugin.frame import RoiManager

print "'Multi Drift Correction' plugin; version 1.1; by Brandon Brown"

#converts microns (or whatever the physical dist is to pixels)
'''
def getPixelPos(x,y, imp):
	point = [0,0]
	point[0] = (x / cal.piXelW)
	point[1] = (imp.height * (y / 100))
	return point
'''
rm = RoiManager.getInstance() #get the open ROI manager instance
ra = rm.getRoisAsArray()  #get all the ROIs in an array
#print r1.getPosition()
imp = IJ.getImage() #get current image
stack = imp.getStack() #get current 
rm = RoiManager.getInstance()
ra = rm.getRoisAsArray()
nRois = len(ra)
proc = IJ.getProcessor() #get the image processor
cal = imp.getCalibration();
#print cal.pixelWidth
#print imp.width
totSlices = int(stack.getSize())
#print stack.getSize()
#print r1.getFloatPolygon().xpoints[0]  #get xpoint
#first convert our ROIs to something more useful, a tuple containing the point (x,y) and the Z position => (x,y,z)
for i in range(0, nRois-1):
	roi1 = rm.getRoi(i)
	roi2 = rm.getRoi(i+1)
	pt1 = (roi1.getFloatPolygon().xpoints[0],roi1.getFloatPolygon().ypoints[0],roi1.getPosition())
	pt2 = (roi2.getFloatPolygon().xpoints[0],roi2.getFloatPolygon().ypoints[0],roi2.getPosition())
	startSlice = pt1[2]
	endSlice = pt2[2]
	nSlices = (endSlice - startSlice)
	xcorrect = (pt1[0]-pt2[0]);
   	ycorrect = (pt1[1]-pt2[1]);
   	print "Point pair: "
   	print pt1
   	print pt2
   	IJ.setSlice(pt1[2]) #set starting slice
	driftx = xcorrect/nSlices; 
	offsetx = 0;
	print "startSlice: %s ;endSlice: %s" % (startSlice, endSlice)
	print "nSlices: %s" % (nSlices,)
	for j in range(startSlice, totSlices+1): 
		IJ.setSlice(j)
		if j <= endSlice:
			offsetx += driftx
		IJ.run("Translate...", "interpolation=Bicubic slice y=0 x="+str(offsetx)); 

	drifty = ycorrect/nSlices; 
	offsety = 0; 
	for k in range(startSlice, totSlices+1):
		IJ.setSlice(k)
		if k <= endSlice:
			offsety += drifty
		IJ.run("Translate...", "interpolation=Bicubic slice x=0 y="+str(offsety));


