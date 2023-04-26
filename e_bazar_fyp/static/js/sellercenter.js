const active_page = window.location.pathname;
const side_bar_links = document.getElementsByClassName("list-group-item list-group-item-action");
const accordian_buttons = document.querySelectorAll(".accordion-button.collapsed");


// if (active_page == "/sellercenter/"){
//     console.log("in");
//     var footer = document.getElementByClassName("bg-dark bg-gradient text-white  pb-4 mt-auto");
//     footer.className += " fixed-bottom"
// }

for (var i=0; i<side_bar_links.length; i++){
    if (side_bar_links[i].href.includes(`${active_page}`)){
        // console.log("in1")
        if (active_page == "/sellercenter/addproduct/" || active_page == "/sellercenter/selectcategory1/" 
        || active_page == "/sellercenter/selectcategory2/" || active_page == "/sellercenter/selectcategory3/" || 
        active_page == "/sellercenter/addpro/" 
        || active_page == "/sellercenter/insertpro/") {
            // console.log("in2")
            var accord_body = document.getElementById("flush-collapseTwo");
            var collapse = new bootstrap.Collapse(accord_body);
            collapse.toggle();
            
            };      


        }
        console.log(side_bar_links[i].href);
    }
    // side_bar_links[i].addEventListener('click', function(){
    //     this.className += " active"
        
    // })
    // console.log(side_bar_links[i].href);
$(document).ready(function () {
        $('#example').DataTable({
            paging: true,
            pageLenght: 10,
            lengthChang: true,
            autoWidth: true,
            searching: true,
            bInfo: true,
            bSort: true,
        });
    });
