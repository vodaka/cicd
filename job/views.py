import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
from django.shortcuts import render
from jenkinstest.settings import STATICFILES_DIRS
import jenkins
# Create your views here.

username = 'tux'
password = '123456'
jenkins_url = 'http://192.168.100.4:8080'
server = jenkins.Jenkins(jenkins_url, username=username, password=password)
print(server.get_version())
print(parse('template.xml'))


def index(request):
    return render(request, 'homepage.html')


def homgepage(request):
    return render(request, 'homepage.html')


def form(request):
    return render(request, 'form.html')


def create_job(request):
    job_name = request.POST.get('job_name', '')
    git_url = request.POST.get('git_url', '')
    triggers_spec = request.POST.get('triggers_spec', '')
    print(job_name, git_url, triggers_spec)
    config_name = '.'.join([job_name, 'xml'])

    #tree = ET.parse('/'.join([STATICFILES_DIRS[0], 'template.xml']))
    tree = ET.parse('template.xml')
    root = tree.getroot()

    for url in root.iter('url'):
        url.text = git_url
    for child in root.iter(tag='hudson.triggers.TimerTrigger'):
        # print(child.tag, child.text)
        for spec in child:
            # print(spec.tag, spec.text)
            spec.text = triggers_spec
    # for spec in root.iter('spec'):
    #     spec.text = triggers_spec
    for item in root.findall('spec'):
        print(spec.tag, spec.text)
    tree.write(config_name)
    config_xml = open(config_name).read()
    server.create_job(job_name, config_xml)
    server.enable_job(job_name)
    return render(request, 'index.html')


def job_list(request):
    alljobs = server.get_all_jobs()
    joblist = []
    for item in alljobs:
        joblist.append(item['fullname'])
    context = {'joblist':joblist}
    return render(request, 'joblist.html', context)
