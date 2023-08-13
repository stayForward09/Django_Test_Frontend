from django.shortcuts import render, redirect
from .models import Category, Type, Article
from .forms import CategoryForm, TypeForm, ArticleForm
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
def view_article(request, type_id):
    category_form = CategoryForm()
    type_form = TypeForm()
    article_form = ArticleForm()

    search_query = request.GET.get('search', '')
    search_by = request.GET.get('search_by', 'location')
    used_filter = request.GET.get('used', '')

    articles = Article.objects.filter(model__id=type_id)

    if search_query:
        if search_by == 'location':
            articles = articles.filter(location__icontains=search_query)
        elif search_by == 'sn':
            articles = articles.filter(sn__icontains=search_query)

    if used_filter:
        articles = articles.filter(used=used_filter)

    categories = Category.objects.all()
    types = Type.objects.all()

    context = {
        'articles': articles,
        'categories': categories,
        'category_form': category_form,
        'type_form': type_form,
        'article_form': article_form,
        'types': types,
        'type_id': type_id
    }

    if request.method == 'POST':
        where = request.POST.get('whereDropdown')
        form = None
        error_message = None
        if where == 'categories':
            form = CategoryForm(request.POST)
            if Category.objects.filter(name=request.POST.get('category-name')).exists():
                error_message = 'Kategorie mit diesem Namen existiert bereits.'
                form.add_error('name', error_message)
        elif where == 'types':
            form = TypeForm(request.POST)
            if Type.objects.filter(name=request.POST.get('type-name')).exists():
                error_message = 'Typ mit diesem Namen existiert bereits.'
                form.add_error('name', error_message)
        elif where == 'articles':
            form = ArticleForm(request.POST)
            if Article.objects.filter(sn=request.POST.get('article-sn')).exists():
                error_message = 'Eintrag mit dieser Seriennummer existiert bereits.'
                form.add_error('sn', error_message)

        if form is not None and form.is_valid():
            form.save()
            return redirect('view_article', type_id=type_id)
        else:
            if form is not None:
                context['form'] = form
            return render(request, 'view_article.html', context)

    return render(request, 'view_article.html', context)




def view_types(request, category_id):
    print("Viewing types for category_id:", category_id) # Debugging-Print-Statement

    category_form = CategoryForm()
    type_form = TypeForm()
    article_form = ArticleForm()
    success = False
    form = None  # Initialisieren der Variable form

    # Wenn die Anfrage ein POST ist, wird ein neuer Eintrag erstellt.
    if request.method == 'POST':
        where = request.POST.get('whereDropdown')
        form = None
        error_message = None

        if where == 'categories':
            category_form = CategoryForm(request.POST)
            form = category_form
            if Category.objects.filter(name=request.POST.get('category-name')).exists():
                error_message = 'Kategorie mit diesem Namen existiert bereits.'
                category_form.add_error('name', error_message)
        elif where == 'types':
            type_form = TypeForm(request.POST)
            form = type_form
            if Type.objects.filter(name=request.POST.get('type-name')).exists():
                error_message = 'Typ mit diesem Namen existiert bereits.'
                type_form.add_error('name', error_message)
        elif where == 'articles':
            article_form = ArticleForm(request.POST)
            form = article_form
            if Article.objects.filter(sn=request.POST.get('article-sn')).exists():
                error_message = 'Eintrag mit dieser Seriennummer existiert bereits.'
                article_form.add_error('sn', error_message)

        if form is not None and form.is_valid():
            print("Form is valid, saving...") # Debugging-Print-Statement
            form.save()
            return redirect('view_types', category_id=category_id) # Ändern Sie die Umleitung je nach Bedarf.
        else:
            # Rendern Sie die Seite erneut mit den vorhandenen Einträgen, auch wenn die Form ungültig ist
            categories = Category.objects.all()
            types = Type.objects.filter(category_id=category_id)
            context = {
                'categories': categories,
                'category_form': category_form,
                'type_form': type_form,
                'article_form': article_form,
                'types': types,
                'category_id': category_id,
            }
            if form is not None:
                context['form'] = form
            return render(request, 'view_types.html', context)

    # Wenn die Anfrage ein GET ist, rendern Sie die Seite mit den vorhandenen Einträgen.
    else:
        print("GET request, rendering page...") # Debugging-Print-Statement
        categories = Category.objects.all()
        types = Type.objects.filter(category_id=category_id) # Filtern basierend auf category_id
        context = {
            'categories': categories,
            'category_form': category_form,
            'type_form': type_form,
            'article_form': article_form,
            'types': types,
            'category_id': category_id,
        }
        if form is not None:  # Verwenden Sie die Variable form nur, wenn sie nicht None ist
            context['form'] = form
        return render(request, 'view_types.html', context)


def index(request):
    category_form = CategoryForm()
    type_form = TypeForm()
    article_form = ArticleForm()

    if request.method == 'POST':
        where = request.POST.get('whereDropdown')
        form = None
        error_message = None

        if where == 'categories':
            category_form = CategoryForm(request.POST)
            form = category_form
            if Category.objects.filter(name=request.POST.get('category-name')).exists():
                error_message = 'Kategorie mit diesem Namen existiert bereits.'
                category_form.add_error('name', error_message)
        elif where == 'types':
            type_form = TypeForm(request.POST)
            form = type_form
            if Type.objects.filter(name=request.POST.get('type-name')).exists():
                error_message = 'Typ mit diesem Namen existiert bereits.'
                type_form.add_error('name', error_message)
        elif where == 'articles':
            article_form = ArticleForm(request.POST)
            form = article_form
            if Article.objects.filter(sn=request.POST.get('article-sn')).exists():
                error_message = 'Eintrag mit dieser Seriennummer existiert bereits.'
                article_form.add_error('sn', error_message)

        if form and form.is_valid():
            form.save()
            request.session['success'] = True
            return HttpResponseRedirect(reverse('index'))
        else:
            print("Form is not valid")
            print("Form errors:", form.errors)
            if error_message:
                request.session['error_message'] = error_message

    success = request.session.pop('success', False)
    error_message = request.session.pop('error_message', None)

    categories = Category.objects.all()
    context = {
        'categories': categories,
        'category_form': category_form,
        'type_form': type_form,
        'article_form': article_form,
    }

    return render(request, 'index.html', context)

def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.save()
        return redirect('index')
    
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('index')

def edit_type(request, type_id):
    type_obj = Type.objects.get(id=type_id)
    category_id = type_obj.category.id
    if request.method == 'POST':
        type_obj.name = request.POST['name']
        type_obj.save()
        return redirect('view_types', category_id=category_id)

def delete_type(request, type_id):
    type_obj = Type.objects.get(id=type_id)
    category_id = type_obj.category.id # Holt die Kategorie-ID, zu der dieser Typ gehört
    type_obj.delete()
    return redirect('view_types', category_id=category_id)

def edit_article(request, article_sn):
    print(request.POST)
    print("edit_article called with sn:", article_sn)  # Log start of function
    article = get_object_or_404(Article, sn=article_sn)
    
    if request.method == 'POST':
        print("POST method detected")  # Log POST method
        form = ArticleForm(request.POST, instance=article)
        
        if form.is_valid():
            print("Form is valid, saving...")  # Log valid form
            form.save()
            print("Form saved successfully")  # Log successful save
            return redirect('view_article', type_id=article.model.id)
        else:
            print("Form is invalid, errors:", form.errors)  # Log form errors
            return JsonResponse({"status": "error", "errors": form.errors})

    print("Invalid request method")  # Log invalid request method
    return JsonResponse({"status": "error", "message": "Invalid request method"})



def delete_article(request, article_sn):
    article = get_object_or_404(Article, sn=article_sn)
    article.delete()
    return redirect('view_article', type_id=article.model.id)