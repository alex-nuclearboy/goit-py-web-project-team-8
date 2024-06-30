from django.shortcuts import render, redirect, get_object_or_404
from .models import UserFile, FileUploadForm, Category
from .forms import CategoryForm
from cloudinary.uploader import upload, destroy

# Create your views here.
# функция для за вантаження файлу + 
# отображення функция списку файлов + 

# скачать файл +
# удалить файл +
# 
# функция для створення сатегории +
# удалить +

# Work file
def upload_file(request):
    
    """
    View function for uploading files to a cloud service list of uploaded files by user
    
    Returns:
        Message about successful or unsuccessful uploaded of user file
    """
    
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = upload(request.FILES['file'])
            user_file = form.save(commit=False)
            user_file.public_id = uploaded_file['public_id']
            user_file.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})
    
    # if request.method == 'POST':
    #     form = FileUploadForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('file_list')
    # else:
    #     form = FileUploadForm()
    # return render(request, 'upload.html', {'form': form})           


def file_list(request, category=None):
    
    """
    View function for viewing uploaded files to a cloud service
    
    Returns:
    file_list  - list of uploads files by user.
    
    """
    
    if category:
        files = UserFile.objects.filter(category=category)
    else:
        files = UserFile.objects.all()
    return render(request, 'file_list.html', {'files': files, 'category': category})


def download_file(request, file_id):
    
    """
    View function for downloading files from cloud service
    
    Returns:
    user_file  - User file.
    
    """
    
    user_file = get_object_or_404(UserFile, id=file_id)
    
    return redirect(user_file.file.url)


def delete_file(request, file_id):
    
    """
    View function for delete files from cloud service
    
    Returns:
    user_file  - delete user file
    
    """
    
    user_file = get_object_or_404(UserFile, id=file_id)
    destroy(user_file.public_id)
    user_file.delete()
    return redirect('file_list')


# *******************************************************
# Category
def manage_category(request):
    
    """
    View function for displaying a list of notes associated with the logged-in user.

    Retrieves notes based on search queries and tag filters, handles pagination.

    Returns:
    HttpResponse: Rendered template with notes, tags, search form, and tag filter.
    """
    
    if request.method == 'POST':
        if 'create' in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_category')
        elif 'delete' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id)
            if not category.is_standard:
                category.delete()
            return redirect('manage_category')
    else:
        form = CategoryForm()

    categories = Category.objects.all()
    
    return render(request, 'manage_category.html', {'categories': categories, 'form': form})