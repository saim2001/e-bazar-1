var remove_cart_item=document.getElementsByTagName("a");
var item_price=document.getElementsByName('price');
for (var i = 0; i < remove_cart_item.length; i++ ){
    var item=remove_cart_item[i];
    item.addEventListener('click', function(event){
        var button_clicked=event.target;
        button_clicked.parentElement.parentElement.parentElement.remove();

            })
        }