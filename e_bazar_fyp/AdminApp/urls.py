from django.urls import path

from .views import Verification

obj= Verification()
urlpatterns = [
    #path('', obj.home, name='home'),
    #path('statuschange/<str:status_type>', obj.status_change, name='status_change'),
    path('',obj.verification,name="verification"),
     path('AccountVerifications/', obj.AccountVerifications, name='AccountVerifications'),
     path('Orders/', obj.Orders, name='Orders'),
     path('avPending/', obj.avPending, name='avPending'),
     path('avDisputed/', obj.avDisputed, name='avDisputed'),
     path('avPendingDetails/', obj.avPendingDetails, name='avPendingDetails'),
     path('avPendingConfirmation/', obj.avPendingConfirmation, name='avPendingConfirmation'),
     path('avDisputedDetails/', obj.avDisputedDetails, name='avDisputedDetails'),
   path('oUnfulfilled/', obj.oUnfulfilled, name='oUnfulfilled'),
   path('oFulfilled/', obj.oFulfilled, name='oFulfilled'),
   path('oReturned/', obj.oReturned, name='oReturned'),
   path('oClusters/', obj.oClusters, name='oClusters'),
   path('oUnfulfilledDetails/', obj.oUnfulfilledDetails, name='oUnfulfilledDetails'),
   path('oUnfulfilledUpdate/', obj.oUnfulfilledUpdate, name='oUnfulfilledUpdate'),
   path('oFulfilledDetails/', obj.oFulfilledDetails, name='oFulfilledDetails'),
   path('oReturnedDetails/', obj.oReturnedDetails, name='oReturnedDetails'),
   path('oClusterDetails/', obj.oClusterDetails, name='oClusterDetails'),
   path('oCreateCluster/', obj.oCreateCluster, name='oCreateCluster'),
]