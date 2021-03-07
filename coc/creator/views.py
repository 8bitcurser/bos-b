from json import dumps
from random import choice

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from creator.constants import SILOUETTES as silouettes
from creator.helpers.investigator import generate_full_half_fifth_values
from creator.helpers.views_helper import (generate_attributes_form,
                                          generate_basic_info_form,
                                          generate_derivative_attributes_form)
from creator.models import (Inventory, Investigator, ManiaInvestigator,
                            Occupation, PhobiaInvestigator, Portrait, Skills,
                            SpellInvestigator)
from creator.random_inv import (RandomInvestigator, base_skills_generator,
                                free_point_assigner, occ_point_assigner)


# Create your views here.
def get_investigators_data(request, inv, **kwargs):
    '''Retrieve all information associated to an
    Investigator.'''
    investigator = Investigator.objects.get(
        uuid=inv
    )
    res = {
        'investigator': investigator
    }

    return render(
        request, 'character_sheet.html',
        {'res': res}
    )


def investigators_basic_info(request, inv):
    '''Generate investigator basic information form.'''
    investigator = generate_basic_info_form(
        request, inv)
    occupations = [
        [occ.uuid, occ.__str__()] for occ in 
        Occupation.objects.all()
    ]
    investigator = {
        'name': investigator.name,
        'uuid': investigator.uuid,
        'sex': investigator.sex,
        'occupation': investigator.occupation.uuid,
        'age': investigator.age,
        'player': investigator.player,
        'residence': investigator.residence,
        'birthplace': investigator.birthplace
    }
    return JsonResponse(
        {
            'investigator': investigator,
            'occupations': occupations
        },
        status=200
    )


def investigators_attributes(request, inv):
    '''Retrieve investigators attributes.'''
    inv = generate_attributes_form(
        request, inv
    )
    attributes = inv.attributes_detail
    attributes['MOV'] = [inv.move]
    attributes["BUILD"] = list(inv.build)
    return JsonResponse(
        {'attributes': attributes}, status=200)


def get_investigators_portrait(request, inv):
    '''Retrieve investigators portrait.'''
    investigator = Investigator.objects.get(
        uuid=inv
    )
    portrait = Portrait.objects.filter(
        investigator=investigator
    ).first()
    default_portrait = silouettes[0] if investigator.sex == 'M' else silouettes[1]

    res = {'portrait': portrait.portrait.url if portrait is not None else default_portrait}
    return JsonResponse(res, status=200)


def investigators_deriv_attrs(request, inv):
    '''Generate investigator derivative attributes form.'''
    inv = generate_derivative_attributes_form(
        request, inv)
    investigator_relevant_data = {
        "health": inv.health,
        "magic_points": inv.magic_points,
        "luck": inv.luck,
        "sanity": inv.sanity
    }
    return JsonResponse(
        {'investigator': investigator_relevant_data},
        status=200
    )


def get_investigators_skills(request, inv):
    investigator = Investigator.objects.get(
        uuid=inv
    )
    # Retrieve skills
    skills = sorted(investigator.skills)
    skills_sanitized = []
    for skill in skills:
        skills_sanitized.append(
            [
                skill,
                *generate_full_half_fifth_values(
                    investigator.skills[skill]['value']
                )
            ]
        )
    res = {'skills': skills_sanitized}
    return JsonResponse(res, status=200)


def investigators_skills_reset(request, inv):
    investigator = Investigator.objects.get(
        uuid=inv
    )
    skills = list(Skills.objects.all())
    base_skills_generator(skills, investigator)
    skills = sorted(investigator.skills)
    skills_sanitized = []
    for skill in skills:
        skills_sanitized.append(
            [
                skill,
                *generate_full_half_fifth_values(
                    investigator.skills[skill]['value']
                )
            ]
        )
    res = {'skills': skills_sanitized}
    return JsonResponse(res, status=200)


def investigators_skills_shuffle(request, inv):
    investigator = Investigator.objects.get(
        uuid=inv
    )
    skills = list(Skills.objects.all())
    base_skills_generator(skills, investigator)
    proff_points = investigator.occupation_skill_points
    occ_point_assigner(proff_points, investigator)
    # Assign free skill points
    free_point_assigner(investigator.free_skill_points, investigator)
    skills = sorted(investigator.skills)
    skills_sanitized = []
    for skill in skills:
        skills_sanitized.append(
            [
                skill,
                *generate_full_half_fifth_values(
                    investigator.skills[skill]['value']
                )
            ]
        )
    res = {'skills': skills_sanitized}
    return JsonResponse(res, status=200)


def get_investigators_weapons(request, inv):
    '''Retrieve investigators weapons.'''
    investigator = Investigator.objects.get(
        uuid=inv
    )
    weapons = Inventory.objects.filter(
        investigator=investigator,
        item__category=3)
    weapons_results = []
    for weapon in weapons:
        w_dict = weapon.properties
        w_dict['skill_value'] = generate_full_half_fifth_values(
            investigator.skills[weapon.item.properties['skill']]['value']
        )
        weapons_results.append(w_dict)
    return JsonResponse({'weapons': weapons_results}, status=200)


def get_investigators_gear(request, inv):
    '''Retrieve investigators gear.'''
    investigator = Investigator.objects.get(
        uuid=inv
    )
    items = Inventory.objects.filter(
        investigator=investigator,
        item__category__in=[2,4]
    )
    gear = [
        {
            'title': item.properties['title'],
            'stock': item.stock,
            'price': item.properties['price']
        } for item in items
    ]
    return JsonResponse({'gear': gear}, status=200)


def get_investigators_manias_and_phobias(request, inv):
    '''Retrieve investigators manias and phobias.'''
    investigator = Investigator.objects.get(
        uuid=inv
    )
    manias = ManiaInvestigator.objects.filter(
        investigator=investigator
    )
    phobias = PhobiaInvestigator.objects.filter(
        investigator=investigator
    )
    phobias = [[phobia.uuid, phobia.title] for phobia in phobias]
    manias = [[mania.uuid, mania.title] for mania in manias]
    res = {
        'manias': manias,
        'phobias': phobias
    }
    return JsonResponse(res, status=200)


def get_investigators_arcane(request, inv):
    '''Retrieve arcane artifacts and spells from investigator.'''
    investigator = Investigator.objects.get(
        uuid=inv
    )
    # Retrieve arcane
    artifacts = Inventory.objects.filter(
        investigator=investigator,
        item__category=1

    )
    spells = SpellInvestigator.objects.filter(
        investigator=investigator
    )
    spells = [
        {
            'name': spell.spell.name,
            'cost': spell.spell.cost,
            'casting_time': spell.spell.casting_time,
            'description': spell.spell.description,
            'deeper_magic': spell.spell.deeper_magic,
            'alternative_names': spell.spell.alternative_names
        }
        for spell in spells
    ]
    artifacts = [
        artifact.properties.title
        for artifact in artifacts
    ]
    res = {
        'artifacts': artifacts,
        'spells': spells,
        'encounters': investigator.encounters_with_strange_entities
    }
    return JsonResponse(res, status=200)


def get_investigators_backstory(request, inv):
    '''Retrieve arcane artifacts and spells from investigator.'''
    investigator = Investigator.objects.get(
        uuid=inv
    )
    res = {
        'description': investigator.description,
        'ideologies': investigator.ideologies,
        'significant_people': investigator.significant_people,
        'meaningful_locations': investigator.meaningful_locations,
        'treasured_possessions': investigator.treasured_possessions,
        'traits': investigator.traits,
        'injuries_scars': investigator.injure_scars
    }
    return JsonResponse(res, status=200)


def generate_random_investigator(request):
    rand = RandomInvestigator()
    rand.build()
    return redirect(get_investigators_data, inv=rand.investigator.uuid)
