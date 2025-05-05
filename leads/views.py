from django.shortcuts import render,redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent, Category
from .forms import LeadForm , LeadModelForms, CustomCreation
from django.views.generic import TemplateView, ListView, DetailView,CreateView,UpdateView,DeleteView, FormView
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorandAgentListView
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
import hashlib
from .forms import ForgotPasswordForm,ResetPasswordForm , AssignAgentForm, LeadCategoryUpdateForm
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.conf import settings
# from django.core.mail import EmailMessage



User=get_user_model()



class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomCreation

    def get_success_url(self):
        return reverse ("login")






class LandingPageView(TemplateView):
    template_name="landing.html"

# def lead_landing(request):
#     return render(request, "landing.html")










class LeadListView(LoginRequiredMixin, ListView):
    template_name = "leads/lead_list.html"
    context_object_name='leads'
    
    def get_queryset(self):
        user=self.request.user

        #initial queryset of leads for the entire organization 
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organization = user.userprofile,
             agent__isnull=False)
        else:
            queryset = Lead.objects.filter(
                organization = user.agent.organization,
             agent__isnull=False)
            #filter for the agent that is logged in
            queryset=queryset.filter (agent__user=user)   

        return queryset
    

    def get_context_data(self, **kwargs):
        context = super(LeadListView,self).get_context_data(**kwargs)
        user=self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organization = user.userprofile, 
                agent__isnull=True
                )
            context.update({
            "unassigned_leads": queryset
        })
        return context
    







# def lead_list(request):
#     # return HttpResponse("Hello World")
#     leads = Lead.objects.all()
#     context = {
#         "leads":leads
#     }
#     return render(request, "leads/lead_list.html", context)







class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/lead_detail.html" 
    context_object_name = "lead"
    
   # queryset = Lead.objects.all()
    def get_queryset(self):
        user=self.request.user


        #initial queryset of leads for the entire organization 
        if user.is_organisor:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
            #filter for the agent that is logged in
            queryset=queryset.filter (agent__user=user)   

        return queryset


# def lead_detail(request,pk):

#     lead = Lead.objects.get(id=pk)
#     context = {
#         "lead":lead
#     }
#     return render(request, "leads/lead_detail.html", context)










class LeadCreateView(OrganisorandAgentListView, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForms
    
    def get_success_url(self):
        return reverse ("leads:lead-list")
    
    def form_valid(self,form):
        user=self.request.user
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A mail has been created",
            message="Go to the site to see the new lead",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super(LeadCreateView,self).form_valid(form)
    

    

# def lead_create(request):
#     form = LeadModelForms()
#     if request.method == "POST":
#         form = LeadModelForms(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")

#     context = {

#         "form":form
#     }
#     return render(request,'leads/lead_create.html',context)


# def lead_create(request):
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent
#             )
#             print("The lead has been created")
#             return redirect("/leads")

#     context = {

#         "form":form
#     }
#     return render(request,'leads/lead_create.html',context)















class LeadUpdateView(OrganisorandAgentListView, UpdateView):
    template_name= "leads/lead_update.html"
    # queryset = Lead.objects.all()

    def get_queryset(self):
        user=self.request.user
        #initial queryset of leads for the entire organization 
        return Lead.objects.filter(organization = user.userprofile)  


    form_class = LeadModelForms
    def get_success_url(self):
        return reverse("leads:lead-list")



# def lead_update(request,pk):
#     lead=Lead.objects.get(id=pk)
#     form = LeadModelForms(instance=lead)
#     if request.method == "POST":
#         form = LeadModelForms(request.POST,instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")

#     context = {
#         "form":form,
#         "lead":lead
#     }
#     return render(request,'leads/lead_update.html',context)





# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk) 
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             lead.first_name = first_name
#             lead.last_name=last_name
#             lead.age=age
#             lead.save()
#             return redirect("/leads")

#     context = {
#         "form":form,
#         "lead":lead
#     }
#     return render(request,'leads/lead_update.html',context)







class LeadDeleteView(OrganisorandAgentListView, DeleteView):
    template_name= "leads/lead_delete.html"
    # queryset = Lead.objects.all()

    def get_queryset(self):
        user=self.request.user
        #initial queryset of leads for the entire organization 
        return Lead.objects.filter(organization = user.userprofile)  






    def get_success_url(self):
        return reverse("leads:lead-list")




def lead_delete(request,pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")





class AssignAgentView(OrganisorandAgentListView, FormView):
    template_name = "leads/assign_agent.html"
    form_class= AssignAgentForm


    def get_form_kwargs(self, **kwargs):
        kwargs=super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update ({
            "request":self.request
        })
        return kwargs
    
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        agent = (form.cleaned_data["agent"])
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent=agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)





















class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "leads/category_list.html"
    context_object_name="category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user=self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organization = user.agent.organization)
        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user=self.request.user


        #initial queryset of leads for the entire organization 
        if user.is_organisor:
            queryset = Category.objects.filter(
                organization = user.userprofile)
        else:
            queryset = Category.objects.filter(
                organization = user.agent.organization) 

        return queryset
    









class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = context = super().get_context_data(**kwargs)
        
    #     # qs = Lead.objects.filter(category = self.get_object())
    #     leads = self.get_object().leads.all()


    #     context.update({
    #         # "unassigned_lead_count":
    #         "leads":leads
    #     })
    #     return context

    def get_queryset(self):
        user=self.request.user



        #initial queryset of leads for the entire organization 
        if user.is_organisor:
            queryset = Category.objects.filter(
                organization = user.userprofile)
        else:
            queryset = Category.objects.filter(
                organization = user.agent.organization) 

        return queryset









class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name= "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user=self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
            #filter for the agent that is logged in
            queryset=queryset.filter (agent__user=user)   

        return queryset


    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})














def forgot_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = hashlib.sha256(user.password.encode()).hexdigest()

                reset_url = request.build_absolute_uri(reverse('reset-password',kwargs={'uid':uid, 'token':token}))


                html_content = render_to_string('email_templates/password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_url,
                })


                send_mail(
                    subject="Reset your password",
                    message=f"Click the link to reset your password: {reset_url}",
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    html_message=html_content
                )

                return render(request, 'registration/reset_email_sent.html')
            except User.DoesNotExist:
                form.add_error('email', 'No user with this email exsits')
    else:
        form = ForgotPasswordForm()
    return render(request, 'registration/forgot_password.html', {'form': form})
        
        
        









def reset_password_view(request,uid,token):
    try:
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid_decoded)
        real_token = hashlib.sha256(user.password.encode()).hexdigest()

        if token!=real_token:
            return render(request, 'registration/invalid_token.html')

    except Exception as e:
        return render(request, 'registration/invalid_token.html')
    
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            return render(request, 'registration/password_reset_successful.html')
    else:
        form=ResetPasswordForm()
    return render(request, 'registration/reset_password_form.html', {'form': form})




    