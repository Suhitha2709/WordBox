import requests
from django.shortcuts import render
from django.http import JsonResponse
from .models import Word
from datetime import date
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def dashboard(request):
    return render(request, 'home.html')
def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # make sure this name matches your url name
    return render(request, 'home.html')
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or redirect to homepage
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



@require_http_methods(["DELETE"])
def delete_word(request):
    word = request.GET.get('word')
    try:
        Word.objects.get(word=word).delete()
        return JsonResponse({'message': f'"{word}" deleted successfully.'})
    except Word.DoesNotExist:
        return JsonResponse({'error': 'Word not found.'}, status=404)

@login_required
def home(request):
    return render(request, 'home.html')

def search_word(request):
    word = request.GET.get('word')
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            entry = data[0]
            meaning_parts = []
            examples = []

            for meaning in entry.get('meanings', []):
                part_of_speech = meaning.get('partOfSpeech', '')
                for definition in meaning.get('definitions', []):
                    definition_text = definition.get('definition', '')
                    example = definition.get('example', '')
                    if definition_text:
                        meaning_parts.append(f"{part_of_speech}: {definition_text}")
                    if example:
                        examples.append(example)

            pronunciation = entry.get('phonetics', [{}])[0].get('text', '')
            return JsonResponse({
                'word': word,
                'pronunciation': pronunciation,
                'meaning': '\n'.join(meaning_parts),
                'examples': examples  # Include example usage!
            })
        else:
            return JsonResponse({'error': 'No definition found'}, status=404)
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)
@login_required
def save_word(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        meaning = request.POST.get('meaning')
        Word.objects.create(user=request.user, word=word, meaning=meaning)
        return JsonResponse({'message': 'Word saved successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def list_saved_words(request):
    search_query = request.GET.get('search', '')
    words = Word.objects.filter(user=request.user, word__icontains=search_query).values('word', 'meaning')
    return JsonResponse(list(words), safe=False)

@login_required
def daily_review(request):
    today_words = Word.objects.filter(user=request.user, saved_at__date=date.today()).values('word', 'meaning')
    return JsonResponse(list(today_words), safe=False)
