import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay

from .models import Customer
from .filters import CustomerFilter


class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (relay.Node,)


class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)

    customer = graphene.Field(CustomerType)

    def mutate(self, info, name, email, phone):
        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(customer=customer)


class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerNode)

    def resolve_all_customers(root, info):
        return Customer.objects.all()


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
