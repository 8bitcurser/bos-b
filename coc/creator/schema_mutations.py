from graphene import (ClientIDMutation, Field, Float, Int, ObjectType, String,
                      relay)
from django.contrib.auth.models import User

from creator.models import (Investigator, Item, Occupation, Portrait, Skills,
                            Spell, Tag)
from creator.schema_nodes import (InvestigatorNode, ItemNode, OccupationNode,
                                  SkillNode, SpellNode, TagNode, UserNode)


class CreateTag(ClientIDMutation):
    tag = Field(TagNode)

    class Input:
        title = String()
        user = Int()

    @classmethod
    def mutate(cls, *args, **kwargs):
        """Generates mutation which is an instance of the Node class which
        results in a instance of our model.
        Arguments:
            input -- (dict) dictionary that has the keys corresponding to the
            Input class (title, user).
        """
        input_ = kwargs.get('input')
        title = input_.get('title')
        user = input_.get('user')
        tag = Tag(
            title=title,
            user=User.objects.get(pk=user)
        )
        tag.save()
        create_tag = CreateTag(tag=tag)
        return create_tag


class UpdateDeleteTag(ClientIDMutation):
    tag = Field(TagNode)

    class Input:
        title = String()
        uuid = String()
        method = String()

    @classmethod
    def mutate(cls, *args, **kwargs):
        input_ = kwargs.get('input')
        uuid = input_.get('uuid', '')
        method = input_.get('method')
        title = input_.get('title')
        ret = None
        if uuid != '':
            tag = Tag.objects.get(uuid=uuid)
            if tag is not None and method != 'DEL':
                tag.title = title
                tag.save()
                ret = UpdateDeleteTag(tag=tag)
            else:
                tag.delete()
                ret = f"Tag: {tag.uuid} deleted"
        return ret


class CreateItem(ClientIDMutation):
    item = Field(ItemNode)

    class Input:
        title = String()
        item_type = Int()
        description = String()
        price = Float()

    @classmethod
    def mutate(cls, *args, **kwargs):
        """Generates mutation which is an instance of the Node class which
        results in a instance of our model.
        Arguments:
            input -- (dict) dictionary that has the keys corresponding to the
            Input class (title, user).
        """
        input_ = kwargs.get('input')
        item = Item(**input_)
        item.save()
        create_item = CreateItem(item=item)
        return create_item

class UpdateDeleteItem(ClientIDMutation):
    item = Field(ItemNode)

    class Input:
        uuid = String()
        title = String()
        item_type = Int()
        description = String()
        price = Float()
        method = String()

    @classmethod
    def mutate(cls, *args, **kwargs):
        input_ = kwargs.get('input')
        uuid = input_.get('uuid', '')
        method = input_.get('method')
        title = input_.get('title')
        item_type = input_.get('item_type')
        description = input_.get('description')
        price = input_.get('price')
        if uuid != '':
            item = Item.objects.get(uuid=uuid)
            if item is not None and method != 'DEL':
                item.title = title
                item.item_type = item_type
                item.description = description
                item.price = price
                item.save()
                ret = UpdateDeleteItem(item=item)
            else:
                item.delete()
                ret = f"Item: {item.uuid} deleted"
            return ret


class CreateOccupation(ClientIDMutation):
    occupation = Field(OccupationNode)

    class Input:
        user = Int()
        title = String()
        description = String()
        suggested_contacts = String()
        credit_rating_min = Float()
        credit_rating_max = Float()

    @classmethod
    def mutate(cls, *args, **kwargs):
        """Generates mutation which is an instance of the Node class which
        results in a instance of our model.
        Arguments:
            input -- (dict) dictionary that has the keys corresponding to the
            Input class (title, user).
        """
        input_ = kwargs.get('input')
        user = input_.get('user')
        title = input_.get('title')
        description = input_.get('description')
        suggested_contacts = input_.get('suggested_contacts')
        credit_rating_min = input_.get('credit_rating_min')
        credit_rating_max = input_.get('credit_rating_max')
        occupation = Occupation(
            user=User.objects.get(pk=user),
            title=title,
            description=description,
            suggested_contacts=suggested_contacts,
            credit_rating_min=credit_rating_min,
            credit_rating_max=credit_rating_max
        )
        occupation.save()
        create_occupation = CreateOccupation(occupation=occupation)
        return create_occupation


class UpdateDeleteOccupation(ClientIDMutation):
    occupation = Field(OccupationNode)

    class Input:
        uuid = String()
        title = String()
        description = String()
        suggested_contacts = String()
        credit_rating_min = Float()
        credit_rating_max = Float()
        method = String()

    @classmethod
    def mutate(cls, *args, **kwargs):
        input_ = kwargs.get('input')
        uuid = input_.get('uuid', '')
        method = input_.get('method')
        title = input_.get('title')
        description = input_.get('description')
        suggested_contacts = input_.get('suggested_contacts')
        credit_rating_min = input_.get('credit_rating_min')
        credit_rating_max = input_.get('credit_rating_max')
        if uuid != '':
            occupation = Occupation.objects.get(uuid=uuid)
            if occupation is not None and method != 'DEL':
                occupation.title = title
                occupation.description = description
                occupation.suggested_contacts = suggested_contacts
                occupation.credit_rating_min = credit_rating_min
                occupation.credit_rating_max = credit_rating_max
                occupation.save()
                ret = UpdateDeleteOccupation(occupation=occupation)
            else:
                occupation.delete()
                ret = f"Occupation: {occupation.uuid} deleted"
            return ret


class CreateSkill(ClientIDMutation):
    skill = Field(SkillNode)

    class Input:
        user = Int()
        title = String()
        description = String()
        default_value = Int()

    @classmethod
    def mutate(cls, *args, **kwargs):
        """Generates mutation which is an instance of the Node class which
        results in a instance of our model.
        Arguments:
            input -- (dict) dictionary that has the keys corresponding to the
            Input class (title, user).
        """
        input_ = kwargs.get('input')
        usr = User.objects.get(pk=input_['user'])
        input_['user'] = usr
        skill = Skills(**input_)
        skill.save()
        create_skill = CreateSkill(skill=skill)
        return create_skill


class UpdateDeleteSkill(ClientIDMutation):
    skill = Field(SkillNode)

    class Input:
        uuid = String()
        user = Int()
        title = String()
        description = String()
        default_value = Int()
        method = String()

    @classmethod
    def mutate(cls, *args, **kwargs):
        input_ = kwargs.get('input')
        uuid = input_.get('uuid', '')
        title = input_.get('title')
        description = input_.get('description')
        default_value = input_.get('default_value')
        method = input_.get('method')
        if uuid != '':
            skill = Skills.objects.get(uuid=uuid)
            if skill is not None and method != 'DEL':
                skill.title = title
                skill.description = description
                skill.default_value = default_value
                skill.save()
                ret = UpdateDeleteSkill(skill=skill)
            else:
                skill.delete()
                ret = f"Skill: {skill.uuid} deleted"
            return ret


class InvestigatorMutation(ClientIDMutation):
    investigator = Field(InvestigatorNode)

    class Input:
        uuid = String()
        name = String()
        player = String()
        sex = String()
        residence = String()
        birthplace = String()
        age = Int()
        occupation = Int()
        ideologies = String()
        description = String()
        traits = String()
        injure_scars = String()
        significant_people = String()
        meaningful_locations = String()
        treasured_possessions = String()
        encounters_with_strange_entities = String()
        method = String()
        user = Int()

    @classmethod
    def mutate(cls, *args, **kwargs):
        """Generates mutation which is an instance of the Node class which
        results in a instance of our model.
        Arguments:
            input -- (dict) dictionary that has the keys corresponding to the
            Input class (title, user).
        """
        input_ = kwargs.get('input')
        uuid = input_.pop('uuid')
        method = input_.pop('method')
        input_['user'] = User.objects.filter(pk=input_.get('user')).first()
        input_['occupation'] = Occupation.objects.filter(
            pk=input_.get('occupation')
        ).first()
        if method != 'CREATE':
            investigator = Investigator.objects.filter(uuid=uuid).first()
            if method == 'DELETE':
                investigator.delete()
                ret = investigator
            elif method == 'UPDATE':
                investigator.__dict__.update(input_)
                investigator.save()
                ret = InvestigatorMutation(investigator=investigator)
        else:
            investigator = Investigator(**input_)
            investigator.save()
            ret = InvestigatorMutation(investigator=investigator)
        return ret


class SpellMutation(ClientIDMutation):
    spell = Field(SpellNode)

    class Input:
        method = String()
        uuid = String()
        name = String()
        alternative_names = String()
        description = String()
        deeper_magic = String()
        notes = String()
        cost = String()
        casting_time = String()
        user = Int()

    @classmethod
    def mutate(cls, *args, **kwargs):
        """Generates mutation which is an instance of the Node class which
        results in a instance of our model.
        Arguments:
            input -- (dict) dictionary that has the keys corresponding to the
            Input class (title, user).
        """
        input_ = kwargs.get('input')
        usr = User.objects.get(pk=input_['user'])
        input_['user'] = usr
        method = input_.pop('method')
        if method != "CREATE":
            spell = Spell.objects.filter(uuid=input_.get('uuid', '')).first()
            if method == 'DELETE':
                spell.delete()
                ret = f"Spell: {spell.uuid} deleted"
            elif method == 'UPDATE':
                spell.__dict__.update(input_)
                spell.save()
                ret = SpellMutation(spell=spell)
        else:
            spell = Spell(**input_)
            spell.save()
            ret = SpellMutation(spell=spell)

        return ret
