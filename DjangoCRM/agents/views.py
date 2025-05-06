from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from django.shortcuts import reverse, redirect
from .forms import AgentModelForm
from leads.models import UserProfile
from .mixins import OrganisorandAgentListView
from django.core.mail import send_mail
import random



class AgentListView(OrganisorandAgentListView, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    

class AgentCreateView(OrganisorandAgentListView, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0,100000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organization = self.request.user.userprofile

        )
        send_mail(
            subject = "You are invited to be an agent",
            message ="You were added as an agent on DJCRM. Please come login to start working",
            from_email="anurag200266@gmail.com",
            recipient_list=[user.email]
        )
        # agent.organization = self.request.user.userprofile
        # agent.save()

        return super(AgentCreateView,self).form_valid(form)
    

class AgentDetailView(OrganisorandAgentListView, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = 'agent'
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    

class AgentUpdateView(OrganisorandAgentListView, generic.UpdateView):
    template_name = "agents/agent_update.html"
    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    form_class = AgentModelForm
    def get_success_url(self):
        return reverse("agents:agent-list")
    


class AgentDeleteView(OrganisorandAgentListView, generic.DeleteView):
    template_name="agents/agent_delete.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)
    
    def get_success_url(self):
        return reverse('agents:agent-list')
