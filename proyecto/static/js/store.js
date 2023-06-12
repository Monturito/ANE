function addToCart(productId) {
    var quantity = parseInt(prompt('Enter quantity:', '1'));

    if (isNaN(quantity) || quantity <= 0) {
        alert('Invalid quantity.');
        return;
    }

    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            nft_id: productId,
            quantity: quantity,
        }),
    })
        .then(function(response) {
            if (response.ok) {
                alert('Item added to cart.');
            } else {
                alert('Failed to add item to cart.');
            }
        })
        .catch(function(error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
}
