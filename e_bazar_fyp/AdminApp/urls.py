from django.urls import path

from .views import Verification

obj= Verification()
urlpatterns = [
    # path('', obj.home, name='home'),
    #path('statuschange/<str:status_type>', obj.status_change, name='status_change'),
    # path('',obj.verification,name="verification"),
     #path('',obj.admin,name="admin"),
     path('', obj.avPending, name='avPending'),
     path('Orders/', obj.Orders, name='Orders'),
     path('avDisputed/', obj.avDisputed, name='avDisputed'),
     path('avVerified/', obj.avVerified, name='avVerified'),
     path('avPendingDetails/<str:vendor_id>/', obj.avPendingDetails, name='avPendingDetails'),
     path('avPendingConfirmation/<str:vendor_id>/', obj.avPendingConfirmation, name='avPendingConfirmation'),
     path('avDisputedDetails/', obj.avDisputedDetails, name='avDisputedDetails'),
     path('oUnfulfilled/', obj.oUnfulfilled, name='oUnfulfilled'),
     path('oFulfilled/', obj.oFulfilled, name='oFulfilled'),
     path('oUpForDelivery/', obj.oReturned, name='oReturned'),
     path('oShipped/', obj.oShiped, name='oShipped'),
     path('oClusters/<str:status>/', obj.oClusters, name='oClusters'),
     path('Details/<str:order_id>/', obj.oUnfulfilledDetails, name='oUnfulfilledDetails'),
     path('oUnfulfilledUpdate/', obj.oUnfulfilledUpdate, name='oUnfulfilledUpdate'),
     path('oFulfilledDetails/', obj.oFulfilledDetails, name='oFulfilledDetails'),
     path('oReturnedDetails/', obj.oReturnedDetails, name='oReturnedDetails'),
     path('oClusterDetails/<str:cluster_id>/', obj.oClusterDetails, name='oClusterDetails'),
     path('oCreateCluster/<str:order_lst>/', obj.oCreateClusterWtord, name='oCreateClusterWthord'),
     path('oCreateCluster/', obj.oCreateCluster, name='oCreateCluster'),
     path('changestatus/<str:vendor_id>/<str:status>/', obj.changeStatus, name='changestatus'),
     path('oInProcess/', obj.oinProcess, name='oinProcess'),
     path('oCancelled/', obj.ocancelled, name='ocancelled'),
     path('received/<str:product_id>/<str:order_id>/', obj.received, name='received'),
     path('cluster/', obj.cluster, name='cluster'),
     path('createclusterWthOrd/', obj.postClusterWtOrd, name='postclusterWthOrd'),
     path('createcluster/', obj.postCluster, name='postcluster'),
     path('shipcluster/<str:cluster_id>/', obj.shipCluster, name='shipcluster'),
     path('oClusters/<str:status>/<str:order_lst>/', obj.oClustersUpd, name='oClustersupds'),
     path('changetoUfD/<str:order_id>/', obj.orderupfordel, name='changetoUfD'),
     path('addtocluster/<str:cluster_id>/<str:order_lst>/', obj.addToCluster, name='addtocluster'),
     path('deletecluster/<str:cluster_id>', obj.odelCluster, name='deletecluster'),
     path('delfromcluster/<str:cluster_id>/<str:order_id>/', obj.deleteFromCluster, name='delfromcluster'),
path('clusterdelivered/<str:cluster_id>/<str:order_id>/', obj.oDelivered, name='clusterdelivered'),
path('allclsdelivered/<str:cluster_id>', obj.ShipWholeCluster, name='allclsdelivered')

]