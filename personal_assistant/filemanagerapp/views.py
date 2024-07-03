# filemanagerapp/views.py

from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import UserFile, Category
from .forms import FileUploadForm, CategoryForm, EditFileCategoryForm

from .context_processors import get_language
from .translations import translations


@login_required
def file_upload(request):
    language = get_language(request)
    trans = translations.get(language, translations['en'])

    if request.method == 'POST':
        form = FileUploadForm(user=request.user, language=language, data=request.POST, files=request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()
            return redirect('filemanagerapp:file_list')
    else:
        form = FileUploadForm(user=request.user, language=language)

    return render(request, 'filemanagerapp/file_upload.html', {'form': form, 'translations': trans})


@login_required
def file_list(request):
    language = get_language(request)
    trans = translations.get(language, translations['en'])

    translated_categories = {
        'Uncategorised': trans.get('uncategorised', 'Uncategorised'),
        'Photos': trans.get('photos', 'Photos'),
        'Videos': trans.get('videos', 'Videos'),
        'Music': trans.get('music', 'Music'),
        'Documents': trans.get('documents', 'Documents'),
        'Archives': trans.get('archives', 'Archives'),
        'Other': trans.get('other', 'Other')
    }

    all_files = UserFile.objects.filter(user=request.user)
    files = all_files
    categories = Category.objects.filter(user=request.user)

    selected_category_name = request.GET.get('category')
    if selected_category_name and selected_category_name != 'All':
        files = files.filter(category__name=selected_category_name)

    paginator = Paginator(files, 5)
    page = request.GET.get('page')
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)

    return render(request, 'filemanagerapp/file_list.html', {
        'files': files,
        'categories': categories,
        'selected_category_name': selected_category_name,
        'has_files': all_files.exists(),
        'translations': trans,
        'translated_categories': translated_categories
    })


@login_required
def file_download(request, file_id):
    language = get_language(request)
    trans = translations.get(language, translations['en'])

    try:
        file = UserFile.objects.get(pk=file_id, user=request.user)
        response = HttpResponse(
            file.file, content_type='application/octet-stream'
        )
        response['Content-Disposition'] = (
            f'attachment; filename="{file.file.name}"'
        )
        return response
    except UserFile.DoesNotExist:
        raise Http404(trans['file_not_found'])


@login_required
def file_delete(request, file_id):
    file = get_object_or_404(UserFile, pk=file_id, user=request.user)
    file.file.delete()  # This deletes the file from Cloudinary
    file.delete()  # This deletes the file record from the database
    return redirect('filemanagerapp:file_list')


@login_required
def create_category(request):
    language = get_language(request)
    trans = translations.get(language, translations['en'])

    if request.method == 'POST':
        form = CategoryForm(user=request.user, language=language, data=request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            try:
                category.save()
                return redirect('filemanagerapp:category_management')
            except IntegrityError:
                form.add_error('name', trans['category_exists'])
    else:
        form = CategoryForm(user=request.user, language=language)

    return render(request, 'filemanagerapp/category_form.html', {'form': form, 'translations': trans})


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    category.delete()
    return redirect('filemanagerapp:category_management')


@login_required
def edit_file_category(request, file_id):
    language = get_language(request)
    trans = translations.get(language, translations['en'])

    file = get_object_or_404(UserFile, pk=file_id, user=request.user)
    if request.method == 'POST':
        form = EditFileCategoryForm(user=request.user, language=language, data=request.POST, instance=file)
        if form.is_valid():
            form.save()
            return redirect('filemanagerapp:file_list')
    else:
        form = EditFileCategoryForm(user=request.user, language=language, instance=file)

    default_categories = {
        'Uncategorised': trans['uncategorised'],
        'Photos': trans['photos'],
        'Videos': trans['videos'],
        'Music': trans['music'],
        'Documents': trans['documents'],
        'Archives': trans['archives'],
        'Other': trans['other'],
    }

    return render(request, 'filemanagerapp/file_upload.html', {
        'form': form,
        'edit_mode': True,
        'file_name': file.file.name,
        'current_category': default_categories.get(file.category.name, file.category.name) if file.category else trans['none'],
        'translations': trans
    })


@login_required
def category_management(request):
    language = get_language(request)
    trans = translations.get(language, translations['en'])
    translated_categories = {
        'Uncategorised': trans.get('uncategorised', 'Uncategorised'),
        'Photos': trans.get('photos', 'Photos'),
        'Videos': trans.get('videos', 'Videos'),
        'Music': trans.get('music', 'Music'),
        'Documents': trans.get('documents', 'Documents'),
        'Archives': trans.get('archives', 'Archives'),
        'Other': trans.get('other', 'Other')
    }
    categories = Category.objects.filter(user=request.user)
    return render(
        request,
        'filemanagerapp/category_management.html',
        {
            'categories': categories,
            'translations': trans,
            'translated_categories': translated_categories
        }
    )

