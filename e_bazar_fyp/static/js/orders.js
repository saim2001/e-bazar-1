window.onload = function () {
    const printBtn = document.getElementById('printbtn');
    printBtn.addEventListener('click', () => {
        const data = JSON.parse(document.getElementById("packaging-data").textContent);
        console.log(data)
      // Get the information to be printed
      const infoToPrint = 'This is the information to be printed';
      
      // Create a new window and write the information to it
      const printWindow = window.open('', '','height=600,width=800');
      printWindow.document.write(`<html><head><title>Packaging slip</title></head><body>
    
      <h1 style="text-align: center;">
    E-bazar
</h1>
<h2 style="text-align: center;">
    Packaging Slip
</h2>
<hr>
<h3 style="text-align: center;">
   Order information
</h3>
<hr style="width: 50%;">
<h4 style="text-align: center;">
    ID: ${data.orderid}
</h4>
<h4 style="text-align: center;">
    Puchase date: ${data.Puchase}
</h4>
<h4 style="text-align: center;">
    Fulfillment: ${data.salecchannel}
</h4>
<h4 style="text-align: center;">
    Fulfillment: ${data.fulfillment}
</h4>
<hr style="width: 25%;">
<h3 style="text-align: center;">
    proceeds

</h3>
<hr style="width: 25%;">

<h4 style="text-align: center;">
    Total: Rs.${data.total}
</h4>
<h4 style="text-align: center;">
    Tax: Rs.${data.tax}
</h4>
<h4 style="text-align: center;">
    Subtotal: Rs.${data.subtotal}
</h4>
<hr style="width: 50%;">
<h3 style="text-align: center;">
    Customer information
 </h3>
<hr style="width: 50%;">
<h4 style="text-align: center;">
    Name: ${data.custname}
</h4>
<h4 style="text-align: center;">
    Address: ${data.custaddress}
</h4>
<h4 style="text-align: center;">
    Phone No: ${data.custphone}
</h4>
<hr></html>`);
      
      // Print the new window
      printWindow.print();
      
      // Close the new window
      
    });
}