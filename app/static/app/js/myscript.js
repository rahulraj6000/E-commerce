$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})



$('.plus-cart').click(function(){
    let id  = $(this).attr("pid").toString();
    let em1 = this.parentNode.children[2];
    let val = "plus"

    //console.log(id);
    $.ajax({
        type:"GET",
        url:"/plus-minus-remove-cart/",
        data:{
            prod_id:id,
            key:val
        },
        success:function(data){
            console.log(data);
            em1.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalAmount;
        }
    })

})
$('.minus-cart').click(function(){
    let id  = $(this).attr("pid").toString();
    let em1 = this.parentNode.children[2];

    //console.log(id);
    $.ajax({
        type:"GET",
        url:"/plus-minus-remove-cart/",
        data:{
            prod_id:id,
            key:"minus"
        },
        success:function(data){
            console.log(data);
            em1.innerText = data.quantity;
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalAmount;
        }
    })

})
$('.remove-cart').click(function(){
    let id  = $(this).attr("pid").toString();
    var em1 = this;

    //console.log(id);
    $.ajax({
        type:"GET",
        url:"/plus-minus-remove-cart/",
        data:{
            prod_id:id,
            key:"remove"
        },
        success:function(data){
           
            console.log(data);
            document.getElementById('amount').innerText = data.amount;
            document.getElementById('totalamount').innerText = data.totalAmount;
            em1.parentNode.parentNode.parentNode.parentNode.remove();
        }
    })

})
















