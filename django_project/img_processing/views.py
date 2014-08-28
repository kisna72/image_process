from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import random, string
from django.conf import settings
## AWS Related Imports
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto
from PIL import Image
from cStringIO import StringIO
import cStringIO

AWSAccessKeyId='AccessKeyHere'
AWSSecretKey='SecurityKeyHere'


def uploadImageToAWS(image="", bucket="testingthistucket"):
    TN_size = (128, 128)
    LAP_size = (1024,1024)
    file_type = '.jpg'
    connection = S3Connection(AWSAccessKeyId, AWSSecretKey)
    sbucket = connection.get_bucket(bucket)
    base_name = random_ascii_generator(25)
    tn_name = '_thumbnail_' + base_name  + file_type
    md_name = '_medium_' + base_name  + file_type
    lg_name = '_large_' + base_name +  file_type
    headers = {'Content-Type': 'image/png'}
    print tn_name, md_name, lg_name

    possible = sbucket.get_key(tn_name)#Always wanna check if the file exists.
    if possible:
        base_name = random_ascii_generator(26)
        tn_name = '_thumbnail_' + base_name  + file_type
        md_name = '_medium_' + base_name  + file_type
        lg_name = '_large_' + base_name +  file_type
    possible = sbucket.get_key(tn_name)#Always wanna check if the file exists.
    if possible:
        base_name = random_ascii_generator(27)
        tn_name = '_thumbnail_' + base_name  + file_type
        md_name = '_medium_' + base_name  + file_type
        lg_name = '_large_' + base_name +  file_type
    
    print possible
    print 'Image open'
    ##Now Start Uploading each file
    im = Image.open(image)#changes to image
    ##Original
    original = StringIO()
    print 'cString Opened'
    im.save(original, 'JPEG')
    print 'image.save in Original'
    k = Key(sbucket)
    k.key = lg_name
    k.set_contents_from_string(original.getvalue() , headers)
    print 'Saved Large'
    ##Large
    large = cStringIO.StringIO()
    im.thumbnail(LAP_size, Image.ANTIALIAS)
    im.save(large, 'JPEG')
    k.key = md_name
    k.set_contents_from_string(large.getvalue(), headers)
    print 'Saved Medium'


    ##ThumbNail
    thumbnail = cStringIO.StringIO()
    im.thumbnail(TN_size)
    im.save(thumbnail, 'JPEG')
    k.key = tn_name
    k.set_contents_from_string(thumbnail.getvalue(), headers)
    print 'Saved ThumbNail'

    output = {}
    output['Success'] = 'Success'
    output['Error'] = False
    output['image_name'] = base_name + file_type
    print 'Returning'
    return output
    try:
        TN_size = (128, 128)
        LAP_size = (1024,1024)
        file_type = '.jpg'
        connection = S3Connection(AWSAccessKeyId, AWSSecretKey)
        sbucket = connection.get_bucket(bucket)
        base_name = random_ascii_generator(25)
        tn_name = '_thumbnail_' + base_name  + file_type
        md_name = '_medium_' + base_name  + file_type
        lg_name = '_large_' + base_name +  file_type

        print tn_name, md_name, lg_name

        possible = sbucket.get_key(tn_name)#Always wanna check if the file exists.
        if possible:
            base_name = random_ascii_generator(26)
            tn_name = '_thumbnail_' + base_name  + file_type
            md_name = '_medium_' + base_name  + file_type
            lg_name = '_large_' + base_name +  file_type
        possible = sbucket.get_key(tn_name)#Always wanna check if the file exists.
        if possible:
            base_name = random_ascii_generator(27)
            tn_name = '_thumbnail_' + base_name  + file_type
            md_name = '_medium_' + base_name  + file_type
            lg_name = '_large_' + base_name +  file_type
        
        print possible

        ##Now Start Uploading each file
        im = Image.open(image)#changes to image
        
        ##Original
        original = cStringIO.StringIO()
        im.save(original, 'JPEG')
        k = Key(sbucket)
        k.key = lg_name
        k.set_metadata('Content-Type', 'image/jpeg')
        k.set_contents_from_string(original.getvalue(), headers)
        print 'Saved Large'
        ##Large
        large = cStringIO.StringIO()
        im.thumbnail(LAP_size, Image.ANTIALIAS)
        im.save(large, 'JPEG')
        k.key = md_name
        k.set_metadata('Content-Type', 'image/jpeg')
        k.set_contents_from_string(large.getvalue(), headers)
        #k.content_type = "image/jpeg"
        print 'Saved Medium'


        ##ThumbNail
        thumbnail = cStringIO.StringIO()
        im.thumbnail(TN_size)
        im.save(thumbnail, 'JPEG')
        k.key = tn_name
        k.set_metadata('Content-Type', 'image/jpeg')
        k.set_contents_from_string(thumbnail.getvalue(), headers)
        k.content_type = "image/jpeg"
        
        print 'Saved ThumbNail'

        output = {}
        output['Success'] = 'Success'
        output['Error'] = False
        output['image_name'] = base_name + file_type
        print 'Returning'
        return output
    except:
        print 'Something Went Wrong'
        output['Success'] = False
        output['Error'] = 'Error'
        output['image_name'] = base_name + file_type
        return output

# Create your views here.
def test(request):
    return HttpResponse('This is tTest')

#Post REquest is always looking for csrf_exempt Status
@csrf_exempt
def upload_image(request):
    print 'Enter Method'
    if request.is_ajax():
        print 'Request is AJAX'
    if request.method == "POST":
        print 'Post Request'
        print request.POST
        images = request.FILES.getlist('file')
        print 'Uploading Files to AWS ...' 
        if images:
            image_name = uploadImageToAWS(images[0])
        else:
            print 'Sucks, The image isnt there'
        output = {}
        print json.dumps(image_name)
        if image_name['Success'] == "Success":
            output['image_name'] = image_name["image_name"];
            output['Success'] = 'Image Saved SuccessFully'
        if image_name['Error'] == "Error":
            output['Error'] = 'Image Saving Failed'
        #image_name = save_file_in_media_folder(images[0])
        print json.dumps(output)
        #print image_name, 'is the image name'
        #print 'Got the firebaseToken'
        #print t
        #p = json.dumps(t)
        #return HttpResponse(json.dumps(t))
        #print 'Post'
    if request.method == "GET":
        output = {}
        output["SuccessGet"] = "This is a GET Request"
        print 'GET'
    return HttpResponse(json.dumps(output))

def save_file_in_media_folder(image):
    im = image.read()
    print "read the Image"
    folder_to_save = '/Users/krishnaregmi/onedrive/django_projects/media'
    print folder_to_save
    print 'getting unique_image_name'
    unique_image_name = random_ascii_generator(24) + '.jpg'
    print unique_image_name
    with open('%s/%s' %(folder_to_save, unique_image_name), 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)
            #print "wrote chunk"    
        image_name = 'media/%s' %(unique_image_name)
        return image_name

def random_ascii_generator(integer):
    ascii_char = string.ascii_uppercase + string.ascii_lowercase + string.digits
    output = ''
    t = output.join(random.choice(ascii_char) for x in range(int(integer)))
    #print t
    return t