from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscard/', views.plus_cart),
    path('minuscard/', views.minus_cart),
    path('removecard/', views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('protein/', views.protein, name='protein'),
    path('protein/<slug:data>', views.protein, name='proteindata'),
    path('tube/', views.tube, name='tube'),
    path('tube/<slug:data>', views.tube, name='tubedata'),
    path('syrup/', views.syrup, name='syrup'),
    path('syrup/<slug:data>', views.syrup, name='syrupdata'),
    path('medicine/', views.medicine, name='medicine'),
    path('medicine/<slug:data>', views.medicine, name='medicinedata'),
    path('search', views.search, name='search'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout-now/', views.buy_now, name='checkout-now'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html', form_class=MyPasswordForm), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/passwordresetdone.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/passwordresetconfirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/passwordresetcomplate.html'), name='password_reset_complete'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('handlepayment/', views.handlerequest, name='HandleRequest'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


