from django.http import HttpResponse


def script(command):
    return HttpResponse('<script>%s</script>' % command)