from django.contrib.auth.models import User, Permission, Group
from ability.ability import Ability


def test_empty_model_can():
    user = User(username='admin')
    ability = Ability(user)

    assert ability.can('view', User) is False


def test_simple_model_can():
    user = User(username='admin')
    ability = Ability(user)
    ability.declare_can('view', User)

    assert ability.can('view', User)
    assert ability.can('view', Permission) is False


def test_simple_model_cannot():
    user = User(username='admin')
    ability = Ability(user)
    ability.declare_cannot('view', User)

    assert ability.can('view', User) is False
    assert ability.can('view', Permission) is False


def test_complex_model_can():
    user = User(username='admin')
    ability = Ability(user)
    ability.declare_can('view', User)
    ability.declare_cannot('view', User)

    assert ability.can('view', User) is False


def test_instance_can():
    user = User(username='admin')
    g1 = Group.objects.create(name='g1')
    g2 = Group.objects.create(name='g2')

    ability = Ability(user)
    # can view group with name == 2
    ability.declare_can('view', Group, name='g2')

    assert ability.can('view', g1) is False
    assert ability.can('view', g2)
