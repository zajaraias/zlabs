#!/usr/bin/env python
import Image, numpy

##Base image
b_im_o = Image.open("az_base.png")
b_im = b_im_o.convert("L")

##stamp params
s_size = 31
s_colour=255
s_num=100
s_radius_limits=[0.5*s_size/2.0, 1.4*s_size/2.0]

##output file param
o_size = [116,43] #number of stamps

stamp_list=[]
radius_list=[]

#stamp generator
#radius generator
for x in xrange(0, s_num):
	radius_list.append( x*((s_radius_limits[1]-s_radius_limits[0])/(s_num-1))+ s_radius_limits[0])
#print s_radius_limits
#print radius_list

for s in xrange(0, s_num):
	s_array = numpy.zeros(s_size**2).reshape(s_size,s_size)
	for x in xrange(0, s_size):
		for y in xrange(0, s_size):
			if ((x-s_size/2)**2 + (y-s_size/2)**2)<(radius_list[s]**2):
				s_array[x,y]= s_colour
	stamp_list.append(s_array)

##output generation
#resize image to match output file stamp number
b_ref=b_im.resize((o_size[0],o_size[1]))

b_ref_min=0.0
b_ref_max=255.0

print b_ref.format, b_ref.size, b_ref.mode

#first row in list form
o_list=[]
for x in xrange(0, o_size[0]):
	s_sel = int((b_ref.getpixel((x,0))-b_ref_min)*(s_num/(b_ref_max-b_ref_min)))
	o_list.append(stamp_list[s_sel])
	
#other stamps / conc en x
for x in xrange(0, o_size[0]):
	for y in xrange(1, o_size[1]):
		s_sel = int((b_ref.getpixel((x,y))-b_ref_min)*(s_num/(b_ref_max-b_ref_min)))
		o_list[x] = numpy.concatenate((o_list[x],stamp_list[s_sel]),axis=0)

#conc en y
o_array=o_list[0]
for x in xrange(1, o_size[0]):
	o_array=numpy.concatenate((o_array,o_list[x]),axis=1)

out=Image.fromarray(o_array.astype(numpy.uint8))
out.save("az_cover v5.png")

