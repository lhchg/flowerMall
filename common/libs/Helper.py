from flask import g, render_template


def ops_render(template, context=None):
    if context is None:
        context = {}
    if "current_user" in g:
        context['current_user'] = g.current_user

    return render_template(template, **context)
