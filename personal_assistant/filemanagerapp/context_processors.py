from .translations import translations


def get_language(request):
    language = request.GET.get('lang')
    if not language:
        language = request.session.get('language', 'en')
    request.session['language'] = language
    return language


def translations_context_processor(request):
    language = get_language(request)
    return {
        'translations': translations.get(language, translations['en']),
    }
