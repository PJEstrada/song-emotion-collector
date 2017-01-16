# -*- coding: utf-8 -*-
"""
Various common usage processing functions.

Python module that provides common functionalities, used in many places through
Edoo.
"""

__version__ = '0.1.0'
__author__ = 'Samuel Chávez <me@samuelchavez.com>'
__date__ = '25 November 2013'
__copyright__ = 'Copyright (c) 2012-2014 Samuel Chávez'
__license__ = 'THE LICENSE'
__status__ = 'development'
__docformat__ = 'reStructuredText'

import errno
import sendgrid
from sendgrid.helpers.mail import *
import os
import subprocess
import urllib

from unidecode import unidecode
from sorl.thumbnail import get_thumbnail
from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.files import locks
from django.core.files.move import file_move_safe
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.utils.http import urlencode, urlunquote
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from datetime import datetime
from django.utils import timezone
from django.core import urlresolvers
from django.http import HttpResponse


def run_shell_command(command):
    """
    Executes a command like if it was executed from command line.

    :param command: command to execute, in string format.
    :rtype: Tuple (result, error).
    """
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out, err


class OverwriteFileSystemStorage(FileSystemStorage):
    """
    Custom SystemStorage to handle rewrite with replace.

    This SystemStorage manager is used to replace previously saved pictures.

    :members:
    """

    def get_available_name(self, name, max_length=None):
        return name  # Instead of checking if it exists,
                     # it just save with the same name as passed

    def _save(self, name, content, max_length=None):
        full_path = self.path(name)

        # Create any intermediate directories that do not exist.
        # Note that there is a race between os.path.exists and os.makedirs:
        # if os.makedirs fails with EEXIST, the directory was created
        # concurrently, and we can continue normally. Refs #16082.
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
        if not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)

        # There's a potential race condition between get_available_name and
        # saving the file; it's possible that two threads might return the
        # same name, at which point all sorts of fun happens. So we need to
        # try to create the file, but if it already exists we have to overwrite.

        while True:
            try:
                # This file has a file path that we can move.
                if hasattr(content, 'temporary_file_path'):
                    file_move_safe(content.temporary_file_path(), full_path)
                    content.close()

                # This is a normal uploadedfile that we can stream.
                else:
                    # This fun binary flag incantation makes os.open throw an
                    # OSError if the file already exists before we open it.
                    flags = (os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                             getattr(os, 'O_BINARY', 0))
                    # The current umask value is masked out by os.open!
                    fd = os.open(full_path, flags, 0o666)
                    try:
                        locks.lock(fd, locks.LOCK_EX)
                        _file = None
                        for chunk in content.chunks():
                            if _file is None:
                                mode = 'wb' if isinstance(chunk, bytes) else 'wt'
                                _file = os.fdopen(fd, mode)
                            _file.write(chunk)
                    finally:
                        locks.unlock(fd)
                        if _file is not None:
                            _file.close()
                        else:
                            os.close(fd)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    # Ooops, the file exists. We need to overwrite this file.
                    self.delete(name)
                    name = self.get_available_name(name)
                    full_path = self.path(name)
                else:
                    raise
            else:
                # OK, the file save worked. Break out of the loop.
                break

        if settings.FILE_UPLOAD_PERMISSIONS is not None:
            os.chmod(full_path, settings.FILE_UPLOAD_PERMISSIONS)

        return name


def url_with_querystring(path, **kwargs):
    return path + '?' + urllib.urlencode(kwargs)


def send_multipart_email(
        subject,
        template,
        data_dict,
        recipient_list,
        request,
        personalizations=None,
        recipient_email_list=None):
    """
    Sends a multipart email (HTML / plain text) to one or many destinies.
    Uses the Sengrid API to send all the email

    :param subject: Email subject.
    :param template: template id string of sendgrid.
    :param data_dict: data to be passed to the rendered template.
    :param recipient_list: array of users that will receipt it.
    :param request: request object context to handle url constructions.
    :param pesonalizations: an array of dictionaries containing template tags to be substituted on the sendgrid mail template.
                            If none is given, function will use the data_dict for all mails.
    :rtype: None.
    """

    if settings.SEND_EMAIL:

        if type(recipient_list) != list:
            recipient_list = [recipient_list]

        # Extract emails from users
        if not recipient_email_list:
            recipient_email_list = [u.email for u in recipient_list]

        email_list_sendgrid = []

        for mail in recipient_email_list:

            email_list_sendgrid.append({"email":mail})

        # Adding footer data substitutions to data_dict
        subs = {}
        data_dict['footerAbout'] = _(u"About")
        data_dict['footerSupport'] = _(u"Technical Support")
        data_dict['footerPress'] = _(u"Press")

        # Arranging personalization dictionary
        if personalizations:
            try:
                sendgrid_personalizations = []
                for data in personalizations:
                    data['footerAbout'] = _(u"About")
                    data['footerSupport'] = _(u"Technical Support")
                    data['footerPress'] = _(u"Press")
                    sendgrid_personalizations.append({"substitutions":data, 'subject': subject})

                for i in range(len(email_list_sendgrid)):
                    sendgrid_personalizations[i]['to'] = [email_list_sendgrid[i]]

                sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

                data = {
                    "personalizations": sendgrid_personalizations,
                    "from": {
                        "email": "info@edoo.io",
                        "name": "Edoo"
                    },
                    "content": [{
                        "type": "text/html",
                        "value": " "
                    }],
                    "subject": subject,
                    "template_id": template
                }

                response = sg.client.mail.send.post(request_body=data)

            except Exception as err:

                if len(email_list_sendgrid) != 0:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        _(u"No pudo enviarse el correo a %s." % recipient_email_list[0]),
                        extra_tags="default")
        else:
            try:
                if len(email_list_sendgrid) != 0:
                    # Test Send grid mailer
                    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

                    to = [email_list_sendgrid[0]]
                    bcc = []
                    for i in range(0,len(email_list_sendgrid)):
                        if i == 0:
                            continue
                        else:
                            bcc.append(email_list_sendgrid[i])

                    if len(email_list_sendgrid) == 1:
                        pers = [{
                                "to": to,
                                "subject": subject,
                                "substitutions": data_dict,
                            }]
                    else:

                        pers = [{
                                "to": to,
                                "subject": subject,
                                "substitutions": data_dict,
                                "bcc": bcc
                            }]

                    data = {
                        "personalizations": pers,
                        "from": {
                            "email": "info@edoo.io",
                            "name": "Edoo"
                        },
                        "content": [{
                            "type": "text/html",
                            "value": " "
                        }],
                        "template_id": template
                    }
                    response = sg.client.mail.send.post(request_body=data)

            except Exception as err:

                if len(email_list_sendgrid) != 0:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        _(u"No pudo enviarse el correo a %s." % recipient_email_list[0]),
                        extra_tags="default")


def place_message(request, cr=None):
    """
    Given a request and a ControllerResponse, sets the flash messages needed.

    :param request: request object, used to store the flash session message.
    :param cr: ControllerResponse object, it's the one that indicates the need\
        of a message.
    :rtype: None.
    """

    if cr is not None:
        # Check if have to place messages
        if cr.message_position is not None:

            extra_tags = [cr.message_position]

            # User related message
            if cr.message_user:  # [position, user, thumb_url]
                profile_picture = get_thumbnail(
                    cr.message_user.profile_picture,
                    '70x70',
                    crop='center').url

                extra_tags.append('user')
                extra_tags.append(profile_picture)

            # Achievement related message
            elif cr.message_achievement_class:   # [position, achievement, achievement_class]
                extra_tags.append('achievement')
                extra_tags.append(cr.message_achievement_class)

            # Standard message type
            else:  # [position, standard, tag_class, icon_class]
                extra_tags.append('standard')
                extra_tags.append(cr.message_tag_class)
                extra_tags.append(cr.message_icon)

            messages.add_message(request,
                                 cr.status,
                                 cr.message,
                                 extra_tags=" ".join(extra_tags))


def clean_slug(name):
    """
    Returns a string that could be used as URL part, based on the string passed.

    :param name: any string to obtain it's URL friendly representation.
    :rtype: string.
    """
    if not name:
        return name
    name = name.lower()
    name = name.rstrip()
    name = name.strip()
    name = "-".join(name.split())
    name = unidecode(name)
    name = name.replace(" ", "-")
    name = name.replace("\"", "")
    return name


def clean_for_json(dictionary):
    """
    Transforms a dictionary of models into a json compatible dictionary.

    :param dictionary: dictionary containing model objects.
    :rtype: dictionary containing model json dumps.
    """

    result = {}
    for key in dictionary:
        try:
            json.dumps(dictionary[key])
            result[key] = dictionary[key]
        except:
            pass
    return result


def dbg(lbl, val):
    """
    Loggin function.

    :param lbl: output label.
    :param val: output value.
    :rtype: None.
    """
    print " %-20s : [%s] " % (lbl, val)


def smart_reverse(*args, **kwargs):
    """
    URL constructor based on view names.

    :param viewname: view name to be reversed.
    :param urlconf: urlconf used to reverse the view name.
    :param args: unlabeled arguments used for the reverse.
    :param kwargs: labeled arguments used for the reverse.
    :param prefix: prefix used for the output URL.
    :param current_app: restricting the reversal to a specific app.
    :param extra_kwargs: labeled arguments to be attached in the get query of\
        the built URL.
    :param safe_urls: uses urlencode algorithm?.
    :rtype: string.
    """

    safe_urls = kwargs.pop('safe_urls', True)
    extra_kwargs = kwargs.pop('extra_kwargs', None)

    url = reverse(*args, **kwargs)
    if extra_kwargs:
        url = u"%s?%s" % (url, urlencode(extra_kwargs))
        if not safe_urls:
            url = urlunquote(url)
    return url


def add_non_field_error(form, str_error):
    """
    Adds a form's non-field-error based on a given string.

    :param form: the form that will contain the non-field-error.
    :param str_error: non-field-error description.
    :rtype: None.
    """

    errors = form._errors.setdefault(
        forms.forms.NON_FIELD_ERRORS,
        forms.utils.ErrorList())
    errors.append(str_error)


# Form transport
def transport_form_through_session(request, form, form_identifier):
    """
    Uses session variables to transport form data through requests.

    The data that this method sets available is identified by a string, and it
    is specifically regarding form's initial data and form's errors.

    **NOTE**: prefix doesn't actually gets correctly deployed when transporting
    formsets. Make sure to define it's prefix in the ``form`` parameter.

    :param request: session medium to store the form's data.
    :param form: form where the data will be extracted.
    :param form_identifier: data label, used to populate a form later.
    :param str_error: non-field-error description.
    :rtype: None.
    """

    request.session['data:%s' % form_identifier] = form.data
    request.session['errors:%s' % form_identifier] = form.errors
    request.session['prefix:%s' % form_identifier] = form.prefix


def transport_formset_through_session(request, formset, formset_identifier):
    """
    Uses session variables to transport formset data through requests.

    The data that this method sets available is identified by a string, and it
    is specifically regarding formset's initial data and formset's errors.

    **NOTE**: prefix doesn't actually gets correctly deployed when transporting
    formsets. Make sure to define it's prefix in the ``formset`` parameter.

    :param request: session medium to store the formset's data.
    :param formset: formset where the data will be extracted.
    :param formset_identifier: data label, used to populate a formset later.
    :param str_error: non-field-error description.
    :rtype: None.
    """

    request.session['data:%s' % formset_identifier] = formset.data
    request.session['errors:%s' % formset_identifier] = formset.errors
    request.session['prefix:%s' % formset_identifier] = formset.prefix


def deploy_form_through_session(request, form, form_identifier):
    """
    Uses session variables to receive form data from requests.

    The data that this method receives is identified by a string, and it is
    specifically regarding form's initial data and form's errors.

    :param request: session medium to retrieve the form's data.
    :param form: form where the data will be set.
    :param form_identifier: data label, used to retrieve the form data.
    :param str_error: non-field-error description.
    :rtype: Tuple (form, success flag).
    """

    if request.session.get('data:%s' % form_identifier):
        data = request.session.get('data:%s' % form_identifier)
        errors = request.session.get('errors:%s' % form_identifier)
        prefix = request.session.get('prefix:%s' % form_identifier)

        form.initial = data

        # Transform error list (try to catch attribute error)
        if not isinstance(errors, list):
            for key in errors.keys():
                errors[key] = forms.utils.ErrorList(errors[key])

        form._errors = errors
        form.prefix = prefix

        del request.session['data:%s' % form_identifier]
        del request.session['errors:%s' % form_identifier]
        del request.session['prefix:%s' % form_identifier]
        return form, True
    return form, False


def deploy_formset_through_session(request, formset, formset_identifier):
    """
    Uses session variables to receive formset data from requests.

    The data that this method receives is identified by a string, and it is
    specifically regarding formset's initial data and formset's errors.

    :param request: session medium to retrieve the formset's data.
    :param formset: formset where the data will be set.
    :param formset_identifier: data label, used to retrieve the formset data.
    :param str_error: non-field-error description.
    :rtype: Tuple (success flag, data, errors, prefix).
    """

    if request.session.get('data:%s' % formset_identifier):
        data = request.session.get('data:%s' % formset_identifier)
        errors = request.session.get('errors:%s' % formset_identifier)
        prefix = request.session.get('prefix:%s' % formset_identifier)

        del request.session['data:%s' % formset_identifier]
        del request.session['errors:%s' % formset_identifier]
        del request.session['prefix:%s' % formset_identifier]

        formset = formset.__class__(data=data, prefix=prefix)

        # Transform error list
        i = 0
        for form in formset:
            form_errors = errors[i]
            for key in form_errors.keys():
                form_errors[key] = forms.utils.ErrorList(form_errors[key])
            form._errors = form_errors
            i += 1

        return formset, True

    return formset, False


def approx_equal(a, b, tol=0.00000001):
    """
    Checks if two floats are semantically equal.

    :param a: first float to compare.
    :param b: second float to compare.
    :param tol: real threshold to announce equality.
    :rtype: boolean.
    """
    return abs(a - b) < tol


def deduct_redirect_response(request, redirect_url):
    """
    Given a request and a redirection url, deducts the best way to respond.

    TODO v1.0: replace all over the place!!
    """

    if redirect_url:
        if redirect_url.startswith('#'):
            return HttpResponseRedirect(
                '%s%s' % (request.META['HTTP_REFERER'], redirect_url))
        else:
            return HttpResponseRedirect(redirect_url)

    if not request.META.get('HTTP_REFERER', None):
        return None

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Obtained from: http://thadeusb.com/weblog/2010/10/10/python_scale_hex_color
def clamp(val, minimum=0, maximum=255):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val


# Obtained from: http://thadeusb.com/weblog/2010/10/10/python_scale_hex_color
def color_scale(hexstr, scalefactor):
    """
    Scales a hex string by ``scalefactor``. Returns scaled hex string.

    To darken the color, use a float value between 0 and 1.
    To brighten the color, use a float value greater than 1.

    >>> color_scale("#DF3C3C", .5)
    #6F1E1E
    >>> color_scale("#52D24F", 1.6)
    #83FF7E
    >>> color_scale("#4F75D2", 1)
    #4F75D2
    """

    hexstr = hexstr.strip('#')

    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr

    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

    r = clamp(r * scalefactor)
    g = clamp(g * scalefactor)
    b = clamp(b * scalefactor)

    return "#%02x%02x%02x" % (r, g, b)


intro_text = """Named URL patterns for the {% url %} tag
========================================

e.g. {% url pattern-name %}
or   {% url pattern-name arg1 %} if the pattern requires arguments

"""


def show_url_patterns(request):
    patterns = _get_named_patterns()
    r = HttpResponse(intro_text, content_type='text/plain')
    longest = max([len(pair[0]) for pair in patterns])
    for key, value in patterns:
        r.write('%s %s\n' % (key.ljust(longest + 1), value))
    return r


def _get_named_patterns():
    "Returns list of (pattern-name, pattern) tuples"
    resolver = urlresolvers.get_resolver(None)
    patterns = sorted([
        (key, value[0][0][0])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, basestring)
    ])
    return patterns


def date_to_tz_datetime(date):
    """
    Convert an ISO date string 2011-01-01 into a timezone aware datetime that
    has the current timezone.
    """
    new_date = datetime(year=date.year, month=date.month, day=date.day)
    current_timezone = timezone.get_current_timezone()
    return current_timezone.localize(new_date, is_dst=None)


def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

CODE_COLOR_RELATION = {
    'standard': '',
    'header': '\033[95m',
    'okblue': '\033[94m',
    'okgreen': '\033[92m',
    'warning': '\033[93m',
    'fail': '\033[91m',
    'endc': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}


def log(msg, code='standard'):
    nw = datetime.now()
    color = CODE_COLOR_RELATION[code]

    return "[%s:%s:%s] \t%s%s%s" % (
        nw.hour,
        nw.minute,
        nw.second,
        color,
        msg,
        CODE_COLOR_RELATION['endc'])


def log_title(message):
    return "%s\n%s\n%s\n%s" % (
        log(""),
        log("=" * (len(message) + 2)),
        log(" %s " % message),
        log("=" * (len(message) + 2))
    )


def log_subtitle(message):
    return "%s\n%s\n%s" % (
        log(""),
        log(" %s " % message),
        log("-" * (len(message) + 2))
    )