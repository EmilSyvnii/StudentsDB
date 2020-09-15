from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(objects, size, request, context, var_name = 'object_list'):
    """ Paginate objects provided by a view

    :param objects: list of elements
    :param size: number of objects per page
    :param request: obj to get url params from
    :param context: to set new vars
    :param var_name: var name for list of objects
    :return: updated context objects
    """

    paginator = Paginator(objects, size)

    page = request.GET.get('page', '1')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        # if page numb is out of the range
        object_list = paginator.page(paginator.num_pages)

    # set vars into context
    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator

    return context

def get_groups(request):
    from .models import Group

    cur_group = get_current_group(request)      # currently selected group

    groups = []
    for group in Group.objects.all().order_by('title'):
        groups.append({
            'id': group.id,
            'title': group.title,
            'leader': group.leader and (u'%s %s' % (group.leader.first_name, group.leader.last_name)) or None,
            'selected': cur_group and cur_group.id == group.id and True or False
        })
    return groups

def get_current_group(request):
    """Returns currently selected group or None"""
    pk = request.COOKIES.get('current_group')

    if pk:
        from .models import Group
        try:
            group = Group.objects.get(pk=int(pk))
        except Group.DoesNotExist:
            return None
        else:
            return group
    else:
        return None