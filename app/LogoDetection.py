import argparse
import io

from google.cloud import vision

def detectLogo( imgPath ) :
	visionClient = vision.Client();

	with io.open( imgPath, "rb" ) as image_file :
		content = image_file.read();

	image = visionClient.image( content = content );

	logos = image.detect_logos();
	ret = [ logo.description for logo in logos ];

	return ret;