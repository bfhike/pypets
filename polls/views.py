
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class IndexView(generic.ListView):

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    keyword = None

    def __init__(self, **kwargs):
        super(IndexView, self).__init__()
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """

    def dispatch(self, request, *args, **kwargs):
        """ had to override this to save the keyword value for some reason??? """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        logger.debug(len(kwargs))
        for key in kwargs:
            logger.debug("kwargs key=%s value=%s" % (key, None))

        if 'keyword' in kwargs:
            logger.debug("keyword=%s" % (kwargs['keyword']))
            self.keyword = kwargs['keyword']

        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        logger.debug(len(args))
        for key, value in args:
            logger.debug("args key=%s value=%s" % (key, value))

        return super(IndexView, self).dispatch(request, args, kwargs)

    def get_queryset(self):
        logger.debug("index keyword=%s" % self.keyword)

        if self.keyword is None:
            """Return the last five published questions."""
            return Question.objects.filter(
                pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]
        else:
            """Return last five matching questions."""
            return Question.objects.filter(
                pub_date__lte=timezone.now(),
                question_text__contains=self.keyword
            ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """ Excludes any questions that aren't published yet.  """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def search(request):
    first_word = request.POST['question_text']
    if len(first_word) == 0:
        first_word = None
    return HttpResponseRedirect(reverse('polls:indexsearch', args=(first_word,)))


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
