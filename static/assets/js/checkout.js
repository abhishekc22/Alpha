$(document).ready(function () {
    $('.paywithRazorpay').click(function (e){
        e.preventDefault();
        console.log('hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
        var proceedUrl = $(this).data('proceed-url');
        var address = $("[name='address']").val();
        var placeOrderUrl = $('script[data-place-order-url]').data('place-order-url'); // Retrieve place_order URL
        var orderdetailsurl=$('script[data-order-details-url]').data('order-details-url');
        var token = $("[name='csrfmiddlewaretoken']").val();
        console.log(address)
        $.ajax({
            
            method: "POST",
            url: proceedUrl,
            headers: {
                "X-CSRFToken": token // Include the CSRF token in the headers
            },
           
            
            success: function (response) {
                console.log(response);

                var options = {
                    key: "rzp_test_noASohsjDhRBC1",
                    amount:1*100, // Amount in currency subunits (INR)
                    currency: "INR",
                    name: "alpha diamond",
                    description: "Thank you",
                    image: "https://example.com/your_logo",
                    handler: function (response){
                        var data = {
                            'address': address,
                            'paymentMethod': "paid by Razorpay",
                            csrfmiddlewaretoken: token
                        };
                        $.ajax({
                            method: "POST",
                            url: placeOrderUrl,
                            data: data,
                            success: function (responsec) {
                                Swal.fire("Congratulations!", responsec.status, "success").then((value) => {
                                    window.location.href = orderdetailsurl;
                                });
                            }
                        });
                    },
                    prefill: {
                        name: "Gaurav Kumar",
                        email: "gaurav.kumar@example.com",
                        contact: "9000090000"
                    },
                    notes: {
                        address: "Razorpay Corporate Office"
                    },
                    theme: {
                        color: "#3399cc"
                    }
                };

                var rzp1 = new Razorpay(options);
                rzp1.open();
            }
        });
    });
});


