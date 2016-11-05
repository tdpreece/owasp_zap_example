from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import FormView, View

from .forms import ContactForm


def index(request):
    return render(request, 'app/index.html')


def thanks(request):
    return HttpResponse("Thanks!")


class ContactView(FormView):
    template_name = 'app/contact.html'
    form_class = ContactForm
    success_url = 'thanks'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(ContactView, self).form_valid(form)


class SearchView(View):
    template_name = 'app/search.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        query = request.POST.get('query')
        return render(request, self.template_name, {'query': query})
