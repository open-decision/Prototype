import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from dashboard.models import DecisionTree, Node
from pages.models import PublishedTree
from users.models import CustomUser
from django.conf import settings

user = CustomUser.objects.get(email=settings.API_TEST_USER_MAIL)

class DecisionTreeNode(DjangoObjectType):
    class Meta:
        model = DecisionTree
        filter_fields = '__all__'
        fields = ('created_at', 'name', 'owner', 'slug', 'node_set')
        interfaces = (relay.Node, )

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(owner=user)

class NodeNode(DjangoObjectType):
    class Meta:
        model = Node
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'slug': ['exact', 'icontains', 'istartswith'],
            'question': ['exact', 'icontains', 'istartswith'],
            'inputs': ['exact', 'icontains', 'istartswith'],
            'decision_tree': ['exact'],
            'start_node': ['exact'],
            'new_node': ['exact'],
            'end_node': ['exact']
                }
        fields = (
            'created_at',
            'name',
            'slug',
            'decision_tree',
            'path',
            'question',
            'inputs',
            'new_node',
            'start_node',
            'end_node',
            'extra_data'
            )
        interfaces = (relay.Node, )

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter(decision_tree__owner=user)

class UserNode(DjangoObjectType):
    class Meta:
        model = CustomUser
        filter_fields = {
            'email': ['exact'],
                }
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):

    decision_tree = relay.Node.Field(DecisionTreeNode)
    all_decision_trees = DjangoFilterConnectionField(DecisionTreeNode)

    node = relay.Node.Field(NodeNode)
    all_nodes = DjangoFilterConnectionField(NodeNode)

    user = relay.Node.Field(UserNode)

#
#
# class QuestionType(DjangoObjectType):
#     class Meta:
#         model = Question
#
#
# class QuestionMutation(graphene.Mutation):
#     class Arguments:
#         # The input arguments for this mutation
#         text = graphene.String(required=True)
#         id = graphene.ID()
#
#     # The class attributes define the response of the mutation
#     question = graphene.Field(QuestionType)
#
#     def mutate(self, info, text, id):
#         question = Question.objects.get(pk=id)
#         question.text = text
#         question.save()
#         # Notice we return an instance of this mutation
#         return QuestionMutation(question=question)
#
#
# class Mutation(graphene.ObjectType):
#     update_question = QuestionMutation.Field()