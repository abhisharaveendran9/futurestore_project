from django.shortcuts import render,redirect

# Create your views here.

from owner.models import Orders
from owner.forms import OrderUpdateForm
from django.views.generic import TemplateView,ListView,DetailView
from django.contrib import messages
from django.core.mail import send_mail
from customer.decorators import signin_required
from django.utils.decorators import method_decorator


@method_decorator(signin_required,name="dispatch")
class AdminDashBoardView(TemplateView):
    template_name: str="dashboard.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cnt=Orders.objects.filter(status="order-placed").count()
        context["count"]=cnt
        return context


@method_decorator(signin_required,name="dispatch")
class OrdersListView(ListView):
    model=Orders
    context_object_name="orders"
    template_name: str="admin-listorder.html"

    def get_queryset(self):
        return Orders.objects.filter(status="order-placed")


@method_decorator(signin_required,name="dispatch")
class OrderDetailView(DetailView):
    model=Orders
    template_name: str="owner/order-details.html"
    pk_url_kwarg: str="id"
    context_object_name: str="order"
    

    def get_context_data(self,**kwargs):
        context=super().get_context_data()
        form=OrderUpdateForm()
        context["form"]=form
        return context

    def post(self,request,*args,**kw):
        order=self.get_object()
        print(self.get_object())
        form=OrderUpdateForm(request.POST)

        if form.is_valid():
            order.status=form.cleaned_data.get("status")
            order.expected_delivery_date=form.cleaned_data.get("expected_delivery_date")
            dt=form.cleaned_data.get("expected_delivery_date")
            messages.success(self.request,"Order status updated")
            order.save()
            send_mail(
                "order delivery update future store",
                f"your order will be delivered on {dt}",
                "abhisharaveendran@gmail.com",
                ["shyamalaravindran99@gmail.com"]
            )

            print(form.cleaned_data)
            return redirect("dashboard")

