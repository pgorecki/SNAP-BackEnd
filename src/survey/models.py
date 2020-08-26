from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import ObjectRoot
from core.managers import AgencyObjectManager
from core.json_yaml_field import JsonYamlField
from client.models import Client
from survey.enums import QuestionCategory


class Question(ObjectRoot):
    class Meta:
        ordering = ['-created_at']

    title = models.CharField(max_length=64)
    description = models.TextField(default='', blank=True)
    category = models.CharField(choices=QuestionCategory.choices,
                                max_length=32, default=QuestionCategory.TEXT)
    options = ArrayField(models.CharField(
        max_length=64), null=True, blank=True)
    other = models.BooleanField(default=False)
    refusable = models.BooleanField(default=False)
    rows = models.IntegerField(null=True, blank=True)
    columns = JsonYamlField(null=True, blank=True)
    is_public = models.BooleanField(default=False)

    objects = AgencyObjectManager()

    @property
    def usage_count(self):
        return self.survey_set.count()

    def __str__(self):
        return self.title


class Survey(ObjectRoot):
    class Meta:
        db_table = 'survey'
        ordering = ['-created_at']

    name = models.CharField(max_length=64)
    definition = JsonYamlField()
    questions = models.ManyToManyField(Question, blank=True)
    is_public = models.BooleanField(default=False)

    objects = AgencyObjectManager()

    def get_definition_items(self):
        def traverse_items(current, all_items=[]):
            yield current
            for item in current.get('items', []):
                yield item

        yield from traverse_items(self.definition)

    def get_related_question_ids(self):
        for item in self.get_definition_items():
            if item.get('type', None) == 'question' and 'questionId' in item:
                yield (item.get('id', None), item['questionId'])

    def __str__(self):
        return self.name


class Response(ObjectRoot):
    class Meta:
        ordering = ['-created_at']

    survey = models.ForeignKey(
        Survey, related_name='responses', on_delete=models.PROTECT
    )
    client = models.ForeignKey(Client, related_name='responses', on_delete=models.CASCADE)
    response_context_type = models.ForeignKey(
        ContentType, related_name='responses', on_delete=models.SET_NULL, blank=True, null=True)
    response_context_id = models.UUIDField(primary_key=False, blank=True, null=True)
    response_context = GenericForeignKey('response_context_type', 'response_context_id')

    objects = AgencyObjectManager()


class Answer(models.Model):
    response = models.ForeignKey(
        Response, related_name='answers', on_delete=models.PROTECT
    )
    question = models.ForeignKey(
        Question, related_name='answers', on_delete=models.PROTECT
    )
    value = models.CharField(max_length=256)


@receiver(pre_save, sender=Survey)
def save_related_questions(sender, instance, *args, **kwargs):
    def traverse_items(current, questions=[]):
        if current.get('type', None) == 'question' and 'questionId' in current:
            q = Question.objects.get(pk=current['questionId'])
            questions.append(q)

        for item in current.get('items', []):
            traverse_items(item, questions)

        return questions

    questions_in_survey = traverse_items(instance.definition)
    instance.questions.set(questions_in_survey)
