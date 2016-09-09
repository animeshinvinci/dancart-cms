from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseServerError
from .forms import ContactForm

def send_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            try:
                send_mail('Contato pelo site', data['message'], "%s <%s>" % (data['name'], data['email']),
                          ['jefernandes.junior@gmail.com'],
                          fail_silently=False)
                return JsonResponse({'alert':'success', 'message':'Mensagem enviada com sucesso.'})
            except Exception:
                return JsonResponse({'alert':'error', 'message':'Não foi possível enviar o e-mail.'})

        else:
            return JsonResponse({'alert':'error', 'message':'O formulário contém erros que devem ser corrigidos.', 'errors':form.errors.as_json()})
    else:
        return HttpResponseNotAllowed(['POST'])