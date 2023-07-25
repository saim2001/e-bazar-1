var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

function openPage(pageName, elmnt, color, context) {
    // Hide all elements with class="tabcontent" by default */
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Remove the background color of all tablinks/buttons
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].style.backgroundColor = ""
      tablinks[i].style.borderBottom = "";
    }
  
    // Show the specific tab content
    document.getElementById(pageName).style.display = "block";
  
    // Add the specific color to the button used to open the tab content
    if (context=='inside'){
    elmnt.style.backgroundColor = color;
    elmnt.style.borderBottom = "5px solid lightblue";}
    else {
    document.getElementById(elmnt).style.backgroundColor = color;
    document.getElementById(elmnt).style.borderBottom = "5px solid lightblue";
    }
  }
  function EnableTextbox(ObjChkId,ObjTxtId,reversed)
  {
      if (reversed=='false'){
          if(document.getElementById(ObjChkId).checked){
              document.getElementById(ObjTxtId).disabled = true;
              }
          else{
              document.getElementById(ObjTxtId).disabled = false;
              }
      }
      else if(reversed=='true'){
       if(document.getElementById(ObjChkId).checked){
              document.getElementById(ObjTxtId).disabled = false;
              }
        else{
              document.getElementById(ObjTxtId).disabled = true;
              }
      }
  }
 
  
  document.getElementById("default").click();

  //new code after saim 

  var prevVarList=[];

function changePrevVarList(varLst){
  console.log(varLst,"changes")
  prevVarList= varLst

}

function getPrevVarList(){
 return prevVarList
}


function showVar() {
    
    document.getElementById('var_p').style.display='block';
    var var_div = document.getElementById('variations_enable');
    var_div.style.display='flex';
    var singleProduct= document.getElementsByClassName("singleProduct");
    var b2bRows= document.getElementsByClassName("b2bBatches");
    for (let i=0;i<singleProduct.length; i++ ){
      singleProduct[i].style.display="none";
    }

    for (let i=0;i<b2bRows.length; i++ ){
      b2bRows[i].style.display="none";
    }
      // singleProduct[i].style.visibility = "hidden";
      // const inputs = singleProduct[i].getElementsByTagName('input');
      // for (let j=0;j<inputs.length; j++ ){
      //   inputs[j].removeAttribute('required');
      //   inputs[j].setAttribute("disabled", true);

      // }
    
  }

  function hideVar() {
    document.querySelector('.myDiv input[type="checkbox"]');
    const var_checkboxes = document.querySelectorAll('.variations input[type="checkbox"]');
    var_checkboxes.forEach(checkbox => {
      checkbox.checked = false;
    });
    var var_div= document.getElementById('variations_enable');
    var b2bno= document.getElementById("b2b_no");
    var b2bRows= document.getElementsByClassName("b2bBatches");
    var_div.style.display='none'
    document.getElementById('var_p').style.display='none';
    singleProduct= document.getElementsByClassName("singleProduct");
    for (let i=0;i<singleProduct.length; i++ ){
      singleProduct[i].style.display="table-row";
    }

    if (!b2bno.checked){
    for (let i=0;i<b2bRows.length; i++ ){
      b2bRows[i].style.display="table-row";
    }
  }

  
    //   singleProduct[i].style.visibility = "visible";
    //   const inputs = singleProduct[i].getElementsByTagName('input');
    //   for (let j=0;j<inputs.length; j++ ){
    //     inputs[j].setAttribute('required', true);
    //     inputs[j].removeAttribute("disabled");

    // }

  }


  //end

//start of checking if it's only b2b

function onlyBtoB() {
  const onlyb2bfields = document.getElementsByClassName("onlyb2bfields");
  if (document.getElementById("onlyb2b").checked) {    
    for (let i=0;i<onlyb2bfields.length; i++ ){
      onlyb2bfields[i].style.display='none';
  
      }
  } else {
    const checkVar= document.getElementById('var_no');
    if (checkVar.checked){
      for (let i=0;i<onlyb2bfields.length; i++ ){
        onlyb2bfields[i].style.display='table-row';
    
        }
    }
  }
}

//end of checking if it's only b2b


//b2b
  
function showB2B() {
    
  var b2b_div = document.getElementsByClassName('b2bBatches');
  var isvar = document.getElementById('var_yes');
  const onlyb2b= document.getElementById("onlyb2b");
  onlyb2b.checked=false;
  onlyb2b.disabled=false;
  if (!isvar.checked){
  for (let i=0;i<b2b_div.length; i++ ){
    b2b_div[i].style.display='table-row';

    }
  }
}


function hideB2B() {
    
  var b2b_div = document.getElementsByClassName('b2bBatches');
  const onlyb2b= document.getElementById("onlyb2b");
  onlyb2b.checked=false;
  onlyb2b.disabled=true;
  for (let i=0;i<b2b_div.length; i++ ){
    b2b_div[i].style.display='none';

    }
}


//end b2b

  //enable input with check box

var enable_checkbox= document.querySelectorAll('.var_custom input[type="checkbox"]')
var textInput= document.querySelectorAll('.var_custom input[type="text"]')



for (let i=0; i < enable_checkbox.length ; i++){

    enable_checkbox[i].addEventListener('change', function() {
        if (this.checked) {
          textInput[i].disabled = false;
        } else {
          textInput[i].disabled = true;
        }
      });

}


//end

  //to count how many checkboxes checked

  var checkboxes = document.querySelectorAll('.variations input[type="checkbox"]');

checkboxes.forEach(checkbox => {
  checkbox.addEventListener('click', function() {
    let checkedCount = 0;
    checkboxes.forEach(checkbox => {
      if (checkbox.checked) {
        checkedCount++;
      }
    });

    if (checkedCount >= 2) {
      checkboxes.forEach(checkbox => {
        if (!checkbox.checked) {
          checkbox.disabled = true;
        }
      });
    } else {
      checkboxes.forEach(checkbox => {
        checkbox.disabled = false;
      });
    }
  });
});

//end

//get variations from information tab

function getVar(){

  var typeList= new Array();
  var varTypeElem= document.getElementsByClassName("variations");
  for(var i=0;i<varTypeElem.length;i++){
    var check= varTypeElem[i].querySelector('input[type="checkbox"]');

    if (check.checked){
        var valuetype= varTypeElem[i].getElementsByClassName("varValue");
        valuetype= valuetype[0].value;
        if (valuetype.length!=0){
        typeList.push(valuetype);
      }
    }
  }
return typeList}
//end getVar

// "Start" Function to create input container in variations tab

function createInputCont(){
  const autoCont= document.getElementById("autoCont");
var newContainer = document.createElement("div");
newContainer.className = "contAutoInput"
newContainer.className+= " js_create";
var newLabel = document.createElement("label");
newLabel.className = "varAutoLabel";
newContainer.appendChild(newLabel);
var newInputGroup = document.createElement("div");
newInputGroup.className = "input-group";
newContainer.appendChild(newInputGroup);
var newInput = document.createElement("input");
newInput.type = "text";
newInput.name = "input[]";
newInputGroup.appendChild(newInput);
var newButton = document.createElement("button");
newButton.type = "button";
newButton.style.marginTop = "10px";
newButton.className = "add-btn";
var buttonText = document.createTextNode("Add Input");
newButton.appendChild(buttonText);
newContainer.appendChild(newButton);
autoCont.appendChild(newContainer)

}

//"End" Function to create input container in variations tab


//"Start" function to create labels and headings for according to input
// provided from product information tab



var initialContent=[];
  function createVarhtml(){
    const checkb2b= document.getElementById("b2b_yes").checked;
    const checkOnlyb2b= document.getElementById("onlyb2b").checked;
    var typeList= getVar();
    newList= [...typeList];
    newList.push(checkb2b);
    newList.push(checkOnlyb2b);
    var preVarCheck= JSON.stringify(getPrevVarList());
    var typeListCheck= JSON.stringify(newList);
    console.log('prev',preVarCheck,'new',typeListCheck)
    if (preVarCheck != typeListCheck){
      changePrevVarList(newList);
    //"Start" delete previous javascript
    var inputContRemove= document.getElementsByClassName("js_create")
    for (let i=0; i<inputContRemove.length;i++){
      inputContRemove[i].remove();
      i--;
    }
    var b2bjsRemove= document.getElementsByClassName("notOnlyb2b")
    for (let i=0; i<b2bjsRemove.length;i++){
      b2bjsRemove[i].remove();
      i--;
    }
    //"End" delete previous javascript
    const imagesdiv= document.getElementById("imagesdiv");
    imagesdiv.style.display="none";
    const tableDiv= document.getElementById("varTableDiv");//variation table
    tableDiv.style.display="none";//hide table at start
    initialContent=[];
    const varNo= document.getElementById("var_no");
    const varNotAllowed= document.getElementById("noVariations");
    const varAllowed= document.getElementById("variations");
    if (varNo.checked || typeList.length==0){
      const varNotAllowed= document.getElementById("noVariations");
      varNotAllowed.style.display="block";
      varAllowed.style.display= "none"

    }
    else{

      varNotAllowed.style.display="none";
      varAllowed.style.display="block";
      for(let i=0;i<typeList.length;i++){
        createInputCont();
        var vari= typeList[i];
        var div1= document.getElementById("variation_type");    //create top of variations
        div1.innerHTML+="<h5 class='js_create'>"+vari+"</h5>";

        }
    }

  const setVarLable= document.getElementsByClassName('varAutoLabel');
  for ( let j=0; j<typeList.length;j++){
    setVarLable[j].textContent=typeList[j];
    }

  inputEventList();

}
  }

 //"End" function to create labels and headings for according to input
// provided from product information tab

  // "Start" event listner for adding and removing inputs
  function inputEventList(){
    var inputContainer= document.getElementsByClassName('contAutoInput');
    const addBtn = document.getElementsByClassName('add-btn');
    for (let i=0; i< inputContainer.length;i++){

    addBtn[i].addEventListener('click', function() {


      const newInputGroup = document.createElement('div');
      newInputGroup.classList.add('input-group');

      const newInput = document.createElement('input');
      newInput.type = 'text';
      newInput.name = 'input[]';

      const removeBtn = document.createElement('button');
      removeBtn.classList.add('remove-btn');
      removeBtn.textContent = 'Remove';
      removeBtn.addEventListener('click', function() {
        newInputGroup.remove();
      });

      newInputGroup.appendChild(newInput);
      newInputGroup.appendChild(removeBtn);
      inputContainer[i].appendChild(newInputGroup);
    });


  }}
   // "End" event listner for adding and removing inputs


//"Start" function to get input given for variations eg color:blue,yellow
function createVariations(){
  let varList= [];
  var flag= false;
  const inputCont= document.getElementsByClassName("contAutoInput");

  for (let i=0; i<inputCont.length ;i++){

    let inputValues=[];
  const allInputField= inputCont[i].querySelectorAll(".input-group input");

  const label = inputCont[i].querySelector("label").textContent;
  inputValues.push(label);
  for (let i=0; i< allInputField.length;i++){
  if (allInputField[i].value.length != 0) {
    inputValues.push(allInputField[i].value)
  }
  
}

if (inputValues.length >1){
  varList.push(inputValues);
  flag=true;
}
}

if (flag==true){
  return createTable(varList);
}


 //move to another function to create table for
// according to the input values
}

//"End" function to get input given for variations eg color:blue,yellow


//"Start" function to create table according to input provided

function createTable(variationList){
  createVarhtml();
  const tableDiv= document.getElementById("varTableDiv");
  tableDiv.style.display="block";
  var tableHead= document.getElementById("varHead");
  for (let i=0; i<variationList.length;i++){
    tableHead.insertCell(2+i).outerHTML = "<th scope='col' class='js_create'>"+variationList[i][0]+"<input name='varname' type='hidden' value='"+variationList[i][0]+"' >"+"</th>";
//  <input name='var1' readonly value='"+variationList[i][0]+"' >
    variationList[i].splice(0,1);
    var lastColindex= 2+i;
  }
  const onlyb2b= document.getElementById("onlyb2b");
  if (!onlyb2b.checked){
  tableHead.insertCell(lastColindex+2).outerHTML = '<th scope="col" class="notOnlyb2b" >Units <span class="required">*</span></th>'
  tableHead.insertCell(lastColindex+4).outerHTML = '<th scope="col" class="notOnlyb2b" >Price/unit(Rs) <span class="required">*</span></th>'
  var notOnlyb2bunits='<td class="notOnlyb2b" > <input name="units" type="number" required> </td>';
  var notOnlyb2bprice= '<td class="notOnlyb2b" ><input name="price" type="number" required> </td>';

}
else{
  var notOnlyb2bunits='';
  var notOnlyb2bprice='';
}



var varSize= variationList.length;
var tableVar= document.getElementById("varTable");
var tbody = tableVar.getElementsByTagName("tbody")[0];
var b2byes= document.getElementById("b2b_yes");
if (b2byes.checked){
  const tableHead= document.getElementById("varHead");
  var batch1 = document.createElement("th");
  batch1.setAttribute("scope", "col");
  batch1.textContent = "Batch 1 Minimum units";
  batch1.classList.add('js_create');

  var batch1price = document.createElement("th");
  batch1price.setAttribute("scope", "col");
  batch1price.textContent = "Batch 1 Price/unit";
  batch1price.classList.add('js_create');

  var batch2 = document.createElement("th");
  batch2.setAttribute("scope", "col");
  batch2.textContent = "Batch 2 Minimum units";
  batch2.classList.add('js_create');

  var batch2price = document.createElement("th");
  batch2price.setAttribute("scope", "col");
  batch2price.textContent = "Batch 2 Price/unit";
  batch2price.classList.add('js_create');

  var batch3 = document.createElement("th");
  batch3.setAttribute("scope", "col");
  batch3.textContent = "Batch 3 Minimum units";
  batch3.classList.add('js_create');

  var batch3price = document.createElement("th");
  batch3price.setAttribute("scope", "col");
  batch3price.textContent = "Batch 3 Price/unit";
  batch3price.classList.add('js_create');
  
  tableHead.appendChild(batch1);
  tableHead.appendChild(batch1price);
  tableHead.appendChild(batch2);
  tableHead.appendChild(batch2price);
  tableHead.appendChild(batch3);
  tableHead.appendChild(batch3price);
}
if (varSize==1){


  for (let j=0; j< variationList[0].length;j++){
    let newRow = tbody.insertRow(-1);
    if (b2byes.checked){
      let htmlRowwithb2b='<tr> <td> <input type="checkbox" onclick="selectRow(this)"/> </td> <th scope="row">'+(j+1)+'</th> <td><input name="var" value="'+variationList[0][j]+'" readonly> </td> <td><input name="sku" type="text" required> </td> '+ notOnlyb2bunits +' <td> <select name="condition" class="form-select" aria-label="Default select example" required> <option selected value="new">New</option> <option value="old">Old</option> </select> </td> '+ notOnlyb2bprice +'<td> <input type="radio" name="mainpage" value="'+variationList[0][j]+'" checked> </td> <td> <input name="batch1MinUnit" type="number" value="0" > </td> <td>  <input name="batch1price" type="number" value="0"> </td> <td><input name="batch2MinUnit" type="number" value="0" > </td> <td> <input name="batch2price" type="number" value="0"> </td> <td><input name="batch3MinUnit" type="number" value="0"> </td> <td> <input name="batch3price" type="number" value="0" > </td> </tr>'
      newRow.innerHTML= htmlRowwithb2b;
    }
    else{
    let htmlRow= '<tr> <td> <input type="checkbox" onclick="selectRow(this)"/> </td> <th scope="row">'+(j+1)+'</th> <td><input name="var" value="'+variationList[0][j]+'" readonly> </td> <td><input name="sku" type="text" required> </td> '+ notOnlyb2bunits +' <td> <select name="condition" class="form-select" aria-label="Default select example" required> <option selected value="new">New</option> <option value="old">Old</option> </select> </td> '+ notOnlyb2bprice +'<td> <input type="radio" name="mainpage" value="'+variationList[0][j]+'" checked> </td> </tr>'
    newRow.innerHTML= htmlRow;
  }
    newRow.classList.add('js_create');
}
}
else{
  var count=0;
  for ( let i=0; i < variationList[0].length;i++){
    for (let j=0; j< variationList[1].length;j++){
      count++;
      let newRow = tbody.insertRow(-1);
      if (b2byes.checked){
        let htmlRowwithb2b= '<tr> <td> <input type="checkbox" onclick="selectRow(this)"/> </td> <th scope="row">'+count+' </th> <td> <input name="var1" readonly value="'+variationList[0][i]+'" > </td> <td> <input name="var2" readonly value="'+variationList[1][j]+'" > </td> <td> <input name="sku" type="text" required> </td> '+ notOnlyb2bunits +' <td> <select name="condition" class="form-select" aria-label="Default select example" required> <option selected value="new">New</option> <option value="old">Old</option> </select> </td> '+ notOnlyb2bprice +' <td> <input type="radio" name="mainpage" value="'+variationList[0][i]+"-"+variationList[1][j]+'" checked> </td> <td> <input name="batch1MinUnit" id=batch1MinUnit"'+variationList[0]+variationList[1]+'" type="number" value="0" > </td> <td>  <input name="batch1price" id=batch1price"'+variationList[0]+variationList[1]+'" type="number" value="0"> </td> <td><input name="batch2MinUnit" id=batch2MinUnit"'+variationList[0]+variationList[1]+'" type="number" value="0" > </td> <td> <input name="batch2price" id=batch2price"'+variationList[0]+variationList[1]+'" type="number" value="0"> </td> <td><input name="batch3MinUnit" id=batch3MinUnit"'+variationList[0]+variationList[1]+'" type="number" value="0" > </td> <td> <input name="batch3price" id=batch3price"'+variationList[0]+variationList[1]+'" type="number" value="0"> </td> </tr>'
        newRow.innerHTML= htmlRowwithb2b;
      }
      else{
      let htmlRow= '<tr> <td> <input type="checkbox" onclick="selectRow(this)"/> </td> <th scope="row">'+count+' </th> <td> <input name="var1" readonly value="'+variationList[0][i]+'" > </td> <td> <input name="var2" readonly value="'+variationList[1][j]+'" > </td> <td> <input name="sku" type="text" required> </td> '+ notOnlyb2bunits +' <td> <select name="condition" class="form-select" aria-label="Default select example" required> <option selected value="new">New</option> <option value="old">Old</option> </select> </td> '+ notOnlyb2bprice +' <td> <input type="radio" name="mainpage" value="'+variationList[0][i]+"-"+variationList[1][j]+'" checked> </td> </tr>'
      newRow.innerHTML= htmlRow;
    }
      newRow.classList.add('js_create');
  }
  }
}

const imagesdiv= document.getElementById("imagesdiv");
imagesdiv.style.display="block";


}

//"End" function to create table according to input provided

//"Start" select rows

function selectRow(checkbox) {
  var row = checkbox.parentNode.parentNode;
  if (checkbox.checked) {
    row.classList.add("selected");
  } else {
    row.classList.remove("selected");
  }
}

//"End" select rows

//"Start" delete selected rows

function deleteSelectedRows(){
  var selectedRows= document.getElementsByClassName("selected");
  for (let i=0; i<selectedRows.length; i++){
    selectedRows[i].remove();
    i--;
  }
}

//"End" delete selected rows


window.onload = function () {
  const data = JSON.parse(document.getElementById("my-data").textContent);
  console.log(data)
   const cat_name = document.getElementById("cat_name");
   cat_name.readOnly = false;
   cat_name.value = data.category;
   
   if (data.isVariation == "yes"){
    console.log(data.var_type)
    const var_vals = Object.values(data.var_type);
   const var_types = Object.keys(data.var_type);
   console.log(var_types)
    document.getElementById('var_yes').click();
    if (data.isb2b == 'yes' ){  
      document.getElementById('b2b_yes').click();
    
    if (data.onlyb2b=='yes'){
      console.log('yes only b2b2')
      document.getElementById('onlyb2b').checked=true;
    }}


    for (const var_type  of var_types ){
      if (var_type == 'size'){

        document.getElementById('var_size').checked = true;
      }
      else if (var_type == 'color'){
        document.getElementById("var_color").checked = true;
      }
      else if (var_type== 'style'){
        document.getElementById("var_style").checked = true;
      }
      else {
        if (document.getElementById("ch_1").checked == false && document.getElementById('ch_2').checked == false){
          let var_checkbox_1 = document.getElementById("ch_1");
          var_checkbox_1.checked = true;
          var_checkbox_1.nextSibling.nextSibling.value = var_type;

        }
        else if (document.getElementById("ch_1").checked == true){
          let var_checkbox_2 = document.getElementById("ch_2");
          var_checkbox_2.checked = true;
          var_checkbox_2.nextSibling.nextSibling.value = var_type;
        }
      }
  
     }
     document.getElementById("var_btn").click();
     const var_lst = document.querySelectorAll('.contAutoInput.js_create');
   for ( div=0; div<var_types.length; div++){
    let div_elem = var_lst[div]
    console.log(div_elem);
    if (div_elem.firstChild.innerHTML == var_types[div] ){
      let var_val = div_elem.querySelectorAll("[name='input[]']");
      console.log(div_elem.firstChild.innerHTML)
      var_val[0].value = var_vals[div][0];
      console.log(var_val[div])
      console.log(var_vals[div])
      for (act_var of var_vals[div]){
        console.log(act_var)
        if (act_var != var_vals[div][0]){
          let button = div_elem.querySelector("button");
          button.click();


        } 
      }
      let all_inpts = div_elem.querySelectorAll("[name='input[]']")
      console.log(all_inpts)
      for (input=0; input<all_inpts.length;input++){
        if (all_inpts[input].value == ''){
          all_inpts[input].value = var_vals[div][input];
        }
      }


    }
  
    

   }
   document.querySelector("[onclick='createVariations()']").click();
   let var_table = document.querySelector('#varTable');
   let tbody = var_table.querySelector('tbody');
   let rows = tbody.querySelectorAll('.js_create');
   console.log(rows.length);
   let variations = Object.keys(data.variations);
   let var_data = Object.values(data.variations);
   for (i=0; i<rows.length; i++){
    console.log(i)
    console.log(rows[i])
    let sku = rows[i].querySelector("[name = 'sku']");
    sku.value = var_data[i]["sku"];



    if (data.onlyb2b=='no'){
      let units = rows[i].querySelector("[name = 'units']");
      units.value = var_data[i]["units"];
      let price = rows[i].querySelector("[name = 'price']");
      price.value = var_data[i]["price"];
    }
  


    let condition =   rows[i].querySelector("[name = 'condition']");  
    condition.value = var_data[i]["condition"];
  }
  let images = document.querySelectorAll("[name = 'images']");
  let pro_images = data.images
  console.log('pro',pro_images)
  let image_divs = document.querySelectorAll('[class = "input-group mb-3"]')

  for (i=0; i<pro_images.length; i++){
    let image = document.createElement('img');
    image.setAttribute('src',pro_images[i])
    image.height = 200;
    image.width = 200;
    image_divs[i].appendChild(image)
    console.log('imgin');


  }
   }
   else{
    document.querySelector('[name = "skuSingle"]').value = data.sku;
    document.querySelector('#productname').value = data.name;
    let images  = data.images;
    let image_feild = document.querySelectorAll("[name = 'imageSingle']")
    for (i=0; i<images.length; i++){
      let image = document.createElement('img');
      image.setAttribute('src',images[i])
      image.height = 200;
      image.width = 200;
      image_feild[i].parentNode.appendChild(image)
    }
    document.querySelector('#unitsSingle').value = data.units;
    document.querySelector('#priceSingle').value = data.price;
    document.querySelector("[name = 'conditionSingle']").value = data.condition


   }


   if (data.isb2b == 'yes' && data.isVariation == "no" ){
    document.getElementById('b2b_yes').click();
    let batches = Object.values(data.batches);
    for (i=0; i<batches.length; i++){
      document.querySelector(`#batchUnits${i+1}`).value = batches[i]["MinUnits"];
      document.querySelector(`#batchPrice${i+1}`).value = batches[i]["Price"];

    }
   }

  //  if (data.isb2b == 'yes' && data.isVariation == "yes" ){
  //   document.getElementById('b2b_yes').click();
  //   let batches = Object.values(data.variations);
  //   for (i=0; i<batches.length; i++){
  //     document.querySelector("[name = 'batch"+i+"MinUnit']").value = batches[i]["MinUnits"];
  //     document.querySelector("[name = 'batch"+i+"price']").value = batches[i]["Price"];

  //   }
  //  }
   document.getElementById("productname").value = data.name;
   if (data.brand){
    document.getElementById('brand').value = data.brand;
   }
   else{
    document.getElementById("isbrand").checked = true;
   } 
   
  document.querySelector("#manufacturer").value  = data.manufacturer;
  if (data.expiry){
    document.querySelector('expireDate').value = data.expiry;

  }
  document.querySelector("#length").value = data.length;
  document.querySelector("#width").value = data.width;
  document.querySelector("#height").value = data.height;
  document.querySelector("#weight").value = data.weight;
  document.querySelector("#descriptionPara").value = data.description;
  let point = document.querySelectorAll("[name = 'points']");
  let pro_points = data.points;
  for (i=0; i<pro_points.length; i++){
    point[i].value = pro_points[i];
  }
  

}