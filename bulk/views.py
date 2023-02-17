from django.shortcuts import render,redirect, HttpResponseRedirect
from .models import Image
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.

def my_view(request):
    if request.method == "POST":
        # messages.success(request, 'upload successfully.')
        # if the post request has a file under the input name 'document', then save the file.
        if 'images' in request.FILES:
            request_file = request.FILES.getlist('images')
            # request_file = request.FILES['images']
            # print(len(request_file))
        else:
            request_file =None
        if request_file:
            # save attached file
            img_url_store = []
            for img in request_file:
                # create a new instance of FileSystemStorage
                fs = FileSystemStorage()
                # the file_url variable now contains the url to the file. This can be used to serve the file when needed.
                file = fs.save(img.name, img)
                file_url = fs.url(file)
                img_url_store.append(file_url)
            # print(img_url_store)
       
            final_url = ','.join(img_url_store)
            # print("final url", final_url)
            record = Image(image=final_url)
            record.save()
            messages.success(request,'uploaded successfully!')
            # print(file_url)
       
            
        
    images = Image.objects.all()
 
    all_image = []
    for first_ob in images:
        lst = first_ob.image.split(',')
        print(lst)
        img_id=first_ob.id
        print(img_id)
        
        img_lst=[]
        img_lst.append(img_id)
        for i in lst:
            print(i)
            img_lst.append(i)
        all_image.append(img_lst)
        # print("sjnakjsn", all_image)
        # return HttpResponse('bulk_upload')

    return render(request, "index.html", {'final_images':all_image})

def update_image(request, id):
    print("ksdnlkdsnsdklndlksn")
    messages.success(request,'update successfully!')
    if request.method == "POST":
        print("hbjhbjhb================================================================,post")
        image_name = request.POST['image_name']
        print(image_name,"..............................")
        new_file = request.FILES.get('new_images')
        print(new_file,",,,,,,,,,,,,,,,,,,,,,,,,,,")
        print("id=======================================",id)
        # retrieve the image record by ID
        image = Image.objects.get(id=id)

        print(image,"++++++++++++++++++++++++++")

        # split the image field by comma to get a list of URLs
        image_urls = image.image.split(',')
        print(image_urls,",,,,,,,,,,,,,,,,,,,,,,,,,,")

        # find the index of the old image URL to be replaced
        old_url_index = image_urls.index(image_name)
        print(old_url_index,",,,,,,,,,,,,,,,,,,,,,,,,,,")

        # if a new file was uploaded, replace the old URL with the new URL
        if new_file:
            fs = FileSystemStorage()
            print(fs,",,,,,,,,,,,,,,,,,,,,,,,,,,")

            file_name = fs.save(new_file.name, new_file)
            print(file_name,",,,,,,,,,,,,,,,,,,,,,,,,,,")

            file_url = fs.url(file_name)
            print(file_url,",,,,,,,,,,,,,,,,,,,,,,,,,,")

            image_urls[old_url_index] = file_url
            print(image_urls[old_url_index],"-----------------------------------")
        # else:
         # if no new file was uploaded, just remove the old URL
            # image_urls.pop(old_url_index)

        # join the list of URLs back into a comma-separated string
        new_image_field = ','.join(image_urls)

      # update the image record with the new image field value
        image.image = new_image_field
        print(new_image_field,",,,,,,,,,,,,,,,,,,,,,,,,,,")
        image.save()
        return redirect('bulk_upload')
    else:
        print("dsnkjsnkldsnldksndsklndsklnds")
    messages.success(request,'update successfully!')
    

# def update_image(request, id):
#     if request.method == "POST":
#         print(".............................",id)
#         # image_id = request.POST['image_id']
#         # print("img_id",image_id)
#         image_name = request.POST['image_name']
#         print('image_name```````````````````````',image_name)
#         # retrieve the image record by ID
#         images = Image.objects.get(id=id)
#         print("list---------------",images.image)
      
#         # save the new image file
#         if 'new_images' in request.FILES:
#             request_file = request.FILES['new_images']
#             print("file name******************************",request_file)
#             fs = FileSystemStorage()
#             print(fs)
#             file = fs.save(request_file.name, request_file)
#             print(file,"###################################")
#             file_url = fs.url(file)
#             print("kabkbjabkjFGNKHGVUYHJUDRTFTZSXD",file_url)
#             img_data=images.image
#             print(img_data,"ahbsakjx naksjchiosdjsos")
#             old_url=img_data.split(',')
#             print(old_url,"oooooooooooooooooooooooooooooooo")
#             old_url.remove(image_name)
#             old_url.append(file_url)
#             print(old_url,"//////////////////////////////////////")
#             new_url=','.join(old_url)
#             print(new_url,"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
#             # # update the image record with the new file URL
#             images.image = new_url
#             images.save()
#             return redirect('bulk_upload')
       

def delete_image(request, id):
    if request.method == 'POST':
        print("deletndkajabnkjn")
        image_name = request.POST['image_delete']
        print('image_name',image_name)
       
    # get the image from the database
    # image = get_object_or_404(Image, pk=pk)
        images = Image.objects.get(id=id)
        img_value=images.image
        delete_img=img_value.split(',')
        delete_img.remove(image_name)
        # print(delete_img,"-----------------------------------------------------")
        new_value=','.join(delete_img)
        images.image = new_value
        images.save()
        if not images.image:
            images.delete()
        messages.success(request,'deleted successfully!')
        # print('ajkadnjkanakjnkjnjkn',new_value)
        # redirect to the index page
        return redirect('bulk_upload')
    return render(request,'index.html')