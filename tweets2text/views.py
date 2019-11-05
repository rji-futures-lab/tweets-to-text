import base64
import hashlib
import hmac
import json
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView, View
from tweets2text.handlers import handle_account_activity
from tweets2text.models import (
    AccountActivity, TweetTextCompilation,
)
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import TextEditForm
from django.views.generic.edit import UpdateView


class Homepage(TemplateView):
    template_name = "tweets2text/homepage.html"


@method_decorator(csrf_exempt, name='dispatch')
class TwitterWebhook(View):

    def get(self, request):
        """
        Perform a Challenge-Response Check (CRC) to secure the Twitter webhook.

        The CRC verifies with Twitter that we own the app and the webhook URL.

        Twitter makes GET method calls to this route with a crc_token, which is
        used along with TWITTER_CONSUMER_SECRET to build a response_token.

        Return JSON that includes the response_token.
        """
        crc = request.GET.get('crc_token')

        validation = hmac.new(
            key=bytes(settings.TWITTER_CONSUMER_SECRET, 'utf-8'),
            msg=bytes(crc, 'utf-8'),
            digestmod=hashlib.sha256
        )
        digested = base64.b64encode(validation.digest())
        resp_data = dict(
            response_token='sha256=' + format(str(digested)[2:-1])
        )

        return JsonResponse(resp_data)

    def post(self, request, *args, **kwargs):
        """
        Route called by Twitter to announce account activity.

        Twitter makes POST method calls to this route.
        """
        aa_obj = AccountActivity.objects.create(
            json_data=json.loads(request.body),
        )

        handle_account_activity(str(aa_obj.id))

        resp_data = dict(
            direct_message_events=len(aa_obj.direct_message_events),
            follow_events=len(aa_obj.direct_message_events),
            tweet_create_events=len(aa_obj.direct_message_events),
        )

        return JsonResponse(resp_data)

def plain_text_view(request, compilation_id):
    try:
        compilation = TweetTextCompilation.objects.filter(
            completed_at__isnull=False
        ).get(id=compilation_id)
    except TweetTextCompilation.DoesNotExist:
        raise Http404("Compilation does not exist")
    response = HttpResponse(
        compilation.text,
        content_type="text/plain; charset=utf-8",
    )

    return response

def text_edit(request, compilation_id):
    compilation = get_object_or_404(TweetTextCompilation, id=compilation_id)
    form = TextEditForm(request.POST or None, instance=compilation)
    if form.is_valid():
        if(request.POST.get('revert')):
            compilation.complete()
        else:
            instance = form.save(commit=False)
            instance.save()

    context = {
        "id": compilation.id,
        "text": compilation.text,
        "form": form,
    }
    return render(request, 'tweets2text/text_edit.html', context)

class TweetTextUpdate(UpdateView):
    model = TweetTextCompilation
    form_class = TextEditForm
    template_name_suffix = '_update_form'
    pk_url_kwarg = 'compilation_id'
    context_object_name = 'compilation'
    success_url = 'edit'
    reverting = False

    def post(self, request, *args, **kwargs):
        compilation = get_object_or_404(TweetTextCompilation, pk=self.kwargs['compilation_id'])
        if "revert" in request.POST:
            print("Reverting...")
            compilation.complete()
            self.reverting = True
            request.POST._mutable = True
        else:
            self.reverting = False
        return super(TweetTextUpdate, self).post(request, *args, **kwargs)
    
    def form_valid(self, form):
        compilation = get_object_or_404(TweetTextCompilation, pk=self.kwargs['compilation_id'])
        if(self.reverting == True):
            pass
        else:
            form.save()
        return HttpResponseRedirect(self.get_success_url())
    